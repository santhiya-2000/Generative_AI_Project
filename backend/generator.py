from diffusers import StableDiffusionPipeline
import torch, os, time, gc

class StoryIllustrator:
    def __init__(self, model_id="stabilityai/sd-turbo"):
        device = "cuda" if torch.cuda.is_available() else "cpu"
        os.makedirs("static", exist_ok=True)
        print(f"Using device: {device} ({torch.cuda.get_device_name(0) if device=='cuda' else 'CPU'})")

        self.device = device
        self.pipe = StableDiffusionPipeline.from_pretrained(
            model_id,
            torch_dtype=torch.float16 if device == "cuda" else torch.float32,
            safety_checker=None,
        ).to(device)

    def generate(self, prompt, num_images=1):
        start = time.time()
        paths = []
        base_prompt = f"{prompt}, consistent art style, cinematic lighting, same characters"

        for i in range(num_images):
            scene_prompt = f"{base_prompt}, scene {i+1}, part {i+1} of the story"
            with torch.inference_mode(), torch.autocast("cuda"):
                image = self.pipe(
                    scene_prompt,
                    num_inference_steps=12,
                    guidance_scale=2.0,
                    height=512,
                    width=512,
                ).images[0]

            path = f"static/story_scene_{i+1}.png"
            image.save(path, quality=95, optimize=True)
            paths.append(path)
            torch.cuda.empty_cache()
            gc.collect()

        print(f"Generated story with {len(paths)} scenes in {time.time() - start:.2f}s")
        return paths
