"use client";

import React, { useState, useEffect } from 'react';

export default function Home() {
  const [url, setUrl] = useState('');
  const [jobId, setJobId] = useState(null);
  const [status, setStatus] = useState(null);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!url) return;

    setError(null);
    setStatus('initializing');
    
    try {
      const res = await fetch('http://localhost:8000/process?youtube_url=' + encodeURIComponent(url), {
        method: 'POST',
      });
      const data = await res.json();
      setJobId(data.job_id);
    } catch (err) {
      setError('Failed to connect to backend');
      setStatus(null);
    }
  };

  useEffect(() => {
    if (!jobId) return;

    const interval = setInterval(async () => {
      try {
        const res = await fetch(`http://localhost:8000/status/${jobId}`);
        const data = await res.json();
        setStatus(data.status);
        if (data.status === 'completed' || data.status === 'failed') {
          if (data.status === 'failed') setError(data.error);
          clearInterval(interval);
        }
      } catch (err) {
        console.error('Error checking status', err);
      }
    }, 2000);

    return () => clearInterval(interval);
  }, [jobId]);

  return (
    <main style={{ minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center', padding: '20px' }}>
      <div className="glass-card animate-glow" style={{ maxWidth: '600px', width: '100%', padding: '40px', textAlign: 'center' }}>
        <h1 style={{ fontSize: '2.5rem', marginBottom: '10px', fontWeight: '700', background: 'linear-gradient(to right, #6366f1, #ec4899)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>
          Youtube Slide Extractor
        </h1>
        <p style={{ opacity: 0.7, marginBottom: '30px' }}>
          Turn your favorite lectures into beautiful PDF slides instantly.
        </p>

        {!status || status === 'failed' ? (
          <form onSubmit={handleSubmit}>
            <input
              type="text"
              className="input-field"
              placeholder="Paste YouTube Link here..."
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              style={{ marginBottom: '20px' }}
            />
            {error && <p style={{ color: '#ef4444', marginBottom: '20px', fontSize: '0.9rem' }}>{error}</p>}
            <button type="submit" className="btn-primary" style={{ width: '100%' }}>
              Generate PDF
            </button>
          </form>
        ) : (
          <div style={{ padding: '20px' }}>
            {status === 'processing' || status === 'initializing' ? (
              <div>
                <div style={{ width: '100%', height: '8px', background: 'rgba(255,255,255,0.1)', borderRadius: '10px', marginBottom: '20px', overflow: 'hidden' }}>
                  <div className="progress-bar-animate" style={{ height: '100%', background: 'linear-gradient(to right, #6366f1, #a855f7)', width: '60%' }}></div>
                </div>
                <p>Analyzing video and extracting slides...</p>
                <p style={{ fontSize: '0.8rem', opacity: 0.5, marginTop: '10px' }}>This may take a minute depending on video length.</p>
              </div>
            ) : status === 'completed' ? (
              <div>
                <div style={{ fontSize: '4rem', marginBottom: '20px' }}>📄</div>
                <h3 style={{ marginBottom: '20px' }}>Extraction Complete!</h3>
                <a 
                  href={`http://localhost:8000/download/${jobId}`} 
                  className="btn-primary" 
                  style={{ textDecoration: 'none', display: 'inline-block' }}
                  download
                >
                  Download PDF
                </a>
                <button 
                  onClick={() => {setStatus(null); setJobId(null); setUrl('');}} 
                  style={{ display: 'block', margin: '20px auto 0', background: 'none', border: 'none', color: 'rgba(255,255,255,0.5)', cursor: 'pointer' }}
                >
                  Process another video
                </button>
              </div>
            ) : null}
          </div>
        )}
      </div>
      
      <style jsx>{`
        .progress-bar-animate {
          animation: progress 2s infinite ease-in-out;
        }
        @keyframes progress {
          0% { transform: translateX(-100%); }
          100% { transform: translateX(200%); }
        }
      `}</style>
    </main>
  );
}
