import pandas as pd
from typing import Callable, Tuple
from dataclasses import dataclass


@dataclass
class CleanReport:
    """
    This class is primarily used by `clean_runner`.

    This class stores information about the dataset pre- and post-cleaning.
    """

    rows_before: int
    rows_remaining: int
    rows_removed: int
    examples: pd.DataFrame

    def out(self) -> None:
        print("\t========== Janitor ========== ")
        print(f"\t\tRows before\t\t: {self.rows_before}")
        print(f"\t\tRows remaining\t\t: {self.rows_remaining}")
        print(f"\t\tRows removed\t\t: {self.rows_removed}")
        print(f"\t\tExamples (max 3)\t: {self.examples.T}")


def clean_runner(
    df: pd.DataFrame, func: Callable[[pd.DataFrame], pd.DataFrame]
) -> Tuple[pd.DataFrame, CleanReport]:
    """
    This is a function wrapper that makes narrative discussions in the notebook easy.

    @params:
      - df :: the dataframe to be cleaned
      - func :: a callable that can take in `df` and return an augmented `df`.

    @returns:
      - An ordered pair. The first entry is the new `df` made by applying `func` on `df`.
        the second entry is a report...
    """
    before = len(df)
    after_df = func(df)
    after = len(after_df)
    removed = before - after
    
    report = CleanReport(
        rows_before=before,
        rows_remaining=after,
        rows_removed=removed,
        examples=after_df.head(3) if after > 0 else pd.DataFrame()
    )
    return after_df, report


def rem_with_markers(df: pd.DataFrame) -> pd.DataFrame:
    """
    The dataset has the following flags which can guide data cleaning:
    - "visible"
    - "import-marked-outlier"
    - "manually-marked-outlier"
    """
    if "visible" in df.columns:
        df = df[df["visible"] == True]
    if "import-marked-outlier" in df.columns:
        df = df[df["import-marked-outlier"] == False]
    if "manually-marked-outlier" in df.columns:
        mmo = df["manually-marked-outlier"].astype("string").str.strip().str.lower()
        df = df[~mmo.isin(["true", "1", "yes"])]
    return df


def rem_bad_fix(df: pd.DataFrame) -> pd.DataFrame:
    if "eobs:type-of-fix" in df.columns:
        df = df[df["eobs:type-of-fix"] == 3]
    return df


def rem_outside_deploy(df: pd.DataFrame) -> pd.DataFrame:
    """
    @warning:
    Assumes `add_utc_time` from `transformer.py` is applied on the input
    `df`.
    """
    if "timestamp-utc" not in df.columns:
        # Fallback in case transformer hasn't renamed the column yet
        ts = pd.to_datetime(df["timestamp"], utc=True, errors="coerce")
    else:
        ts = df["timestamp-utc"]
        
    don = pd.to_datetime(df["deploy-on-date"], utc=True, errors="coerce")
    doff = pd.to_datetime(df["deploy-off-date"], utc=True, errors="coerce")
    
    # Keep rows where timestamp is >= deploy-on AND (<= deploy-off OR deploy-off is missing)
    mask = (ts >= don) & ((ts <= doff) | doff.isna())
    return df[mask]


def keep_only_bobcats(df: pd.DataFrame) -> pd.DataFrame:
    """Filters the dataset to only include Lynx rufus records."""
    if "animal-taxon" in df.columns:
        df = df[df["animal-taxon"] == "Lynx rufus"]
    return df

def drop_dupes_and_nulls(df: pd.DataFrame) -> pd.DataFrame:
    """Removes duplicate GPS fixes (same animal, same instant) and drops critical missing values."""
    # Drop duplicate fixes: same animal at the same timestamp
    df = df.drop_duplicates(subset=["animal-id", "timestamp-utc"])
    
    # Drop rows where critical movement or spatial data is missing
    critical_cols = ['location-lat', 'location-long', 'ground-speed']
    existing_critical = [c for c in critical_cols if c in df.columns]
    df = df.dropna(subset=existing_critical)
    
    return df

def drop_invalid_movement(df: pd.DataFrame) -> pd.DataFrame:
    """Removes rows where step-distance couldn't be computed (first fix per animal)."""
    if "step-meters" in df.columns:
        df = df.dropna(subset=["step-meters"])
    return df