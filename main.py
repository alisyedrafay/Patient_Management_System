from fastapi import FastAPI, HTTPException, Path, Query
from scalar_fastapi import get_scalar_api_reference
from fastapi.responses import JSONResponse
from pydantic import BaseModel,Field,computed_field, model_validator, field_validator
from typing import List, Dict, Annotated,Optional, Literal

import json

app = FastAPI()

class Patient(BaseModel):
    id:Annotated[str,Field(...,max_length=20, description="this field is for patient id",examples=["P001"])]
    name:Annotated[str,Field(...,max_length=120, description="this field is for patient id",examples=["rahul", "nitish"])]
    age:Annotated[int,Field(...,gt=0, lt=100, description="this field is for patient id")]
    city:Annotated[str, Field(...,max_length=120, description="this feild is for city")]
    height:Annotated[float, Field(...,gt=0, lt=120, description="this field is for patient height")]
    weight:Annotated[float, Field(...,gt=0, lt=120, description="this field is for patient weight")]
    gender:Annotated[Literal["male", "female", "others"], Field(...,description="This field is for Gender")]

    @computed_field
    @property
    def cal_bmi(self)->float:
        bmi = round(self.weight/(self.height**2),2)
        return bmi
        
    @computed_field
    @property
    def verdict(self)->str:

        if self.cal_bmi < 18.5:
            return "Underweight"
        elif self.cal_bmi < 25:
            return "Normal"
        elif self.cal_bmi < 30:
            return "Normal"
        else:
            return "Obese"


class UpdatePatient(BaseModel):
    name:Annotated[Optional[str],Field(default=None)]
    age:Annotated[Optional[int], Field(default=None, gt=0)]
    city:Annotated[Optional[str], Field(default=None)]
    height:Annotated[Optional[float], Field(default=None,gt=0)]
    weight:Annotated[Optional[float], Field(default=None, gt=0)]
    gender:Annotated[Optional[Literal["male", "female"]], Field(default=None)]




def load_data():
    with open("patient.json", "r") as f:
        data = json.load(f)
        return data
    
def save_data(data):
    with open("patient.json", "w") as f:
        json.dump(data,f)


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


@app.post("/create")
def create_patient(patient:Patient):
    data = load_data()
    if patient.id in data:
        raise HTTPException(status_code=400, detail="pateint id is already exist")
    data[patient.id] = patient.model_dump(exclude=["id"])

    save_data(data)
    return JSONResponse(status_code=201, content={"message":"patiene created sucesfully"})


@app.put('/edit/{patient_id}')
def update_patient(patient_id: str, patient_update: UpdatePatient):

    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail='Patient not found')
    
    existing_patient_info = data[patient_id]

    updated_patient_info = patient_update.model_dump(exclude_unset=True)

    for key, value in updated_patient_info.items():
        existing_patient_info[key] = value

    #existing_patient_info -> pydantic object -> updated bmi + verdict
    existing_patient_info['id'] = patient_id
    patient_pydandic_obj = Patient(**existing_patient_info)
    #-> pydantic object -> dict
    existing_patient_info = patient_pydandic_obj.model_dump(exclude='id')

    # add this dict to data
    data[patient_id] = existing_patient_info

    # save data
    save_data(data)

    return JSONResponse(status_code=200, content={'message':'patient updated'})
     





@app.get("/scalar")
def scalar():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title="Scalar"

    )