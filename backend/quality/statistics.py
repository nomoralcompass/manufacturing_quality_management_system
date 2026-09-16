import numpy as np


def calculate_subgroup_statistics(measurements):
    """
    Calculate mean and range for each subgroup.

    measurements:
        List of subgroups.
        Example:
        [
            [20.01, 19.98, 20.02, 20.00, 20.01],
            [19.99, 20.03, 20.01, 20.00, 19.98]
        ]
    """

    results = []

    for index, subgroup in enumerate(measurements, start=1):
        values = np.array(subgroup, dtype=float)

        subgroup_mean = np.mean(values)
        subgroup_range = np.max(values) - np.min(values)

        results.append({
            "subgroup": index,
            "mean": subgroup_mean,
            "range": subgroup_range
        })

    return results