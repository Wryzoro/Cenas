import random
import sqlite3

#Listas das seleções
teams = [
    "Portugal", "França", "Alemanha", "Espanha",
    "Itália", "Inglaterra", "Bélgica", "Países Baixos",
    "Croácia", "Suíça", "Áustria", "Suécia",
    "Polônia", "Dinamarca", "República Tcheca", "Turquia",
]

#Baralhar as equipas
random.shuffle(teams)

# Distribuir as equipas por grupos
groups = {}
group_names = ["Grupo A", "Grupo B", "Grupo C", "Grupo D"]

for i in range(len(group_names)):
    groups[group_names[i]] = teams[i*4:(i+1)*4]

# Exibir os grupos
for group, teams in groups.items():
    print(f"{group}: {', '.join(teams)}")
print()

def initialize_db():
    conn = sqlite3.connect('euro_2024.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS matches (
            id INTEGER PRIMARY KEY,
            stage TEXT NOT NULL,
            group_name TEXT NOT NULL,
            team1 TEXT NOT NULL,
            score1 INTEGER NOT NULL,
            team2 TEXT NOT NULL,
            score2 INTEGER NOT NULL,
            winner TEXT,
            decided_by_penalty INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

def simulate_match(team1, team2):
    score1 = random.randint(0, 3)
    score2 = random.randint(0, 3)
    
    
    if score1 == score2:
        if random.random() < 0.5:
            score1 += 1
        else:
            score2 += 1
            
    return score1, score2

def simulate_group_stage():
    initialize_db()
    conn = sqlite3.connect('euro_2024.db')
    cursor = conn.cursor()

    matchdays = [
        [(0, 1), (2, 3)],
        [(0, 2), (1, 3)],
        [(0, 3), (1, 2)]
    ]

    for group, teams_in_group in groups.items():
        print(f"----- {group} -----")
        for day, matches in enumerate(matchdays, 1):
            print(f"Jornada {day}:")
            for match in matches:
                team1 = teams_in_group[match[0]]
                team2 = teams_in_group[match[1]]
                score1, score2 = simulate_match(team1, team2)
                cursor.execute('''
                    INSERT INTO matches (stage, group_name, team1, score1, team2, score2)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (f"Jornada {day}", group, team1, score1, team2, score2))
                conn.commit()
                print(f"{team1} {score1} - {score2} {team2}")
            print()

    conn.close()

def calculate_group_standings():
    conn = sqlite3.connect('euro_2024.db')
    cursor = conn.cursor()

    standings = {group: {} for group in groups.keys()}
    cursor.execute('SELECT group_name, team1, score1, team2, score2 FROM matches WHERE stage LIKE "Jornada %"')
    matches = cursor.fetchall()

    for match in matches:
        group, team1, score1, team2, score2 = match[:5]

        if team1 not in standings[group]:
            standings[group][team1] = {'points': 0, 'goals': 0}
        if team2 not in standings[group]:
            standings[group][team2] = {'points': 0, 'goals': 0}

        standings[group][team1]['goals'] += score1
        standings[group][team2]['goals'] += score2

        if score1 > score2:
            standings[group][team1]['points'] += 3
        elif score1 < score2:
            standings[group][team2]['points'] += 3
        else:
            standings[group][team1]['points'] += 1
            standings[group][team2]['points'] += 1

    for group in standings:
        standings[group] = sorted(standings[group].items(), key=lambda x: (x[1]['points'], x[1]['goals']), reverse=True)

    conn.close()
    return standings

def get_teams_for_knockout_stage(standings):
    knockout_stage_teams = []
    third_place_teams = []

    for group in standings:
        knockout_stage_teams.append(standings[group][0][0])
        knockout_stage_teams.append(standings[group][1][0])
        third_place_teams.append((group, standings[group][2][0], standings[group][2][1]['goals']))

    third_place_teams = sorted(third_place_teams, key=lambda x: (x[2], x[1]), reverse=True)
    knockout_stage_teams.extend([team[1] for team in third_place_teams[:4]])

    return knockout_stage_teams

def simulate_knockout_stage(teams):
    random.shuffle(teams) 
    quarterfinals = [
        (teams[0], teams[7]),
        (teams[3], teams[4]),
        (teams[1], teams[6]),
        (teams[2], teams[5])
    ]
    semifinals = []
    finals = []

    conn = sqlite3.connect('euro_2024.db')
    cursor = conn.cursor()

    def play_round(matches, stage):
        winners = []
        for match in matches:
            team1, team2 = match
            score1, score2 = simulate_match(team1, team2)
            cursor.execute('''
                INSERT INTO matches (stage, group_name, team1, score1, team2, score2)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (stage, "Eliminatórias", team1, score1, team2, score2))
            conn.commit()
            winner = team1 if score1 > score2 else team2
            cursor.execute('''
                UPDATE matches
                SET winner = ?
                WHERE stage = ? AND team1 = ? AND team2 = ?
            ''', (winner, stage, team1, team2))
            conn.commit()
            winners.append(winner)
        return winners

    # Quartos de final
    quarterfinal_winners = play_round(quarterfinals, "Quartas de Final")
    print("Resultados das Quartas de Final:")
    for match, winner in zip(quarterfinals, quarterfinal_winners):
        score1, score2 = simulate_match(match[0], match[1])
        print(f"{match[0]} {score1} - {score2} {match[1]}")
        print(f"Vencedor: {winner}")
    print()

    # Meias de Finais
    semifinal_winners = play_round([(quarterfinal_winners[0], quarterfinal_winners[1]),
                                    (quarterfinal_winners[2], quarterfinal_winners[3])],
                                    "Semifinais")
    print("Resultados das Semifinais:")
    for match, winner in zip([(quarterfinal_winners[0], quarterfinal_winners[1]),
                                (quarterfinal_winners[2], quarterfinal_winners[3])],
                                semifinal_winners):
        score1, score2 = simulate_match(match[0], match[1])
        print(f"{match[0]} {score1} - {score2} {match[1]}")
        print(f"Vencedor: {winner}")
    print()

    # Final
    final_winner = play_round([(semifinal_winners[0], semifinal_winners[1])], "Final")[0]
    print("Resultado da Final:")
    score1, score2 = simulate_match(semifinal_winners[0], semifinal_winners[1])
    print(f"{semifinal_winners[0]} {score1} - {score2} {semifinal_winners[1]}")
    print(f"Vencedor do torneio: {final_winner}")
    print()

    conn.close()
    return final_winner

# Execução da simulação
simulate_group_stage()
print("Simulação dos grupos concluída.")
print()

standings = calculate_group_standings()
for group, teams in standings.items():
    print(f"{group} Classificação:")
    for team, stats in teams:
        print(f"{team}: {stats['points']} pontos, {stats['goals']} gols")
    print()

knockout_stage_teams = get_teams_for_knockout_stage(standings)
print("Times classificados para as eliminatórias:", knockout_stage_teams)
print()

winner = simulate_knockout_stage(knockout_stage_teams)
print("O vencedor do torneio é:", winner)
