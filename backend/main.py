from fastapi import FastAPI, UploadFile, HTTPException, File
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from decouple import config
import openai
from functions.openai_requests import convert_audio_to_text

app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://localhost:4173",
    "http://localhost:5174",
    "http://localhost:4174",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/health")
def check_health():
    return {"message": "healthy"}


@app.post("/post-audio/")
def post_audio(file: UploadFile = File(...)):

    pass


@app.post("/post-audio-get/")
def get_audio():
    audio_input = open("test_recording.mp3", "rb")
    message_decoded = convert_audio_to_text(audio_input)
    print(message_decoded)
    return message_decoded
