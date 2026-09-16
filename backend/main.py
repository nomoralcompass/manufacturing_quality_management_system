from fastapi import FastAPI
from pydantic import BaseModel
from quality.statistics import (
    calculate_subgroup_statistics,
    calculate_control_limits,
    detect_out_of_control,
    calculate_process_capability
)
class CapabilityRequest(BaseModel):
    measurements: list[list[float]]
    usl: float
    lsl: float

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
@app.post("/process-capability")
def process_capability(request: CapabilityRequest):
    result = calculate_process_capability(
        request.measurements,
        request.usl,
        request.lsl
    )

    return {
        "process_capability": result
    }