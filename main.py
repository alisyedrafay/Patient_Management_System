from fastapi import FastAPI, HTTPException, Path, Query
from scalar_fastapi import get_scalar_api_reference
import json
app = FastAPI()

def load_data():
    with open("patient.json", "r") as f:
        data = json.load(f)
        return data

@app.get("/")
def home():
    return {"message":"Patient Management System"}

@app.get("/about")
def about():
    return {"message":"This is first api end point"}


@app.get("/view")
def view():
    data = load_data()
    return data

@app.get("/patient/{patient_id}")
def show_patient_id(patient_id:str=Path(...,description="this end point is for pateints id", example="P001")):

    data = load_data()
    if patient_id in data:
        return data[patient_id]
    else:
        raise HTTPException(status_code=404, detail="patient not found")

@app.get("/sort")
def sort_view(sort_by:str=Query(...,description="sort on the basis of height, weight, bmi"), order_by:str=Query("asc",description="sort on the basis of asc and desc")):
    valid_fields = ["height","weight", "bmi"]
    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail=f"invalid fields{valid_fields}")
    if order_by not in ["asc", "desc"]:
        raise HTTPException(status_code=400, detail="not sort")
    data = load_data()
    sort_order = True if order_by=="desc" else False
    sorted_data = sorted(data.values(),key=lambda x:x.get(sort_by,0),reverse=sort_order)
    return sorted_data




@app.get("/scalar")
def scalar():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title="Scalar"

    )