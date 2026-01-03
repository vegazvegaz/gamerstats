import requests
import json
import os
from datetime import datetime

# Ton robot va utiliser tes clés secrètes STEAM_KEY et STEAM_ID
STEAM_KEY = os.environ['STEAM_KEY']
STEAM_ID = os.environ['STEAM_ID']

def update_data():
    # 1. On récupère les données fraîches de Steam
    url = f"http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={STEAM_KEY}&steamid={STEAM_ID}&format=json&include_appinfo=true"
    response = requests.get(url)
    data = response.json()
    
    # On sauvegarde le fichier principal des jeux
    with open('steam_data.json', 'w') as f:
        json.dump(data, f)

    # 2. On gère l'historique dans history.json
    history_file = 'history.json'
    today = datetime.now().strftime('%Y-%m-%d')
    
    # Calcul du total d'heures actuel
    total_minutes = sum(game.get('playtime_forever', 0) for game in data['response']['games'])
    total_hours = round(total_minutes / 60)

    # On ouvre l'historique existant ou on en crée un nouveau
    if os.path.exists(history_file):
        with open(history_file, 'r') as f:
            history = json.load(f)
    else:
        history = {}

    # On ajoute le score du jour
    history[today] = total_hours
    
    # On garde les 90 derniers jours pour ne pas ralentir ton iPhone
    sorted_history = dict(sorted(history.items())[-90:])

    with open(history_file, 'w') as f:
        json.dump(sorted_history, f)

if __name__ == "__main__":
    update_data()
