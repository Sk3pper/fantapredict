import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import re
import sys, getopt
import csv

# standard(stats)
stats = ["player","nationality","position","team","age","birth_year","games","games_starts","minutes","goals","assists","pens_made","pens_att","cards_yellow","cards_red","goals_per90","assists_per90","goals_assists_per90","goals_pens_per90","goals_assists_pens_per90","xg","npxg","xa","xg_per90","xa_per90","xg_xa_per90","npxg_per90","npxg_xa_per90"]
stats3 = ["players_used","possession","games","games_starts","minutes","goals","assists","pens_made","pens_att","cards_yellow","cards_red","goals_per90","assists_per90","goals_assists_per90","goals_pens_per90","goals_assists_pens_per90","xg","npxg","xa","xg_per90","xa_per90","xg_xa_per90","npxg_per90","npxg_xa_per90"] 

# goalkeeping(keepers)
keepers = ["player","nationality","position","team","age","birth_year","gk_games","gk_games_starts","gk_minutes","gk_goals_against","gk_goals_against_per90","gk_shots_on_target_against","gk_saves","gk_save_pct","gk_wins","gk_ties","gk_losses","gk_clean_sheets","gk_clean_sheets_pct","gk_pens_att","gk_pens_allowed","gk_pens_saved","gk_pens_missed"]
keepers3 = ["players_used","gk_games","gk_games_starts","gk_minutes","gk_goals_against","gk_goals_against_per90","gk_shots_on_target_against","gk_saves","gk_save_pct","gk_wins","gk_ties","gk_losses","gk_clean_sheets","gk_clean_sheets_pct","gk_pens_att","gk_pens_allowed","gk_pens_saved","gk_pens_missed"]

# advance goalkeeping(keepersadv)
keepersadv = ["player","nationality","position","team","age","birth_year","minutes_90s","gk_goals_against","gk_pens_allowed","gk_free_kick_goals_against","gk_corner_kick_goals_against","gk_own_goals_against","gk_psxg","gk_psnpxg_per_shot_on_target_against","gk_psxg_net","gk_psxg_net_per90","gk_passes_completed_launched","gk_passes_launched","gk_passes_pct_launched","gk_passes","gk_passes_throws","gk_pct_passes_launched","gk_passes_length_avg","gk_goal_kicks","gk_pct_goal_kicks_launched","gk_goal_kick_length_avg","gk_crosses","gk_crosses_stopped","gk_crosses_stopped_pct","gk_def_actions_outside_pen_area","gk_def_actions_outside_pen_area_per90","gk_avg_distance_def_actions"]
keepersadv2 = ["minutes_90s","gk_goals_against","gk_pens_allowed","gk_free_kick_goals_against","gk_corner_kick_goals_against","gk_own_goals_against","gk_psxg","gk_psnpxg_per_shot_on_target_against","gk_psxg_net","gk_psxg_net_per90","gk_passes_completed_launched","gk_passes_launched","gk_passes_pct_launched","gk_passes","gk_passes_throws","gk_pct_passes_launched","gk_passes_length_avg","gk_goal_kicks","gk_pct_goal_kicks_launched","gk_goal_kick_length_avg","gk_crosses","gk_crosses_stopped","gk_crosses_stopped_pct","gk_def_actions_outside_pen_area","gk_def_actions_outside_pen_area_per90","gk_avg_distance_def_actions"]

# shooting(shooting)
shooting = ["player","nationality","position","team","age","birth_year","minutes_90s","goals","pens_made","pens_att","shots_total","shots_on_target","shots_free_kicks","shots_on_target_pct","shots_total_per90","shots_on_target_per90","goals_per_shot","goals_per_shot_on_target","xg","npxg","npxg_per_shot","xg_net","npxg_net"]
shooting2 = ["minutes_90s","goals","pens_made","pens_att","shots_total","shots_on_target","shots_free_kicks","shots_on_target_pct","shots_total_per90","shots_on_target_per90","goals_per_shot","goals_per_shot_on_target","xg","npxg","npxg_per_shot","xg_net","npxg_net"]
shooting3 = ["goals","pens_made","pens_att","shots_total","shots_on_target","shots_free_kicks","shots_on_target_pct","shots_total_per90","shots_on_target_per90","goals_per_shot","goals_per_shot_on_target","xg","npxg","npxg_per_shot","xg_net","npxg_net"]

