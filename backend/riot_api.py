import requests
from constants import *

class RiotAPI():
    def get_summoner(server, summoner):
        url = "https://" + server + ".api.riotgames.com/lol/summoner/v4/summoners/by-name/" + summoner
        print(url)
        res = requests.get(url, headers=RIOT_API_KEY_HEADER)

        return res.status_code, res.json()

    def get_match_history(region, puuid, queue_type, count):
        url = "https://" + region + ".api.riotgames.com/lol/match/v5/matches/by-puuid/" + puuid + "/ids?queue=" + str(queue_type) + "&start=0&count=" + str(count)
        res = requests.get(url, headers=RIOT_API_KEY_HEADER)

        return res.status_code, res.json()

    def get_match_stats(region, match_id):
        url = "https://" + region + ".api.riotgames.com/lol/match/v5/matches/" + match_id
        res = requests.get(url, headers=RIOT_API_KEY_HEADER)

        return res.status_code, res.json()

    def get_rank(server, summoner_id):
        url = 'https://'+ server + '.api.riotgames.com/lol/league/v4/entries/by-summoner/' + summoner_id
        res = requests.get(url, headers=RIOT_API_KEY_HEADER)

        return res.status_code, res.json()
