from pydantic import BaseModel, Field
from typing import List, Dict, Annotated,Optional
class Patient(BaseModel):
    name:str=Field(max_length=50, examples=["henry", "potter"])
    age:int=Field(gt=0, lt=120)
    weight:float=Field(gt=0, lt=120)
    height:Annotated[float,Field(gt=0, lt=120)]
    marriage:Optional[bool]=None
    allergies:List[str]
    contact:Dict[str, str]


def insert_patient(patient:Patient):
    print(patient.name)
    print(patient.age)
    print(patient.weight)
    print(patient.height)
    print(patient.marriage)
    print(patient.allergies)
    print(patient.contact)
    
patient_info = {"name":"abc","age":22,"weight":76.,"height":5.6,"allergies":["poolen", "dust"], "contact":{"phone":"515461"}}

patient1 = Patient(**patient_info)
insert_patient(patient1)