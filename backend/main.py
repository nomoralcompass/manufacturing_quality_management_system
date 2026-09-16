from fastapi import FastAPI
from pydantic import BaseModel
from quality.statistics import (
    calculate_subgroup_statistics,
    calculate_control_limits
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