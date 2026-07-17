import numpy as np

from typing import Dict, Optional, Tuple
from dataclasses import dataclass

from sklearn.cluster import HDBSCAN


@dataclass
class ClusterReport:
    """Summarizes an HDBSCAN clustering run."""

    n_points: int
    n_clusters: int
    n_noise: int
    noise_frac: float
    cluster_sizes: Dict[int, int]

    def out(self) -> None:
        print("\t========== HDBSCAN Clustering ========== ")
        print(f"\t\tPoints clustered\t: {self.n_points}")
        print(f"\t\tClusters found\t\t: {self.n_clusters}")
        print(
            f"\t\tNoise fixes\t\t: {self.n_noise} "
            f"({100 * self.noise_frac:.1f}%)"
        )
        sizes = sorted(self.cluster_sizes.items())
        print(f"\t\tCluster sizes\t\t: {sizes}")


def hdbscan_cluster(
    X: np.ndarray,
    min_cluster_size: int = 300,
    min_samples: Optional[int] = 30,
    sample_size: Optional[int] = 20000,
    random_state: int = 0,
) -> Tuple[np.ndarray, np.ndarray, ClusterReport]:
    """
    Clusters observations with HDBSCAN to reveal dense behavioral modes.
    This is simply a wrapper for sklearn's HDBSCAN algorithm implementation.

    @params:
      - X :: an (n, d) array of features (standardized recommended)
      - min_cluster_size :: smallest group accepted as a cluster
      - min_samples :: conservativeness of the density estimate; higher
                       values push more points into noise
      - sample_size :: optional random subsample size for tractability
      - random_state :: seed for the subsample

    @returns:
      - A tuple (labels, used, ClusterReport): the cluster label per
        clustered row, the integer positions of the rows actually used
        (into the input `X`), and a summary report. Use `used` to align
        the labels back to the source frame for profiling.
    """
    X = np.asarray(X, dtype=float)
    n = len(X)

    if sample_size is not None and sample_size < n:
        rng = np.random.default_rng(random_state)
        used = np.sort(rng.choice(n, size=sample_size, replace=False))
    else:
        used = np.arange(n)

    model = HDBSCAN(
        min_cluster_size=min_cluster_size, min_samples=min_samples, copy=True
    )
    labels = model.fit_predict(X[used])

    clusters = [c for c in np.unique(labels) if c != -1]
    sizes = {int(c): int(np.sum(labels == c)) for c in clusters}
    n_noise = int(np.sum(labels == -1))

    report = ClusterReport(
        n_points=len(used),
        n_clusters=len(clusters),
        n_noise=n_noise,
        noise_frac=n_noise / len(used),
        cluster_sizes=sizes,
    )
    return labels, used, report
