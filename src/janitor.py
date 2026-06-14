import pandas as pd
from typing import Callable, Tuple
from dataclasses import dataclass

@dataclass
class CleanReport:
    """
    This class is primarily used by `clean_runner`.

    This class stores information about the dataset pre- and post-cleaning.
    """
    rows_remaining: int
    rows_removed: int
    examples: pd.DataFrame

    def out(self) -> None:
      print("\t========== Janitor ========== ")
      print(f"\t\tRows remaining\t: {self.rows_remaining}")
      print(f"\t\tRows removed\t: {self.rows_removed}")
      print(f"\t\tExamples (max 3)\t: {self.examples.T}")

def clean_runner(df: pd.DataFrame, func: Callable[[pd.DataFrame], pd.DataFrame]) -> Tuple[pd.DataFrame, CleanReport]:
    """
    This is a function wrapper that makes narrative discussions in the notebook easy.

    @params:
      - df :: the dataframe to be cleaned
      - func :: a callable that can take in `df` and return an augmented `df`.
      
    @returns:
      - An ordered pair. The first entry is the new `df` made by applying `func` on `df`.
        the second entry is a report of the data cleaning.


    @warning:
      This function ASSUMES that the callable `func` does not reset
      the indices of `df`. 
    
      Example: `df` has indices (1,2,3). `func(df)` removes index 2.
      The augmented version of `df` has indices (1,3). We do not fix
      the indices after cleaning.
    """

    cleaned_df: pd.DataFrame = func(df)
    
    rows_kept = len(cleaned_df)
    rows_removed = len(df) - rows_kept
    
    removed_indices = df.index.difference(cleaned_df.index)
    removed_rows = df.loc[removed_indices]
    
    report = CleanReport(
        rows_remaining=rows_kept,
        rows_removed=rows_removed,
        examples=removed_rows.head(3) 
    )

    # only after generating the report can we reset the indices
    cleaned_df = cleaned_df.reset_index(drop=True)
    
    return cleaned_df, report

def rem_fishers(df: pd.DataFrame) -> pd.DataFrame:
  return df[df["individual-taxon-canonical-name"] == "Lynx rufus"]

def rem_bad_gps(df: pd.DataFrame) -> pd.DataFrame:
   return df.dropna(subset=["location-long", "location-lat"])