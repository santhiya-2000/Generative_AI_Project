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
    # Split prompt into sentences for story text
    import re
    sentences = [s.strip() for s in re.split(r"[.!?]+", prompt) if s.strip()]
    if not sentences:
        sentences = [prompt.strip()]
    
    # Limit to requested count
    if count > 0:
        sentences = sentences[:count]
    
    # Generate images
    images = illustrator.generate(prompt, count)
    
    return {
        "story": sentences,
        "images": images
    }

@app.get("/image/{filename}")
def get_image(filename: str):
    return FileResponse(f"static/{filename}")
