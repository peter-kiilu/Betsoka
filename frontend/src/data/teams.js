// Premier League teams with attributes that map to model features
const EPL_TEAMS = [
  { name: 'Arsenal', short: 'ARS', color: '#EF0107', strength: 88, form: 8.2, avgGoals: 2.1, shots: 6.8, badge: '🔴', logo: '/logos/arsenal.png' },
  { name: 'Aston Villa', short: 'AVL', color: '#670E36', strength: 78, form: 7.0, avgGoals: 1.5, shots: 5.2, badge: '🟤', logo: '/logos/aston-villa.png' },
  { name: 'Bournemouth', short: 'BOU', color: '#DA291C', strength: 68, form: 6.5, avgGoals: 1.3, shots: 4.5, badge: '🍒', logo: '/logos/bournemouth.png' },
  { name: 'Brentford', short: 'BRE', color: '#E30613', strength: 70, form: 6.0, avgGoals: 1.4, shots: 4.8, badge: '🐝', logo: '/logos/brentford.png' },
  { name: 'Brighton', short: 'BHA', color: '#0057B8', strength: 76, form: 7.2, avgGoals: 1.6, shots: 5.5, badge: '🔵', logo: '/logos/brighton.png' },
  { name: 'Chelsea', short: 'CHE', color: '#034694', strength: 82, form: 7.5, avgGoals: 1.8, shots: 6.0, badge: '🦁', logo: '/logos/chelsea.png' },
  { name: 'Crystal Palace', short: 'CRY', color: '#1B458F', strength: 67, form: 5.8, avgGoals: 1.1, shots: 4.2, badge: '🦅', logo: '/logos/crystal-palace.png' },
  { name: 'Everton', short: 'EVE', color: '#003399', strength: 62, form: 4.5, avgGoals: 1.0, shots: 3.8, badge: '🔷', logo: '/logos/everton.png' },
  { name: 'Fulham', short: 'FUL', color: '#000000', strength: 70, form: 6.3, avgGoals: 1.3, shots: 4.6, badge: '⚪', logo: '/logos/fulham.png' },
  { name: 'Ipswich Town', short: 'IPS', color: '#0044AA', strength: 55, form: 3.8, avgGoals: 0.9, shots: 3.2, badge: '🔹', logo: '/logos/Ipswich Town.png' },
  { name: 'Leicester City', short: 'LEI', color: '#003090', strength: 60, form: 4.2, avgGoals: 1.0, shots: 3.5, badge: '🦊', logo: '/logos/leicester.jpg' },
  { name: 'Liverpool', short: 'LIV', color: '#C8102E', strength: 92, form: 9.0, avgGoals: 2.3, shots: 7.2, badge: '🔴', logo: '/logos/liverpool.png' },
  { name: 'Man City', short: 'MCI', color: '#6CABDD', strength: 90, form: 7.8, avgGoals: 2.2, shots: 7.0, badge: '🩵', logo: '/logos/man-city.png' },
  { name: 'Man United', short: 'MUN', color: '#DA291C', strength: 78, form: 5.5, avgGoals: 1.4, shots: 5.0, badge: '🔴', logo: '/logos/man-united.png' },
  { name: 'Newcastle', short: 'NEW', color: '#241F20', strength: 80, form: 7.3, avgGoals: 1.7, shots: 5.8, badge: '⬛', logo: '/logos/newcastle.png' },
  { name: 'Nott\'m Forest', short: 'NFO', color: '#DD0000', strength: 74, form: 7.5, avgGoals: 1.5, shots: 5.0, badge: '🌳', logo: '/logos/nottingham.png' },
  { name: 'Southampton', short: 'SOU', color: '#D71920', strength: 52, form: 3.2, avgGoals: 0.8, shots: 3.0, badge: '⭕', logo: '/logos/southampton.png' },
  { name: 'Tottenham', short: 'TOT', color: '#132257', strength: 79, form: 6.0, avgGoals: 1.7, shots: 5.6, badge: '🐓', logo: '/logos/tottenham.png' },
  { name: 'West Ham', short: 'WHU', color: '#7A263A', strength: 72, form: 5.5, avgGoals: 1.3, shots: 4.7, badge: '⚒️', logo: '/logos/west-ham-united.png' },
  { name: 'Wolves', short: 'WOL', color: '#FDB913', strength: 64, form: 4.8, avgGoals: 1.1, shots: 4.0, badge: '🐺', logo: '/logos/wolves.png' },
];

// Generate a set of matchday fixtures from the teams
export function generateFixtures(teams = EPL_TEAMS, matchday = 1) {
  // Shuffle teams deterministically based on matchday
  const shuffled = [...teams].sort((a, b) => {
    const hashA = (a.strength * matchday + a.name.charCodeAt(0)) % 100;
    const hashB = (b.strength * matchday + b.name.charCodeAt(0)) % 100;
    return hashA - hashB;
  });

  const fixtures = [];
  for (let i = 0; i < shuffled.length - 1; i += 2) {
    fixtures.push({
      id: `${matchday}-${i}`,
      matchday,
      home: shuffled[i],
      away: shuffled[i + 1],
      time: `${15 + (i % 6)}:${i % 2 === 0 ? '00' : '30'}`,
      status: 'upcoming',
    });
  }
  return fixtures;
}

// Convert two teams into model feature inputs
export function teamsToFeatures(home, away) {
  return {
    home_strength: home.strength,
    away_strength: away.strength,
    home_form: home.form,
    away_form: away.form,
    home_avg_goals: home.avgGoals,
    away_avg_goals: away.avgGoals,
    home_shots_on_target: home.shots,
    away_shots_on_target: away.shots,
    possession_diff: Math.round((home.strength - away.strength) * 0.3),
    home_advantage: 4.5,
    h2h_advantage: Math.round((home.form - away.form) * 0.5 * 10) / 10,
    goal_diff_trend: Math.round((home.avgGoals - away.avgGoals) * 10) / 10,
  };
}

export default EPL_TEAMS;
