$(document).on('change', '.select_team', function () {
    let home_team = document.getElementById("h_team").value;
    let away_team = document.getElementById("a_team").value;
    // console.log(home_team, away_team);

    if (home_team != 'default' && away_team != 'default') {
        d3.json("/teams-data", function (error, teamData) {
            if (error) return console.warn(error);
            // console.log(teamData);

            let homeTeamInfo,
                awayTeamInfo;

            for (t = 0; t < teamData.length; t++) {
                let teamInfo = teamData[t];
                if (teamInfo.ha == 'home' && teamInfo.team == home_team) {
                    homeTeamInfo = teamInfo;
                    // console.log(homeTeamInfo)
                }
                else if (teamInfo.ha == 'away' && teamInfo.team == away_team) {
                    awayTeamInfo = teamInfo;
                    // console.log(awayTeamInfo)
                }
            }

            // Calculate Time Of Possessions
            let homeTOP = 60 * parseFloat(homeTeamInfo.TOP) / (parseFloat(homeTeamInfo.TOP) + parseFloat(awayTeamInfo.TOP));
            let awayTOP = 60 - homeTOP;
            document.getElementById("h_top").value = homeTOP.toFixed(2);
            document.getElementById("a_top").value = awayTOP.toFixed(2);
            // console.log(homeTOP, awayTOP)

            // Calculate Third Down Percentages
            let homeTDP = .5 * (parseFloat(homeTeamInfo.third_per) + parseFloat(awayTeamInfo.third_per_allowed));
            let awayTDP = .5 * (parseFloat(awayTeamInfo.third_per) + parseFloat(homeTeamInfo.third_per_allowed));
            document.getElementById("h_tdp").value = homeTDP.toFixed(2);
            document.getElementById("a_tdp").value = awayTDP.toFixed(2);
            // console.log(homeTDP, awayTDP);

            // Calculate First Down Stats
            let homeFD = .5 * (parseFloat(homeTeamInfo.first_downs) + parseFloat(awayTeamInfo.first_downs_allowed));
            let awayFD = .5 * (parseFloat(awayTeamInfo.first_downs) + parseFloat(homeTeamInfo.first_downs_allowed));
            document.getElementById("h_first").value = homeFD.toFixed(2);
            document.getElementById("a_first").value = awayFD.toFixed(2);
            // console.log(homeFD, awayFD);

            // Calculate Passing Stats
            let homePass = .5 * (parseFloat(homeTeamInfo.pass_yards) + parseFloat(awayTeamInfo.pass_yards_allowed));
            let awayPass = .5 * (parseFloat(awayTeamInfo.pass_yards) + parseFloat(homeTeamInfo.pass_yards_allowed));
            document.getElementById('h_pass').value = homePass.toFixed(2);
            document.getElementById('a_pass').value = awayPass.toFixed(2);
            // console.log(homePass, awayPass);

            // Calculate Penalty
            let homePenalty = parseFloat(homeTeamInfo.penalty_yards);
            let awayPenalty = parseFloat(awayTeamInfo.penalty_yards);
            document.getElementById('h_penalty').value = homePenalty.toFixed(2);
            document.getElementById('a_penalty').value = awayPenalty.toFixed(2);
            // console.log(homePenalty, awayPenalty);

            // Calculate Rush Stats
            let homeRush = .5 * (parseFloat(homeTeamInfo.rush_yards) + parseFloat(awayTeamInfo.rush_yards_allowed));
            let awayRush = .5 * (parseFloat(awayTeamInfo.rush_yards) + parseFloat(homeTeamInfo.rush_yards_allowed));
            document.getElementById('h_rush').value = homeRush.toFixed(2);
            document.getElementById('a_rush').value = awayRush.toFixed(2);
            // console.log(homeRush, awayRush);

            // Calculate Plays Run
            let homePlays = parseFloat(homeTeamInfo.plays);
            let awayPlays = parseFloat(awayTeamInfo.plays);
            document.getElementById('h_plays').value = homePlays.toFixed(2);
            document.getElementById('a_plays').value = awayPlays.toFixed(2);
            // console.log(homePlays, awayPlays);

            // Calculate Sack Data
            let homeSacks = .5 * (parseFloat(homeTeamInfo.sacks) + parseFloat(awayTeamInfo.sacked));
            let awaySacks = .5 * (parseFloat(awayTeamInfo.sacks) + parseFloat(homeTeamInfo.sacked));
            document.getElementById('h_sacks').value = homeSacks.toFixed(2);
            document.getElementById('a_sacks').value = awaySacks.toFixed(2);
            // console.log(homeSacks, awaySacks);

            // Calculate Total Yards Data
            let homeYards = .5 * (parseFloat(homeTeamInfo.total_yards) + parseFloat(awayTeamInfo.total_yards_allowed));
            let awayYards = .5 * (parseFloat(awayTeamInfo.total_yards) + parseFloat(homeTeamInfo.total_yards_allowed));
            document.getElementById('h_total').value = homeYards.toFixed(2);
            document.getElementById('a_total').value = awayYards.toFixed(2);
            // console.log(homeYards, awayYards);

            // Calculate Turnovers Data
            let homeTO = .5 * (parseFloat(homeTeamInfo.turnovers) + parseFloat(awayTeamInfo.takeaways));
            let awayTO = .5 * (parseFloat(awayTeamInfo.turnovers) + parseFloat(homeTeamInfo.takeaways));
            document.getElementById('h_tos').value = homeTO.toFixed(2);
            document.getElementById('a_tos').value = awayTO.toFixed(2);
            // console.log(homeTO, awayTO);

        });
    }
});



