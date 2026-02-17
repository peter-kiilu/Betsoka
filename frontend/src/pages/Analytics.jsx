import { useState } from 'react';
import { useApp } from '../context/AppContext';
import {
  BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell, RadarChart,
  PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar, Legend,
} from 'recharts';

const COLORS = ['#6C63FF', '#00D2FF', '#F7B731'];
const CM_LABELS = ['Away Win', 'Draw', 'Home Win'];

function ConfusionMatrix({ matrix, title }) {
  if (!matrix) return null;
  const maxVal = Math.max(...matrix.flat());

  return (
    <div className="card" style={{marginBottom: '1.2rem'}}>
      <div className="card-header">{title}</div>
      <div style={{ display: 'flex', gap: '0.5rem', fontSize: '0.7rem', color: 'var(--text-muted)', marginBottom: '0.5rem' }}>
        <span>Rows = Actual</span><span>|</span><span>Columns = Predicted</span>
      </div>
      <div className="confusion-grid">
        <div className="confusion-header"></div>
        {CM_LABELS.map(l => <div key={l} className="confusion-header">{l.split(' ')[0]}</div>)}
        {matrix.map((row, i) => (
          <>
            <div key={`label-${i}`} className="confusion-header">{CM_LABELS[i].split(' ')[0]}</div>
            {row.map((val, j) => {
              const intensity = maxVal > 0 ? val / maxVal : 0;
              return (
                <div key={`${i}-${j}`} className="confusion-cell" style={{
                  background: `rgba(108, 99, 255, ${0.1 + intensity * 0.6})`,
                  color: intensity > 0.4 ? 'white' : 'var(--text-secondary)',
                }}>
                  {val}
                </div>
              );
            })}
          </>
        ))}
      </div>
    </div>
  );
}

export default function Analytics() {
  const { trainingResults } = useApp();
  const [activeTab, setActiveTab] = useState('comparison');

  if (!trainingResults) {
    return (
      <>
        <div className="page-header">
          <h2>📊 Analytics</h2>
          <p>Model evaluation and performance analysis</p>
        </div>
        <div className="card" style={{ textAlign: 'center', padding: '3rem' }}>
          <p style={{ fontSize: '2.5rem', marginBottom: '1rem' }}>📊</p>
          <h3 style={{ color: 'var(--text-primary)', marginBottom: '0.5rem' }}>No Results Yet</h3>
          <p style={{ color: 'var(--text-secondary)' }}>Train models to view analytics.</p>
        </div>
      </>
    );
  }

  const { comparison, results, feature_importance } = trainingResults;

  // Prepare radar chart data
  const radarData = ['Accuracy', 'Precision', 'Recall', 'F1-Score', 'ROC-AUC'].map(metric => {
    const entry = { metric };
    comparison.forEach(m => { entry[m.Model] = +(m[metric] * 100).toFixed(1); });
    return entry;
  });

  // Accuracy bar chart data
  const barData = comparison.map((m, i) => ({
    name: m.Model,
    accuracy: +(m.Accuracy * 100).toFixed(1),
    color: COLORS[i],
  }));

  return (
    <>
      <div className="page-header">
        <h2>📊 Model Analytics</h2>
        <p>Evaluate and compare machine learning model performance</p>
      </div>

      {/* Tabs */}
      <div className="tabs">
        {['comparison', 'confusion', 'features'].map(tab => (
          <button key={tab} className={`tab ${activeTab === tab ? 'active' : ''}`}
            onClick={() => setActiveTab(tab)}>
            {tab === 'comparison' ? 'Comparison' : tab === 'confusion' ? 'Confusion Matrices' : 'Feature Importance'}
          </button>
        ))}
      </div>

      {/* Comparison Tab */}
      {activeTab === 'comparison' && (
        <>
          <div className="card" style={{ marginBottom: '1.5rem' }}>
            <div className="card-header">Performance Table</div>
            <table className="comparison-table">
              <thead>
                <tr>
                  <th>Model</th>
                  <th>Accuracy</th>
                  <th>Precision</th>
                  <th>Recall</th>
                  <th>F1-Score</th>
                  <th>ROC-AUC</th>
                </tr>
              </thead>
              <tbody>
                {comparison.map((row, i) => (
                  <tr key={row.Model}>
                    <td style={{ fontWeight: 600, color: COLORS[i] }}>{row.Model}</td>
                    {['Accuracy', 'Precision', 'Recall', 'F1-Score', 'ROC-AUC'].map(m => (
                      <td key={m}>{(row[m] * 100).toFixed(1)}%</td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          <div className="grid-2">
            <div className="card">
              <div className="card-header">Accuracy Comparison</div>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={barData}>
                  <XAxis dataKey="name" tick={{ fill: '#9A9ABF', fontSize: 12 }} />
                  <YAxis domain={[0, 100]} tick={{ fill: '#9A9ABF', fontSize: 12 }} />
                  <Tooltip contentStyle={{ background: '#222240', border: '1px solid #2E2E4A', borderRadius: 8 }}
                    labelStyle={{ color: '#EAEAEA' }} />
                  <Bar dataKey="accuracy" radius={[6, 6, 0, 0]}>
                    {barData.map((entry, i) => <Cell key={i} fill={entry.color} />)}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            </div>

            <div className="card">
              <div className="card-header">Radar Overview</div>
              <ResponsiveContainer width="100%" height={300}>
                <RadarChart data={radarData}>
                  <PolarGrid stroke="#2E2E4A" />
                  <PolarAngleAxis dataKey="metric" tick={{ fill: '#9A9ABF', fontSize: 11 }} />
                  <PolarRadiusAxis domain={[0, 100]} tick={false} axisLine={false} />
                  {comparison.map((m, i) => (
                    <Radar key={m.Model} name={m.Model} dataKey={m.Model}
                      stroke={COLORS[i]} fill={COLORS[i]} fillOpacity={0.15} />
                  ))}
                  <Legend wrapperStyle={{ fontSize: 12, color: '#9A9ABF' }} />
                </RadarChart>
              </ResponsiveContainer>
            </div>
          </div>
        </>
      )}

      {/* Confusion Matrices Tab */}
      {activeTab === 'confusion' && (
        <div className="grid-3">
          {Object.entries(results).map(([name, data]) => (
            <ConfusionMatrix key={name} matrix={data.confusion_matrix} title={name} />
          ))}
        </div>
      )}

      {/* Feature Importance Tab */}
      {activeTab === 'features' && feature_importance && (
        <div className="card">
          <div className="card-header">Random Forest Feature Importance</div>
          <ResponsiveContainer width="100%" height={450}>
            <BarChart data={[...feature_importance].reverse()} layout="vertical" margin={{ left: 140 }}>
              <XAxis type="number" tick={{ fill: '#9A9ABF', fontSize: 12 }} />
              <YAxis dataKey="feature" type="category" tick={{ fill: '#9A9ABF', fontSize: 12 }} width={140} />
              <Tooltip contentStyle={{ background: '#222240', border: '1px solid #2E2E4A', borderRadius: 8 }}
                labelStyle={{ color: '#EAEAEA' }} />
              <Bar dataKey="importance" radius={[0, 6, 6, 0]}>
                {[...feature_importance].reverse().map((_, i) => (
                  <Cell key={i} fill={`hsl(${250 - i * 8}, 70%, ${55 + i * 2}%)`} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
      )}
    </>
  );
}
