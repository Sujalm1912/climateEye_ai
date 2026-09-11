import React, { useEffect, useState } from 'react';
import { apiClient } from './services/api';

interface HealthStatus {
  status: string;
  service: string;
  version?: string;
}

export const App: React.FC = () => {
  const [health, setHealth] = useState<HealthStatus | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    // Check connection with the FastAPI backend
    apiClient
      .get<HealthStatus>('/health')
      .then((data) => {
        setHealth(data);
        setError(null);
      })
      .catch((err) => {
        console.warn('Backend connection notice:', err);
        setError(err.message || 'Unable to connect to FastAPI backend');
      })
      .finally(() => {
        setLoading(false);
      });
  }, []);

  return (
    <div className="app-container">
      {/* Navigation / Header */}
      <header className="app-header">
        <div className="logo-badge">
          <div className="logo-icon">
            <svg viewBox="0 0 24 24">
              <path d="M12 2a10 10 0 1 0 10 10A10 10 0 0 0 12 2zm1 17.93A8 8 0 0 1 4.07 13H7a1 1 0 0 0 1-1V9a1 1 0 0 0 1-1h1V6a1 1 0 0 0-1-1h-.29A8 8 0 0 1 13 4.07V6a1 1 0 0 0 1 1h2a1 1 0 0 0 1-1V4.25A8 8 0 0 1 19.93 11H17a1 1 0 0 0-1 1v1a1 1 0 0 0 1 1h2.7A8 8 0 0 1 13 19.93z" />
            </svg>
          </div>
          <span>ClimateEye AI</span>
        </div>

        <div className="system-badge" id="backend-status-badge">
          <span
            className={`status-indicator ${
              loading ? '' : health?.status === 'ok' ? 'connected' : 'error'
            }`}
          />
          <span>
            {loading
              ? 'Checking backend...'
              : health?.status === 'ok'
              ? `Backend: Connected (${health.service})`
              : 'Backend: Disconnected'}
          </span>
        </div>
      </header>

      {/* Main Hero View */}
      <main className="hero-content">
        <h1 className="project-title" id="main-title">ClimateEye AI</h1>
        <p className="tagline">"See Earth through data. Understand it through AI."</p>

        <div className="placeholder-card" id="placeholder-container">
          <h2 className="placeholder-text">Environmental intelligence starts here.</h2>
          <p className="placeholder-desc">
            The foundation is configured with a high-performance FastAPI backend,
            Open-Meteo meteorological services, and Google Gemini AI ready for full integration.
          </p>

          <div className="architecture-chips">
            <span className="chip">React + Vite + TypeScript</span>
            <span className="chip">FastAPI Backend</span>
            <span className="chip">Open-Meteo Weather</span>
            <span className="chip">google-genai SDK</span>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="app-footer">
        <div>ClimateEye AI — Competition Foundation</div>
        <div className="footer-meta">
          <span>Phase 1: Foundation Setup</span>
          {error && <span style={{ color: '#ef4444' }}>Backend offline</span>}
        </div>
      </footer>
    </div>
  );
};

export default App;
