from typing import List
import pandas as pd

"""
This constant stores all the column names we need to keep.

This also stores columns that are not as important (or used in 
inference) but will help us make sense of the dataset in the EDA.
"""


def reduce(df: pd.DataFrame, cols: List[str]) -> pd.DataFrame:
    """
    Reduces the dimension of the dataset by only keeping important
    columns.

    @params:
      - df :: the (preprocessed) dataframe to prune
      - cols :: a list of strings that defines the columns to keep in
                `df`.

    @returns:
      - The reduced `df` which only contains columns in `cols`.
    """
    present = [c for c in cols if c in df.columns]
    return df[present]
