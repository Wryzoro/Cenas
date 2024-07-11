import random
import time
from collections import defaultdict


teams = [
    "Benfica", "Porto", "Sporting", "Braga", "Vitoria SC",
    "Boavista", "Nacional", "Estrela Da Amadora", "Gil Vicente",
    "Santa Clara", "Rio Ave", "AVS", "Estoril", "Arouca",
    "Famalicao", "Casa Pia", "Moreirense", "Farense"
]

# 
def generate_round_robin_schedule(teams):
    if len(teams) % 2 != 0:
        teams.append(None)  # 
    
    schedule = []
    num_teams = len(teams)
    rounds = num_teams - 1
    
    for round_num in range(rounds):
        round_matches = []
        for i in range(num_teams // 2):
            team1 = teams[i]
            team2 = teams[num_teams - 1 - i]
            if team1 is not None and team2 is not None:
                if round_num % 2 == 0:
                    round_matches.append((team1, team2))
                else:
                    round_matches.append((team2, team1))
        teams.insert(1, teams.pop())  # Gira a lista de times
        schedule.append(round_matches)
    
    return schedule

# 
def double_round_robin_schedule(teams):
    first_half = generate_round_robin_schedule(teams)
    second_half = [(away, home) for home, away in sum(first_half, [])]
    second_half = [second_half[i:i + len(teams) // 2] for i in range(0, len(second_half), len(teams) // 2)]
    return first_half + second_half

# 
def simulate_match(team1, team2):
    score1 = random.randint(0, 5)  # 
    score2 = random.randint(0, 5)  #
    return (team1, score1, team2, score2)

# 
def calculate_standings(results):
    standings = defaultdict(lambda: {'points': 0, 'goals_scored': 0, 'goals_against': 0, 'goal_difference': 0})

    for team1, score1, team2, score2 in results:
        standings[team1]['goals_scored'] += score1
        standings[team1]['goals_against'] += score2
        standings[team1]['goal_difference'] += (score1 - score2)

        standings[team2]['goals_scored'] += score2
        standings[team2]['goals_against'] += score1
        standings[team2]['goal_difference'] += (score2 - score1)

        if score1 > score2:
            standings[team1]['points'] += 3
        elif score1 < score2:
            standings[team2]['points'] += 3
        else:
            standings[team1]['points'] += 1
            standings[team2]['points'] += 1

    return standings

# 
def display_standings(standings):
    sorted_standings = sorted(standings.items(), key=lambda x: (-x[1]['points'], -x[1]['goals_scored']))
    print("\nClassificação Final:")
    for position, (team, stats) in enumerate(sorted_standings, start=1):
        print(f"{position}. {team} - {stats['points']} pts, GD: {stats['goal_difference']}, GF: {stats['goals_scored']}, GA: {stats['goals_against']}")

# 
def main():
    # Bem-vindo ao sorteio
    input("Bem vindo ao sorteio da Liga Betclic 2024/2025, carregue ENTER para começar: ")

    # Baralhar
    random.shuffle(teams)
    schedule = double_round_robin_schedule(teams)

    # Exibição das jornadas
    for round_num, round_matches in enumerate(schedule, start=1):
        print(f"\nJornada {round_num}:")
        for match in round_matches:
            print(f"{match[0]} vs {match[1]}")
        time.sleep(1)

    # começar o campeonato
    while True:
        start_championship = input("\nEstá pronto para começar o campeonato (y/n): ").strip().lower()
        if start_championship == 'y':
            break
        elif start_championship == 'n':
            print("Aguardando...")
            time.sleep(2)
        else:
            print("Entrada inválida. Por favor, digite 'y' para começar ou 'n' para aguardar.")

    # 
    standings = defaultdict(lambda: {'points': 0, 'goals_scored': 0, 'goals_against': 0, 'goal_difference': 0})
    all_results = []

    for round_num, round_matches in enumerate(schedule, start=1):
        print(f"\nJornada {round_num}:")
        for match in round_matches:
            team1, score1, team2, score2 = simulate_match(match[0], match[1])
            all_results.append((team1, score1, team2, score2))
            print(f"    {team1} {score1} - {score2} {team2}")
            time.sleep(1)

    standings = calculate_standings(all_results)
    display_standings(standings)

    # 
    with open("resultados.txt", "w") as f:
        for result in all_results:
            f.write(f"{result[0]} {result[1]} - {result[3]} {result[2]}\n")

    with open("classificacao.txt", "w") as f:
        sorted_standings = sorted(standings.items(), key=lambda x: (-x[1]['points'], -x[1]['goals_scored']))
        for position, (team, stats) in enumerate(sorted_standings, start=1):
            f.write(f"{position}. {team} - {stats['points']} pts, GD: {stats['goal_difference']}, GF: {stats['goals_scored']}, GA: {stats['goals_against']}\n")

if __name__ == "__main__":
    main()
