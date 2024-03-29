from fastapi import FastAPI, UploadFile, HTTPException, File
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from decouple import config
import openai
from functions.openai_requests import convert_audio_to_text, get_chat_response
from functions.database import store_message, reset_conversation
from functions.text_to_speech import convert_text_to_speech
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


@app.get("/reset-messages")
def reset_messages():
    reset_conversation()
    return {"message": "reset done"}


@app.post("/post-audio/")
def post_audio(file: UploadFile = File(...)):
    # audio_input = open("test_recording.mp3", "rb")
    with open(file.filename, "wb") as buffer:
        buffer.write(file.file.read())

    audio_input = open(file.filename, "rb")

    message_decoded = convert_audio_to_text(audio_input)
    print(message_decoded)
    if not message_decoded:
        return HTTPException(status_code=400, detail="Failed to decode the audio ")
    chat_response = get_chat_response(message_decoded)
    store_message(message_decoded, chat_response)

    audio_output = convert_text_to_speech(chat_response)

    if not audio_output:
        return HTTPException(status_code=400, detail="Failed to get eleven labs audio response")

    def iterfile():
        yield audio_output

    return StreamingResponse(iterfile(), media_type="application/octet-stream")


@app.post("/post-audio-get/")
def get_audio():
    audio_input = open("test_recording.mp3", "rb")
    message_decoded = convert_audio_to_text(audio_input)
    print(message_decoded)
    if not message_decoded:
        return HTTPException(status_code=400, detail="Failed to decode the audio ")
    chat_response = get_chat_response(message_decoded)
    store_message(message_decoded, chat_response)

    audio_output = convert_text_to_speech(chat_response)
    print(chat_response)
    if not audio_output:
        return HTTPException(status_code=400, detail="Failed to get eleven labs audio response")

    def iterfile():
        yield audio_output

    return StreamingResponse(iterfile(), media_type="audio/mpeg")
