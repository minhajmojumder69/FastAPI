from fastapi import FastAPI , Path ,HTTPException , Query,Body
from pydantic import BaseModel, Field
from typing import Annotated

import json
from fastapi.responses import JSONResponse

app = FastAPI()

class Student(BaseModel):
    id: Annotated[str,Field(..., description='Student ID',example='S001')]
    name: Annotated[str,Field(..., description='Student Name')]
    age : Annotated[int,Field(..., gt=3,lt=20)]
    student_class: Annotated[int,Field(...,gt=0,lt=13)]
    roll: Annotated[int,Field(..., gt=0,lt=101)]
    Math_marks: Annotated[int,Field(...,gt=0,lt=101)]
    English_marks: Annotated[int,Field(...,gt=0,lt=101)]
    Science_marks: Annotated[int,Field(...,gt=0,lt=101)]
    phone: Annotated[int,Field(..., example='01900000000')]

def loaddata():
    with open('students.json','r') as f:
        data = json.load(f)
        return data

def savedata(data):
    with open('students.json','w') as f:
        json.dump(data,f)


@app.get('/')
def hello():
    return 'Student management System API'

@app.get('/about')
def about():
    return 'Fully functional API to manage SMS records'


@app.get('/view')
def view_students():
    data = loaddata()
    return data

@app.get('/view/{student_id}')
def view_student_by_id(student_id: str = Path(..., description='students by id',example='S001')):
    data = loaddata()
    if student_id in data:
        return data[student_id]
    else: 
        raise HTTPException(status_code=404, detail="Student not found..!!") 

    
@app.get('/sort')
def view_sorted_students(sorted_by: str = Query(..., description='sorted Student'),order: str = Query('asc')):

    valid_fields =["age","student_class","roll","Math_marks","English_marks","Science_marks",]
    if sorted_by not in valid_fields:
        raise HTTPException(status_code=404, detail= f"Invalid field, select from {valid_fields}")
    
    if order not in ['asc','desc']:
        raise HTTPException(status_code=404, detail= f"Choose asc or desc")

    data = loaddata()

    sort_order = True if order == 'desc' else False

    sorted_data = list(data.values())
    sorted_data.sort(key= lambda x: x[sorted_by], reverse=sort_order)

    return sorted_data


@app.post('/create')
def create_student(student: Student):

    data = loaddata()

    if student.id in data:
        raise HTTPException(status_code=400, detail= "Student id already exist..")
    
    data[student.id] = student.model_dump(exclude=["id"])
    # del data[student_id]['id']
    savedata(data)
    
    return JSONResponse(status_code= 201, content={'massage': 'Student created Successfully..'})