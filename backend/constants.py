import os

RIOT_API_KEY = os.environ.get('RIOT_API_KEY')
RIOT_API_KEY_HEADER = {"X-Riot-Token": RIOT_API_KEY}

AMERICAS = "americas"
EUROPE = "europe"
ASIA = "asia"

server_to_region_map = {
    "na1": AMERICAS,
    "br1": AMERICAS,
    "eun1": EUROPE,
    "euw1": EUROPE,
    "la1": AMERICAS,
    "la2": AMERICAS,
    "na1": AMERICAS,
    "oc1": AMERICAS,
    "ru": EUROPE,
    "tr1": EUROPE,
    "jp1": ASIA,
    "kr": ASIA,
}