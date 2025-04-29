import pandas as pd
import random
from itertools import combinations, product
CHARACTER_RATIOS = {
    'Character': [
        'Buttobi', 'Dr. K', 'Kinoko', 'Masako', 'Masao', 'Taro', 'Garasha', 'Jakor', 'Robo Azuma', 'Spike', 'Zacky Wild', 'Blues', 'Gator',            'K. Kyanta', 'Michelle', 'Nanatsu', 'Natanee', 'Rogue', 'Well Done', 'Cocorn', 'Kyanta', 'M. Michelle', 'Myusha', 'Rare', 'Anna',              'Chihiro', 'Gyanta', 'Hatoyan', 'Hisomi', 'Sendou', 'Tsuki'
    ],
    'Stamina': [1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5, 5, 5],
    'Super': [1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5, 5, 5],
    'Ex': [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4],
    'Demon': [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4],
    'Speed': [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4],
    'Parry': [-1, -1, -1, -1, -1, -1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3]
}

df = pd.DataFrame(CHARACTER_RATIOS)
df.set_index('Character', inplace=True)

def get_kyanta_team(characters=3, points=7, teams=1):
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
