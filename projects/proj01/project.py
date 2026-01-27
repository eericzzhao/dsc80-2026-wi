# project.py


import pandas as pd
import numpy as np
from pathlib import Path
import plotly.express as px


# ---------------------------------------------------------------------
# QUESTION 1
# ---------------------------------------------------------------------


def get_assignment_names(grades):
    syllabus_dict = {
        'lab':[],
        'project':[],
        'midterm':[],
        'final':[],
        'disc': [],
        'checkpoint':[]
    }

    for col in grades.columns:
        col_lower = col.lower()
        if col_lower.startswith('lab') and len(col) <= 5:
            syllabus_dict['lab'].append(col)
        elif col_lower.startswith('project') and 'checkpoint' in col and len(col_lower) <= 22:
            syllabus_dict['checkpoint'].append(col)
        elif col_lower.startswith('project') and len(col) <= 9:
            syllabus_dict['project'].append(col)
        elif col_lower.startswith('midterm') and len(col) <= 9:
            syllabus_dict['midterm'].append(col)
        elif col == 'Final':
            syllabus_dict['final'].append(col)
        elif col_lower.startswith('discussion') and len(col) <= 12:
            syllabus_dict['disc'].append(col)
    return syllabus_dict



# ---------------------------------------------------------------------
# QUESTION 2
# ---------------------------------------------------------------------


def projects_overall(grades):
    proj_names = get_assignment_names(grades)['project']
    proj_scores = []

    for pr in proj_names:
        pr_mp = f'{pr} - Max Points'
        fr = f'{pr}_free_response'
        fr_mp = f'{pr}_free_response - Max Points'

        if fr in grades.columns and fr_mp in grades.columns:
            total_earned = grades[pr].fillna(0) + grades[fr].fillna(0)
            total_max = grades[pr_mp] + grades[fr_mp]
        else:
            total_earned = grades[pr].fillna(0)
            total_max = grades[pr_mp]

        proj_score = total_earned / total_max
        proj_scores.append(proj_score)

    total = pd.concat(proj_scores, axis=1).mean(axis=1)

    return total


# ---------------------------------------------------------------------
# QUESTION 3
# ---------------------------------------------------------------------


def lateness_penalty(late_series):
    def change_time_to_hours(time):
        if pd.isna(time) or time == '00:00:00':
            return 0

        parts = str(time).split(':')
        hours = int(parts[0])
        minutes = int(parts[1])
        seconds = int(parts[2])

        lateness_hours = hours + minutes / 60 + seconds / 3600

        return lateness_hours

    hours = late_series.apply(change_time_to_hours)

    lateness_score = pd.Series(1.0, index = late_series.index)

    lateness_score[hours > 2] = 0.9
    lateness_score[hours > 168] = 0.7
    lateness_score[hours > 336] = 0.4

    return lateness_score


# ---------------------------------------------------------------------
# QUESTION 4
# ---------------------------------------------------------------------


def process_labs(grades):
    lab_names = get_assignment_names(grades)['lab']
    lab_data = {}

    for lab in lab_names:
        raw = grades[lab].fillna(0)

        max_pts = grades[lab + ' - Max Points']
        multiplier = lateness_penalty(grades[lab + ' - Lateness (H:M:S)'])

        lab_data[lab] = (raw * multiplier) / max_pts

    return pd.DataFrame(lab_data, index=grades.index)
    




# ---------------------------------------------------------------------
# QUESTION 5
# ---------------------------------------------------------------------


def labs_overall(process_labs):
    
    num_labs = process_labs.shape[1]
    total_labs = process_labs.sum(axis=1)
    if (num_labs <= 1):
        return total_labs
    lowest = process_labs.min(axis=1)
    
    return (total_labs - lowest) / (num_labs - 1)



# ---------------------------------------------------------------------
# QUESTION 6
# ---------------------------------------------------------------------


def total_points(grades):
    def calculate_score(grades, syllabus_list):
        if len(syllabus_list) == 0:
            return pd.Series(0.0, index=grades.index)

        scores = []

        for syllabus in syllabus_list:
            max_score = f'{syllabus} - Max Points'
            normalize = grades[syllabus].fillna(0) / grades[max_score]
            scores.append(normalize)

        return pd.concat(scores, axis=1).mean(axis=1)

    assignment_names = get_assignment_names(grades)
    labs_score = labs_overall(process_labs(grades)) * 0.20
    projects_score = projects_overall(grades) * 0.30
    checkpoints_score = calculate_score(grades, assignment_names['checkpoint']) * 0.025
    discussions_score = calculate_score(grades, assignment_names['disc']) * 0.025
    midterm_score = calculate_score(grades, assignment_names['midterm']) * 0.15
    final_score = calculate_score(grades, assignment_names['final']) * 0.30

    return (labs_score + projects_score + checkpoints_score 
            + discussions_score + midterm_score + final_score)



# ---------------------------------------------------------------------
# QUESTION 7
# ---------------------------------------------------------------------


def final_grades(total):
    def change_grade_to_letter(grade):
        if grade >= 0.9:
            return 'A'
        elif grade >= 0.8:
            return 'B'
        elif grade >= 0.7:
            return 'C'
        elif grade >= 0.6:
            return 'D'
        else:
            return 'F'
    return total.apply(change_grade_to_letter)

def letter_proportions(grades):
    letters = final_grades(grades)
    props = letters.value_counts(normalize=True)
    return props.sort_values(ascending=False)


