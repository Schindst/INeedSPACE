from typing import Tuple

import matplotlib.pyplot as plt
import pandas as pd
from potential_field_planning import potential_field_planning


def main(
    filepath: str = "ice_thickness_01-01-2020.csv",
    rescaling_factor: int = 2,
    grid_size: float = 0.1,
    robot_radius: float = 0.01,
):
    """Loads the ice thickness data and plans a route over safe ice."""

    gx, gy, sx, sy, ox, oy = process_data(filepath, rescaling_factor)

    plt.grid(True)
    plt.axis("equal")

    # path generation
    _, _ = potential_field_planning(sx, sy, gx, gy, ox, oy, grid_size, robot_radius)

    plt.show()


def process_data(
    filepath: str = "ice_thickness_01-01-2020.csv",
    rescaling_factor: int = 2,
    safety_threshold: float = 1.0,
):
    """Rescales data, then provides the coordinates needed for the pathfinder."""
    df = pd.read_csv(filepath)
    df_rescaled = df.iloc[::rescaling_factor, :]
    sx, sy, gx, gy = find_start_end(df_rescaled)

    df_rescaled = df_rescaled.fillna(safety_threshold)  # NaN values are land
    unsafe = df_rescaled[df_rescaled.sithick < safety_threshold]

    ox = unsafe.latitude.values.tolist()
    oy = unsafe.longitude.values.tolist()

    return gx, gy, sx, sy, ox, oy


def find_closest(df, lat, lon):
    dist = (df["latitude"] - lat).abs() + (df["longitude"] - lon).abs()
    return df.loc[dist.idxmin()]


def find_start_end(df_rescaled: pd.DataFrame) -> Tuple[int, int, int, int]:
    """Finds start and end points of ulukhaktok and sachs harbour, then scales their coordinate values to the origin."""
    origin_x = min(df_rescaled.longitude)
    origin_y = min(df_rescaled.latitude)
    df_rescaled["longitude"] = df_rescaled.longitude - origin_x
    df_rescaled["latitude"] = df_rescaled.latitude - origin_y

    ulukhaktok_y, ulukhaktok_x = (
        70.74025296172513 - origin_y,
        -117.77122885607929 - origin_x,
    )
    sachs_y, sachs_x = 71.98715823380064 - origin_y, -125.24848194895534 - origin_x

    closest = find_closest(df_rescaled, ulukhaktok_y, ulukhaktok_x)
    sy, sx = closest["latitude"], closest["longitude"]

    closest = find_closest(df_rescaled, sachs_y, sachs_x)
    gy, gx = closest["latitude"], closest["longitude"]

    return sx, sy, gx, gy
