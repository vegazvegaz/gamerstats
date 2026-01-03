import requests
import json
import os
from datetime import datetime

# Identifiants fournis intégrés directement
STEAM_KEY = "645EB0A81C05DE3962B5902819BB75E9"
STEAM_ID = "76561198025652371"

def update_data():
    try:
        url = f"http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={STEAM_KEY}&steamid={STEAM_ID}&format=json&include_appinfo=true"
        response = requests.get(url)
        data = response.json()
        
        # Sauvegarde bibliothèque
        with open('steam_data.json', 'w') as f:
            json.dump(data, f)

        # Gestion historique
        history_file = 'history.json'
        today = datetime.now().strftime('%Y-%m-%d')
        total_hrs = sum(g.get('playtime_forever', 0) for g in data['response']['games']) // 60

        if os.path.exists(history_file):
            with open(history_file, 'r') as f:
                history = json.load(f)
        else:
            history = {}

        history[today] = total_hrs
        # On garde 90 entrées
        history = dict(sorted(history.items())[-90:])

        with open(history_file, 'w') as f:
            json.dump(history, f)
            
        print("Mise à jour réussie.")
    except Exception as e:
        print(f"Erreur : {e}")

if __name__ == "__main__":
    update_data()
