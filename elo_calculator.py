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

def get_rating_sheet(path=r"./Data/elo_ratings.csv"):
    """
    Load the Elo ratings from a CSV file.
    :param path: Path to the CSV file containing Elo ratings.
    :return: DataFrame with Elo ratings.
    """
    try:
        df = pd.read_csv(path, index_col=0, header=0)
        df.index.name = 'Player'
    except FileNotFoundError:
        print(f"File not found: {path}")
        return None
    return df

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
if __name__ == "__main__":
    # Initialize EloCalculator with a K-factor of 32
    elo_calculator = EloCalculator(k=32)
    df = get_rating_sheet()
    # rating_dict = BASE_RATINGS.copy()
    rating_dict = {}
    set_cutoff = 19
    # Count occurrences of players in Player1 and Player2 columns
    player_counts = df.groupby('Player1').size().add(df.groupby('Player2').size(), fill_value=0)
    # Filter players who appear more than 19 times
    frequent_players = player_counts[player_counts > set_cutoff].index
    # Filter df to include only rows where both Player1 and Player2 are frequent players
    df = df[(df['Player1'].isin(frequent_players) & df['Player2'].isin(frequent_players))]    
    for _, x in df.iterrows():
        p1 = x['Player1']
        p2 = x['Player2']
        p1_rating = rating_dict.get(p1, 1500)
        p2_rating = rating_dict.get(p2, 1500)
        p1_rating, p2_rating = elo_calculator.update_ratings(p1_rating, p2_rating, x['P1Result'])
        rating_dict[p1] = p1_rating
        rating_dict[p2] = p2_rating
    rdf = pd.DataFrame.from_dict(rating_dict, orient='index', columns=['Rating']).reset_index(names='Player')
    rdf['Rating'] = rdf['Rating'].round(2)
    rdf = rdf.sort_values(by='Rating', ascending=False).reset_index(drop=True)   
    print(rdf)
    rdf.to_csv(r"./Data/player_ratings.csv", index=False)