# ---------------------------------------------------------------------
# QUESTION 8
# ---------------------------------------------------------------------


def raw_redemption(final_breakdown, redemption_q):
    
    redeem = final_breakdown.iloc[:, redemption_q]

    earned = redeem.fillna(0).sum(axis=1)
    possible = redeem.max().sum()

    return pd.DataFrame({
        "PID": final_breakdown["PID"],
        "Raw Redemption Score": earned / possible
    })

    
def combine_grades(grades,redemption_scores):
    return grades.merge(redemption_scores, on='PID', how='left')


# ---------------------------------------------------------------------
# QUESTION 9
# ---------------------------------------------------------------------


def z_score(ser):
    mean = ser.mean()
    std = ser.std(ddof=0)

    return (ser - mean) / std
    
def add_post_redemption(grades_combined):
    out = grades_combined.copy()

    pre = out["Midterm"].copy()
    pre_filled = pre.fillna(0)
    out["Midterm Score Pre-Redemption"] = pre_filled

    z_mid = z_score(pre_filled)
    z_red = z_score(out["Raw Redemption Score"])   # should have no nans

    mid_mean = pre_filled.mean()
    mid_sd = pre_filled.std(ddof=0)

    proposed = z_red * mid_sd + mid_mean

    post = pre_filled.where(z_red <= z_mid, proposed)

    # need to cap the score here between 0-1
    post = post.clip(lower=0, upper=1)

    out["Midterm Score Post-Redemption"] = post

    return out


# ---------------------------------------------------------------------
# QUESTION 10
# ---------------------------------------------------------------------


def total_points_post_redemption(grades_combined):
    total_pre = total_points(grades_combined)
    with_mid = add_post_redemption(grades_combined)

    MIDTERM_OUT_OF = 47 

    mid_pre_prop = (with_mid['Midterm Score Pre-Redemption'] / MIDTERM_OUT_OF).clip(0, 1)
    redeem_prop = with_mid['Raw Redemption Score'].clip(0, 1)

    mid_effective = np.maximum(mid_pre_prop, redeem_prop)

    total_post = total_pre - 0.15 * mid_pre_prop + 0.15 * mid_effective
    return total_post.clip(0, 1)
        
def proportion_improved(grades_combined):
    pre = final_grades(total_points(grades_combined))
    post = final_grades(total_points_post_redemption(grades_combined))

    order = {"F": 0, "D": 1, "C": 2, "B": 3, "A": 4}
    return (post.map(order) > pre.map(order)).mean()


# ---------------------------------------------------------------------
# QUESTION 11
# ---------------------------------------------------------------------


def section_most_improved(grades_analysis):
    order = {"F": 0, "D": 1, "C": 2, "B": 3, "A": 4}

    pre = grades_analysis["Letter Grade Pre-Redemption"]
    post = grades_analysis["Letter Grade Post-Redemption"]

    improved = post.map(order) > pre.map(order)

    props = improved.groupby(grades_analysis["Section"]).mean()

    return props.idxmax()

    
def top_sections(grades_analysis, t, n):
    cols = list(grades_analysis.columns)
    lower = {c: c.lower() for c in cols}

    final_col = None
    for c in cols:
        name = lower[c]
        if "final" in name and "raw" in name:
            final_col = c
            break

    if final_col is None:
        for c in cols:
            if "final" in lower[c]:
                final_col = c
                break

    if final_col is None:
        raise KeyError("Couldn't find a final exam score column in grades_analysis.")

    good = grades_analysis[final_col] >= t
    counts = good.groupby(grades_analysis["Section"]).sum()

    return np.array(sorted(counts[counts >= n].index))


# ---------------------------------------------------------------------
# QUESTION 12
# ---------------------------------------------------------------------


def rank_by_section(grades_analysis):
    total_col = [c for c in grades_analysis.columns
                 if "total" in c.lower() and ("post" in c.lower() or "redemption" in c.lower())][0]

    ranked = (grades_analysis[["PID", "Section", total_col]]
              .sort_values(["Section", total_col, "PID"], ascending=[True, False, True])
              .assign(**{"Section Rank": lambda df: df.groupby("Section").cumcount() + 1}))

    out = ranked.pivot_table(index="Section Rank",
                             columns="Section",
                             values="PID",
                             aggfunc="first")

    n = grades_analysis["Section"].value_counts().max()
    cols = [f"A{str(i).zfill(2)}" for i in range(1, 31)]

    return (out.reindex(index=range(1, n + 1), columns=cols)
               .fillna(""))



# ---------------------------------------------------------------------
# QUESTION 13
# ---------------------------------------------------------------------


def letter_grade_heat_map(grades_analysis):

    grade_col = [c for c in grades_analysis.columns
                 if "letter" in c.lower() and ("post" in c.lower() or "redemption" in c.lower())][0]

    props = (grades_analysis.groupby("Section")[grade_col]
             .value_counts(normalize=True)
             .rename("proportion")
             .reset_index())

    heat = props.pivot(index=grade_col, columns="Section", values="proportion")

    rows = ["A", "B", "C", "D", "F"]
    cols = [f"A{str(i).zfill(2)}" for i in range(1, 31)]
    heat = heat.reindex(index=rows, columns=cols).fillna(0)

    fig = px.imshow(
        heat,
        color_continuous_scale="Blues", 
        aspect="auto",
        labels=dict(x="Section", y="Letter Grade", color="Proportion"),
        title="Distribution of Letter Grades by Section"
    )
    return fig
