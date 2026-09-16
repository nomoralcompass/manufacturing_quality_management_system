from fastapi import FastAPI, HTTPException
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
    try:
        results = calculate_subgroup_statistics(request.measurements)

        return {
            "results": results
        }

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

@app.post("/control-limits")
def control_limits(request: MeasurementRequest):
    try:
        limits = calculate_control_limits(request.measurements)

        return {
            "control_limits": limits
        }

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )
@app.post("/detect-out-of-control")
def detect_control(request: MeasurementRequest):
    try:
        results = detect_out_of_control(request.measurements)

        return {
            "results": results
        }

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )
@app.post("/process-capability")
def process_capability(request: CapabilityRequest):
    try:
        result = calculate_process_capability(
            request.measurements,
            request.usl,
            request.lsl
        )

        return {
            "process_capability": result
        }

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )