import numpy as np


# Control chart constants for subgroup size n = 5
A2 = 0.577
D3 = 0
D4 = 2.114

def validate_measurements(measurements):
    if not measurements:
        raise ValueError("Measurements cannot be empty.")

    if any(len(subgroup) == 0 for subgroup in measurements):
        raise ValueError("Subgroups cannot be empty.")

    subgroup_sizes = {len(subgroup) for subgroup in measurements}

    if len(subgroup_sizes) != 1:
        raise ValueError("All subgroups must contain the same number of measurements.")

    if len(subgroup_sizes) != 1 or list(subgroup_sizes)[0] != 5:
        raise ValueError("Currently, subgroup size must be 5.")


def calculate_subgroup_statistics(measurements):
    validate_measurements(measurements)

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
    validate_measurements(measurements)

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
def detect_out_of_control(measurements):
    validate_measurements(measurements)

    subgroup_stats = calculate_subgroup_statistics(measurements)
    limits = calculate_control_limits(measurements)

    x_ucl = limits["x_bar"]["ucl"]
    x_lcl = limits["x_bar"]["lcl"]

    r_ucl = limits["range"]["ucl"]
    r_lcl = limits["range"]["lcl"]

    results = []

    for subgroup in subgroup_stats:
        mean = subgroup["mean"]
        subgroup_range = subgroup["range"]

        x_bar_status = "in_control"
        r_status = "in_control"

        if mean > x_ucl or mean < x_lcl:
            x_bar_status = "out_of_control"

        if subgroup_range > r_ucl or subgroup_range < r_lcl:
            r_status = "out_of_control"

        overall_status = "in_control"

        if x_bar_status == "out_of_control" or r_status == "out_of_control":
            overall_status = "out_of_control"

        results.append({
            "subgroup": subgroup["subgroup"],
            "mean": mean,
            "range": subgroup_range,
            "x_bar_status": x_bar_status,
            "range_status": r_status,
            "overall_status": overall_status
        })

    return results
def calculate_process_capability(measurements, usl, lsl):
    validate_measurements(measurements)

    if usl <= lsl:
        raise ValueError("USL must be greater than LSL.")

    # existing code...
    """
    Calculate Cp and Cpk for a manufacturing process.

    usl = Upper Specification Limit
    lsl = Lower Specification Limit
    """

    values = np.array(
        [value for subgroup in measurements for value in subgroup],
        dtype=float
    )

    mean = np.mean(values)
    std_dev = np.std(values, ddof=1)
    if std_dev == 0:
        raise ValueError("Standard deviation must be greater than zero.")

    cp = (usl - lsl) / (6 * std_dev)

    cpu = (usl - mean) / (3 * std_dev)
    cpl = (mean - lsl) / (3 * std_dev)

    cpk = min(cpu, cpl)

    return {
        "mean": round(float(mean), 4),
        "standard_deviation": round(float(std_dev), 4),
        "usl": usl,
        "lsl": lsl,
        "cp": round(float(cp), 4),
        "cpu": round(float(cpu), 4),
        "cpl": round(float(cpl), 4),
        "cpk": round(float(cpk), 4)
    }