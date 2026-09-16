import numpy as np


# Control chart constants for subgroup size n = 5
A2 = 0.577
D3 = 0
D4 = 2.114


def calculate_subgroup_statistics(measurements):
    results = []

    for index, subgroup in enumerate(measurements, start=1):
        values = np.array(subgroup, dtype=float)

        subgroup_mean = np.mean(values)
        subgroup_range = np.max(values) - np.min(values)

        results.append({
            "subgroup": index,
            "mean": round(float(subgroup_mean), 4),
            "range": round(float(subgroup_range), 4)
        })

    return results


def calculate_control_limits(measurements):
    subgroup_stats = calculate_subgroup_statistics(measurements)

    means = [item["mean"] for item in subgroup_stats]
    ranges = [item["range"] for item in subgroup_stats]

    x_double_bar = np.mean(means)
    r_bar = np.mean(ranges)

    x_ucl = x_double_bar + A2 * r_bar
    x_lcl = x_double_bar - A2 * r_bar

    r_ucl = D4 * r_bar
    r_lcl = D3 * r_bar

    return {
        "x_bar": {
            "center_line": round(float(x_double_bar), 4),
            "ucl": round(float(x_ucl), 4),
            "lcl": round(float(x_lcl), 4)
        },
        "range": {
            "center_line": round(float(r_bar), 4),
            "ucl": round(float(r_ucl), 4),
            "lcl": round(float(r_lcl), 4)
        }
    }