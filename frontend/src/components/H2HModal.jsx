import { X } from 'lucide-react';

// Generate imaginary H2H history for two teams
function generateH2H(home, away) {
  const matches = [];
  const seasons = ['2023/24', '2023/24', '2022/23', '2022/23', '2021/22'];
  const venues = ['H', 'A', 'H', 'A', 'H'];
  
  for (let i = 0; i < 5; i++) {
    const isHomeVenue = venues[i] === 'H';
    const team1 = isHomeVenue ? home : away;
    const team2 = isHomeVenue ? away : home;
    
    // Generate score based on team strength
    const strengthDiff = team1.strength - team2.strength;
    const baseGoals1 = Math.max(0, Math.round(team1.avgGoals + (strengthDiff / 50)));
    const baseGoals2 = Math.max(0, Math.round(team2.avgGoals - (strengthDiff / 50)));
    
    // Add randomness
    const goals1 = Math.max(0, Math.min(5, baseGoals1 + Math.floor(Math.random() * 3) - 1));
    const goals2 = Math.max(0, Math.min(5, baseGoals2 + Math.floor(Math.random() * 3) - 1));
    
    matches.push({
      season: seasons[i],
      date: `${15 + i} ${['Aug', 'Dec', 'Feb', 'Apr', 'Oct'][i]} ${2021 + Math.floor(i / 2)}`,
      homeTeam: team1.name,
      awayTeam: team2.name,
      homeScore: goals1,
      awayScore: goals2,
      venue: isHomeVenue ? 'Home' : 'Away',
    });
  }
  
  return matches;
}

export default function H2HModal({ home, away, onClose }) {
  const h2h = generateH2H(home, away);
  
  // Calculate stats
  const stats = h2h.reduce((acc, m) => {
    const isHomeMatch = m.homeTeam === home.name;
    const homeGoals = isHomeMatch ? m.homeScore : m.awayScore;
    const awayGoals = isHomeMatch ? m.awayScore : m.homeScore;
    
    if (homeGoals > awayGoals) acc.homeWins++;
    else if (awayGoals > homeGoals) acc.awayWins++;
    else acc.draws++;
    
    return acc;
  }, { homeWins: 0, draws: 0, awayWins: 0 });

  const getResultClass = (match) => {
    const isHomeMatch = match.homeTeam === home.name;
    const homeGoals = isHomeMatch ? match.homeScore : match.awayScore;
    const awayGoals = isHomeMatch ? match.awayScore : match.homeScore;
    
    if (homeGoals > awayGoals) return 'win';
    if (awayGoals > homeGoals) return 'loss';
    return 'draw';
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={e => e.stopPropagation()}>
        {/* Header */}
        <div className="modal-header">
          <div className="modal-teams">
            <div className="modal-team">
              {home.logo ? (
                <img src={home.logo} alt={home.name} className="team-logo" />
              ) : (
                <span className="team-badge" style={{ background: home.color }}>
                  {home.short.charAt(0)}
                </span>
              )}
              <span>{home.name}</span>
            </div>
            <span className="vs">vs</span>
            <div className="modal-team">
              {away.logo ? (
                <img src={away.logo} alt={away.name} className="team-logo" />
              ) : (
                <span className="team-badge" style={{ background: away.color }}>
                  {away.short.charAt(0)}
                </span>
              )}
              <span>{away.name}</span>
            </div>
          </div>
          <button className="modal-close" onClick={onClose}>
            <X size={20} />
          </button>
        </div>

        {/* Stats Summary */}
        <div className="h2h-stats">
          <div className="stat-item win">
            <div className="stat-value">{stats.homeWins}</div>
            <div className="stat-label">{home.short} Wins</div>
          </div>
          <div className="stat-item draw">
            <div className="stat-value">{stats.draws}</div>
            <div className="stat-label">Draws</div>
          </div>
          <div className="stat-item loss">
            <div className="stat-value">{stats.awayWins}</div>
            <div className="stat-label">{away.short} Wins</div>
          </div>
        </div>

        {/* Match History */}
        <div className="h2h-title">Last 5 Meetings</div>
        <div className="h2h-matches">
          {h2h.map((match, i) => (
            <div key={i} className={`h2h-match ${getResultClass(match)}`}>
              <div className="h2h-match-header">
                <span className="h2h-season">{match.season}</span>
                <span className="h2h-date">{match.date}</span>
                <span className="h2h-venue">{match.venue}</span>
              </div>
              <div className="h2h-match-result">
                <span className="h2h-team">{match.homeTeam}</span>
                <span className="h2h-score">
                  {match.homeScore} - {match.awayScore}
                </span>
                <span className="h2h-team">{match.awayTeam}</span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