# passing(passing)
passing = ["player","nationality","position","team","age","birth_year","minutes_90s","passes_completed","passes","passes_pct","passes_total_distance","passes_progressive_distance","passes_completed_short","passes_short","passes_pct_short","passes_completed_medium","passes_medium","passes_pct_medium","passes_completed_long","passes_long","passes_pct_long","assists","xa","xa_net","assisted_shots","passes_into_final_third","passes_into_penalty_area","crosses_into_penalty_area","progressive_passes"]
passing2 = ["passes_completed","passes","passes_pct","passes_total_distance","passes_progressive_distance","passes_completed_short","passes_short","passes_pct_short","passes_completed_medium","passes_medium","passes_pct_medium","passes_completed_long","passes_long","passes_pct_long","assists","xa","xa_net","assisted_shots","passes_into_final_third","passes_into_penalty_area","crosses_into_penalty_area","progressive_passes"]

# passtypes(passing_types)
passing_types = ["player","nationality","position","team","age","birth_year","minutes_90s","passes","passes_live","passes_dead","passes_free_kicks","through_balls","passes_pressure","passes_switches","crosses","corner_kicks","corner_kicks_in","corner_kicks_out","corner_kicks_straight","passes_ground","passes_low","passes_high","passes_left_foot","passes_right_foot","passes_head","throw_ins","passes_other_body","passes_completed","passes_offsides","passes_oob","passes_intercepted","passes_blocked"]
passing_types2 = ["passes","passes_live","passes_dead","passes_free_kicks","through_balls","passes_pressure","passes_switches","crosses","corner_kicks","corner_kicks_in","corner_kicks_out","corner_kicks_straight","passes_ground","passes_low","passes_high","passes_left_foot","passes_right_foot","passes_head","throw_ins","passes_other_body","passes_completed","passes_offsides","passes_oob","passes_intercepted","passes_blocked"]

# goal and shot creation(gca)
gca = ["player","nationality","position","team","age","birth_year","minutes_90s","sca","sca_per90","sca_passes_live","sca_passes_dead","sca_dribbles","sca_shots","sca_fouled","gca","gca_per90","gca_passes_live","gca_passes_dead","gca_dribbles","gca_shots","gca_fouled","gca_defense"]
gca2 = ["sca","sca_per90","sca_passes_live","sca_passes_dead","sca_dribbles","sca_shots","sca_fouled","gca","gca_per90","gca_passes_live","gca_passes_dead","gca_dribbles","gca_shots","gca_fouled","gca_defense"]

# defensive actions(defense)
defense = ["player","nationality","position","team","age","birth_year","minutes_90s","tackles","tackles_won","tackles_def_3rd","tackles_mid_3rd","tackles_att_3rd","dribble_tackles","dribbles_vs","dribble_tackles_pct","dribbled_past","pressures","pressure_regains","pressure_regain_pct","pressures_def_3rd","pressures_mid_3rd","pressures_att_3rd","blocks","blocked_shots","blocked_shots_saves","blocked_passes","interceptions","clearances","errors"]
defense2 = ["tackles","tackles_won","tackles_def_3rd","tackles_mid_3rd","tackles_att_3rd","dribble_tackles","dribbles_vs","dribble_tackles_pct","dribbled_past","pressures","pressure_regains","pressure_regain_pct","pressures_def_3rd","pressures_mid_3rd","pressures_att_3rd","blocks","blocked_shots","blocked_shots_saves","blocked_passes","interceptions","clearances","errors"]

# possession(possession)
possession = ["player","nationality","position","team","age","birth_year","minutes_90s","touches","touches_def_pen_area","touches_def_3rd","touches_mid_3rd","touches_att_3rd","touches_att_pen_area","touches_live_ball","dribbles_completed","dribbles","dribbles_completed_pct","players_dribbled_past","nutmegs","carries","carry_distance","carry_progressive_distance","progressive_carries","carries_into_final_third","carries_into_penalty_area","pass_targets","passes_received","passes_received_pct","miscontrols","dispossessed"]
possession2 = ["touches","touches_def_pen_area","touches_def_3rd","touches_mid_3rd","touches_att_3rd","touches_att_pen_area","touches_live_ball","dribbles_completed","dribbles","dribbles_completed_pct","players_dribbled_past","nutmegs","carries","carry_distance","carry_progressive_distance","progressive_carries","carries_into_final_third","carries_into_penalty_area","pass_targets","passes_received","passes_received_pct","miscontrols","dispossessed"]

