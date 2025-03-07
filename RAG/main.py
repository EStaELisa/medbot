from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.ollama import Ollama
from llama_index.core import Settings
from llama_index.postprocessor.jinaai_rerank import JinaRerank
import os
import pickle
from rich.console import Console
from rich.panel import Panel

console = Console()

# 1 - Check if cached documents exist
def save_to_cache(obj, filename):
    with open(filename, 'wb') as f:
        pickle.dump(obj, f)
        f.flush()
        os.fsync(f.fileno())
        console.print("[dim]Saved to cache...[/dim]")

def load_from_cache(filename):
    try:
        with open(filename, 'rb') as f:
            console.print("[dim]Loading from cache...[/dim]")
            return pickle.load(f)
    except (FileNotFoundError, EOFError):
        return None

console.print("[dim]Initializing system...[/dim]")

# 2 - Load medical data from CSV files if cache is not found
docs = load_from_cache('docs_cache.pkl')
if docs is None:
    loader = SimpleDirectoryReader(
        input_dir="./diseases",
        required_exts=[".csv"],
        recursive=True
    )
    docs = loader.load_data()
    save_to_cache(docs, 'docs_cache.pkl')

# 3 - Create embeddings using Hugging Face model
embed_model = HuggingFaceEmbedding(
    model_name="BAAI/bge-large-en-v1.5",
    trust_remote_code=True
)

Settings.embed_model = embed_model

# 4 - Store embeddings in vector database
index = VectorStoreIndex.from_documents(docs)

# 5 - Set up LLM (Llama 3 via Ollama)
llm = Ollama(model="llama3", request_timeout=120.0)
Settings.llm = llm

# 6 - Rerank results with Jina AI
jina_api_key = "jina_1dee82039836463cbee8b84c224de7a67CK1nvflzxjIZBch8y1i1PKqM6LZ"
jina_rerank = JinaRerank(api_key=jina_api_key, top_n=5)  # Keep only top 5 results

# 7 - Create the query engine
query_engine = index.as_query_engine(
    similarity_top_k=20,  
    node_postprocessors=[jina_rerank],  
    use_async=True
)

# Function to process the query and synthesize the response
def query_with_rerank(query_str):
    """Retrieve and synthesize response (reranking is done)."""
    console.print("[dim]Processing your query...[/dim]")
    console.print(f"[dim]Context Sent to LLM: {query_str}[/dim]") 

    response = query_engine.query(query_str)
    
    sources = getattr(response, "source_nodes", [])
    
    return response, sources

# test run the query engine
console.print("\n[bold green]Medical Assistant Ready![/bold green]")
console.print("[dim]Enter your symptoms or questions. Type 'quit' to exit.[/dim]\n")

while True:
    chat_input = console.input("[bold blue]You:[/bold blue] ")
    
    if chat_input.lower() in ['quit', 'exit', 'q']:
        console.print("\n[bold green]Goodbye! Take care![/bold green]")
        break
        
    response, sources = query_with_rerank(chat_input)
    
    console.print("\n[bold cyan]Assistant:[/bold cyan]", style="bold")
    console.print(Panel(str(response), border_style="cyan"))
    
    console.print("\n[bold yellow]Relevant Sources:[/bold yellow]")
    if sources:
        for idx, source in enumerate(sources, 1):
            console.print(Panel(
                f"[bold]Source {idx}[/bold]\n"
                f"File: {source.node.metadata.get('file_name', 'unknown file')}\n"
                f"Score: {source.score:.3f}\n"
                f"Content: {source.node.text[:500]}...",  # Limit to first 500 chars
                border_style="yellow"
            ))
    else:
        console.print("[dim]No sources were found.[/dim]")
    
    console.print("\n" + "-" * 80 + "\n")