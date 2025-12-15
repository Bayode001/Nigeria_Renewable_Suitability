"""
AHP / MCDA Weight Definitions
----------------------------
Centralized weight management for renewable energy suitability analysis.
"""

from analysis.utils_raster import log_step


def normalize_weights(weights: dict) -> dict:
    """
    Normalize weights so they sum to 1.
    """
    total = sum(weights.values())

    if total == 0:
        raise ValueError("Total weight cannot be zero")

    return {k: v / total for k, v in weights.items()}


def validate_weights(weights: dict):
    """
    Ensure weights are valid.
    """
    if not isinstance(weights, dict):
        raise TypeError("Weights must be a dictionary")

    for k, v in weights.items():
        if v < 0:
            raise ValueError(f"Negative weight detected: {k}")


# ==========================
# SOLAR WEIGHTS
# ==========================

SOLAR_WEIGHTS_RAW = {
    "ghi": 0.35,
    "slope": 0.20,
    "landcover": 0.15,
    "distance_to_grid": 0.20,
    "distance_to_roads": 0.10,
}

validate_weights(SOLAR_WEIGHTS_RAW)
SOLAR_WEIGHTS = normalize_weights(SOLAR_WEIGHTS_RAW)


# ==========================
# WIND WEIGHTS
# ==========================

WIND_WEIGHTS_RAW = {
    "wind_speed": 0.40,
    "slope": 0.15,
    "landcover": 0.15,
    "distance_to_grid": 0.20,
    "distance_to_settlements": 0.10,
}

validate_weights(WIND_WEIGHTS_RAW)
WIND_WEIGHTS = normalize_weights(WIND_WEIGHTS_RAW)


# ==========================
# HYDRO WEIGHTS
# ==========================

HYDRO_WEIGHTS_RAW = {
    "flow_accumulation": 0.40,
    "slope": 0.20,
    "stream_order": 0.20,
    "distance_to_demand": 0.10,
    "protected_areas": 0.10,
}

validate_weights(HYDRO_WEIGHTS_RAW)
HYDRO_WEIGHTS = normalize_weights(HYDRO_WEIGHTS_RAW)


def print_weights():
    log_step("Solar Weights")
    for k, v in SOLAR_WEIGHTS.items():
        print(f"  {k}: {v:.3f}")

    log_step("Wind Weights")
    for k, v in WIND_WEIGHTS.items():
        print(f"  {k}: {v:.3f}")

    log_step("Hydro Weights")
    for k, v in HYDRO_WEIGHTS.items():
        print(f"  {k}: {v:.3f}")
