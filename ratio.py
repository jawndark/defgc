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

# Convert to DataFrame
df = pd.DataFrame(CHARACTER_RATIOS)
df.set_index('Character', inplace=True)

def get_kytanta_team(characters=3, points=7, teams=1):
    # Get all possible character-stat pairs
    counter = 0
    while counter < teams:
        try:
            char_list = []
            while len(char_list) < characters:
                character = random.choice(df.index)
                if character not in char_list:
                    char_list.append(character)
            # print(char_list)
            char_df = df.loc[char_list]
            # print(char_df)
            all_pairs = list(product(char_df.index, char_df.columns))
            # print(all_pairs)
    
        # Find valid combinations of 3 pairs that sum to 7
            valid_combos = []
            combos = combinations(all_pairs, characters)
        # print(combos)
            for combo in combos:
            # Check if any character appears more than once
                chars_in_combo = [char for char, _ in combo]
                if len(set(chars_in_combo)) < characters:
                    continue            
                # print(combo)
                values = [char_df.loc[char, stat] for char, stat in combo]
                # print(values)
                if sum(values) == points:
                    # print(combo)
                    char_combos = []
                    for idx, char_vals in enumerate(combo):
                        # print(f"{char_vals}")
                        char_combos.append((char_vals[0], char_vals[1], int(values[idx])))  
                    valid_combos.append(char_combos)
            if valid_combos:
                # print(f"Valid combos: {valid_combos}")
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
            
    
        


    

# Test the function




# def get_groove_nums(max):
#     groove_nums = [0,0,0]
#     # print(f"Max: {max}")
#     # print(f"Groove nums: {sum(groove_nums)}")
#     while (sum(groove_nums) + max) != 0:
#         groove_nums =  [randint(-2,0), randint(-2,0),randint(-2,0)]
#     return groove_nums

# def random_team(points_needed = 7, characters_needed = 3):
#     points = 0
#     while points != points_needed:
#         tier_nums = [randint(1,min(points_needed + 2, 5)) for x in range(characters_needed)] 
#         total_tier_nums = sum(tier_nums)
#         if total_tier_nums > 6 * characters_needed:
#             continue
#         # print(f"Tier sum: {sum(tier_nums)}")
#         # print(f"Tier nums: {tier_nums}")
#         if total_tier_nums > 13 or total_tier_nums < 7:
#             continue
#         elif total_tier_nums == 13:
#             groove_nums = [-2 for x in range(chars_needed)]
#         elif total_tier_nums == 12:
#             if not base_groove_nums:
#                 groove_nums = [-2, -2, -1]
#                 shuffle(groove_nums)
#             else:
#                 groove_nums = base_groove_nums
#                 if len(groove_nums) >= 3:
#                     break
#                 if len(groove_nums) == 2 and sum(groove_nums) == -4:
#                     groove_nums.append(-1)
#                 elif len(groove_nums) == 2 and sum(groove_nums) == -3:
#                     groove_nums.append(-2)
#                 elif len(groove_nums) == 1 and sum(groove_nums) == -2:
#                     new_groove_nums = [-2,-1]
#                     shuffle(new_groove_nums)
#                     groove_nums.extend(new_groove_nums)
#                 elif len(groove_nums) == 1 and sum(groove_nums) == -1:
#                     groove_nums.extend([-2,-2])
#                 else:
#                     print("Error. Invalid groove num entry.")
#         elif total_tier_nums == 7:
#             groove_nums = [0, 0, 0]
#         else:
#             groove_nums = get_groove_nums(sum(tier_nums) - 7)     
#         points = sum(tier_nums) + sum(groove_nums)

#     for tier_num, groove_num in zip(tier_nums, groove_nums):
#         # print(tier_num)
#         # print(groove_num)
        
#         character = choice(TIER_CHAR[tier_num])
#         if character in characters:
#             while character in characters:
#                 character = choice(TIER_CHAR[tier_num])
#         characters.append(character)
#         groove = choice(TIER_GROOVE[groove_num])
#         # print(character)
#         # print(groove)
#         team.append({"Character" : character, "Groove" : groove, "Points" : sum([tier_num, groove_num])})                    
#     return team