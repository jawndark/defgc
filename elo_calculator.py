import pandas as pd

BASE_RATINGS = {'Boog': 1500,
 'Tension': 1500,
 'Pnuema': 1500,
 'Poke': 1500,
 'Squid': 1500,
 'Cherub': 1500,
 'Benirenge': 1500,
 'Cosmic': 1500,
 'Gravfu': 1500,
 'Valentine': 1500,
 'Trickster': 1500,
 'Jawn': 1500,
 'D-Cint': 1500,
 'AaronDaGawd': 1500,
 'RickWa': 1500,
 'Dwarl': 1500,
 'Parappa': 1500,
 'Timestop': 1500}

MOCK_TEAMS = {'Boog': ['Hatoyan', 'Tsuki', 'Gyanta'],
 'Tension': ['Cocorn', 'Hatoyan','Zacky Wild'],
 'Poke': ['Kyanta', 'Jakor', 'Gyanta'],
 'Squid': ['Garasha', 'Chihiro', 'Sendou'],
 'Cosmic': ['M. Michelle', 'Anna', 'Investigator'],
 'Valentine': ['Natanee', 'Myusha', 'Hatoyan'],
 'Jawn': ['Nanatsu', 'Rare', 'Natanee'],
 'D-Cint': ['Hatoyan', 'Michelle', 'Gyanta'],
 'Parappa': ['Hatoyan', 'Anna', 'Chihiro']}

def get_rating_sheet(path=r"./Data/elo_ratings.csv"):
    """
    Load the Elo ratings from a CSV file.
    :param path: Path to the CSV file containing Elo ratings.
    :return: DataFrame with Elo ratings.
    """
    try:
        df = pd.read_csv(path, index_col=0, header=0)
        df.index.name = 'Player'
        # df = df.sort_index(ascending=False)
    except FileNotFoundError:
        print(f"File not found: {path}")
        return None
    return df

def calculate_odds(rating_a, rating_b):
    """
    Calculate the odds of player A winning against player B.
    :param rating_a: Rating of player A.
    :param rating_b: Rating of player B.
    :return: Odds of player A winning.
    """
    return 1 / (1 + 10 ** ((rating_b - rating_a) / 400))

class EloCalculator:
    def __init__(self, k=32):
        """
        Initialize the EloCalculator with a K-factor.
        :param k: The K-factor determines how much ratings change after a match.
        """
        self.k = k

    def calculate_expected_score(self, rating_a, rating_b):
        """
        Calculate the expected score for a player.
        :param rating_a: Rating of player A.
        :param rating_b: Rating of player B.
        :return: Expected score for player A.
        """
        return 1 / (1 + 10 ** ((rating_b - rating_a) / 400))

    def update_ratings(self, rating_a, rating_b, result_a):
        """
        Update the ratings for two players based on the match result.
        :param rating_a: Current rating of player A.
        :param rating_b: Current rating of player B.
        :param result_a: Result for player A (0.0 to 1.0). Player B's result is (1 - result_a).
        :return: Updated ratings for player A and player B.
        """
        expected_a = self.calculate_expected_score(rating_a, rating_b)
        expected_b = 1 - expected_a

        new_rating_a = rating_a + self.k * (result_a - expected_a)
        new_rating_b = rating_b + self.k * ((1 - result_a) - expected_b)

        return new_rating_a, new_rating_b


# Example usage
# if __name__ == "__main__":
#     # Initialize EloCalculator with a K-factor of 32
#     elo_calculator = EloCalculator(k=32)
#     df = get_rating_sheet()
#     # rating_dict = BASE_RATINGS.copy()
#     rating_dict = {}
#     set_cutoff = 19
#     player_counts = df.groupby('Player1').size().add(df.groupby('Player2').size(), fill_value=0)
#     frequent_players = player_counts[player_counts > set_cutoff].index
#     df = df[(df['Player1'].isin(frequent_players) & df['Player2'].isin(frequent_players))]    
#     for _, x in df.iterrows():
#         p1 = x['Player1']
#         p2 = x['Player2']
#         p1_rating = rating_dict.get(p1, 1500)
#         p2_rating = rating_dict.get(p2, 1500)
#         p1_rating, p2_rating = elo_calculator.update_ratings(p1_rating, p2_rating, x['P1Result'])
#         rating_dict[p1] = p1_rating
#         rating_dict[p2] = p2_rating
#     rdf = pd.DataFrame.from_dict(rating_dict, orient='index', columns=['Rating']).reset_index(names='Player')
#     rdf['Rating'] = rdf['Rating'].round(2)
#     rdf = rdf.sort_values(by='Rating', ascending=False).reset_index(drop=True)   
#     print(rdf)
#     rdf.to_csv(r"./Data/player_ratings.csv", index=False)

