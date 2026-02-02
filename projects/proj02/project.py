# project.py


import pandas as pd
import numpy as np
np.set_printoptions(threshold=20, suppress=True, legacy='1.21')

from pathlib import Path

import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
pd.options.plotting.backend = 'plotly'

from IPython.display import display

# DSC 80 preferred styles
pio.templates["dsc80"] = go.layout.Template(
    layout=dict(
        margin=dict(l=30, r=30, t=30, b=30),
        autosize=True,
        width=600,
        height=400,
        xaxis=dict(showgrid=True),
        yaxis=dict(showgrid=True),
        title=dict(x=0.5, xanchor="center"),
    )
)
pio.templates.default = "simple_white+dsc80"
import warnings
warnings.filterwarnings("ignore")


# ---------------------------------------------------------------------
# QUESTION 1
# ---------------------------------------------------------------------


def clean_loans(loans):
    cleaned = loans.copy()

    cleaned["issue_d"] = pd.to_datetime(cleaned["issue_d"])
    cleaned["term"] = cleaned["term"].astype(str).str.extract(r"(\d+)").astype(int)

    cleaned["emp_title"] = cleaned["emp_title"].str.lower().str.strip()
    cleaned["emp_title"] = cleaned["emp_title"].replace("rn", "registered nurse")

    def add_months(m):
        return pd.DateOffset(months=int(m))

    cleaned["term_end"] = cleaned["issue_d"] + cleaned["term"].map(add_months)

    return cleaned




# ---------------------------------------------------------------------
# QUESTION 2
# ---------------------------------------------------------------------


def correlations(df, pairs):
    rs = []
    names = []

    for col1, col2 in pairs:
        r = df[col1].corr(df[col2]) # pearson correlation on the dti, interest rate to the annual income, credit score
        rs.append(r)
        names.append(f'r_{col1}_{col2}') # 

    return pd.Series(data=rs, index=names)



# ---------------------------------------------------------------------
# QUESTION 3
# ---------------------------------------------------------------------


def create_boxplot(loans):
    score_range = []
    for score in loans["fico_range_low"]:
        if score < 670:
            score_range.append("[580, 670)")
        elif score < 740:
            score_range.append("[670, 740)")
        elif score < 800:
            score_range.append("[740, 800)")
        else:
            score_range.append("[800, 850)")

    fig = px.box(
        loans,
        x=score_range,
        y="int_rate",
        color="term",
        category_orders={"x": ["[580, 670)", "[670, 740)", "[740, 800)", "[800, 850)"]},
        labels={
            "x": "Credit Score Range",
            "int_rate": "Interest Rate (%)",
            "term": "Loan Length (Months)"
        },
        title="Interest Rate vs. Credit Score",
        color_discrete_map={36: "purple", 60: "gold"}
    )

    fig.update_layout(legend_title_text="Loan Length (Months)")
    return fig



# ---------------------------------------------------------------------
# QUESTION 4
# ---------------------------------------------------------------------


def ps_test(loans, N):
    df = loans.copy()

    has_ps = df["desc"].notna()
    observed = (
        df.loc[has_ps, "int_rate"].mean() - df.loc[~has_ps, "int_rate"].mean()
    )

    diffs = []
    for _ in range(N):
        shuffled = has_ps.sample(frac=1, replace=False).reset_index(drop=True)
        diff = (
            df.loc[shuffled, "int_rate"].mean()
            - df.loc[~shuffled, "int_rate"].mean()
        )
        diffs.append(diff)

    diffs = np.array(diffs)
    p_value = np.mean(diffs >= observed)

    return p_value
    
def missingness_mechanism():
    return 2

def other_missingness():
    return 2


# ---------------------------------------------------------------------
# QUESTION 5
# ---------------------------------------------------------------------


def tax_owed(income, brackets):
    ...


# ---------------------------------------------------------------------
# QUESTION 6
# ---------------------------------------------------------------------


def clean_state_taxes(state_taxes_raw): 
    ...


# ---------------------------------------------------------------------
# QUESTION 7
# ---------------------------------------------------------------------


def state_brackets(state_taxes):
    ...
    
def combine_loans_and_state_taxes(loans, state_taxes):
    # Start by loading in the JSON file.
    # state_mapping is a dictionary; use it!
    import json
    state_mapping_path = Path('data') / 'state_mapping.json'
    with open(state_mapping_path, 'r') as f:
        state_mapping = json.load(f)
        
    # Now it's your turn:
    ...


# ---------------------------------------------------------------------
# QUESTION 8
# ---------------------------------------------------------------------


def find_disposable_income(loans_with_state_taxes):
    FEDERAL_BRACKETS = [
     (0.1, 0), 
     (0.12, 11000), 
     (0.22, 44725), 
     (0.24, 95375), 
     (0.32, 182100),
     (0.35, 231251),
     (0.37, 578125)
    ]
    ...


# ---------------------------------------------------------------------
# QUESTION 9
# ---------------------------------------------------------------------


def aggregate_and_combine(loans, keywords, quantitative_column, categorical_column):
    ...


# ---------------------------------------------------------------------
# QUESTION 10
# ---------------------------------------------------------------------


def exists_paradox(loans, keywords, quantitative_column, categorical_column):
    ...
    
def paradox_example(loans):
    return {
        'loans': loans,
        'keywords': [..., ...],
        'quantitative_column': ...,
        'categorical_column': ...
    }
