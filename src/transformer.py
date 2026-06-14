import pandas as pd
import numpy as np

from typing import Callable, Tuple, Optional, List
from dataclasses import dataclass
import pandas as pd


@dataclass
class TransformReport:
    """
    See documentation for CleanReport in `janitor.py`.
    """

    added_cols: List[str]
    before: pd.DataFrame
    after: pd.DataFrame

    def out(self) -> None:
        print("\t========== Transformer ========== ")
        print(f"\t\tAdded columns\t: {self.added_cols}")
        print(f"\t\tBefore (max 3)\t:\n{self.before.head(3).T}")
        print(f"\t\tAfter  (max 3)\t:\n{self.after.head(3).T}")


def transform_runner(
    df: pd.DataFrame,
    func: Callable[[pd.DataFrame], pd.DataFrame],
    source_cols: Optional[List[str]] = None,
    key: str = "event-id",
) -> Tuple[pd.DataFrame, TransformReport]:
    """
    The transform-step counterpart to `clean_runner`. Applies an `add_*`
    callable and builds a focused before/after report (no row counts).

    @params:
      - df :: the dataframe to transform
      - func :: a callable that can take in `df` and return an augmented `df`.
      - source_cols :: existing columns the new ones derive from; shown as the
                       "before" context (optional)
      - key :: stable row id used to align before/after even if `func`
               re-sorts the frame (default "event-id")

    @returns:
      - An ordered pair: the transformed `df`, and a TransformReport.
    """
    after = func(df)
    new_cols = [c for c in after.columns if c not in df.columns]
    src = [c for c in (source_cols or []) if c in df.columns]

    after_head = after.head(3)
    if key in df.columns and key in after.columns:
        sel = df[df[key].isin(after_head[key])]
    else:
        sel = df.head(3)

    before = sel[[c for c in ([key] + src) if c in sel.columns]]
    after_view = after_head[
        [c for c in ([key] + src + new_cols) if c in after_head.columns]
    ]

    report = TransformReport(added_cols=new_cols, before=before, after=after_view)
    return after, report


def _helper_season_from_month(month: int) -> str:
    """Meteorological seasons (northern hemisphere)."""
    return {
        12: "winter",
        1: "winter",
        2: "winter",
        3: "spring",
        4: "spring",
        5: "spring",
        6: "summer",
        7: "summer",
        8: "summer",
        9: "fall",
        10: "fall",
        11: "fall",
    }.get(month)


def _helper_haversine_m(lat1, lon1, lat2, lon2):
    R = 6_371_000.0
    p1, p2 = np.radians(lat1), np.radians(lat2)
    dphi = np.radians(lat2 - lat1)
    dlmb = np.radians(lon2 - lon1)
    a = np.sin(dphi / 2) ** 2 + np.cos(p1) * np.cos(p2) * np.sin(dlmb / 2) ** 2
    return 2 * R * np.arcsin(np.sqrt(a))


def add_local_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    local = df["timestamp-utc"].dt.tz_convert("America/New_York")
    df["timestamp-local"] = local
    df["hour-local"] = local.dt.hour
    df["date-local"] = local.dt.date
    df["month-local"] = local.dt.month
    df["season"] = df["month-local"].map(_helper_season_from_month)
    return df


def add_utc_time(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["timestamp-utc"] = pd.to_datetime(df["timestamp"], utc=True, errors="coerce")
    return df


def add_movement(df: pd.DataFrame) -> pd.DataFrame:
    df = df.sort_values(["animal-id", "timestamp-utc"]).reset_index(drop=True)
    g = df.groupby("animal-id", group_keys=False)
    df["dt-seconds"] = g["timestamp-utc"].diff().dt.total_seconds()
    prev_lat = g["location-lat"].shift(1)
    prev_lon = g["location-long"].shift(1)
    df["step-meters"] = _helper_haversine_m(
        prev_lat, prev_lon, df["location-lat"], df["location-long"]
    )
    df["derived-speed-ms"] = (df["step-meters"] / df["dt-seconds"]).where(
        df["dt-seconds"] > 0
    )
    return df