# playingtime(playingtime)
playingtime = ["player","nationality","position","team","age","birth_year","minutes_90s","games","minutes","minutes_per_game","minutes_pct","games_starts","minutes_per_start","games_subs","minutes_per_sub","unused_subs","points_per_match","on_goals_for","on_goals_against","plus_minus","plus_minus_per90","plus_minus_wowy","on_xg_for","on_xg_against","xg_plus_minus","xg_plus_minus_per90","xg_plus_minus_wowy"]
playingtime2 = ["games","minutes","minutes_per_game","minutes_pct","games_starts","minutes_per_start","games_subs","minutes_per_sub","unused_subs","points_per_match","on_goals_for","on_goals_against","plus_minus","plus_minus_per90","plus_minus_wowy","on_xg_for","on_xg_against","xg_plus_minus","xg_plus_minus_per90","xg_plus_minus_wowy"]

# miscallaneous(misc)
misc = ["player","nationality","position","team","age","birth_year","minutes_90s","cards_yellow","cards_red","cards_yellow_red","fouls","fouled","offsides","crosses","interceptions","tackles_won","pens_won","pens_conceded","own_goals","ball_recoveries","aerials_won","aerials_lost","aerials_won_pct"]
misc2 = ["cards_yellow","cards_red","cards_yellow_red","fouls","fouled","offsides","crosses","interceptions","tackles_won","pens_won","pens_conceded","own_goals","ball_recoveries","aerials_won","aerials_lost","aerials_won_pct"]

# Function to get team-wise data accross all categories as mentioned above
# def get_team_data(top, end, text):
#     df1 = frame_for_category_team('stats',top,end,stats3,text)
#     df2 = frame_for_category_team('keepers',top,end,keepers3,text)
#     df3 = frame_for_category_team('keepersadv',top,end,keepersadv2,text)
#     df4 = frame_for_category_team('shooting',top,end,shooting3,text)
#     df5 = frame_for_category_team('passing',top,end,passing2,text)
#     df6 = frame_for_category_team('passing_types',top,end,passing_types2,text)
#     df7 = frame_for_category_team('gca',top,end,gca2,text)
#     df8 = frame_for_category_team('defense',top,end,defense2,text)
#     df9 = frame_for_category_team('possession',top,end,possession2,text)
#     df10 = frame_for_category_team('misc',top,end,misc2,text)
#     df = pd.concat([df1, df2, df3, df4, df5, df6, df7, df8, df9, df10], axis=1)
#     df = df.loc[:,~df.columns.duplicated()]
#     return df

# def frame_for_category_team(category, top, end, features, text):
#    url = (top + category + end)
#    player_table, team_table = get_tables(url,text)
#    df_team = get_frame_team(features, team_table)
#    return df_team

# def get_frame_team_2(features, team_table):
#     pre_df_squad = dict()
#     # Note: features does not contain squad name, it requires special treatment
#     features_wanted_squad = features
#     rows_squad = team_table.find_all('tr')
#     for row in rows_squad:
#         if(row.find('th',{"scope":"row"}) != None):
#             name = row.find('th',{"data-stat":"squad"}).text.strip().encode().decode("utf-8")
#             if 'squad' in pre_df_squad:
#                 pre_df_squad['squad'].append(name)
#             else:
#                 pre_df_squad['squad'] = [name]
#             for f in features_wanted_squad:
#                 cell = row.find("td",{"data-stat": f})
#                 a = cell.text.strip().encode()
#                 text=a.decode("utf-8")
#                 if(text == ''):
#                     text = '0'
#                 if((f!='player')&(f!='nationality')&(f!='position')&(f!='squad')&(f!='age')&(f!='birth_year')&(f!='team')):
#                     text = float(text.replace(',',''))
#                     print(f)
#                 if f in pre_df_squad:
#                     pre_df_squad[f].append(text)
#                 else:
#                     pre_df_squad[f] = [text]
#     df_squad = pd.DataFrame.from_dict(pre_df_squad)
#     return df_squad

