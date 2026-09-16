from fastapi import FastAPI
from pydantic import BaseModel
from quality.statistics import (
    calculate_subgroup_statistics,
    calculate_control_limits,
    detect_out_of_control
)


app = FastAPI(
    title="Manufacturing Quality Management System"
)


class MeasurementRequest(BaseModel):
    measurements: list[list[float]]


@app.get("/")
def home():
    return {
        "message": "Manufacturing Quality Management System API",
        "status": "running"
    }


@app.post("/calculate")
def calculate(request: MeasurementRequest):
    results = calculate_subgroup_statistics(request.measurements)

@app.post("/control-limits")
def control_limits(request: MeasurementRequest):
    limits = calculate_control_limits(request.measurements)

    return {
        "control_limits": limits
    }

    return {
        "results": results
    }
@app.post("/detect-out-of-control")
def detect_control(request: MeasurementRequest):
    results = detect_out_of_control(request.measurements)

    return {
        "results": results
    }