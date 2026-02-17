import { NavLink } from 'react-router-dom';
import { useApp } from '../context/AppContext';
import { LayoutDashboard, Target, BarChart3, Info, Zap, Brain, Menu, X } from 'lucide-react';
import { useState } from 'react';

export default function Sidebar() {
  const { status, loading, generateData, trainModels } = useApp();
  const [nMatches, setNMatches] = useState(2000);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const closeMobileMenu = () => setMobileMenuOpen(false);

  return (
    <>
      {/* Mobile menu button */}
      <button 
        className="mobile-menu-btn"
        onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
        aria-label="Toggle menu"
      >
        {mobileMenuOpen ? <X size={24} /> : <Menu size={24} />}
      </button>

      {/* Mobile overlay */}
      {mobileMenuOpen && (
        <div className="mobile-overlay" onClick={closeMobileMenu} />
      )}

      <aside className={`sidebar ${mobileMenuOpen ? 'open' : ''}`}>
        {/* Brand */}
        <div className="sidebar-brand">
          <span className="logo-icon">⚽</span>
          <h1>BETSOKA</h1>
          <span>AI Football Predictor</span>
        </div>

        {/* Navigation */}
        <nav>
          <ul className="sidebar-nav">
            <li><NavLink to="/" className={({ isActive }) => isActive ? 'active' : ''} onClick={closeMobileMenu}>
              <LayoutDashboard size={18} /> Dashboard
            </NavLink></li>
            <li><NavLink to="/predictions" className={({ isActive }) => isActive ? 'active' : ''} onClick={closeMobileMenu}>
              <Target size={18} /> Predictions
            </NavLink></li>
            <li><NavLink to="/analytics" className={({ isActive }) => isActive ? 'active' : ''} onClick={closeMobileMenu}>
              <BarChart3 size={18} /> Analytics
            </NavLink></li>
            <li><NavLink to="/about" className={({ isActive }) => isActive ? 'active' : ''} onClick={closeMobileMenu}>
              <Info size={18} /> About
            </NavLink></li>
          </ul>
        </nav>

        {/* Data Controls */}
        <p className="sidebar-section-title">Data Controls</p>
        <div className="feature-input" style={{ padding: '0 0.3rem' }}>
          <label>Matches: {nMatches.toLocaleString()}</label>
          <input type="range" min={500} max={5000} step={250} value={nMatches}
            onChange={e => setNMatches(+e.target.value)} />
        </div>
        <button className="btn btn-primary" onClick={() => generateData(nMatches)} disabled={loading.generate}
          style={{ marginBottom: '0.6rem' }}>
          {loading.generate ? <><span className="spinner" /> Generating...</> : <><Zap size={16} /> Generate Data</>}
        </button>

        <p className="sidebar-section-title">Training</p>
        <button className="btn btn-primary" onClick={trainModels}
          disabled={loading.train || !status.data_loaded} style={{ marginBottom: '1rem' }}>
          {loading.train ? <><span className="spinner" /> Training...</> : <><Brain size={16} /> Train Models</>}
        </button>

        {/* Status */}
        <div className={`sidebar-status ${status.models_trained ? 'ready' : status.data_loaded ? 'pending' : 'empty'}`}>
          {status.models_trained ? '✅ Models Ready' :
           status.data_loaded ? `📦 ${status.data_rows.toLocaleString()} matches loaded` :
           '🔄 Generate data to start'}
        </div>
      </aside>
    </>
  );
}
