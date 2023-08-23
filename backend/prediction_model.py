import pandas as pd

from sklearn import datasets, linear_model
from sklearn.metrics import accuracy_score, confusion_matrix, recall_score
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, export_text

import pickle

all_data = pd.read_csv('Sep-09-2022_10000matches.csv', sep=',')
# print(data.columns)

# TOP, JUNGLE (assume Invalid = JUNGLE), MIDDLE, BOTTOM, UTILITY
grouped = all_data.groupby('individualPosition')

dfs = {key: group for key, group in grouped}

# print(dfs)

combined_df = pd.concat([dfs['JUNGLE'], dfs['Invalid']], ignore_index=True)
dfs.pop('Invalid')

# print(dfs)

# seperate dataset by role
for role, data in dfs.items():
    print(role)

    df = pd.DataFrame()

    # TODO add kill participation (essential for support analysis)
    # df['kill_participation'] = (data['kills'] + data['assists']) / data['ally_champion_kills']
    df['kda'] = (data['kills'] + data['assists']) / data['deaths'].apply(lambda x: 0.5 if x == 0 else x)
    df['kills'] = data['kills']
    df['deaths'] = data['deaths']
    df['assists'] = data['assists']
    df['avg_gold_per_min'] = data['goldEarned'] / (data['timePlayed'] / 60)
    df['avg_cs_per_min'] = data['totalMinionsKilled'] / (data['timePlayed'] / 60)
    df['total_damage_dealt_to_champions_per_min'] = data['totalDamageDealtToChampions'] / (data['timePlayed'] / 60)
    df['total_damage_taken_per_min'] = data['totalDamageTaken'] / (data['timePlayed'] / 60)
    df['damage_self_mitigated_per_min'] = data['damageSelfMitigated'] / (data['timePlayed'] / 60)
    df['damage_dealt_to_buildings_per_min'] = data['damageDealtToObjectives'] / (data['timePlayed'] / 60)
    df['damage_dealt_to_objectives_per_min'] = data['damageDealtToObjectives'] / (data['timePlayed'] / 60)
    df['turret_takedowns_per_min'] = data['turretTakedowns'] / (data['timePlayed'] / 60)
    df['inhibitor_takedowns_per_min'] = data['inhibitorKills'] / (data['timePlayed'] / 60)
    df['total_damage_shielded_on_teammates_per_min'] = data['totalDamageShieldedOnTeammates'] / (data['timePlayed'] / 60)
    df['total_heals_on_teammates_per_min'] = data['totalHealsOnTeammates'] / (data['timePlayed'] / 60)
    df['time_ccing_others_per_min'] = data['timeCCingOthers'] / (data['timePlayed'] / 60)
    df['vision_score_per_min'] = data['visionScore'] / (data['timePlayed'] / 60)

    # training / testing data
    X = df.copy() # features
    y = data['win'].apply(lambda x: 1 if x == True else 0) # 0 or 1 for win or loss
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.05)
    # print(X_train, X_test, y_train, y_test)

    # # classify data
    clf = DecisionTreeClassifier(
        max_depth=6,
    )
    clf = clf.fit(X_train, y_train)

    # default param values
    # clf.get_params()

    # predictions
    # predictions = clf.predict(X_test)

    predictions = clf.predict_proba(X_test) # need early stopping critiera to use probalbity

    print(predictions)

    # compare to info
    # accuracy = accuracy_score(y_test, predictions) 

    # accuracy = confusion_matrix(y_test, predictions, labels=[0,1])
    # print(accuracy)

    # r = recall_score(y_test, predictions)

    # classification report


    # feature importance
    # clf.feature_importances

    # r = export_text(clf, feature_names=df.columns)
    # print(r)

    file_name = None
    if role == 'TOP':
        file_name = 'model_top.pkl'
    elif role == 'JUNGLE':
        file_name = 'model_jungle.pkl'
    elif role == 'MIDDLE':
        file_name = 'model_middle.pkl'
    elif role == 'BOTTOM':
        file_name = 'model_bottom.pkl'
    elif role == 'UTILITY':
        file_name = 'model_support.pkl'

    pickle.dump(
        obj=clf,
        file=open(file_name, 'wb'),
    )


