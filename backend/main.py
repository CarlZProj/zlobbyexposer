from flask import Flask, request
from flask_restful import Resource, Api
from flask_cors import CORS

import requests
import pandas as pd
import pickle

from riot_api import RiotAPI
from constants import *
from helpers import *

model_top = pickle.load(open('model_top.pkl','rb'))
model_jungle = pickle.load(open('model_jungle.pkl','rb'))
model_middle = pickle.load(open('model_middle.pkl','rb'))
model_bottom = pickle.load(open('model_bottom.pkl','rb'))
model_support = pickle.load(open('model_support.pkl','rb'))

app = Flask(__name__)
CORS(app)

@app.route('/lobby', methods=["GET"])
def lobby_exposer():
    args = request.args
    server = args.get("server")
    summoners = [
        args.get("s1"),
        args.get("s2"),
        args.get("s3"),
        args.get("s4"),
        args.get("s5"),
    ]

    lobby_response = {}

    for summoner in summoners:
        res_summoner_sc, summoner_data = RiotAPI.get_summoner(
            server=server,
            summoner=summoner
        )

        if res_summoner_sc == 200:
            summoner_name=summoner_data.get('name')
            puuid=summoner_data.get('puuid')
            summoner_id=summoner_data.get('id')

            res_rank_sc, rank_data = RiotAPI.get_rank(
                server=server,
                summoner_id=summoner_id
            )

            ranked_solo_data  = None
            for rd in rank_data:
                if rd and rd.get('queueType') == 'RANKED_SOLO_5x5':
                    ranked_solo_data = rd

            _, match_history_data = RiotAPI.get_match_history(
                    region=server_to_region_map.get(server),
                    puuid=puuid,
                    queue_type=420, # 400 - normal, 420 - ranked (disabled)
                    count=10,
                )

            games_played = 0
            duration_of_games = 0
            wins = 0
            total_team_damage = 0

            ally_champion_kills = 0 
            enemy_champion_kills = 0
            kills = 0
            deaths = 0
            assists = 0

            # champion_level = 0
            gold_earned = 0
            cs = 0

            total_damage_dealt_to_champions = 0
            total_damage_taken = 0
            damage_self_mitigated = 0

            damage_dealt_to_buildings = 0
            damage_dealt_to_objectives = 0
            turret_takedowns = 0
            inhibitor_takedowns = 0

            total_damage_shielded_on_teammates = 0
            total_heals_on_teammates = 0
            time_ccing_others = 0 # cc score 
            vision_score = 0

            # champion_id = 0
            role_top = 0
            role_jungle = 0
            role_mid = 0
            role_bot = 0
            role_sup = 0

            rating = 0

            for match_id in match_history_data:
                print(match_id)

                _, match_data = RiotAPI.get_match_stats(
                    region=server_to_region_map.get(server),
                    match_id=match_id
                )

                # print(match_data)

                info_data = match_data.get('info')
                summoner_index = match_data.get('metadata').get('participants').index(puuid)
                summoner_match_data = info_data.get('participants')[summoner_index]

                # remaked game (due to afk)
                time_played = summoner_match_data.get('timePlayed')
                if time_played <= 270:
                    continue

                games_played += 1
        
                team100 = [0, 1, 2, 3, 4]
                team200 = [5, 6, 7, 8, 9]

                if summoner_match_data.get('teamId') == 100:
                    ally_objective_data = info_data.get('teams')[0].get('objectives')
                    enemy_objective_data = info_data.get('teams')[1].get('objectives')

                    for x in range(len(team100)):
                        total_team_damage += info_data.get('participants')[x].get("totalDamageDealtToChampions")
                else:
                    ally_objective_data = info_data.get('teams')[1].get('objectives')
                    enemy_objective_data = info_data.get('teams')[0].get('objectives')

                    for x in range(len(team200)):
                        total_team_damage += info_data.get('participants')[x].get("totalDamageDealtToChampions")


                duration_of_games += info_data.get('gameDuration')
                wins += 1 if summoner_match_data.get('win') else 0

                ally_champion_kills += ally_objective_data.get('champion').get('kills')
                enemy_champion_kills += enemy_objective_data.get('champion').get('kills')
                kills += summoner_match_data.get('kills')
                deaths += summoner_match_data.get('deaths')
                assists += summoner_match_data.get('assists')

                # champion_level +=  summoner_match_data.get('champLevel')
                gold_earned += summoner_match_data.get('goldEarned')
                cs += summoner_match_data.get('totalMinionsKilled') + summoner_match_data.get('neutralMinionsKilled')

                total_damage_dealt_to_champions += summoner_match_data.get('totalDamageDealtToChampions')
                total_damage_taken += summoner_match_data.get('totalDamageTaken')
                damage_self_mitigated += summoner_match_data.get('damageSelfMitigated')

                damage_dealt_to_buildings += summoner_match_data.get('damageDealtToBuildings')
                damage_dealt_to_objectives += summoner_match_data.get('damageDealtToObjectives')
                turret_takedowns += summoner_match_data.get('turretTakedowns')
                inhibitor_takedowns += summoner_match_data.get('inhibitorTakedowns')

                total_damage_shielded_on_teammates += summoner_match_data.get('totalDamageShieldedOnTeammates')
                total_heals_on_teammates += summoner_match_data.get('totalHealsOnTeammates')
                time_ccing_others += summoner_match_data.get('timeCCingOthers') # cc score 
                vision_score += summoner_match_data.get('visionScore')

                # df['kill_participation'] = (data['kills'] + data['assists']) / data['ally_champion_kills']
                
                df_match_data = {
                    # TODO add kill participation
                    'kda': (summoner_match_data.get('kills') + summoner_match_data.get('assists')) / (0.5 if summoner_match_data.get('deaths') == 0 else summoner_match_data.get('deaths')),
                    'kills': summoner_match_data.get('kills'),
                    'deaths': summoner_match_data.get('deaths'),
                    'assists': summoner_match_data.get('assists'),
                    'avg_gold_per_min': summoner_match_data.get('goldEarned') / (summoner_match_data.get('timePlayed') / 60),
                    'avg_cs_per_min': summoner_match_data.get('totalMinionsKilled') / (summoner_match_data.get('timePlayed') / 60),
                    'total_damage_dealt_to_champions_per_min': summoner_match_data.get('totalDamageDealtToChampions') / (summoner_match_data.get('timePlayed') / 60),
                    'total_damage_taken_per_min': summoner_match_data.get('totalDamageTaken') / (summoner_match_data.get('timePlayed') / 60),
                    'damage_self_mitigated_per_min': summoner_match_data.get('damageSelfMitigated') / (summoner_match_data.get('timePlayed') / 60),
                    'damage_dealt_to_buildings_per_min': summoner_match_data.get('damageDealtToObjectives') / (summoner_match_data.get('timePlayed') / 60),
                    'damage_dealt_to_objectives_per_min': summoner_match_data.get('damageDealtToObjectives') / (summoner_match_data.get('timePlayed') / 60),
                    'turret_takedowns_per_min': summoner_match_data.get('turretTakedowns') / (summoner_match_data.get('timePlayed') / 60),
                    'inhibitor_takedowns_per_min': summoner_match_data.get('inhibitorKills') / (summoner_match_data.get('timePlayed') / 60),
                    'total_damage_shielded_on_teammates_per_min': summoner_match_data.get('totalDamageShieldedOnTeammates') / (summoner_match_data.get('timePlayed') / 60),
                    'total_heals_on_teammates_per_min': summoner_match_data.get('totalHealsOnTeammates') / (summoner_match_data.get('timePlayed') / 60),
                    'time_ccing_others_per_min': summoner_match_data.get('timeCCingOthers') / (summoner_match_data.get('timePlayed') / 60),
                    'vision_score_per_min': summoner_match_data.get('visionScore') / (summoner_match_data.get('timePlayed') / 60),
                }
                df = pd.DataFrame([df_match_data])
                match_rating = None

                role = summoner_match_data.get('teamPosition') if summoner_match_data.get('teamPosition') == '' else summoner_match_data.get('individualPosition')
                if role == "TOP": 
                    role_top += 1
                    match_rating = model_top.predict_proba(df)[0][1]
                elif role == "JUNGLE":
                    role_jungle += 1
                    match_rating = model_jungle.predict_proba(df)[0][1]
                elif role == "MIDDLE":
                    role_mid += 1
                    match_rating = model_middle.predict_proba(df)[0][1]
                elif role == "BOTTOM":
                    role_bot += 1
                    match_rating = model_bottom.predict_proba(df)[0][1]
                elif role == "UTILITY":
                    role_sup += 1
                    match_rating = model_support.predict_proba(df)[0][1]
                else:
                    match_rating = model_support.predict_proba(df)[0][1]
                
                rating += match_rating

                # print(match_rating, rating, games_played, rating / games_played)

            if games_played == 0:
                # print("No Ranked Games Played")
                lobby_response.update({
                    summoner: None
                })
                continue

            duration_of_games_in_min = duration_of_games / 60

            lobby_response.update({
                summoner: {
                    'summoner_name': summoner_name,
                    'tier': None if not ranked_solo_data else ranked_solo_data.get('tier'),
                    'rank': None if not ranked_solo_data else ranked_solo_data.get('rank'),
                    'games_played': games_played, 
                    'duration_of_games_in_min_per_game': duration_of_games_in_min / games_played,
                    'win_rate': wins / games_played,

                    'damage_participation': total_damage_dealt_to_champions / total_team_damage,
                    'kill_participation': (kills + assists) / ally_champion_kills,
                    'kda': 'inf' if deaths == 0 else (kills + assists) / deaths,
                    'avg_kills': kills / games_played,
                    'avg_deaths': deaths / games_played,
                    'avg_assists': assists / games_played,
            
                    'avg_gold_per_min': gold_earned / duration_of_games_in_min,
                    'avg_cs_per_min': cs / duration_of_games_in_min,

                    'total_damage_dealt_to_champions_per_min': total_damage_dealt_to_champions / duration_of_games_in_min,
                    'total_damage_taken_per_min': total_damage_taken / duration_of_games_in_min,
                    'damage_self_mitigated_per_min': damage_self_mitigated / duration_of_games_in_min,

                    'damage_dealt_to_buildings_per_min': damage_dealt_to_buildings / duration_of_games_in_min,
                    'damage_dealt_to_objectives_per_min': damage_dealt_to_objectives / duration_of_games_in_min,
                    'turret_takedowns_per_min': turret_takedowns / duration_of_games_in_min,
                    'inhibitor_takedowns_per_min': inhibitor_takedowns / duration_of_games_in_min,

                    'total_damage_shielded_on_teammates_per_min': total_damage_shielded_on_teammates / duration_of_games_in_min,
                    'total_heals_on_teammates_per_min': total_heals_on_teammates / duration_of_games_in_min,
                    'time_ccing_others_per_min': time_ccing_others / duration_of_games_in_min,
                    'vision_score_per_min': vision_score / duration_of_games_in_min,

                    'main_role': get_main_role(role_top, role_jungle, role_mid, role_bot, role_sup),

                    'match_rating': rating * 100 / games_played
                }
            })
        else:
            lobby_response.update({
                summoner: None
            })

    return lobby_response

if __name__ == '__main__':
    app.run(debug=True)