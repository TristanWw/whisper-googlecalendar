from fastapi import FastAPI, WebSocket
from parser import parse_event
import whisper

app = FastAPI()

@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()

    filename = f"audio.webm"

    with open(filename, "ab") as f:
        try:
            while True:
                data = await ws.receive_bytes()
                f.write(data)
        except Exception:
            pass

    model = whisper.load_model("small.en")
    result = model.transcribe("audio.webm")
    parse_event(result["text"])
    #print(result["text"])
 