# def get_frame_team(features, team_table):
#     pre_df_squad = dict()
#     # Note: features does not contain squad name, it requires special treatment
#     features_wanted_squad = features
#     rows_squad = team_table.find_all('tr')
#     for row in rows_squad:
#         if(row.find('th',{"scope":"row"}) != None):
#             name = row.find('th',{"data-stat":"team"}).text.strip().encode().decode("utf-8")
#             if 'team' in pre_df_squad:
#                 pre_df_squad['team'].append(name)
#             else:
#                 pre_df_squad['team'] = [name]
#             for f in features_wanted_squad:
#                 cell = row.find("td",{"data-stat": f})
#                 if(cell == None):
#                   continue
#                 a = cell.text.strip().encode()
#                 text=a.decode("utf-8")
#                 if(text == ''):
#                     text = '0'
#                 if((f!='player')&(f!='nationality')&(f!='position')&(f!='squad')&(f!='age')&(f!='birth_year')&(f!='team')):
#                     text = float(text.replace(',',''))
#                 if f in pre_df_squad:
#                     pre_df_squad[f].append(text)
#                 else:
#                     pre_df_squad[f] = [text]
#     df_squad = pd.DataFrame.from_dict(pre_df_squad)
#     return df_squad

# given url, download the tables with all the data inside the tbody tag
def get_tables(url, text):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    res = requests.get(url, headers = headers)

    # The next two lines get around the issue with comments breaking the parsing.
    comm = re.compile("<!--|-->")
    soup = BeautifulSoup(comm.sub("", res.text),'lxml')
    all_tables = soup.findAll("tbody")
    
    team_table = all_tables[0]
    team_vs_table = all_tables[1]
    player_table = all_tables[2]
    if text == 'for':
      return player_table, team_table
    if text == 'vs':
      return player_table, team_vs_table

# given the features and the table extract all
def get_frame(features, player_table):
    pre_df_player = dict()
    features_wanted_player = features
    rows_player = player_table.find_all('tr')
    for row in rows_player:
        if(row.find('th',{"scope":"row"}) != None):
    
            for f in features_wanted_player:
                cell = row.find("td",{"data-stat": f})
                if(cell == None):
                  continue
                a = cell.text.strip().encode()
                text=a.decode("utf-8")
                if(text == ''):
                    text = '0'
                if((f!='player')&(f!='nationality')&(f!='position')&(f!='squad')&(f!='age')&(f!='birth_year')&(f!='team')):
                    text = float(text.replace(',',''))                  
                if f in pre_df_player:
                    pre_df_player[f].append(text)
                else:
                    pre_df_player[f] = [text]
    df_player = pd.DataFrame.from_dict(pre_df_player)

    return df_player

def frame_for_category(category, top, end, features):
    
    url = (top + category + end)
    print("    from", url)
    player_table, _ = get_tables(url, 'for')
    df_player = get_frame(features, player_table)
    return df_player

# Function to get the player data for outfield player, includes all categories - standard stats, shooting
# passing, passing types, goal and shot creation, defensive actions, possession, and miscallaneous
def get_outfield_data(top, end):
    print("  Downloading data..")
    df1 = frame_for_category('stats', top, end, stats)
    df2 = frame_for_category('shooting',top, end, shooting2)
    df3 = frame_for_category('passing',top, end, passing2)
    df4 = frame_for_category('passing_types',top, end, passing_types2)
    df5 = frame_for_category('gca',top, end, gca2)
    df6 = frame_for_category('defense',top, end, defense2)
    df7 = frame_for_category('possession',top, end, possession2)
    df8 = frame_for_category('misc',top, end, misc2)
    df = pd.concat([df1, df2, df3, df4, df5, df6, df7, df8], axis=1)
    df = df.loc[:,~df.columns.duplicated()]
    return df

# Function to get keeping and advance goalkeeping data
def get_keeper_data(top, end):
    print("  Downloading data..")
    df1 = frame_for_category('keepers',top,end,keepers)
    df2 = frame_for_category('keepersadv',top,end,keepersadv2)
    df = pd.concat([df1, df2], axis=1)
    df = df.loc[:,~df.columns.duplicated()]
    return df

if __name__ == "__main__":
    print("Building csv file for Serie-A players stats")
    df_outfield = get_outfield_data('https://fbref.com/en/comps/11/','/Serie-A-Stats')
    df_outfield.to_csv('fbref_data/outfield_players.csv', index=False)
    print("\n  Printing outfield_players.csv table.. *saved on fbref_data/*")
    print(df_outfield)

    print("Building csv file for Serie-A goolkeeprs stats")
    print("\n  Printing keepers_players.csv table.. *saved on fbref_data/*")
    df_keeper = get_keeper_data('https://fbref.com/en/comps/11/','/Serie-A-Stats')
    df_keeper.to_csv('fbref_data/keepers_players.csv', index=False)
    print(df_keeper)