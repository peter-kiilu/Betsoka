import { useState, useEffect } from 'react';
import { useApp } from '../context/AppContext';
import { getFeatures } from '../api';

export default function Predictions() {
  const { status, trainingResults, predict, loading } = useApp();
  const [features, setFeatures] = useState([]);
  const [values, setValues] = useState({});
  const [selectedModel, setSelectedModel] = useState('');
  const [result, setResult] = useState(null);

  useEffect(() => {
    getFeatures().then(({ data }) => {
      setFeatures(data.features);
      const defaults = {};
      data.features.forEach(f => { defaults[f.key] = f.default; });
      setValues(defaults);
    }).catch(() => {});
  }, []);

  useEffect(() => {
    if (trainingResults?.comparison?.length) {
      setSelectedModel(trainingResults.comparison[0].Model);
    }
  }, [trainingResults]);

  const handlePredict = async () => {
    const payload = { model_name: selectedModel, ...values };
    const res = await predict(payload);
    if (res) setResult(res);
  };

  const outcomeClass = (label) => {
    if (label === 'Home Win') return 'win';
    if (label === 'Draw') return 'draw';
    return 'loss';
  };

  if (!status.models_trained) {
    return (
      <>
        <div className="page-header">
          <h2>🎯 Match Predictor</h2>
          <p>Input match features and predict the outcome</p>
        </div>
        <div className="card" style={{ textAlign: 'center', padding: '3rem' }}>
          <p style={{ fontSize: '2.5rem', marginBottom: '1rem' }}>🔒</p>
          <h3 style={{ color: 'var(--text-primary)', marginBottom: '0.5rem' }}>Models Not Ready</h3>
          <p style={{ color: 'var(--text-secondary)' }}>Generate data and train models using the sidebar first.</p>
        </div>
      </>
    );
  }

  return (
    <>
      <div className="page-header">
        <h2>🎯 Match Predictor</h2>
        <p>Input simulated match statistics and let the AI predict the result</p>
      </div>

      {/* Feature Inputs */}
      <div className="card" style={{ marginBottom: '1.5rem' }}>
        <div className="card-header">Match Features</div>
        <div className="grid-3">
          {features.map(f => (
            <div key={f.key} className="feature-input">
              <label>{f.label}</label>
              <input type="range" min={f.min} max={f.max} step={f.step}
                value={values[f.key] ?? f.default}
                onChange={e => setValues(v => ({ ...v, [f.key]: +e.target.value }))} />
              <div className="input-value">{values[f.key] ?? f.default}</div>
            </div>
          ))}
        </div>
      </div>

      {/* Model Select & Predict Button */}
      <div style={{ display: 'flex', gap: '1rem', marginBottom: '1.5rem', alignItems: 'flex-end' }}>
        <div style={{ flex: 1 }} className="select-wrapper">
          <label style={{ display: 'block', fontSize: '0.78rem', color: 'var(--text-secondary)', marginBottom: '0.35rem' }}>
            Model
          </label>
          <select value={selectedModel} onChange={e => setSelectedModel(e.target.value)}>
            {trainingResults?.comparison?.map(m => (
              <option key={m.Model} value={m.Model}>{m.Model}</option>
            ))}
          </select>
        </div>
        <button className="btn btn-primary" onClick={handlePredict} disabled={loading.predict}
          style={{ flex: 0, minWidth: '200px' }}>
          {loading.predict ? <><span className="spinner" /> Predicting...</> : '🚀 Predict Outcome'}
        </button>
      </div>

      {/* Result */}
      {result && (
        <div className="card">
          <div className="card-header">Prediction Result — {result.model_used}</div>
          <div className="prediction-result">
            <div className="result-outcome card" style={{ borderLeft: '4px solid' }}>
              <div className={`outcome-label ${outcomeClass(result.predicted_outcome)}`}>
                {result.predicted_outcome}
              </div>
              <div className="result-confidence">{result.confidence}% confidence</div>
            </div>
            <div className="result-bars" style={{ flex: 1 }}>
              {Object.entries(result.probabilities).map(([label, pct]) => (
                <div key={label} className="prob-bar-container">
                  <div className="prob-bar-header">
                    <span className="label">{label}</span>
                    <span className="value" style={{ color: `var(--${outcomeClass(label)})` }}>{pct}%</span>
                  </div>
                  <div className="prob-bar-track">
                    <div className={`prob-bar-fill ${outcomeClass(label)}`} style={{ width: `${pct}%` }} />
                  </div>
                </div>
              ))}
            </div>
          </div>
          <p style={{ fontSize: '0.78rem', color: 'var(--text-muted)', marginTop: '1rem' }}>
            ⚠️ Probabilistic estimates from synthetic data. For educational purposes only.
          </p>
        </div>
      )}
    </>
  );
}
