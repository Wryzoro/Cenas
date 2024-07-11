import random
import sqlite3
import tkinter as tk
from tkinter import ttk
import threading
import time


teams = [
    "Benfica", "Porto", "Sporting", "Braga", "Vitoria SC",
    "Boavista", "Nacional", "Estrela Da Amadora", "Gil Vicente",
    "Santa Clara", "Rio Ave", "AVS", "Estoril", "Arouca",
    "Famalicao", "Casa Pia", "Moreirense", "Farense"
]


def initialize_db():
    conn = sqlite3.connect('liga_betclic.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS teams (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL UNIQUE,
            points INTEGER DEFAULT 0,
            goals_scored INTEGER DEFAULT 0,
            goals_against INTEGER DEFAULT 0,
            goal_difference INTEGER DEFAULT 0
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS matches (
            id INTEGER PRIMARY KEY,
            team1 TEXT NOT NULL,
            score1 INTEGER NOT NULL,
            team2 TEXT NOT NULL,
            score2 INTEGER NOT NULL
        )
    ''')

    for team in teams:
        cursor.execute('''
            INSERT OR IGNORE INTO teams (name) VALUES (?)
        ''', (team,))
    conn.commit()
    conn.close()


def get_teams():
    conn = sqlite3.connect('liga_betclic.db')
    cursor = conn.cursor()
    cursor.execute('SELECT name FROM teams')
    teams = [row[0] for row in cursor.fetchall()]
    conn.close()
    return teams


def generate_round_robin_schedule(teams):
    if len(teams) % 2 != 0:
        teams.append(None)  
    
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
        teams.insert(1, teams.pop())  
        schedule.append(round_matches)
    
    return schedule


def double_round_robin_schedule(teams):
    first_half = generate_round_robin_schedule(teams)
    second_half = [(away, home) for home, away in sum(first_half, [])]
    second_half = [second_half[i:i + len(teams) // 2] for i in range(0, len(second_half), len(teams) // 2)]
    return first_half + second_half


def insert_match_result(team1, score1, team2, score2):
    conn = sqlite3.connect('liga_betclic.db')
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO matches (team1, score1, team2, score2) VALUES (?, ?, ?, ?)
    ''', (team1, score1, team2, score2))
    conn.commit()
    conn.close()


def update_team_stats(team, points, goals_scored, goals_against):
    conn = sqlite3.connect('liga_betclic.db')
    cursor = conn.cursor()
    cursor.execute('''
    UPDATE teams
    SET points = points + ?, goals_scored = goals_scored + ?, goals_against = goals_against + ?, goal_difference = goal_difference + ?
    WHERE name = ?
    ''', (points, goals_scored, goals_against, goals_scored - goals_against, team))
    conn.commit()
    conn.close()


def simulate_match(team1, team2):
    score1 = random.randint(0, 3)
    score2 = random.randint(0, 3)
    return score1, score2


def calculate_standings():
    conn = sqlite3.connect('liga_betclic.db')
    cursor = conn.cursor()
    cursor.execute('''
    SELECT name, points, goals_scored, goals_against, goal_difference
    FROM teams
    ORDER BY points DESC, goals_scored DESC, goal_difference DESC
    ''')
    standings = cursor.fetchall()
    conn.close()
    return standings

def start_tournament():
    initialize_db()
    teams = get_teams()
    random.shuffle(teams)
    schedule = double_round_robin_schedule(teams)

    for round_num, round_matches in enumerate(schedule, start=1):
        txt_results.insert(tk.END, f"\nJornada {round_num}:\n")
        for match in round_matches:
            team1, team2 = match
            score1, score2 = simulate_match(team1, team2)
            insert_match_result(team1, score1, team2, score2)
            update_team_stats(team1, 3 if score1 > score2 else 1 if score1 == score2 else 0, score1, score2)
            update_team_stats(team2, 3 if score2 > score1 else 1 if score2 == score1 else 0, score2, score1)
            txt_results.insert(tk.END, f"    {team1} {score1} - {score2} {team2}\n")
            txt_results.update()
            time.sleep(1)

    display_standings()


def display_standings():
    standings = calculate_standings()
    txt_results.insert(tk.END, "\nClassificação Final:\n")
    for position, (team, points, goals_scored, goals_against, goal_difference) in enumerate(standings, start=1):
        txt_results.insert(tk.END, f"{position}. {team} - {points} pts, GD: {goal_difference}, GF: {goals_scored}, GA: {goals_against}\n")


root = tk.Tk()
root.title("Simulação da Liga Betclic 2024/2025")
root.geometry("800x600")

frame = ttk.Frame(root)
frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

lbl_welcome = ttk.Label(frame, text="Simulação da Liga Betclic 2024/2025", font=('Helvetica', 16))
lbl_welcome.pack(pady=10)

btn_start_tournament = ttk.Button(frame, text="Iniciar Sorteio e Campeonato", command=start_tournament)
btn_start_tournament.pack(pady=20)

txt_results = tk.Text(frame, wrap='word')
txt_results.pack(fill=tk.BOTH, expand=True)

scrollbar = ttk.Scrollbar(frame, command=txt_results.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
txt_results['yscrollcommand'] = scrollbar.set

root.mainloop()
