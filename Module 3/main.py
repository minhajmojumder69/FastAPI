from fastapi import FastAPI , Path ,HTTPException , Query,Body
import json

app = FastAPI()

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

    valid_fields =["age","class","roll","Math marks","English marks","Science marks",]
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
def create_student(student: dict = Body()):

    data = loaddata()
    student_id = student['id']
    data[student_id] = student
    del data[student_id]['id']
    savedata(data)