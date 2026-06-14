import numpy as np

def haversine_m(lat1, lon1, lat2, lon2):
    """Great-circle distance in metres between consecutive fixes."""
    R = 6_371_000.0
    p1, p2 = np.radians(lat1), np.radians(lat2)
    dphi   = np.radians(lat2 - lat1)
    dlmb   = np.radians(lon2 - lon1)
    a = np.sin(dphi / 2) ** 2 + np.cos(p1) * np.cos(p2) * np.sin(dlmb / 2) ** 2
    return 2 * R * np.arcsin(np.sqrt(a))