from diffusers import StableDiffusionPipeline
import torch, os, time, gc, re


class StoryIllustrator:
    def __init__(self, model_id="stabilityai/sd-turbo"):
        # Determine if CUDA (GPU) is available for faster processing
        device = "cuda" if torch.cuda.is_available() else "cpu"
        # Create static directory for storing generated images
        os.makedirs("static", exist_ok=True)
        print(f"Using device: {device} ({torch.cuda.get_device_name(0) if device=='cuda' else 'CPU'})")

        # Store device and initialize Stable Diffusion pipeline
        self.device = device
        self.pipe = StableDiffusionPipeline.from_pretrained(
            model_id,
            torch_dtype=torch.float16 if device == "cuda" else torch.float32,
            safety_checker=None,
        ).to(device)

        # Demographic groups for flexible bias analysis 
        self.demographic_groups = {
            "gender": ["a man", "a woman", "a non-binary person"],
            "ethnicity": [
                "a Black person",
                "an East Asian person",
                "a South Asian person",
                "a White person",
                "a Hispanic person",
            ],
            "age": ["a child", "a teenager", "an adult", "an elderly person"],
        }

    # ---------------------------------------------------------
    # 1) ORIGINAL STORY GENERATION
    # ---------------------------------------------------------
    def generate(self, prompt, num_images=1):
        start = time.time()
        paths = []
        base_prompt = f"{prompt}, consistent art style, cinematic lighting, same characters"

        for i in range(num_images):
            scene_prompt = f"{base_prompt}, scene {i+1}, part {i+1} of the story"

            if self.device == "cuda":
                ctx = torch.autocast("cuda")
            else:
                ctx = torch.no_grad()

            with torch.inference_mode(), ctx:
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

            gc.collect()
            if self.device == "cuda":
                torch.cuda.empty_cache()

        print(f"Generated story with {len(paths)} scenes in {time.time() - start:.2f}s")
        return paths

    # ---------------------------------------------------------
    # 2) STORYLINE MODE: each sentence = one scene 
    # ---------------------------------------------------------
    def generate_storyline(self, story_text, character_description, max_scenes=None):
        """
        story_text: full story as text. Each sentence ~ one scene.
        character_description: very specific description of main characters
                              (same boy, same dragon, same clothes, etc.)
        max_scenes: optionally limit number of scenes/images.
        """
        sentences = [s.strip() for s in re.split(r"[.!?]+", story_text) if s.strip()]
        if max_scenes is not None:
            sentences = sentences[:max_scenes]

        paths = []
        start = time.time()

        for i, sentence in enumerate(sentences, start=1):
            scene_prompt = (
                f"{character_description}. "
                f"Scene {i}: {sentence}. "
                f"consistent art style, same recurring characters, cinematic lighting."
            )

            if self.device == "cuda":
                ctx = torch.autocast("cuda")
            else:
                ctx = torch.no_grad()

            with torch.inference_mode(), ctx:
                image = self.pipe(
                    scene_prompt,
                    num_inference_steps=12,
                    guidance_scale=2.0,
                    height=512,
                    width=512,
                ).images[0]

            path = f"static/story_scene_{i}.png"
            image.save(path, quality=95, optimize=True)
            paths.append(path)

            gc.collect()
            if self.device == "cuda":
                torch.cuda.empty_cache()

        print(f"Generated storyline with {len(paths)} scenes in {time.time() - start:.2f}s")
        return paths

    def generate_story(self, prompt, num_images=1):
        """
        Wrapper similar to code 2: splits prompt into sentences
        and uses a generic recurring-character description.
        """
        sentences = [s.strip() for s in re.split(r"[.!?]+", prompt) if s.strip()]
        if not sentences:
            sentences = [prompt.strip()]

        try:
            num_images = int(num_images)
            if num_images > 0:
                sentences = sentences[:num_images]
        except Exception:
            pass

        story_text = ". ".join(sentences)
        character_description = (
            "The same main characters appear in all scenes, drawn in a consistent storybook style"
        )
        return self.generate_storyline(story_text, character_description, max_scenes=len(sentences))

    # ---------------------------------------------------------
    # 3) STYLE TRANSFER WITH DIFFUSION
    # ---------------------------------------------------------
    def style_transfer(self, content_prompt, style_prompt, num_images=1):
        """
        Simple style transfer using prompting:
        content_prompt = what is happening
        style_prompt   = how it should look (art style)
        """
        combined_prompt = f"{content_prompt}, in the style of {style_prompt}"
        paths = []

        for i in range(num_images):
            if self.device == "cuda":
                ctx = torch.autocast("cuda")
            else:
                ctx = torch.no_grad()

            with torch.inference_mode(), ctx:
                image = self.pipe(
                    combined_prompt,
                    num_inference_steps=12,
                    guidance_scale=2.0,
                    height=512,
                    width=512
                ).images[0]

            path = f"static/style_transfer_{int(time.time())}_{i}.png"
            image.save(path, quality=95, optimize=True)
            paths.append(path)

            gc.collect()
            if self.device == "cuda":
                torch.cuda.empty_cache()

        return paths

    # ---------------------------------------------------------
    # 4) BIAS & FAIRNESS ANALYSIS 
    # ---------------------------------------------------------
    def generate_bias_grid(self, base_prompt, attribute_type="gender", per_value=1):
        """
        Creates multiple images for different demographics to analyze bias.

        attribute_type: "gender", "ethnicity", or "age"
        per_value: how many images per group (1–4 recommended on 4GB GPU)
        """
        if attribute_type not in self.demographic_groups:
            raise ValueError(f"Unsupported attribute_type: {attribute_type}")

        groups = self.demographic_groups[attribute_type]
        try:
            per_value = int(per_value)
        except Exception:
            per_value = 1
        per_value = max(1, min(per_value, 4))

        start = time.time()
        results = []

        for group in groups:
            group_images = []
            for j in range(per_value):
                prompt = f"{base_prompt}, portrait of {group}, studio lighting, high quality, continuous art style with same objects"

                if self.device == "cuda":
                    ctx = torch.autocast("cuda")
                else:
                    ctx = torch.no_grad()

                with torch.inference_mode(), ctx:
                    image = self.pipe(
                        prompt,
                        num_inference_steps=12,
                        guidance_scale=2.0,
                        height=512,
                        width=512,
                    ).images[0]

                safe_name = re.sub(r"[^a-zA-Z0-9]", "_", group)
                filename = f"static/bias_{attribute_type}_{safe_name}_{j+1}.png"
                image.save(filename, quality=95, optimize=True)
                group_images.append(filename)

                gc.collect()
                if self.device == "cuda":
                    torch.cuda.empty_cache()

            results.append({"group": group, "images": group_images})

        print(
            f"Generated bias grid ({attribute_type}) with "
            f"{len(groups)} groups in {time.time() - start:.2f}s"
        )
        return results
