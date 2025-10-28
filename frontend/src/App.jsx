import React, { useState } from 'react';
import UploadForm from './components/UploadForm';
import ReportOutput from './components/ReportOutput';

function App() {
  const [note, setNote] = useState('');
  const [warnings, setWarnings] = useState([]);
  const [confidence, setConfidence] = useState(0);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleGenerate = async (payload) => {
    setLoading(true);
    setError('');
    try {
      // Use environment variable for API base URL
      // Vite reads environment variables prefixed with VITE_
      const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'; // Fallback for local dev
      const response = await fetch(`${API_BASE_URL}/generate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to generate note');
      }

      const data = await response.json();
      setNote(data.generated_note);
      setWarnings(data.warnings);
      setConfidence(data.confidence_score);
    } catch (err) {
      console.error("API Error:", err);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 p-4 md:p-8">
      <div className="max-w-7xl mx-auto">
        <header className="mb-8 text-center">
          <h1 className="text-3xl md:text-4xl font-bold text-gray-800">MedReportGen AI - Sickle Cell</h1>
          <p className="text-gray-600 mt-2">AI-Assisted Clinical Note Generation</p>
        </header>

        <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
          {/* Left Panel: Form and Output */}
          <div className="lg:col-span-3 space-y-6">
            <UploadForm onGenerate={handleGenerate} loading={loading} />
            {loading && <div className="text-center text-blue-600">Generating...</div>}
            {error && <div className="text-center text-red-600 p-4 bg-red-50 rounded-lg">Error: {error}</div>}
            {note && <ReportOutput note={note} warnings={warnings} confidence={confidence} />}
          </div>

          {/* Right Panel: Metrics Dashboard */}
          <div className="lg:col-span-1">
            <div className="bg-white p-6 rounded-xl shadow-md h-fit">
              <h2 className="text-xl font-semibold text-gray-800 mb-4">Dashboard Metrics</h2>
              <div className="space-y-4">
                <div className="p-4 bg-blue-50 rounded-lg">
                  <p className="text-sm text-blue-800">Notes Generated</p>
                  <p className="text-2xl font-bold text-blue-600">0</p> {/* Placeholder */}
                </div>
                <div className="p-4 bg-green-50 rounded-lg">
                  <p className="text-sm text-green-800">Avg. Confidence</p>
                  <p className="text-2xl font-bold text-green-600">{confidence ? `${(confidence * 100).toFixed(1)}%` : 'N/A'}</p>
                </div>
                <div className="p-4 bg-yellow-50 rounded-lg">
                  <p className="text-sm text-yellow-800">Warnings Raised</p>
                  <p className="text-2xl font-bold text-yellow-600">{warnings.length}</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;