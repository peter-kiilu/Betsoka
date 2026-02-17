export default function About() {
  return (
    <>
      <div className="page-header">
        <h2>⚙️ System Information</h2>
        <p>Academic context, architecture, and presentation notes</p>
      </div>

      <details className="info-section" open>
        <summary>🧪 How Synthetic Data Is Generated</summary>
        <div className="info-body">
          <p>The system generates <strong>2,000+</strong> simulated matches using a probabilistic framework:</p>
          <ol style={{ paddingLeft: '1.2rem', marginTop: '0.5rem' }}>
            <li><strong>Base Features</strong> — Each team gets a random strength (35–95) and form score.</li>
            <li><strong>Derived Stats</strong> — Goals, shots, possession are computed from strength + Gaussian noise.</li>
            <li><strong>Latent Score Model</strong> — The match outcome is determined by:</li>
          </ol>
          <p style={{ marginTop: '0.5rem' }}>
            <code>Score = (HomeStr − AwayStr) × 0.35 + (HomeForm − AwayForm) × 2.0 + HomeAdv + Noise</code>
          </p>
          <p>Score &gt; 7 → Home Win | Score &lt; −7 → Away Win | Else → Draw</p>
        </div>
      </details>

      <details className="info-section">
        <summary>🧠 Model Architectures</summary>
        <div className="info-body">
          <table className="comparison-table">
            <thead><tr><th>Model</th><th>Type</th><th>Key Parameters</th></tr></thead>
            <tbody>
              <tr><td>Logistic Regression</td><td>Linear Baseline</td><td>solver=lbfgs, multinomial</td></tr>
              <tr><td>Random Forest</td><td>Ensemble</td><td>150 trees, max_depth=12</td></tr>
              <tr><td>Neural Network</td><td>Deep Learning</td><td>64→32→16 MLP, dropout=0.3</td></tr>
            </tbody>
          </table>
        </div>
      </details>

      <details className="info-section">
        <summary>📐 Why Models Differ in Performance</summary>
        <div className="info-body">
          <ul style={{ paddingLeft: '1.2rem' }}>
            <li><strong>Logistic Regression</strong> assumes linear separability; football features often interact non-linearly.</li>
            <li><strong>Random Forest</strong> captures non-linear interactions via ensemble decision trees.</li>
            <li><strong>ANN</strong> learns hierarchical feature representations but may overfit on smaller datasets.</li>
          </ul>
        </div>
      </details>

      <details className="info-section">
        <summary>🎓 Academic Conclusion</summary>
        <div className="info-body">
          <p>
            Football outcome prediction is inherently stochastic — even with perfect features,
            the random variance in sport limits achievable accuracy to roughly 50–70%.
          </p>
          <p style={{ marginTop: '0.5rem' }}>
            This system demonstrates that a complete ML pipeline — from data generation through
            preprocessing, training, evaluation, to interactive deployment — provides a robust
            framework for decision support in sports analytics.
          </p>
          <p style={{ marginTop: '0.5rem' }}><strong>Key takeaways:</strong></p>
          <ul style={{ paddingLeft: '1.2rem' }}>
            <li>Ensemble methods handle non-linear feature interactions well.</li>
            <li>Neural networks require careful regularization on tabular data.</li>
            <li>Probabilistic outputs are always preferred over hard classifications.</li>
          </ul>
        </div>
      </details>

      <details className="info-section">
        <summary>🔮 Future Improvements</summary>
        <div className="info-body">
          <ul style={{ paddingLeft: '1.2rem' }}>
            <li>Player-level data — injuries, suspensions, individual form.</li>
            <li>Temporal models — LSTMs or Transformers for time-series trends.</li>
            <li>Real-world calibration — map synthetic distributions to historical data.</li>
            <li>Explainability — SHAP values for per-prediction attribution.</li>
          </ul>
        </div>
      </details>

      <details className="info-section">
        <summary>🏗️ System Architecture</summary>
        <div className="info-body">
          <pre style={{ background: 'var(--bg-primary)', padding: '1rem', borderRadius: '8px', fontSize: '0.82rem', lineHeight: 1.6 }}>
{`├── api/                     # FastAPI REST backend
│   ├── main.py              # App + CORS
│   └── routes.py            # Endpoints
│
├── core/                    # ML business logic
│   ├── config.py            # Configuration
│   ├── data_processing.py   # Data gen & preprocessing
│   └── services.py          # Training & prediction
│
├── frontend/                # React / Vite
│   └── src/
│       ├── pages/           # Dashboard, Predictions, Analytics, About
│       ├── components/      # Sidebar
│       └── context/         # App state
│
├── requirements.txt
└── README.md`}
          </pre>
        </div>
      </details>

      <div style={{ textAlign: 'center', padding: '2rem 0', color: 'var(--text-muted)', fontSize: '0.8rem' }}>
        BETSOKA © 2026 — AI Football Match Outcome Prediction Demo System — University Assignment
      </div>
    </>
  );
}