if __name__ == "__main__":
    # Initialize EloCalculator with a K-factor of 32
    elo_calculator = EloCalculator(k=32)
    df = get_rating_sheet()
    # rating_dict = BASE_RATINGS.copy()
    char_rating_dict = {}
    player_rating_dict = {}
    set_cutoff = 19
    player_counts = df.groupby('Player1').size().add(df.groupby('Player2').size(), fill_value=0)
    frequent_players = player_counts[player_counts > set_cutoff].index
    df = df[(df['Player1'].isin(frequent_players) & df['Player2'].isin(frequent_players))]   
    for char_num in range(1,4):
        df[f'P1C{char_num}'] = df['Player1'].apply(lambda x: MOCK_TEAMS[x][char_num-1])
        df[f'P2C{char_num}'] = df['Player2'].apply(lambda x: MOCK_TEAMS[x][char_num-1])    
    for _, x in df.iterrows():
        p1 = x['Player1']
        p2 = x['Player2']
        old_p1_rating = player_rating_dict.get(p1, 1500)
        old_p2_rating = player_rating_dict.get(p2, 1500)
        # print(f'P1: {p1}, P2: {p2}')
        # print(f"P1 Rating: {old_p1_rating}, P2 Rating: {old_p2_rating}")
        p1_rating, p2_rating = elo_calculator.update_ratings(old_p1_rating, old_p2_rating, x['P1Result'])   
        player_rating_dict[p1] = p1_rating
        player_rating_dict[p2] = p2_rating  
        p1_rating_change = p1_rating - old_p1_rating
        p2_rating_change = p2_rating - old_p2_rating    
        for p1_num in range(1,4):
            p1ch = x[f'P1C{p1_num}']
            for p2_num in range(1,4):
                p2ch = x[f'P2C{p2_num}']
                if p1ch == p2ch:
                    continue
                # print(f" P1character: {p1ch}, P2character: {p2ch}")
                character_1_rating = char_rating_dict.get(p1ch, 1500)
                character_2_rating = char_rating_dict.get(p2ch, 1500)
                # print(f"Current Character Rating: {character_1_rating}, Current Character Rating: {character_2_rating}")
                p1ch_rating, p2ch_rating = elo_calculator.update_ratings(character_1_rating, character_2_rating, x['P1Result'])
                char_rating_dict[p1ch] = p1ch_rating - (p1_rating_change * 1.0)
                char_rating_dict[p2ch] = p2ch_rating - (p2_rating_change * 1.0)
                # p1ch_rating, p2ch_rating = elo_calculator.update_ratings(current_p1ch_rating, current_p2ch_rating, x['P1Result'])
                # print(f"Updated P1character Rating: {p1ch_rating}, Updated P2Character Rating: {p2ch_rating}")
                # p1ch_rating += p1_rating_change
                # p2ch_rating += p2_rating_change
                # print(f"Adjusted P1character Rating: {p1ch_rating}, Adjusted P2Character Rating: {p2ch_rating}")
                # current_p1ch_rating = (character_1_rating + p1_rating) / 2.0
                # current_p2ch_rating = (character_2_rating + p2_rating) / 2.0
                # print(f" Adjusted P1character Rating: {current_p1ch_rating}, Adjusted P2Character Rating: {current_p2ch_rating}")

                # print(f" Updated P1character Rating: {p1ch_rating}, Updated P2Character Rating: {p2ch_rating}")

                # char_rating_dict[p2ch] = character_2_rating + ((p2ch_rating - current_p2ch_rating) * 0.5)
    rdf = pd.DataFrame.from_dict(char_rating_dict, orient='index', columns=['Rating']).reset_index(names='Character')
    rdf['Rating'] = rdf['Rating'].round(2)
    rdf = rdf.sort_values(by='Rating', ascending=False).reset_index(drop=True)   
    print(rdf)
    rdf.to_csv(r"./Data/player_character_ratings_weighted.csv", index=False)
    prdf = pd.DataFrame.from_dict(player_rating_dict, orient='index', columns=['Rating']).reset_index(names='Player')
    prdf['Rating'] = prdf['Rating'].round(2)
    prdf = prdf.sort_values(by='Rating', ascending=False).reset_index(drop=True)   
    print(prdf)
    prdf.to_csv(r"./Data/player_ratings.csv", index=False)    

