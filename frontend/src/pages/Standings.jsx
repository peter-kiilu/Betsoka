import { useMemo } from "react";
import EPL_TEAMS from "../data/teams";

// Seed-based pseudo-random number generator for deterministic standings
function seededRandom(seed) {
  let s = seed;
  return () => {
    s = (s * 16807 + 12345) % 2147483647;
    return (s & 0x7fffffff) / 0x7fffffff;
  };
}

// Generate realistic league standings from team attributes
function generateStandings(teams, matchesPlayed = 25) {
  const rand = seededRandom(2025);

  const standings = teams.map((team) => {
    let wins = 0,
      draws = 0,
      losses = 0,
      goalsFor = 0,
      goalsAgainst = 0;
    const form = []; // Last 5 results: 'W', 'D', 'L'

    for (let i = 0; i < matchesPlayed; i++) {
      const r = rand();
      // Higher strength & form → higher win probability
      const winProb = (team.strength / 100) * 0.55 + (team.form / 10) * 0.15;
      const drawProb = 0.22;

      let result;
      if (r < winProb) {
        wins++;
        result = "W";
        const scored = Math.floor(team.avgGoals + rand() * 1.5);
        const conceded = Math.floor(rand() * 1.5);
        goalsFor += Math.max(1, scored);
        goalsAgainst += conceded;
      } else if (r < winProb + drawProb) {
        draws++;
        result = "D";
        const goals = Math.floor(rand() * 2.5);
        goalsFor += goals;
        goalsAgainst += goals;
      } else {
        losses++;
        result = "L";
        const scored = Math.floor(rand() * 1.2);
        const conceded = Math.floor(team.avgGoals * 0.8 + rand() * 1.5);
        goalsFor += scored;
        goalsAgainst += Math.max(1, conceded);
      }

      form.push(result);
    }

    const points = wins * 3 + draws;
    const goalDifference = goalsFor - goalsAgainst;

    return {
      ...team,
      played: matchesPlayed,
      wins,
      draws,
      losses,
      goalsFor,
      goalsAgainst,
      goalDifference,
      points,
      recentForm: form.slice(-5),
    };
  });

  // Sort by points, then GD, then GF
  standings.sort((a, b) => {
    if (b.points !== a.points) return b.points - a.points;
    if (b.goalDifference !== a.goalDifference)
      return b.goalDifference - a.goalDifference;
    return b.goalsFor - a.goalsFor;
  });

  return standings;
}

export default function Standings() {
  const standings = useMemo(() => generateStandings(EPL_TEAMS), []);

  const getZoneClass = (position) => {
    if (position <= 4) return "zone-ucl";
    if (position === 5) return "zone-uel";
    if (position >= 18) return "zone-rel";
    return "";
  };

  const getFormDotClass = (result) => {
    if (result === "W") return "form-dot win";
    if (result === "D") return "form-dot draw";
    return "form-dot loss";
  };

  const getFormDotLabel = (result) => {
    if (result === "W") return "W";
    if (result === "D") return "D";
    return "L";
  };

  return (
    <>
      {/* League Header */}
      <div className="league-header">
        <div className="league-title">
          <img
            src="/logos/premier-league.png"
            alt="Premier League"
            className="league-badge-img"
          />
          <div>
            <h2>Premier League</h2>
            <span className="league-country">England · 2024/25</span>
          </div>
        </div>
        <div className="league-tag">Standings</div>
      </div>

      {/* Zone Legend */}
      <div className="standings-legend">
        <div className="legend-item">
          <span className="legend-color ucl"></span>
          <span>Champions League</span>
        </div>
        <div className="legend-item">
          <span className="legend-color uel"></span>
          <span>Europa League</span>
        </div>
        <div className="legend-item">
          <span className="legend-color rel"></span>
          <span>Relegation</span>
        </div>
      </div>

      {/* Standings Table */}
      <div className="standings-wrapper">
        <table className="standings-table" id="standings-table">
          <thead>
            <tr>
              <th className="col-pos">#</th>
              <th className="col-team">Team</th>
              <th className="col-stat">MP</th>
              <th className="col-stat">W</th>
              <th className="col-stat">D</th>
              <th className="col-stat">L</th>
              <th className="col-stat hide-mobile">GF</th>
              <th className="col-stat hide-mobile">GA</th>
              <th className="col-stat">GD</th>
              <th className="col-pts">Pts</th>
              <th className="col-form hide-mobile">Form</th>
            </tr>
          </thead>
          <tbody>
            {standings.map((team, index) => {
              const pos = index + 1;
              return (
                <tr key={team.short} className={getZoneClass(pos)}>
                  <td className="col-pos">
                    <span className="pos-number">{pos}</span>
                  </td>
                  <td className="col-team">
                    <div className="standings-team-info">
                      {team.logo ? (
                        <img
                          src={team.logo}
                          alt={team.name}
                          className="standings-team-logo"
                        />
                      ) : (
                        <span
                          className="team-badge"
                          style={{ background: team.color }}
                        >
                          {team.short.charAt(0)}
                        </span>
                      )}
                      <span className="standings-team-name">{team.name}</span>
                      <span className="standings-team-short">{team.short}</span>
                    </div>
                  </td>
                  <td className="col-stat">{team.played}</td>
                  <td className="col-stat">{team.wins}</td>
                  <td className="col-stat">{team.draws}</td>
                  <td className="col-stat">{team.losses}</td>
                  <td className="col-stat hide-mobile">{team.goalsFor}</td>
                  <td className="col-stat hide-mobile">{team.goalsAgainst}</td>
                  <td className="col-stat col-gd">
                    <span
                      className={
                        team.goalDifference > 0
                          ? "gd-positive"
                          : team.goalDifference < 0
                            ? "gd-negative"
                            : ""
                      }
                    >
                      {team.goalDifference > 0 ? "+" : ""}
                      {team.goalDifference}
                    </span>
                  </td>
                  <td className="col-pts">
                    <span className="pts-value">{team.points}</span>
                  </td>
                  <td className="col-form hide-mobile">
                    <div className="form-dots">
                      {team.recentForm.map((result, i) => (
                        <span
                          key={i}
                          className={getFormDotClass(result)}
                          title={getFormDotLabel(result)}
                        >
                          {getFormDotLabel(result)}
                        </span>
                      ))}
                    </div>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </>
  );
}
