from fastapi  import FastAPI,Path,HTTPException,Query
import json
from pydantic import BaseModel,Field,computed_field
from typing import Annotated,Literal,Optional
from  fastapi.responses import JSONResponse

#app created here
app = FastAPI()

#pydantic model here
class Patient(BaseModel):
    id : Annotated[str,Field(...,description = "ID of the patient",examples=["P001"])]
    name : Annotated[str,Field(...,description = "Name of the patient")]
    city : Annotated[str,Field(...,description = "City where patient lives")]
    age : Annotated[int,Field(...,gt=0,lt=120,description = "Age of the patient")]
    gender : Annotated[Literal['male','female','others'],Field(...,description = "Gender of the patient")]
    height : Annotated[float,Field(...,gt=0 ,description = "Height of the patient in meters")]
    weight : Annotated[float,Field(...,gt=0 ,description="Weight of the patient in kgs")]

    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(self.weight/(self.height**2),2)
        return bmi
    
    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi <18.5:
            return "Under Weight"
        elif self.bmi < 25:
            return "Normal"
        elif self.bmi < 30:
            return "Over Weight"
        else:
            return "Obese"

class PatientUpdate(BaseModel):
    name : Annotated[Optional[str],Field(description = "Name of the patient",default = None)]
    city : Annotated[Optional[str],Field(description = "City where patient lives",default = None)]
    age : Annotated[Optional[int],Field(gt=0,lt=120,description = "Age of the patient",default = None)]
    gender : Annotated[Optional[Literal['male','female','others']],Field(description = "Gender of the patient",default = None)]
    height : Annotated[Optional[float],Field(gt=0 ,description = "Height of the patient in meters",default = None)]
    weight : Annotated[Optional[float],Field(gt=0 ,description="Weight of the patient in kgs",default = None)]
    
#utility funcs here    
def load_data():
    with open('patients.json','r') as f:
        data = json.load(f)
    return data

def save_data(data):
    with open('patients.json','w') as f:
        json.dumps(data,f)
        
#GET        
@app.get("/")
def hello():
    return {"message":"Welcome"}

@app.get("/view")
def view():
    data = load_data()
    return data

@app.get("/patient/{patient_id}")
def view_patient(patient_id:str = Path(...,description = 'ID of the patient from DB',example ='P001')):
    #load_all patients
    data = load_data()
    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code =404,detail = "patient not found")

@app.get("/sort")
def sort_patients(sort_by:str= Query(..., description = 'Sort on basis of height,weight and bmi'),order :str=Query('asc',description = 'Sort in ascending or descending order')):
    valid_fields =['height','weight','bmi']
    
    if sort_by not in valid_fields:
        raise HTTPException(status_code =400,detail = f'Invalid field select it from {valid_fields}')
    
    if order not in ['asc','desc']:
        raise HTTPException(status_code =400,detail = f'Invalid order select between asc or desc')
    
    data = load_data()
    
    sort_order = True if  order == 'desc' else False
    
    sorted_data = sorted(data.values() ,key = lambda x:x.get(sort_by,0),reverse = sort_order)
    
    return sorted_data

#POST
@app.post("/create")
def create_patient(patient: Patient):
    #load existing data
    data = load_data()
    #check if the patient is already exists in db
    if patient.id in data:
        raise HttpException(status_code = 400,detail = "Patient already exists")
    #else add to db
    data[patient.id] = patient.model_dump(exclude=['id'])
    #save to json
    save_data(data)
    return JSONResponse(status_code=201,content = {"message":"patient created successfully."})

#UPDATE- PUT
@app.put("/edit")
def update_patient(patient_id: str, patient_update:PatientUpdate):
    #load data
    data = load_data()
    #check if patient id exists
    if patient_id not in data:
        raise HTTPException(status_code = 404,detail = "Pateint ID not found")
    old_data = data[patient_id]
    new_data =patient_update.model_dump(exclude_unset = True)
    for key,val in new_data.items():
        old_data[key] = val
    #convert old data now to calculate bmi n verdict by converting it into pydantic model - as the model wil recalculate
    old_data['id'] = patient_id
    patient_pydantic_object = Patient(**old_data)
    old_data = patient_pydantic_object.model_dump(exclude = 'id')
    data[patient_id] = old_data
    save_data(data) 
    return JSONResponse(status_code = 200,content = {"message":"Pateint new data updated"})

#DELETE
@app.delete("/delete/{patient_id}")
def delete_patient(patient_id:str):
    data = load_data()
    if patient_id not in data:
        raise HTTPException(status_code =404,detail = "Patient not found")
    
    del data[patient_id]
    save_data(data)
    return JSONResponse(status_code=200,content = {"message":"Patient id deleted successfully"})