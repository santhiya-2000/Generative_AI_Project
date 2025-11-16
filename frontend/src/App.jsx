import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { FaBookOpen, FaPlay, FaArrowLeft, FaArrowRight, FaRedo, FaCog } from "react-icons/fa";
import "./App.css";

function App() {
  const [storyPrompt, setStoryPrompt] = useState("");
  const [numScenes, setNumScenes] = useState(3);
  const [story, setStory] = useState(null);
  const [currentScene, setCurrentScene] = useState(0);
  const [isGenerating, setIsGenerating] = useState(false);

  const generateStory = async () => {
    if (!storyPrompt.trim()) return;
    
    setIsGenerating(true);
    try {
      const formData = new FormData();
      formData.append('prompt', storyPrompt);
      formData.append('count', numScenes);
      
      const response = await fetch('http://127.0.0.1:8000/generate', {
        method: 'POST',
        body: formData
      });
      
      const data = await response.json();
      setStory(data);
      setCurrentScene(0);
    } catch (error) {
      console.error('Error generating story:', error);
    } finally {
      setIsGenerating(false);
    }
  };

  const nextScene = () => {
    if (currentScene < story.images.length - 1) {
      setCurrentScene(currentScene + 1);
    }
  };

  const prevScene = () => {
    if (currentScene > 0) {
      setCurrentScene(currentScene - 1);
    }
  };

  const resetStory = () => {
    setStory(null);
    setCurrentScene(0);
    setStoryPrompt("");
  };

  return (
    <div className="app-container">
      <header className="app-header">
        <div className="header-content">
          <div className="logo">
            <FaBookOpen className="logo-icon" />
            <h1>StoryIllustrator AI</h1>
          </div>
        </div>
        <div className="header-info">
          <p>AI-Powered Story Generation with Illustrations</p>
        </div>
      </header>

      <main className="main-content">
        <AnimatePresence mode="wait">
          {!story ? (
            <motion.div 
              className="creator-panel"
              key="creator"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              transition={{ duration: 0.3 }}
            >
              <div className="panel-header">
                <h2>Create New Story</h2>
                <p>Enter a story prompt and generate AI-powered illustrations</p>
              </div>

              <div className="input-group">
                <label htmlFor="story-prompt">Story Prompt</label>
                <textarea
                  id="story-prompt"
                  value={storyPrompt}
                  onChange={(e) => setStoryPrompt(e.target.value)}
                  placeholder="Describe your story concept... (e.g., 'A brave knight discovers a hidden forest filled with magical creatures')"
                  rows={6}
                />
              </div>

              <div className="options-group">
                <div className="option-item">
                  <label htmlFor="scene-count">Number of Scenes</label>
                  <select 
                    id="scene-count" 
                    value={numScenes} 
                    onChange={(e) => setNumScenes(parseInt(e.target.value))}
                  >
                    <option value={1}>1 Scene</option>
                    <option value={2}>2 Scenes</option>
                    <option value={3}>3 Scenes</option>
                    <option value={4}>4 Scenes</option>
                    <option value={5}>5 Scenes</option>
                  </select>
                </div>
              </div>

              <motion.button
                className="generate-button"
                onClick={generateStory}
                disabled={!storyPrompt.trim() || isGenerating}
                whileHover={{ scale: storyPrompt.trim() && !isGenerating ? 1.02 : 1 }}
                whileTap={{ scale: storyPrompt.trim() && !isGenerating ? 0.98 : 1 }}
              >
                {isGenerating ? (
                  <>
                    <div className="loading-spinner"></div>
                    Generating Story...
                  </>
                ) : (
                  <>
                    <FaPlay /> Generate Story
                  </>
                )}
              </motion.button>
            </motion.div>
          ) : (
            <motion.div 
              className="viewer-panel"
              key="viewer"
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -20 }}
              transition={{ duration: 0.3 }}
            >
              <div className="viewer-header">
                <div className="viewer-title">
                  <h2>Generated Story</h2>
                  <span className="scene-counter">Scene {currentScene + 1} of {story.images.length}</span>
                </div>
                <button className="reset-button" onClick={resetStory}>
                  <FaRedo /> New Story
                </button>
              </div>

              <div className="story-content">
                <AnimatePresence mode="wait">
                  <motion.div
                    key={currentScene}
                    className="scene-panel"
                    initial={{ opacity: 0, x: 50 }}
                    animate={{ opacity: 1, x: 0 }}
                    exit={{ opacity: 0, x: -50 }}
                    transition={{ duration: 0.3 }}
                  >
                    <div className="illustration-container">
                      <img 
                        src={`http://127.0.0.1:8000/image/${story.images[currentScene]}`}
                        alt={`Scene ${currentScene + 1}`}
                        className="illustration"
                      />
                    </div>
                    <div className="story-text">
                      <h3>Scene {currentScene + 1}</h3>
                      <p>{story.story[currentScene]}</p>
                    </div>
                  </motion.div>
                </AnimatePresence>
              </div>

              <div className="viewer-controls">
                <button 
                  className="control-button prev" 
                  onClick={prevScene}
                  disabled={currentScene === 0}
                >
                  <FaArrowLeft /> Previous
                </button>
                
                <div className="scene-indicators">
                  {story.images.map((_, index) => (
                    <button
                      key={index}
                      className={`indicator ${index === currentScene ? 'active' : ''}`}
                      onClick={() => setCurrentScene(index)}
                    >
                      {index + 1}
                    </button>
                  ))}
                </div>
                
                <button 
                  className="control-button next" 
                  onClick={nextScene}
                  disabled={currentScene === story.images.length - 1}
                >
                  Next <FaArrowRight />
                </button>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </main>
    </div>
  );
}

export default App;
