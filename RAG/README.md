# Medical Assistant with Disease Symptom Query

This part is a medical assistant for querying diseases and their symptoms using RAG, as an alternative and a potential improvement to making a more conversational bot faster with efficient retrieval. It processes medical data, creates embeddings for querying, and provides relevant responses using a language model.

## Setup

### 1. Install Dependencies

Install the required Python packages:

```bash
pip install -r requirements.txt
```


### Key Points for Llama 3:

- **Ollama Installation**: Ollama is required for running Llama 3 models locally. Install Ollama from [here](https://ollama.com/download) and ensure it’s up and running.

- After installation: you still need to install the llama3 model and run it so that it starts the server.
```bash
ollama pull llama3
```

```bash
ollama run llama3 
```

After these steps, continue to the part to clean the data used in the main project bot. Here we also use the dataset sourced from NHS. 
```bash
python clean.py
```

Individual Disease Files as Knowledge Base:
The disease files now act as the “knowledge base” for your RAG system. When the query engine (from main.py) looks for relevant documents, it will search through this knowledge base, retrieve the most relevant document, and use that information to augment the response generation. 

finally, we are ready to test the bot. 

```bash
python main.py
```


Example: 

You: What are the symptoms of diabetes?
Assistant: [response]
Relevant Sources:
Source 1:
File: diabetes.csv
Score: 0.92
Content: "Frequent urination, excessive thirst..."