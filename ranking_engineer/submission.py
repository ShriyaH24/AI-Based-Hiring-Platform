# submission.py

import pandas as pd

def generate_submission(df):

    submission = df[[
        "candidate_id",
        "final_score"
    ]].copy()

    submission = submission.sort_values(
        by="final_score",
        ascending=False
    )

    submission.insert(
        0,
        "rank",
        range(1, len(submission)+1)
    )

    submission.to_csv(
        "submission.csv",
        index=False
    )

    print("\nsubmission.csv created successfully\n")

    print(submission.head())

    return submission