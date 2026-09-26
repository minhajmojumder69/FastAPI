from fastapi import FastAPI , Path ,HTTPException
import json

app = FastAPI()

def loaddata():
    with open('studentsl.json','r') as f:
        data = json.load(f)
        return data

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