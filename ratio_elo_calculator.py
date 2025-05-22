import pandas as pd
from collections import defaultdict
from itertools import combinations, product

class EloCalculator:
    def __init__(self, k=32):
        self.k = k

    def calculate_expected_score(self, rating_a, rating_b):
        return 1 / (1 + 10 ** ((rating_b - rating_a) / 400))

    def update_ratings(self, rating_a, rating_b, result_a, scale=1.0, k_value=None):
        k_value = k_value or self.k
        expected_a = self.calculate_expected_score(rating_a, rating_b)
        expected_b = 1 - expected_a

        new_rating_a = rating_a + (k_value * scale * (result_a - expected_a)) * 1.0
        new_rating_b = rating_b + (k_value * scale * ((1 - result_a) - expected_b)) * 1.0

        return new_rating_a, new_rating_b

def load_initial_ratings(file_path):
    """
    Load initial ratings from a CSV file into a dictionary.
    :param file_path: Path to the CSV file.
    :return: A dictionary with keys as the first column and values as the 'Rating' column.
    """
    try:
        df = pd.read_csv(file_path)
        return dict(zip(df.iloc[:, 0], df['Rating']))
    except FileNotFoundError:
        # If the file doesn't exist, return an empty dictionary
        return {}

def calculate_elo_from_csv(file_path, fresh=False, averaged=False):
    # Load data
    df = pd.read_csv(file_path)
    df = df.loc[df['Character 1'].notnull()]
    if fresh == True:
        player_ratings = defaultdict(lambda: 1500)
        character_ratings = defaultdict(lambda: 1500)
        groove_ratings = defaultdict(lambda: 1500)
        char_groove_ratings = defaultdict(
            lambda: 1500,
            {f"{char}-{groove}": (character_ratings[char] + groove_ratings[groove]) / 2
             for char in character_ratings for groove in groove_ratings}
        )
    else:
    # Load initial ratings from CSV files
        player_ratings = defaultdict(lambda: 1500, load_initial_ratings(r"./Data/Ratio/player_elo.csv"))
        character_ratings = defaultdict(lambda: 1500, load_initial_ratings(r"./Data/Ratio/character_elo.csv"))
        groove_ratings = defaultdict(lambda: 1500, load_initial_ratings(r"./Data/Ratio/groove_elo.csv"))
        char_groove_ratings = defaultdict(lambda: 1500, load_initial_ratings(r"./Data/Ratio/char_groove_elo.csv"))

    # Initialize ELO calculator
    elo_calculator = EloCalculator(k=32)

    # Process each set
    for set_id, set_df in df.groupby('Set'):
        players = set_df['Player'].unique()
        if len(players) != 2:
            continue  # Skip sets without exactly 2 players

        player1, player2 = players
        player1_data = set_df[set_df['Player'] == player1].iloc[0]
        player2_data = set_df[set_df['Player'] == player2].iloc[0]

        # Extract characters and grooves
        player1_characters = [player1_data[f'Character {i}'] for i in range(1, 4)]
        player1_grooves = [player1_data[f'Groove {i}'] for i in range(1, 4)]
        player2_characters = [player2_data[f'Character {i}'] for i in range(1, 4)]
        player2_grooves = [player2_data[f'Groove {i}'] for i in range(1, 4)]

        # Process each win for Player 1
        for _ in range(player1_data['Wins']):
            # Update Player ELO
            player1_rating = player_ratings[player1]
            player2_rating = player_ratings[player2]
            player1_rating, player2_rating = elo_calculator.update_ratings(player1_rating, player2_rating, 1.0)
            player_ratings[player1] = player1_rating
            player_ratings[player2] = player2_rating

            # Update Character, Groove, and Character + Groove ELOs
            for char1, groove1 in zip(player1_characters, player1_grooves):
                for char2, groove2 in zip(player2_characters, player2_grooves):
                    if char1 != char2:
                        if averaged:
                            base_char1_rating = character_ratings[char1]
                            base_char2_rating = character_ratings[char2]
                            averaged_char1_rating = (base_char1_rating + player1_rating) / 2
                            averaged_char2_rating = (base_char2_rating + player2_rating) / 2
                            new_average_char1_rating, new_average_char2_rating = elo_calculator.update_ratings(averaged_char1_rating, averaged_char2_rating, 1.0, 0.33)
                            character_ratings[char1] = base_char1_rating + (new_average_char1_rating - averaged_char1_rating)
                            character_ratings[char2] = base_char2_rating + (new_average_char2_rating - averaged_char2_rating)
                        else:
                            char1_rating = character_ratings[char1]
                            char2_rating = character_ratings[char2]
                            char1_rating, char2_rating = elo_calculator.update_ratings(char1_rating, char2_rating, 1.0, 0.33)
                            character_ratings[char1] = char1_rating
                            character_ratings[char2] = char2_rating
                    if groove1 != groove2:
                        if averaged:
                            base_groove1_rating = groove_ratings[groove1]
                            base_groove2_rating = groove_ratings[groove2]
                            averaged_groove1_rating = (base_groove1_rating + player1_rating) / 2
                            averaged_groove2_rating = (base_groove2_rating + player2_rating) / 2
                            new_average_groove1_rating, new_average_groove2_rating = elo_calculator.update_ratings(averaged_groove1_rating, averaged_groove2_rating, 1.0, 0.33)
                            groove_ratings[groove1] = base_groove1_rating + (new_average_groove1_rating - averaged_groove1_rating)
                            groove_ratings[groove2] = base_groove2_rating + (new_average_groove2_rating - averaged_groove2_rating)
                        else:
                            groove1_rating = groove_ratings[groove1]
                            groove2_rating = groove_ratings[groove2]
                            groove1_rating, groove2_rating = elo_calculator.update_ratings(groove1_rating, groove2_rating, 1.0, 0.33)
                            groove_ratings[groove1] = groove1_rating
                            groove_ratings[groove2] = groove2_rating
                    if char1 != char2 or groove1 != groove2:
                        if averaged:
                            base_char_groove1_rating = char_groove_ratings[f"{char1}-{groove1}"]
                            base_char_groove2_rating = char_groove_ratings[f"{char2}-{groove2}"]
                            averaged_char_groove1_rating = (base_char_groove1_rating + player1_rating) / 2
                            averaged_char_groove2_rating = (base_char_groove2_rating + player2_rating) / 2
                            new_average_char_groove1_rating, new_average_char_groove2_rating = elo_calculator.update_ratings(averaged_char_groove1_rating, averaged_char_groove2_rating, 1.0, 0.33)
                            char_groove_ratings[f"{char1}-{groove1}"] = base_char_groove1_rating + (new_average_char_groove1_rating - averaged_char_groove1_rating)
                            char_groove_ratings[f"{char2}-{groove2}"] = base_char_groove2_rating + (new_average_char_groove2_rating - averaged_char_groove2_rating)
                        else:
                            char_groove1 = f"{char1}-{groove1}"
                            char_groove2 = f"{char2}-{groove2}"
                            char_groove1_rating = char_groove_ratings[char_groove1]
                            char_groove2_rating = char_groove_ratings[char_groove2]
                            char_groove1_rating, char_groove2_rating = elo_calculator.update_ratings(char_groove1_rating, char_groove2_rating, 1.0, 0.33)
                            char_groove_ratings[char_groove1] = char_groove1_rating
                            char_groove_ratings[char_groove2] = char_groove2_rating

        # Process each win for Player 2
        for _ in range(player2_data['Wins']):
            player1_rating = player_ratings[player1]
            player2_rating = player_ratings[player2]
            player2_rating, player1_rating = elo_calculator.update_ratings(player2_rating, player1_rating, 1.0)
            player_ratings[player1] = player1_rating
            player_ratings[player2] = player2_rating

            for char2, groove2 in zip(player2_characters, player2_grooves):
                for char1, groove1 in zip(player1_characters, player1_grooves):
                    if char1 != char2:
                        if averaged:
                            base_char1_rating = character_ratings[char1]
                            base_char2_rating = character_ratings[char2]
                            averaged_char1_rating = (base_char1_rating + player2_rating) / 2
                            averaged_char2_rating = (base_char2_rating + player1_rating) / 2
                            new_average_char1_rating, new_average_char2_rating = elo_calculator.update_ratings(averaged_char1_rating, averaged_char2_rating, 1.0, 0.33)
                            character_ratings[char1] = base_char1_rating + (new_average_char1_rating - averaged_char1_rating)
                            character_ratings[char2] = base_char2_rating + (new_average_char2_rating - averaged_char2_rating)
                        else:
                            char2_rating = character_ratings[char2]
                            char1_rating = character_ratings[char1]
                            char2_rating, char1_rating = elo_calculator.update_ratings(char2_rating, char1_rating, 1.0, 0.33)
                            character_ratings[char2] = char2_rating
                            character_ratings[char1] = char1_rating
                    if groove1 != groove2:
                        if averaged:
                            base_groove1_rating = groove_ratings[groove1]
                            base_groove2_rating = groove_ratings[groove2]
                            averaged_groove1_rating = (base_groove1_rating + player1_rating) / 2
                            averaged_groove2_rating = (base_groove2_rating + player2_rating) / 2
                            new_average_groove2_rating, new_average_groove1_rating = elo_calculator.update_ratings(averaged_groove2_rating, averaged_groove1_rating, 1.0, 0.33)
                            groove_ratings[groove1] = base_groove1_rating + (new_average_groove1_rating - averaged_groove1_rating)
                            groove_ratings[groove2] = base_groove2_rating + (new_average_groove2_rating - averaged_groove2_rating)
                        else:
                            groove1_rating = groove_ratings[groove1]
                            groove2_rating = groove_ratings[groove2]
                            groove2_rating, groove1_rating = elo_calculator.update_ratings(groove2_rating, groove1_rating, 1.0, 0.33)
                            groove_ratings[groove1] = groove1_rating
                            groove_ratings[groove2] = groove2_rating
                    if char1 != char2 or groove1 != groove2:
                        if averaged:
                            base_char_groove1_rating = char_groove_ratings[f"{char1}-{groove1}"]
                            base_char_groove2_rating = char_groove_ratings[f"{char2}-{groove2}"]
                            averaged_char_groove1_rating = (base_char_groove1_rating + player1_rating) / 2
                            averaged_char_groove2_rating = (base_char_groove2_rating + player2_rating) / 2
                            new_average_char_groove2_rating, new_average_char_groove1_rating = elo_calculator.update_ratings(averaged_char_groove2_rating, averaged_char_groove1_rating, 1.0, 0.33)
                            char_groove_ratings[f"{char1}-{groove1}"] = base_char_groove1_rating + (new_average_char_groove1_rating - averaged_char_groove1_rating)
                            char_groove_ratings[f"{char2}-{groove2}"] = base_char_groove2_rating + (new_average_char_groove2_rating - averaged_char_groove2_rating)
                        else:
                            char_groove1 = f"{char1}-{groove1}"
                            char_groove2 = f"{char2}-{groove2}"
                            char_groove1_rating = char_groove_ratings[char_groove1]
                            char_groove2_rating = char_groove_ratings[char_groove2]
                            char_groove2_rating, char_groove1_rating = elo_calculator.update_ratings(char_groove2_rating, char_groove1_rating, 1.0, 0.33)
                            char_groove_ratings[char_groove1] = char_groove1_rating
                            char_groove_ratings[char_groove2] = char_groove2_rating

    # Convert results to DataFrames
    player_df = pd.DataFrame.from_dict(player_ratings, orient='index', columns=['Rating']).reset_index(names='Player')
    character_df = pd.DataFrame.from_dict(character_ratings, orient='index', columns=['Rating']).reset_index(names='Character')
    groove_df = pd.DataFrame.from_dict(groove_ratings, orient='index', columns=['Rating']).reset_index(names='Groove')
    char_groove_df = pd.DataFrame.from_dict(char_groove_ratings, orient='index', columns=['Rating']).reset_index(names='Character-Groove')

    # Save results to CSV
    player_df.to_csv(r"./Data/Ratio/player_elo_avg.csv", index=False)
    character_df.to_csv(r"./Data/Ratio/character_elo_avg.csv", index=False)
    groove_df.to_csv(r"./Data/Ratio/groove_elo_avg.csv", index=False)
    char_groove_df.to_csv(r"./Data/Ratio/char_groove_elo_avg.csv", index=False)

    print_elo_values_from_dataframe(player_df, "Player ELO")
    print_elo_values_from_dataframe(character_df, "Character ELO")
    print_elo_values_from_dataframe(groove_df, "Groove ELO")
    print_elo_values_from_dataframe(char_groove_df, "Character-Groove ELO")


def print_elo_values_from_dataframe(df, df_name=None):
    """
    Print ELO values from a DataFrame, sorted by the first column, rounded to 2 decimal places,
    and formatted with aligned, space-padded rows.
    :param df: The DataFrame containing ELO values.
    :param column_name: The name of the first column to display.
    """
    # Sort by the first column and round the Rating column
    column_name = df.columns[0]
    df = df.sort_values(by='Rating', ascending=False)
    df['Rating'] = df['Rating'].round(2)

    # Calculate column widths for alignment
    col1_width = max(len(column_name), df[column_name].astype(str).str.len().max())
    col2_width = max(len('Rating'), len(str(df['Rating'].max())))

    # Print header
    print(f"{column_name.ljust(col1_width)}  {'Rating'.rjust(col2_width)}")
    print("-" * (col1_width + col2_width + 2))

    # Print each row
    for _, row in df.iterrows():
        print(f"{row[column_name].ljust(col1_width)}  {str(row['Rating']).rjust(col2_width)}")
    print("\n")
    print(" *" * 20)
    print("\n")   

# Run the calculation
calculate_elo_from_csv(r"Data\ratio_team_results.csv", fresh=True, averaged=True)
