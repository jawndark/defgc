import pandas as pd
import random
from itertools import combinations, product
CHARACTER_RATIOS = {
    'Character': [
        'Buttobi', 'Dr. K', 'Kinoko', 'Masako', 'Masao', 'Taro', 'Garasha', 'Jakor', 'Robo Azuma', 'Spike', 'Zacky Wild', 'Blues', 'Investigator', 'K. Kyanta', 'Michelle', 'Nanatsu', 'Natanee', 'Rogue', 'Well Done', 'Cocorn', 'Kyanta', 'M. Michelle', 'Myusha', 'Rare', 'Anna', 'Chihiro', 'Gyanta', 'Hatoyan', 'Hisomi', 'Sendou', 'Tsuki'
    ],
    'Stamina': [1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5, 5, 5],
    'Super': [1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5, 5, 5],
    'Ex': [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4],
    'Demon': [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4],
    'Speed': [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4],
    'Parry': [-1, -1, -1, -1, -1, -1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3]
}

GROOVE_VALUES = {'Stamina' : 0, 'Super' : 0, 'Ex' : -1, 'Demon' : -1, 'Speed' : -1, 'Parry' : -2}

def create_tier_dataframe(path=".\Data\character_tiers.csv", grooves=None):
    if grooves is None:
        grooves = GROOVE_VALUES
    try:
        df = pd.read_csv(path, index_col=0, header=0)
        df.index.name = 'Character'        
    except FileNotFoundError:
        print(f"File not found: {path}")
        df = pd.DataFrame(CHARACTER_RATIOS)
        df.set_index('Character', inplace=True)
        return df
    df['Average'] = df.mean(axis=1).round(0)
    for key, value in grooves.items():
        df[key] = df['Average'] + value
    return df[grooves.keys()]




def get_kyanta_team(characters=3, points=7, teams=1):
    df = create_tier_dataframe()
    counter = 0
    while counter < teams:
        try:
            char_list = []
            while len(char_list) < characters:
                character = random.choice(df.index)
                if character not in char_list:
                    char_list.append(character)
            char_df = df.loc[char_list]
            all_pairs = list(product(char_df.index, char_df.columns))
            valid_combos = []
            combos = combinations(all_pairs, characters)
            for combo in combos:
                chars_in_combo = [char for char, _ in combo]
                if len(set(chars_in_combo)) < characters:
                    continue            
                values = [char_df.loc[char, stat] for char, stat in combo]
                if sum(values) == points:
                    char_combos = []
                    for idx, char_vals in enumerate(combo):
                        char_combos.append((char_vals[0], char_vals[1], int(values[idx])))  
                    valid_combos.append(char_combos)
            if valid_combos:
                selected = random.choice(valid_combos)
                counter += 1
                print(f"Team {counter}")                
                for csv in selected:
                    print(f"{csv[0]:<15}{csv[1]:<8}{csv[2]:>2}")
                print("")
            else:
                print("No valid combinations found. Trying again...")
        except Exception as e:
            print(f"Error: {e}")
            pass
