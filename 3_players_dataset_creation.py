# Players dataset creation
# The Fantacalcio players list is manually downloaded from https://www.fantacalcio.it/quotazioni-fantacalcio
# Here, the players database is generated, by merging the Fantacalcio list to stats generated from 1_scraping_fbref.py script (fbref_data/outfield_players.csv and fbref_data/keepers_players.csv)

import pandas as pd
import unicodedata
import numpy as np

def normalize_name(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    only_ascii = nfkd_form.encode('ASCII', 'ignore')
    return only_ascii.decode('utf-8')

# Load fbref data for outfield players and goalkeepers.
# Generate fbref player list, adding player surname (with special characters replaced to normal ones)

print("Loading fbref data for outfield players and goalkeepers...")
rcsv = pd.read_csv('fbref_data/outfield_players.csv')   
outfield_players = pd.DataFrame(rcsv)

rcsv = pd.read_csv('fbref_data/keepers_players.csv')   
keeper_players = pd.DataFrame(rcsv)

# concat the two files but only player and team columns
players = pd.concat([outfield_players[['player', 'team']], keeper_players[['player', 'team']] ], axis = 0, ignore_index = True)
keepers_ID = len(outfield_players)

# create two new colums surname and initial
players['surname'] = players['player']
players['initial'] = players['player']

print("Split name and surname, take only the first letter of the name and normalize the surname...")
# normalize the surname
for i in range(players.shape[0]):
    # take only the surname and normalize it
    players['surname'][i] = players['surname'][i].split(' ')[-1]
    players['surname'][i] = normalize_name(players['surname'][i]).replace('\'', '')

    # take only the first letter of the name
    players['initial'][i] = players['player'][i][0]

# Replace the surname for some specific players, according to config/name_fix.txt file.
# This is done for players for which the decoded fbref surname doesn't correspond to Fantacalcio list. 

print("Replace the surname for some specific players, according to config/name_fix.txt file...")   
rcsv = pd.read_csv('config/name_fix.txt')   
name_fix = pd.DataFrame(rcsv)

for i in range(name_fix.shape[0]):
    for j in range(players.shape[0]):
        if(players['surname'][j].lower() == name_fix['FROM'][i].lower() and players['team'][j].lower() == name_fix['TEAM'][i].lower()):
            players['surname'][j] = name_fix['TO'][i]
            # print(name_fix['TO'][i])

# Load players from Fantacalcio list
print("Loading players from Fantacalcio quoatazioni fantacalcio...")
fc_data = pd.read_excel('fantacalcio/Quotazioni_Fantacalcio.xlsx', 'Tutti', header = 1)
fc_players = fc_data [['Id', 'R', 'Nome', 'Squadra']]
fc_players = fc_players.rename(columns = {'Id' : 'id', 'R': 'r', 'Nome' : 'name', 'Squadra' : 'team'})
fc_players['surname'] = fc_players['name']
fc_players['initial'] = fc_players['name']

print("Normalize the columns name, the name and surname...")
for i in range(fc_players.shape[0]):
    spl = normalize_name( fc_players['name'][i].replace('\'', '') ).split(' ')
    if('.' in spl[-1]):
        fc_players.loc[i, 'surname'] = spl[-2]
        fc_players.loc[i, 'initial'] = spl[-1][0]
    else:
        fc_players.loc[i, 'surname'] = spl[-1]
        fc_players.loc[i, 'initial'] = ''

# Associate players from Fantacalcio list to ID for FBref data.
fc_players['fb_ID'] = fc_players['id']

for i in range(fc_players.shape[0]):
    fc_players.loc[i, 'fb_ID']  = -1
    
    for j in range(players.shape[0]):
        if(fc_players['team'][i].lower() in players['team'][j].lower()):
            if(fc_players['surname'][i].lower() == players['surname'][j].lower()):              
                # if(fc_players['initial'][i] == '' or fc_players['initial'][i].lower() == players['initial'][j].lower()):
                if((fc_players['r'][i] == 'P') == (j >= keepers_ID)): # check wether they're a goalkeeper for both FBREF and Fantacalcio
                    fc_players.loc[i, 'fb_ID'] = j

# Print players for which the association failed.
# Most of them are players who didn't play a single Serie A game this season with their team. If that is the case, and there is data from their previous team, that is taken here.
# Others are ones for which the FBRef surname doesn't correspond to Fantacalcio one.
# For example, Cabral is Arthur for FBref.
# Correction is made in the name_fix code above.

exceptions = ['pellegrini', 'bastoni', 'kristensen'] # exceptions for such players that have the same surname as others (Berardi A., Luca Pellegrini)

for i in range(fc_players.shape[0]):
    if(fc_players['fb_ID'][i] == -1):
        found = False
        for j in range(players.shape[0]):
            if(fc_players['surname'][i].lower() == players['surname'][j].lower()):
                if(not(players['surname'][j].lower() in exceptions)):
                    if((fc_players['r'][i] == 'P') == (j >= keepers_ID)):
                        fc_players.loc[i, 'fb_ID']= j
                        found = True
        if(found):
            print(fc_players['name'][i] + ' from previous team stats')
        else:
            print(fc_players['name'][i] + ' not found')


print(fc_players)

# Populate players dataset with stats from FBref, for outfield players and goalkeepers
# Data for Outfield players
columns_to_copy = outfield_players.columns[4:]

fc_players[columns_to_copy] = 0

for i in range(fc_players.shape[0]):
    if(fc_players['fb_ID'][i] != -1 and fc_players['r'][i] != 'P'):
         for j in range(columns_to_copy.shape[0]):
            #fc_players[columns_to_copy[j]][i] = outfield_players[columns_to_copy[j]][fc_players['fb_ID'][i]]
            fc_players.loc[i, columns_to_copy[j]] = outfield_players.loc[fc_players['fb_ID'][i], columns_to_copy[j]]


keeper_players.columns[4:]

# Data for Keepers
columns_to_copy = keeper_players.columns[4:]
fc_players[columns_to_copy[2:]] = 0 # add columns but do not override age and birth_year
delta_k = outfield_players.shape[0]

for i in range(fc_players.shape[0]):
    if(fc_players['fb_ID'][i] != -1 and fc_players['r'][i] == 'P'):
         for j in range(columns_to_copy.shape[0]):
            #fc_players[columns_to_copy[j]][i] = keeper_players[columns_to_copy[j]][fc_players['fb_ID'][i] - delta_k]
            fc_players.loc[i, columns_to_copy[j]] = keeper_players.loc[fc_players['fb_ID'][i] - delta_k, columns_to_copy[j]]

print(fc_players)

# Load votes database, to add data to players database (mean vote and its standard deviation)
votes = pd.read_excel('mid_outputs/players_votes.xlsx', index_col = 0)

# Compute the average Serie A Goal Keeper mean vote and vote std
min_votes = 3 # TO BE UPDATED WHEN SERIE A HAS MORE CALENDAR WEEKS PLAYED

perf_df_P = pd.DataFrame(columns = ['vote_avg', 'vote_std'])

for i in range(fc_players.shape[0]): 
    if(fc_players.loc[i]['r'] == 'P'):
        v = np.array([])
        for j in range(votes.shape[0]):
            if(fc_players['name'][i] == votes['player'][j]):
                v = np.append(v, votes['vote'][j])

        if(v.shape[0] >= min_votes - 1):
            row_df = pd.DataFrame(data = [[np.mean(v), np.std(v)]], columns = perf_df_P.columns)
            perf_df_P = pd.concat([perf_df_P, row_df], ignore_index = True)


print(perf_df_P.mean())

print(perf_df_P)

# Add to players data their mean vote (and its standard deviation).
# For players who don't have a minimum amount of games, more data to reach this value is computed, according to the average Serie A player vote (and std). For goalkeepers, this values are different.
min_votes = 3 # TO BE UPDATED WHEN SERIE A HAS MORE CALENDAR WEEKS PLAYED

# outfield players
mean_def = 6
std_def = 0.58

# goalkeepers
mean_def_P = 6.22
std_def_P = 0.43

perf_df = pd.DataFrame(columns = ['vote_avg', 'vote_std'])

for i in range(fc_players.shape[0]):
    v = np.array([])
    for j in range(votes.shape[0]):
        if(fc_players['name'][i] == votes['player'][j]):
            v = np.append(v, votes['vote'][j])
    
    mean_def_i = mean_def
    std_def_i = std_def
    
    if(fc_players['r'][i] == 'P'):
        mean_def_i = mean_def_P
        std_def_i = std_def_P
        
    if(v.shape[0] < min_votes):
         for k in range(min_votes - v.shape[0]):
            v = np.append( v, np.random.normal(mean_def_i, std_def_i) )
    
    row_df = pd.DataFrame(data = [[np.mean(v), np.std(v)]], columns = perf_df.columns)
    perf_df = pd.concat([perf_df, row_df], ignore_index = True)
    
print(perf_df)


fc_players = pd.concat([fc_players, perf_df], axis = 1)

print(fc_players)

GK_GAMES_COLUMN = 118
fc_players.columns[GK_GAMES_COLUMN]

# check it if is 'gk_games'

# For goalkeepers who didn't play a miminum amount of games, data is weightly averaged with one of the main goalkeeper of their same team.
min_gk_games = 3 # TO BE UPDATED WHEN SERIE A HAS MORE CALENDAR WEEKS PLAYED
fc_players_newgk = fc_players.copy()
columns_to_avg = fc_players.columns[GK_GAMES_COLUMN:] # from gk_games to end

for i in range(fc_players.shape[0]):
    if(fc_players['r'][i] == 'P'):
        if(fc_players['gk_games'][i] < min_gk_games):
            for j in range(fc_players.shape[0]):
                if(fc_players['team'][i] == fc_players['team'][j] and fc_players['gk_games'][j] >= min_gk_games):
                    break
                    
            weight = 1 - (min_gk_games - fc_players['gk_games'][i]) / min_gk_games
            
            fc_players_newgk.at[i, columns_to_avg] = fc_players.loc[i][columns_to_avg] * weight + (1 - weight) * fc_players.loc[j][columns_to_avg]
            
            print(fc_players['name'][i] + ', ' + str(weight))
            
fc_players = fc_players_newgk

print(fc_players)

fc_players.to_excel('mid_outputs/players_stats.xlsx')
    