import pandas as pd
CHARACTER_LIST =  [
        'Buttobi', 'Dr. K', 'Kinoko', 'Masako', 'Masao', 'Taro', 'Garasha', 'Jakor', 'Robo Azuma', 'Spike', 'Zacky Wild', 'Blues', 'Investigator', 'K. Kyanta', 'Michelle', 'Nanatsu', 'Natanee', 'Rogue', 'Well Done', 'Cocorn', 'Kyanta', 'M. Michelle', 'Myusha', 'Rare', 'Anna', 'Chihiro', 'Gyanta', 'Hatoyan', 'Hisomi', 'Sendou', 'Tsuki'
    ]

def get_bans_dataframe(path=r"./Data/bans.csv"):
    try:
        df = pd.read_csv(path, index_col=0, header=0)
        df.index.name = 'Character'
    except FileNotFoundError:
        print(f"File not found: {path}")
        df = pd.DataFrame()
    return df

def bans_by_player_character(ban_df):
    bdf = ban_df.copy()
    player_counts = bdf.groupby(['Player', 'Character']).size()
    return player_counts

def bans_by_character(ban_df):
    bdf = ban_df.copy()
    player_counts = bdf.groupby(['Character']).size()
    return player_counts

def get_bans_tier(ban_df):
    bdf = bans_by_character(ban_df).reset_index().rename(columns={0: 'Bans'})
    missing = [x for x in CHARACTER_LIST if x not in bdf['Character'].tolist()]
    mdf = pd.DataFrame(missing, columns=['Character'])
    mdf['Bans'] = 0
    bdf = pd.concat([bdf, mdf], ignore_index=True).set_index('Character').sort_index()
    bdf['BanTier'] = pd.qcut(bdf['Bans'], q=5, labels=[1,2,3,4,5]) #This doesn't work with so many characters with low bans
    return bdf['BanTier']
