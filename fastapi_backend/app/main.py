import time
from typing import Union

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from app.AnonymizationPipeline import anonymize


class Message(BaseModel):
    text: str


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows requests from all origins (adjust as needed)
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/message/")
async def read_message(message: Message):
    anon_text, entities = anonymize.anonymize_prompt(message.text)
    return JSONResponse(
        content={"status": "success", "message_received": anon_text},
        status_code=200
    )


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
