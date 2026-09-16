from fastapi import FastAPI, HTTPException, UploadFile, File
import pandas as pd
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
@app.post("/upload-csv")
async def upload_csv(file: UploadFile = File(...)):
    try:
        if not file.filename.endswith(".csv"):
            raise ValueError("Only CSV files are supported.")

        contents = await file.read()

        with open("temp.csv", "wb") as temp_file:
            temp_file.write(contents)

        data = pd.read_csv("temp.csv")

        if "measurement" not in data.columns:
            raise ValueError(
                "CSV must contain a 'measurement' column."
            )

        values = data["measurement"].dropna().tolist()

        if len(values) % 5 != 0:
            raise ValueError(
                "Number of measurements must be divisible by 5."
            )

        measurements = [
            values[i:i + 5]
            for i in range(0, len(values), 5)
        ]

        subgroup_results = calculate_subgroup_statistics(
            measurements
        )

        control_limits = calculate_control_limits(
            measurements
        )

        control_status = detect_out_of_control(
            measurements
        )

        return {
            "filename": file.filename,
            "total_measurements": len(values),
            "number_of_subgroups": len(measurements),
            "subgroup_results": subgroup_results,
            "control_limits": control_limits,
            "control_status": control_status
        }

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Failed to process CSV file."
        )