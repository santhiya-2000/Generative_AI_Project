import { useState } from "react";
import "./App.css";

function App() {
  const [prompt, setPrompt] = useState("");
  const [count, setCount] = useState(1);
  const [images, setImages] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleGenerate = async () => {
    if (!prompt) return alert("Enter a story prompt!");
    setLoading(true);
    const form = new FormData();
    form.append("prompt", prompt);
    form.append("count", count);

    const res = await fetch("http://127.0.0.1:8000/generate", {
      method: "POST",
      body: form,
    });
    const data = await res.json();
    setImages(data.images);
    setLoading(false);
  };

  return (
    <div style={{ textAlign: "center", padding: "30px" }}>
      <h1>AI Story Illustrator</h1>
      <textarea
        rows="3"
        cols="60"
        placeholder="Enter your story idea..."
        value={prompt}
        onChange={(e) => setPrompt(e.target.value)}
        style={{ margin: "10px" }}
      />
      <br />
      <label>Number of Scenes: </label>
      <input
        type="number"
        min="1"
        max="10"
        value={count}
        onChange={(e) => setCount(e.target.value)}
      />
      <br /><br />
      <button
        onClick={handleGenerate}
        disabled={loading}
        style={{
          padding: "10px 20px",
          backgroundColor: "#007bff",
          color: "#fff",
          border: "none",
          borderRadius: "8px",
        }}
      >
        {loading ? "Generating..." : "Generate Story"}
      </button>

      <div style={{ marginTop: "40px" }}>
        {images.length > 0 && <h2>Story Scenes</h2>}
        <div
          style={{
            display: "flex",
            flexWrap: "wrap",
            justifyContent: "center",
            gap: "20px",
          }}
        >
          {images.map((img, i) => (
            <div key={i} style={{ textAlign: "center" }}>
              <h3>Scene {i + 1}</h3>
              <img
                src={`http://127.0.0.1:8000/image/${img.split("/").pop()}`}
                alt={`Scene ${i + 1}`}
                style={{
                  width: "512px",
                  borderRadius: "10px",
                  boxShadow: "0 0 10px rgba(0,0,0,0.3)",
                }}
              />
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default App;
