# Generate player votes database, containing votes for Serie-A matchday and player.
# Votes data is manually downloaded from https://www.fantacalcio.it/voti-fantacalcio-serie-a
# Serie A calendar is loaded from another file, to add information not containing in votes files: home/away, team opponent.

import pandas as pd
import numpy as np

# loading calendar from fantacalcio/seriea_calendar.xlsx file
cal = np.array(pd.read_excel('fantacalcio/seriea_calendar.xlsx', header = None))
cal_df = pd.DataFrame(columns = ['matchday', 'team1', 'team2'])
matchday = 0

# parse the information to have the following structure in cal_df DataFrame object
# 	    matchday	team1	    team2
# 0	    1	        Bologna	    Milan
# 1	    1	        Empoli	    Verona
# ...   ...	        ...	        ...
# 378	38	        Milan   	Salernitana
# 379	38	        Napoli  	Lecce
for i in range(cal.shape[0]):
    if(cal[i, 0][0].isnumeric()):
        matchday = matchday + 1
        continue
    
    teams = cal[i, 0].split('-')    
    frame = pd.DataFrame([[matchday, teams[0], teams[1]]], columns = cal_df.columns)
    cal_df = pd.concat([cal_df, frame], ignore_index = True)

# looking for previusly mathces in the current season (23-24) to make players_votes.xlsx
df = pd.DataFrame(
    columns = ['matchday', 'player', 'team', 'oppteam', 'home', 'vote', 'goals', 'assists', 'cards_malus', 'fantavote']
    )

LAST_MATCH = 38
for matchday in range(1, LAST_MATCH + 1):  
    votes_file = 'fantacalcio/voti/Voti_Fantacalcio_Stagione_2023_24_Giornata_' + str(matchday) + '.xlsx'

    # not all the matches are already played
    try:
        rx = np.array(pd.read_excel(votes_file, header = None))
    except:
        break

    read = 0
    for i in range(rx.shape[0]):
        if(rx[i, 0] == "Cod."):
            # extract team
            read = 1
            team = rx[i-1, 0];
            continue

        if(read):
            if(isinstance(rx[i, 0], int)):
                if((isinstance(rx[i, 3], float) or isinstance(rx[i, 3], int)) and rx[i, 1] != "ALL") :
                    player = rx[i, 2];
                    vote = float(rx[i, 3])
                    goals = rx[i, 4] + rx[i, 8] - rx[i, 5]
                    assists = rx[i, 12]
                    cards_malus = rx[i, 10] * 0.5 + rx[i, 11]
                    
                    # extract the home and oppteam information using cal_df obj
                    oppteam = ''
                    home = 0
                    for j in range(cal_df.shape[0]):
                        if(cal_df['matchday'][j] == matchday):
                            if(cal_df['team1'][j] == team):
                                oppteam = cal_df['team2'][j] 
                                home = 1
                            elif(cal_df['team2'][j] == team):
                                oppteam = cal_df['team1'][j] 
                                home = 0

                    goals_gen = goals * 3;
                    if(goals < 0):
                        goals_gen = goals
                        
                    fantavote = vote + goals_gen + assists - cards_malus 
                    
                    frame = pd.DataFrame(
                        [[matchday, player, team, oppteam, home, vote, goals, assists, cards_malus, fantavote]], 
                        columns = df.columns
                    )

                    df = pd.concat([df, frame], axis = 0, ignore_index = True)
            else:
                read = 0
                continue
    
    print('loaded votes for matchday ' + str(matchday))

# df
# 	matchday	player  	    team    	oppteam 	home    vote	goals	assists	cards_malus	fantavote
# 0	1	        Musso   	    Atalanta    Sassuolo    0       6.5	    0	    0	    0	        6.5
# 1	1	        Zappacosta  	Atalanta    Sassuolo    0       6.5	    0	    0	    0	        6.5
# 2	1	        Djimsiti    	Atalanta    Sassuolo    0       6	    0	    0	    0	        6
# 3	1	        Kolasinac   	Atalanta    Sassuolo    0       6.5	    0	    0	    0	        6.5

# write out the fantacalcio players vote
df.to_excel('mid_outputs/players_votes.xlsx')

# Elaborate data for past seasons
# Do not repeat if data is already present
# todo mettere un check se il file esiste, nel caso elaborare i dati?

# BACKUP CODE FOR SEASON 2122 and 2021 (different calendar file format than 2223 and 2324)
# cal_df = pd.read_excel('fantacalcio/season2122/seriea_calendar.xlsx')
# to_drop = list()
# for i in range(cal_df.shape[0]):
#     if(not isinstance(cal_df['matchday'][i], int)):
#         to_drop.append(i)
    
# cal_df = cal_df.drop(to_drop)
# cal_df = cal_df.reset_index(drop = True)
# print(cal_df)

cal = np.array(pd.read_excel('fantacalcio/season2223/seriea_calendar.xlsx', header = None))
cal_df = pd.DataFrame(columns = ['matchday', 'team1', 'team2'])
matchday = 0
for i in range(cal.shape[0]):
    if(cal[i, 0][0].isnumeric()):
        matchday = matchday + 1
        continue
    
    teams = cal[i, 0].split('-')
    frame = pd.DataFrame([[matchday, teams[0], teams[1]]], columns = cal_df.columns)
    cal_df = pd.concat([cal_df, frame], ignore_index = True)


df = pd.DataFrame(columns = ['matchday', 'player', 'team', 'oppteam', 'home', 'vote', 'goals', 'assists', 'cards_malus', 'fantavote'])

LAST_MATCH = 38

for matchday in range(1, LAST_MATCH + 1):
    votes_file = 'fantacalcio/season2223/voti/Voti_Fantacalcio_Stagione_2022_23_Giornata_' + str(matchday) + '.xlsx'
    rx = np.array(pd.read_excel(votes_file, header = None))

    read = 0
    for i in range(rx.shape[0]):
        if(rx[i, 0] == "Cod."):
            read = 1
            team = rx[i-1, 0];
            continue

        if(read):
            if(isinstance(rx[i, 0], int)):
                if((isinstance(rx[i, 3], float) or isinstance(rx[i, 3], int)) and rx[i, 1] != "ALL") :
                    player = rx[i, 2];
                    vote = float(rx[i, 3])
                    goals = rx[i, 4] + rx[i, 8] - rx[i, 5]
                    assists = rx[i, 12]
                    cards_malus = rx[i, 10] * 0.5 + rx[i, 11]

                    oppteam = ''
                    home = 0
                    for j in range(cal_df.shape[0]):
                        if(cal_df['matchday'][j] == matchday):
                            if(cal_df['team1'][j] == team):
                                oppteam = cal_df['team2'][j] 
                                home = 1
                            elif(cal_df['team2'][j] == team):
                                oppteam = cal_df['team1'][j] 
                                home = 0

                    goals_gen = goals * 3;
                    if(goals < 0):
                        goals_gen = goals
                        
                    fantavote = vote + goals_gen + assists - cards_malus 
                    
                    frame = pd.DataFrame([[matchday, player, team, oppteam, home, vote, goals, assists, cards_malus, fantavote]], columns = df.columns)

                    df = pd.concat([df, frame], axis = 0, ignore_index = True)
            else:
                read = 0
                continue


df.to_excel('mid_outputs/season2223/players_votes.xlsx')