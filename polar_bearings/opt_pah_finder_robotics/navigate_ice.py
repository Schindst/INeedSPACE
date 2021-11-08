from typing import Tuple

import matplotlib.pyplot as plt
import pandas as pd

from polar_bearings.opt_pah_finder_robotics.potential_field_planning import (
    potential_field_planning,
)


def main(
    filepath: str = "ice_thickness_01-01-2020.csv",
    rescaling_factor: int = 2,
    grid_size: float = 0.1,
    robot_radius: float = 0.01,
):
    """Loads the ice thickness data and plans a route over safe ice."""
    df = pd.read_csv(filepath)
    df_rescaled = df.iloc[::rescaling_factor, :]

    gx, gy, sx, sy, ox, oy = process_data(df_rescaled)

    plt.grid(True)
    plt.axis("equal")

    # path generation
    _, _ = potential_field_planning(sx, sy, gx, gy, ox, oy, grid_size, robot_radius)

    plt.show()


def process_data(
    single_day_df: pd.DataFrame,
    safety_threshold: float = 1.0,
):
    """Rescales data, then provides the coordinates needed for the pathfinder."""
    sx, sy, gx, gy = find_start_end(single_day_df)

    single_day_df = single_day_df.fillna(safety_threshold)  # NaN values are land
    unsafe = single_day_df[single_day_df.sithick < safety_threshold]

    ox = unsafe.latitude.values.tolist()
    oy = unsafe.longitude.values.tolist()

    print(f"{len(ox)}/{len(single_day_df)} co-ordinates considered as dangerous ice.")
    return gx, gy, sx, sy, ox, oy


def find_closest(df, lat, lon):
    dist = (df["latitude"] - lat).abs() + (df["longitude"] - lon).abs()
    return df.loc[dist.idxmin()]


def find_start_end(df_rescaled: pd.DataFrame) -> Tuple[int, int, int, int]:
    """Finds start and end points of ulukhaktok and sachs harbour, then scales their coordinate values to the origin."""
    df_rescaled["longitude"] = df_rescaled.longitude
    df_rescaled["latitude"] = df_rescaled.latitude

    ulukhaktok_y, ulukhaktok_x = (
        70.74025296172513,
        -117.77122885607929,
    )
    sachs_y, sachs_x = 71.98715823380064, -125.24848194895534

    closest = find_closest(df_rescaled, ulukhaktok_y, ulukhaktok_x)
    sy, sx = closest["latitude"], closest["longitude"]

    closest = find_closest(df_rescaled, sachs_y, sachs_x)
    gy, gx = closest["latitude"], closest["longitude"]

    return sx, sy, gx, gy
