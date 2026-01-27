# lab.py


import os
import io
from pathlib import Path
import pandas as pd
import numpy as np


# ---------------------------------------------------------------------
# QUESTION 1
# ---------------------------------------------------------------------


def trick_me():

    tricky_1 = {
        'Name': ['Adam', 'Eric', 'Gavin', 'Trent', 'M'],
        'Name': ['some', 'name', 'that', 'I', 'have'],
        'Age': [22, 21, 21, 21, 22],
    }
    df = pd.DataFrame(tricky_1)
    df.to_csv("tricky_1.csv", index=False)

    tricky_2 = df.copy()
    
    return 3
    

def trick_bool():
    bools ={
        True: [1, 1],
        True: [1, 1],
        False: [0, 0],
        False: [0, 0],
    }
    df = pd.DataFrame(bools)
    return [10, 6, 13]



# ---------------------------------------------------------------------
# QUESTION 2
# ---------------------------------------------------------------------


def population_stats(df):
    n = len(df)
    num_nonnull = df.notna().sum()
    prop_nonnull = num_nonnull / n
    num_distinct = df.nunique(dropna=True)
    prop_distinct = num_distinct / num_nonnull.replace(0, np.nan)

    return pd.DataFrame({
        "num_nonnull": num_nonnull,
        "prop_nonnull": prop_nonnull,
        "num_distinct": num_distinct,
        "prop_distinct": prop_distinct
    })





# ---------------------------------------------------------------------
# QUESTION 3
# ---------------------------------------------------------------------


def most_common(df, N):

    out = pd.DataFrame(index=range(N))

    for col in df.columns:
        vc = df[col].value_counts(dropna=False)

        vals = [np.nan] * N
        counts = [np.nan] * N

        k = min(N, len(vc))
        vals[:k] = list(vc.index[:k])   
        counts[:k] = list(vc.iloc[:k].values)

        out[col + "_values"] = vals
        out[col + "_counts"] = counts
    
    return out
        
    ...


# ---------------------------------------------------------------------
# QUESTION 4
# ---------------------------------------------------------------------


def super_hero_powers(powers):
    df = powers.copy()
    
    names = df['hero_names']
    X = df.drop(columns='hero_names').astype(bool)

    power_counts = X.sum(axis=1)
    hero_most = names.loc[power_counts.idxmax()]

    fliers = X['Flight']
    most_common_flyer_power = X.loc[fliers].drop(columns='Flight').sum().idxmax()

    one_power = power_counts == 1
    most_common_single_power = X.loc[one_power].sum().idxmax()

    return [hero_most, most_common_flyer_power, most_common_single_power]



# ---------------------------------------------------------------------
# QUESTION 5
# ---------------------------------------------------------------------


def clean_heroes(df):
    return df.replace({'-': np.nan, -99: np.nan})



# ---------------------------------------------------------------------
# QUESTION 6
# ---------------------------------------------------------------------


def super_hero_stats():
    return [
        "Onslaught",
        "George Lucas",
        "bad",
        "Marvel Comics",
        "NBC - Heroes",
        "Groot"
    ]


# ---------------------------------------------------------------------
# QUESTION 7
# ---------------------------------------------------------------------


def clean_universities(df):
    out = df.copy()

    out["institution"] = out["institution"].str.replace("\n", ", ", regex=False)

    out["broad_impact"] = out["broad_impact"].astype(int)

    split = out["national_rank"].str.split(",", expand=True)
    out["nation"] = split[0].str.strip()
    out["national_rank_cleaned"] = split[1].astype(int)

    country_map = {
        "USA": "United States",
        "United States": "United States",

        "UK": "United Kingdom",
        "United Kingdom": "United Kingdom",

        "South Korea": "Korea, South",
        "Korea, South": "Korea, South",

        "Czechia": "Czech Republic",
        "Czech Republic": "Czech Republic",

        "Russia": "Russian Federation",
        "Russian Federation": "Russian Federation",
    }
    out["nation"] = out["nation"].replace(country_map)

    out = out.drop(columns="national_rank")

    out["is_public"] = out["control"].eq("Public")

    return out


def university_info(cleaned):
    df = cleaned.copy()

    state_counts = df["state"].value_counts()
    valid_states = state_counts[state_counts >= 3].index
    q1 = (
        df[df["state"].isin(valid_states)]
        .groupby("state")["score"]
        .mean()
        .idxmin()
    )

    top_100 = df[df["world_rank"] <= 100]
    q2 = (top_100["quality_of_faculty"] <= 100).mean()

    private_prop = (
        df.groupby("state")["is_public"]
        .apply(lambda x: (~x).mean())
    )
    q3 = (private_prop >= 0.5).sum()

    best_in_nation = df[df["national_rank_cleaned"] == 1]
    q4 = best_in_nation.loc[best_in_nation["world_rank"].idxmax(), "institution"]

    return [q1, q2, q3, q4]


