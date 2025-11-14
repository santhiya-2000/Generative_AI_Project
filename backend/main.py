from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from generator import StoryIllustrator

app = FastAPI()
illustrator = StoryIllustrator()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/generate")
def generate(prompt: str = Form(...), count: int = Form(1)):
    return {"images": illustrator.generate(prompt, count)}

@app.get("/image/{filename}")
def get_image(filename: str):
    return FileResponse(f"static/{filename}")
