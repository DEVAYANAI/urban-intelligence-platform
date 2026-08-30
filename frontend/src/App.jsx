import { useState } from "react";
import "./App.css";

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  // Select video
  const handleFileChange = (event) => {
    const file = event.target.files[0];

    if (file) {
      setSelectedFile(file);
      setResult(null);
      setError("");
    }
  };

  // Send video to FastAPI
  const analyzeVideo = async () => {
    if (!selectedFile) {
      setError("Please select a traffic video first.");
      return;
    }

    setLoading(true);
    setError("");
    setResult(null);

    const formData = new FormData();

    formData.append("file", selectedFile);

    try {
      const response = await fetch("http://127.0.0.1:8000/analyze-video", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error("Video analysis failed.");
      }

      const data = await response.json();

      setResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">
      {/* HEADER */}

      <header className="header">
        <div>
          <h1>URBAN INTELLIGENCE</h1>

          <p>AI-Powered Traffic & Road Event Monitoring System</p>
        </div>

        <div className="system-status">
          <span className="status-dot"></span>
          SYSTEM ONLINE
        </div>
      </header>

      {/* MAIN */}

      <main className="main-container">
        {/* HERO */}

        <section className="hero">
          <div className="hero-badge">AI TRAFFIC ANALYSIS</div>

          <h2>Intelligent Traffic Monitoring</h2>

          <p>
            Upload traffic footage and let our AI analyze vehicle density and
            possible road events.
          </p>
        </section>

        {/* UPLOAD CARD */}

        <section className="upload-card">
          <div className="upload-icon">📹</div>

          <h3>Upload Traffic Video</h3>

          <p>Select a video from a bus camera or traffic camera.</p>

          <input type="file" accept="video/*" onChange={handleFileChange} />

          {selectedFile && (
            <div className="selected-file">
              <span>📁</span>

              <span>{selectedFile.name}</span>
            </div>
          )}

          <button
            className="analyze-btn"
            onClick={analyzeVideo}
            disabled={loading}
          >
            {loading ? "AI ANALYZING..." : "ANALYZE WITH AI"}
          </button>
        </section>

        {/* ERROR */}

        {error && <div className="error-box">⚠ {error}</div>}

        {/* LOADING */}

        {loading && (
          <div className="loading-card">
            <div className="loader"></div>

            <h3>AI is analyzing your traffic video</h3>

            <p>Detecting vehicles and analyzing road conditions...</p>
          </div>
        )}

        {/* RESULTS */}

        {result && (
          <section className="results-section">
            {/* RESULT HEADER */}

            <div className="section-header">
              <div>
                <p className="section-label">AI ANALYSIS COMPLETE</p>

                <h2>Traffic Intelligence Report</h2>
              </div>

              <div
                className={`traffic-badge ${result.traffic_level?.toLowerCase()}`}
              >
                {result.traffic_level} TRAFFIC
              </div>
            </div>

            {/* VEHICLE CARDS */}

            <div className="stats-grid">
              <div className="stat-card">
                <div className="stat-icon">🚗</div>

                <p>Cars</p>

                <h3>{result.cars}</h3>
              </div>

              <div className="stat-card">
                <div className="stat-icon">🏍️</div>

                <p>Motorcycles</p>

                <h3>{result.motorcycles}</h3>
              </div>

              <div className="stat-card">
                <div className="stat-icon">🚌</div>

                <p>Buses</p>

                <h3>{result.buses}</h3>
              </div>

              <div className="stat-card">
                <div className="stat-icon">🚛</div>

                <p>Trucks</p>

                <h3>{result.trucks}</h3>
              </div>
            </div>

            {/* TRAFFIC SUMMARY */}

            <div className="summary-grid">
              <div className="summary-card">
                <p>TOTAL VEHICLES</p>

                <h2>{result.total_vehicles}</h2>

                <span>Maximum vehicles detected</span>
              </div>

              <div className="summary-card">
                <p>TRAFFIC LEVEL</p>

                <h2>{result.traffic_level}</h2>

                <span>AI traffic density classification</span>
              </div>

              <div className="summary-card">
                <p>ANALYSIS TIME</p>

                <h2 className="time-text">
                  {result.timestamp
                    ? new Date(result.timestamp).toLocaleTimeString()
                    : "--"}
                </h2>

                <span>AI processing timestamp</span>
              </div>
            </div>

            {/* ROAD EVENT */}

            <section
              className={`road-event-card ${
                result.road_event_detected ? "event-detected" : "event-clear"
              }`}
            >
              <div className="road-event-header">
                <div>
                  <p className="section-label">ROAD EVENT ANALYSIS</p>

                  <h2>🚨 Road Condition Intelligence</h2>
                </div>

                <div
                  className={`event-status ${
                    result.road_event_detected ? "detected" : "clear"
                  }`}
                >
                  {result.road_event_detected ? "EVENT DETECTED" : "NO EVENT"}
                </div>
              </div>

              <div className="road-event-grid">
                <div className="event-info">
                  <span>EVENT STATUS</span>

                  <h3>
                    {result.road_event_detected
                      ? "Detected"
                      : "No Event Detected"}
                  </h3>
                </div>

                <div className="event-info">
                  <span>EVENT TYPE</span>

                  <h3>
                    {result.road_event_type ? result.road_event_type : "None"}
                  </h3>
                </div>
              </div>

              {/* ALERT MESSAGE */}

              <div className="alert-box">
                <div className="alert-icon">
                  {result.road_event_detected ? "⚠️" : "✓"}
                </div>

                <div>
                  <p>AI ROUTE ALERT</p>

                  <h3>
                    {result.alert_message || "No alert information available."}
                  </h3>
                </div>
              </div>
            </section>
          </section>
        )}
      </main>

      {/* FOOTER */}

      <footer>Urban Intelligence Platform • AI Powered Monitoring</footer>
    </div>
  );
}

export default App;
