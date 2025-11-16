#  StoryIllustrator AI - Kids Storybook Generator

A magical AI-powered storybook application that creates illustrated stories for children! Watch as your story ideas come to life with beautiful AI-generated images and kid-friendly animations.

##  Features

- ** Story Generation**: Enter a story prompt and watch AI create multiple illustrated scenes
- ** Kid-Friendly UI**: Colorful pink and blue theme with fun animations
- ** AI Illustrations**: Stable Diffusion-powered image generation for each story scene
- ** Carousel Navigation**: Slide through story scenes with smooth animations
- ** Interactive Elements**: Bouncing buttons, floating text, and sparkling decorations
- ** Fun Typography**: Comic Sans fonts and playful design elements

##  Quick Start

### Prerequisites

- Python 3.8+
- Node.js 16+
- CUDA-compatible GPU (recommended for faster image generation)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Generative_AI_Project
   ```

2. **Backend Setup**
   ```bash
   # Create virtual environment
   python -m venv venv
   
   # Activate virtual environment
   # Windows:
   venv\Scripts\activate
   # Mac/Linux:
   source venv/bin/activate
   
   # Install dependencies
   pip install -r requirements.txt
   ```

3. **Frontend Setup**
   ```bash
   cd frontend
   npm install
   ```

4. **Start the Application**
   
   **Terminal 1 - Backend:**
   ```bash
   # From project root
   python backend/main.py
   ```
   
   **Terminal 2 - Frontend:**
   ```bash
   # From frontend directory
   npm run dev
   ```

5. **Open your browser** and navigate to `http://localhost:5173`

##  How to Use

1. **Enter Your Story Idea**: Type a creative story prompt in the text area
   - Example: "A brave knight discovers a hidden forest filled with magical creatures"
   - Example: "A little girl finds a talking rainbow butterfly"

2. **Choose Scene Count**: Select how many illustrated scenes you want (1-5)

3. **Generate Story**: Click the green "Generate Story" button

4. **Enjoy Your Story**: Watch as AI creates both the story text and beautiful illustrations!

5. **Navigate Scenes**: Use the Previous/Next buttons to explore each scene

##  Project Structure

```
Generative_AI_Project/
├── backend/
│   ├── main.py              # FastAPI server
│   ├── generator.py         # AI image generation logic
│   └── static/              # Generated images storage
├── frontend/
│   ├── src/
│   │   ├── App.jsx          # Main React component
│   │   ├── index.css        # Styling and animations
│   │   └── App.css          # Additional component styles
│   ├── package.json         # Node.js dependencies
│   └── public/              # Static assets
└── requirements.txt         # Python dependencies
```

##  Technology Stack

### Backend
- **FastAPI**: Modern Python web framework
- **Stable Diffusion**: AI image generation
- **PyTorch**: Deep learning framework
- **Uvicorn**: ASGI server

### Frontend
- **React 18**: Modern UI framework
- **Framer Motion**: Smooth animations
- **React Icons**: Beautiful iconography
- **Vite**: Fast build tool

##  Design Features

### Color Scheme
- **Background**: Pink and blue gradient
- **Buttons**: Bright green with hover effects
- **Text**: Pink headings with colorful accents
- **Decorations**: Sparkling emojis and floating elements

### Animations
- **Floating Headers**: Gentle up-and-down movement
- **Bouncing Buttons**: Interactive hover animations
- **Sliding Carousel**: Smooth scene transitions
- **Sparkle Effects**: Floating emoji decorations
- **Background Bubbles**: Subtle animated gradients

##  Configuration

### Backend Settings
- **Model**: Uses `stabilityai/sd-turbo` for fast generation
- **Image Size**: 512x512 pixels
- **Inference Steps**: 12 (optimized for speed)
- **Device**: Auto-detects CUDA or CPU

### Frontend Settings
- **API Endpoint**: `http://127.0.0.1:8000/generate`
- **Image URL**: `http://127.0.0.1:8000/image/{filename}`
- **Animation Duration**: Configurable in CSS

##  Troubleshooting

### Common Issues

1. **422 Unprocessable Entity Error**
   - **Cause**: Frontend/Backend communication mismatch
   - **Fix**: Ensure both frontend and backend are running with latest code

2. **Blank Page**
   - **Cause**: Missing CSS styles or component errors
   - **Fix**: Check browser console for errors

3. **Slow Image Generation**
   - **Cause**: CPU-only processing
   - **Fix**: Install CUDA-compatible GPU for faster generation

4. **CORS Errors**
   - **Cause**: Backend not allowing frontend requests
   - **Fix**: Ensure FastAPI CORS middleware is configured

### Performance Tips
- **GPU Acceleration**: Use CUDA for 10x faster image generation
- **Scene Limit**: Start with 1-3 scenes for quicker results
- **Simple Prompts**: Clear, concise prompts work best

##  Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin amazing-feature`
5. Open a Pull Request

##  License

This project is licensed under the MIT License - see the LICENSE file for details.

##  Acknowledgments

- **Stability AI**: For the amazing Stable Diffusion model
- **React Team**: For the incredible UI framework
- **Framer Motion**: For beautiful animations
- **FastAPI**: For the modern Python web framework

##  Created With ❤️ for Kids

This application was designed to spark creativity and imagination in children. Every animation, color, and interaction was carefully crafted to create a magical storytelling experience!

---

**Made with 💜 for young storytellers everywhere!**