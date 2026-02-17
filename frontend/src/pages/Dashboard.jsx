import { useState, useEffect } from 'react';
import { useApp } from '../context/AppContext';
import { generateFixtures, teamsToFeatures } from '../data/teams';
import H2HModal from '../components/H2HModal';

const MATCHDAYS = [24, 25, 26, 27, 28];

export default function Dashboard() {
  const { status, trainingResults, predict, loading } = useApp();
  const [activeMatchday, setActiveMatchday] = useState(25);
  const [fixtures, setFixtures] = useState([]);
  const [predictions, setPredictions] = useState({});
  const [selectedMatch, setSelectedMatch] = useState(null);

  useEffect(() => {
    setFixtures(generateFixtures(undefined, activeMatchday));
    setPredictions({});
  }, [activeMatchday]);

  // Auto-predict all fixtures when models are ready
  useEffect(() => {
    if (!status.models_trained || fixtures.length === 0) return;

    const predictAll = async () => {
      const bestModel = trainingResults?.comparison?.[0]?.Model || 'Random Forest';
      const results = {};
      for (const fix of fixtures) {
        const features = teamsToFeatures(fix.home, fix.away);
        try {
          const res = await predict({ model_name: bestModel, ...features });
          if (res) results[fix.id] = res;
        } catch { /* skip */ }
      }
      setPredictions(results);
    };
    predictAll();
  }, [status.models_trained, fixtures, trainingResults, predict]);

  const getOutcomeColor = (outcome) => {
    if (outcome === 'Home Win') return 'var(--win)';
    if (outcome === 'Draw') return 'var(--draw)';
    return 'var(--loss)';
  };

  const getOutcomeShort = (outcome) => {
    if (outcome === 'Home Win') return 'H';
    if (outcome === 'Draw') return 'D';
    return 'A';
  };

  return (
    <>
      {/* League Header */}
      <div className="league-header">
        <div className="league-title">
          <img src="/logos/premier-league.png" alt="Premier League" className="league-badge-img" />
          <div>
            <h2>Premier League</h2>
            <span className="league-country">England</span>
          </div>
        </div>
        <div className="league-tag">AI Predictions</div>
      </div>

      {/* Matchday Tabs */}
      <div className="matchday-tabs">
        {MATCHDAYS.map(md => (
          <button
            key={md}
            className={`matchday-tab ${activeMatchday === md ? 'active' : ''}`}
            onClick={() => setActiveMatchday(md)}
          >
            <span className="md-label">Matchday</span>
            <span className="md-number">{md}</span>
          </button>
        ))}
      </div>

      {/* Loading Bar */}
      {(loading.generate || loading.train) && (
        <div className="loading-banner">
          <span className="spinner" />
          {loading.generate ? 'Generating match data...' : 'Training models...'}
        </div>
      )}

      {/* Match Cards */}
      <div className="match-list">
        {fixtures.map(fix => {
          const pred = predictions[fix.id];
          return (
            <div 
              key={fix.id} 
              className="match-card"
              onClick={() => setSelectedMatch(fix)}
              style={{ cursor: 'pointer' }}
            >
              {/* Home Team */}
              <div className="match-team home">
                {fix.home.logo ? (
                  <img src={fix.home.logo} alt={fix.home.name} className="team-logo" />
                ) : (
                  <span className="team-badge" style={{ background: fix.home.color }}>
                    {fix.home.short.charAt(0)}
                  </span>
                )}
                <span className="team-name">{fix.home.name}</span>
              </div>

              {/* Center: Prediction or Time */}
              <div className="match-center">
                {pred ? (
                  <>
                    <div className="match-prediction" style={{ color: getOutcomeColor(pred.predicted_outcome) }}>
                      {getOutcomeShort(pred.predicted_outcome)}
                    </div>
                    <div className="match-confidence">{pred.confidence}%</div>
                    <div className="match-probs">
                      <span style={{ color: 'var(--win)' }}>{pred.probabilities['Home Win']}%</span>
                      <span style={{ color: 'var(--draw)' }}>{pred.probabilities['Draw']}%</span>
                      <span style={{ color: 'var(--loss)' }}>{pred.probabilities['Away Win']}%</span>
                    </div>
                  </>
                ) : (
                  <div className="match-time">{fix.time}</div>
                )}
              </div>

              {/* Away Team */}
              <div className="match-team away">
                <span className="team-name">{fix.away.name}</span>
                {fix.away.logo ? (
                  <img src={fix.away.logo} alt={fix.away.name} className="team-logo" />
                ) : (
                  <span className="team-badge" style={{ background: fix.away.color }}>
                    {fix.away.short.charAt(0)}
                  </span>
                )}
              </div>
            </div>
          );
        })}
      </div>

      {!status.models_trained && (
        <div className="card" style={{ textAlign: 'center', padding: '2rem', marginTop: '1rem' }}>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.85rem' }}>
            ⏳ Waiting for models to initialize... Predictions will appear automatically.
          </p>
        </div>
      )}

      {/* H2H Modal */}
      {selectedMatch && (
        <H2HModal 
          home={selectedMatch.home} 
          away={selectedMatch.away} 
          onClose={() => setSelectedMatch(null)} 
        />
      )}
    </>
  );
}
