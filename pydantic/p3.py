from pydantic import BaseModel

class Adress(BaseModel):
    city:str
    country:str
    pin_code:int

class Patient(BaseModel):
    name:str
    gender:str
    Adress:Adress
Adress_info = {"city":"karachi", "country":"pakistan","pin_code":75800}
Adress1 = Adress(**Adress_info)

patient_info = {"name":"abc", "gender":"male","Adress":Adress1}
patient1 = Patient(**patient_info)

temp = patient1.model_dump()
print(type(temp))

temp1 = patient1.model_dump_json()
print(type(temp1))

# print(patient1)
# print(patient1.Adress.pin_code)