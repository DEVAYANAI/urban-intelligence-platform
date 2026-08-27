import { useState } from "react";
import "./App.css";

function App() {
  const [selectedVideo, setSelectedVideo] = useState(null);
  const [videoPreview, setVideoPreview] = useState(null);
  const [traffic, setTraffic] = useState(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);

  // Handle video selection
  const handleVideoChange = (event) => {
    const file = event.target.files[0];

    if (!file) {
      return;
    }

    setSelectedVideo(file);
    setTraffic(null);

    // Create preview URL
    const previewURL = URL.createObjectURL(file);
    setVideoPreview(previewURL);
  };

  // Temporary analysis function
  // Later this will call your FastAPI backend
  const handleAnalyze = () => {
    if (!selectedVideo) {
      return;
    }

    setIsAnalyzing(true);
    setTraffic(null);

    // Temporary delay to simulate AI processing
    setTimeout(() => {
      const aiResult = {
        event_type: "traffic_density",
        timestamp: "2026-08-26T22:02:34.304366",
        cars: 1,
        motorcycles: 4,
        buses: 0,
        trucks: 0,
        total_vehicles: 5,
        traffic_level: "LOW",
      };

      setTraffic(aiResult);
      setIsAnalyzing(false);
    }, 1500);
  };

  return (
    <main className="app">
      {/* ================= HEADER ================= */}

      <header className="topbar">
        <div>
          <div className="brand">
            <span className="brand-icon">◈</span>
            SADHAK NETRA
          </div>

          <p>AI-Powered Road Intelligence</p>
        </div>

        <div className="system-status">
          <span className="status-dot"></span>
          SYSTEM ONLINE
        </div>
      </header>

      {/* ================= INTRO ================= */}

      <section className="intro">
        <div>
          <span className="eyebrow">TRAFFIC ANALYSIS</span>

          <h1>Traffic Intelligence</h1>

          <p>AI-powered vehicle detection and traffic density analysis.</p>
        </div>
      </section>

      {/* ================= UPLOAD + STATUS ================= */}

      <section className="top-grid">
        {/* UPLOAD CARD */}

        <div className="upload-card">
          <div className="upload-icon">↑</div>

          <h2>Analyze Traffic Video</h2>

          <p>Upload a road or traffic video to detect and analyze vehicles.</p>

          {/* Hidden file input */}

          <input
            type="file"
            accept="video/*"
            id="video-upload"
            hidden
            onChange={handleVideoChange}
          />

          {/* Select button */}

          <label htmlFor="video-upload" className="upload-button">
            📁 Select Video
          </label>

          {/* Selected file */}

          {selectedVideo && (
            <div className="selected-video">
              <span>🎥</span>

              <div>
                <strong>{selectedVideo.name}</strong>

                <small>
                  {(selectedVideo.size / (1024 * 1024)).toFixed(2)} MB
                </small>
              </div>
            </div>
          )}

          {/* Analyze button */}

          {selectedVideo && (
            <button
              className="analyze-button"
              onClick={handleAnalyze}
              disabled={isAnalyzing}
            >
              {isAnalyzing ? "⏳ Analyzing..." : "▶ Analyze Video"}
            </button>
          )}

          <span className="upload-hint">
            MP4, AVI or MOV • Select a traffic video
          </span>
        </div>

        {/* VIDEO PREVIEW / STATUS CARD */}

        <div className="traffic-card">
          <div className="card-header">
            <span>VIDEO PREVIEW</span>

            {selectedVideo && <span className="live">● READY</span>}
          </div>

          {videoPreview ? (
            <video className="video-preview" src={videoPreview} controls />
          ) : (
            <div className="empty-video">
              <div>🎥</div>

              <p>No video selected</p>

              <span>Upload a traffic video to preview it</span>
            </div>
          )}
        </div>
      </section>

      {/* ================= RESULTS ================= */}

      {traffic && (
        <>
          {/* TRAFFIC STATUS */}

          <section className="traffic-result-card">
            <div className="result-header">
              <div>
                <span className="eyebrow">AI ANALYSIS RESULT</span>

                <h2>Traffic Status</h2>
              </div>

              <span className="analysis-complete">✓ ANALYSIS COMPLETE</span>
            </div>

            <div className="traffic-result-content">
              <div className="traffic-circle">
                <span>{traffic.traffic_level}</span>
              </div>

              <div className="result-info">
                <span>CURRENT TRAFFIC DENSITY</span>

                <strong>{traffic.traffic_level}</strong>

                <p>Based on {traffic.total_vehicles} detected vehicles.</p>

                <small>
                  Last analyzed: {new Date(traffic.timestamp).toLocaleString()}
                </small>
              </div>
            </div>
          </section>

          {/* VEHICLE DETECTION */}

          <section>
            <div className="section-title">
              <div>
                <span className="eyebrow">AI DETECTION</span>

                <h2>Vehicle Detection</h2>
              </div>

              <span className="detection-count">
                {traffic.total_vehicles} DETECTED
              </span>
            </div>

            <div className="vehicle-grid">
              <VehicleCard icon="🚗" number={traffic.cars} label="Cars" />

              <VehicleCard
                icon="🏍️"
                number={traffic.motorcycles}
                label="Motorcycles"
              />

              <VehicleCard icon="🚌" number={traffic.buses} label="Buses" />

              <VehicleCard icon="🚚" number={traffic.trucks} label="Trucks" />
            </div>
          </section>

          {/* ANALYTICS */}

          <section className="analytics-grid">
            {/* TOTAL */}

            <div className="total-card">
              <span className="eyebrow">TOTAL VEHICLES</span>

              <div className="total-number">
                {String(traffic.total_vehicles).padStart(2, "0")}
              </div>

              <p>Vehicles detected in the analyzed traffic scene.</p>

              <div className="total-line"></div>

              <span className="event-type">
                EVENT TYPE
                <strong>Traffic Density</strong>
              </span>
            </div>

            {/* DISTRIBUTION */}

            <div className="distribution-card">
              <div className="section-heading">
                <div>
                  <span className="eyebrow">BREAKDOWN</span>

                  <h3>Vehicle Distribution</h3>
                </div>
              </div>

              <Distribution
                label="Cars"
                value={traffic.cars}
                total={traffic.total_vehicles}
              />

              <Distribution
                label="Motorcycles"
                value={traffic.motorcycles}
                total={traffic.total_vehicles}
              />

              <Distribution
                label="Buses"
                value={traffic.buses}
                total={traffic.total_vehicles}
              />

              <Distribution
                label="Trucks"
                value={traffic.trucks}
                total={traffic.total_vehicles}
              />
            </div>
          </section>
        </>
      )}

      {/* ================= INITIAL STATE ================= */}

      {!traffic && !isAnalyzing && !selectedVideo && (
        <section className="welcome-message">
          <div className="welcome-icon">✦</div>

          <h2>Ready for Traffic Analysis</h2>

          <p>
            Upload a traffic video above to begin vehicle detection and traffic
            analysis.
          </p>
        </section>
      )}

      {/* ================= ANALYZING ================= */}

      {isAnalyzing && (
        <section className="processing-card">
          <div className="spinner"></div>

          <h2>Analyzing Traffic Video</h2>

          <p>AI is detecting and tracking vehicles...</p>

          <div className="processing-steps">
            <span>✓ Video uploaded</span>

            <span>✓ YOLO detection</span>

            <span>⏳ Vehicle analysis</span>
          </div>
        </section>
      )}

      {/* ================= FOOTER ================= */}

      <footer>SADHAK NETRA • AI-Powered Road Intelligence</footer>
    </main>
  );
}

/* ================================================= */
/* VEHICLE CARD                                     */
/* ================================================= */

function VehicleCard({ icon, number, label }) {
  return (
    <div className="vehicle-card">
      <div className="vehicle-icon">{icon}</div>

      <div className="vehicle-number">{String(number).padStart(2, "0")}</div>

      <div className="vehicle-label">{label}</div>
    </div>
  );
}

/* ================================================= */
/* DISTRIBUTION                                     */
/* ================================================= */

function Distribution({ label, value, total }) {
  const percentage = total > 0 ? (value / total) * 100 : 0;

  return (
    <div className="distribution-row">
      <div className="distribution-info">
        <span>{label}</span>

        <strong>{value}</strong>
      </div>

      <div className="progress">
        <div
          className="progress-fill"
          style={{
            width: `${percentage}%`,
          }}
        ></div>
      </div>
    </div>
  );
}

export default App;
