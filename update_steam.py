import requests, json

def sync():
    # Tes clés intégrées directement
    key = "645EB0A81C05DE3962B5902819BB75E9"
    sid = "76561198025652371"
    url = f"http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={key}&steamid={sid}&format=json&include_appinfo=true"
    
    try:
        data = requests.get(url).json()
        with open('steam_data.json', 'w') as f:
            json.dump(data, f)
        print("Synchronisation Steam réussie.")
    except:
        print("Erreur de connexion.")

if __name__ == "__main__":
    sync()
