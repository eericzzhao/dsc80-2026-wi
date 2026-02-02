# lab.py


import os
import io
from pathlib import Path
import pandas as pd
import numpy as np


# ---------------------------------------------------------------------
# QUESTION 1
# ---------------------------------------------------------------------


def read_linkedin_surveys(survey_dir):
    p = Path(survey_dir)
    dfs = []

    for f in p.iterdir():
        if f.name.startswith("survey") and f.suffix == ".csv":
            df = pd.read_csv(f)

            df.columns = [
                "first name",
                "last name",
                "current company",
                "job title",
                "email",
                "university",
            ]

            dfs.append(df)
        
    return pd.concat(dfs, ignore_index=True)


def linkedin_stats(read_linkedin_surveys):
    ohio = read_linkedin_surveys["university"].str.contains("Ohio", na=False)
    prog = read_linkedin_surveys["job title"].str.contains("Programmer", na=False)
    prop = (ohio & prog).sum() / ohio.sum()

    engineer_titles = read_linkedin_surveys["job title"].str.endswith("Engineer", na=False)
    num_engineer_titles = read_linkedin_surveys.loc[engineer_titles, "job title"].nunique()

    longest_title = read_linkedin_surveys.loc[read_linkedin_surveys["job title"].str.len().idxmax(), "job title"]
    
    num_mnagers = read_linkedin_surveys["job title"].str.contains("manager", case=False, na=False).sum()
    return [prop, num_engineer_titles, longest_title, num_mnagers]



# ---------------------------------------------------------------------
# QUESTION 2
# ---------------------------------------------------------------------


def read_student_surveys(fav_dir):
    path = Path(fav_dir)
    if not path.exists():
        raise FileNotFoundError
    
    files = sorted(path.glob("favorite*.csv"))
    
    df = pd.read_csv(files[0]).set_index("id")

    for f in files[1:]:
        temp = pd.read_csv(f).set_index("id")
        df = df.join(temp)


    return df


def check_credit(read_student_surv):

    surveys = read_student_surv.drop(columns="name")

    surveys = surveys.replace("(no genres listed)", pd.NA)

    answered_frac = surveys.notna().mean(axis=1)
    student_ec = (answered_frac >= 0.5) * 5

    question_frac = surveys.notna().mean()
    class_ec = min(2, (question_frac >= 0.9).sum())

    return pd.DataFrame({
        "name": read_student_surv["name"],
        "ec": student_ec + class_ec
    })


# ---------------------------------------------------------------------
# QUESTION 3
# ---------------------------------------------------------------------


def most_popular_procedure_type(pets, procedure_history):
    in_pets = procedure_history[procedure_history["PetID"].isin(pets["PetID"])]
    return in_pets["ProcedureType"].value_counts().idxmax()

def pet_name_by_owner(owners, pets):
    first_col = "FirstName" if "FirstName" in owners.columns else "Name"

    pet_lists = pets.groupby("OwnerID")["Name"].apply(list)

    def convert(owner_id):
        xs = pet_lists.get(owner_id, [])
        if len(xs) == 1:
            return xs[0]
        return xs

    values = owners["OwnerID"].apply(convert)
    return pd.Series(values.values, index=owners[first_col])



def total_cost_per_city(owners, pets, procedure_history, procedure_detail):

    pet_city = pets.merge(
        owners[["OwnerID", "City"]],
        on="OwnerID",
        how="left"
    )[["PetID", "City"]]

    hist = procedure_history[procedure_history["PetID"].isin(pets["PetID"])]

    hist = hist.merge(
        procedure_detail[["ProcedureType", "ProcedureSubCode", "Price"]],
        on=["ProcedureType", "ProcedureSubCode"],
        how="left"
    )

    hist = hist.merge(pet_city, on="PetID", how="left")

    spend = hist.groupby("City")["Price"].sum().fillna(0)

    all_cities = owners["City"].drop_duplicates()
    return spend.reindex(all_cities, fill_value=0)


# ---------------------------------------------------------------------
# QUESTION 4
# ---------------------------------------------------------------------


def average_seller(sales):
    out = sales.pivot_table(
        index="Name",
        values="Total",
        aggfunc="mean"
    )
    out = out.rename(columns={"Total": "Average Sales"})
    return out.fillna(0)

def product_name(sales):
    return sales.pivot_table(
        index="Name",
        columns="Product",
        values="Total",
        aggfunc="sum"
    )

def count_product(sales):
    return sales.pivot_table(
        index=["Product", "Name"],
        columns="Date",
        values="Total",
        aggfunc="size",
        fill_value=0
    )

def total_by_month(sales):
    sales = sales.copy()
    sales["Month"] = pd.to_datetime(sales["Date"]).dt.month

    return sales.pivot_table(
        index=["Name", "Product"],
        columns="Month",
        values="Total",
        aggfunc="sum",
        fill_value=0
    )
