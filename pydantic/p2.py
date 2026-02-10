from pydantic import BaseModel, Field,field_validator,model_validator, computed_field
from typing import List, Dict, Annotated,Optional
class Patient(BaseModel):
    name:str
    age:int=Field(gt=0, lt=120)
    weight:float=Field(gt=0, lt=120)
    height:Annotated[float,Field(gt=0, lt=120)]
    marriage:Optional[bool]=None
    allergies:List[str]
    contact:Dict[str, str]

    @field_validator("name")
    @classmethod
    def transform_name(cls, value):
        return value.upper()
    
    @field_validator("age", mode="after")
    @classmethod
    def check_value(cls, value):
        if 0<value<100:
            return value
        raise ValueError("age value should be greater than zero")
    
    @model_validator(mode="after")
    @classmethod
    def pateint_check(cls, model):
        if model.age>60 and "emergency" not in model.contact:
            raise ValueError("emergency contact not in our model")
        return model
    
    @computed_field
    @property
    def cal_bmi(self)->float:
        bmi = round((self.weight/self.height*2),2)
        return bmi
    


def insert_patient(patient:Patient):
    print(patient.name)
    print(patient.age)
    print(patient.weight)
    print(patient.height)
    print(patient.marriage)
    print(patient.allergies)
    print(patient.contact)
    print("BMI", patient.cal_bmi)
    
patient_info = {"name":"abc","age":50,"weight":76.,"height":5.6,"allergies":["poolen", "dust"], "contact":{"phone":"515461"}}

patient1 = Patient(**patient_info)
insert_patient(patient1)