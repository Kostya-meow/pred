from fastapi import FastAPI, UploadFile, File, Form, Depends, HTTPException, status
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastai.vision.all import *
import shutil
import os

app = FastAPI()
templates = Jinja2Templates(directory="templates")

API_KEY = "your_api_key1"

def get_api_key(api_key: str = Form(...)):
    if api_key == API_KEY:
        return True
    else:
        raise HTTPException(status_code=403, detail="Invalid API Key")

@app.get('/')
async def main(request: Request):
    return templates.TemplateResponse('index.html', {'request': request, 'result': None})

@app.post('/classify')
async def classify(request: Request, file: UploadFile = File(...), api_key: str = Form(...), authorized: bool = Depends(get_api_key)):
    if not file:
        raise HTTPException(status_code=400, detail="File not found")
    temp_file = f"tempfile.{file.filename.split('.')[-1]}"
    with open(temp_file, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    learner = load_learner("app/model.pkl")
    result = learner.predict(temp_file)
    
    name_pred = str(result[1])
    name_pred = int(name_pred[name_pred.find('(')+1:name_pred.find(')')])
    perc_pred = str(result[2][name_pred])
    perc_pred = round(float(perc_pred[perc_pred.find('(')+1:perc_pred.find(')')]),2)
    
    if result[0] == 'бронза':
        tech = 'литье'
    elif result[0] == 'глина':
        tech = 'лепка'
    elif result[0] == 'железо':
        tech = 'ковка'
    elif result[0] == 'камень':
        tech = 'скалывание'
    elif result[0] == 'керамика':
        tech = 'лепка'
    elif result[0] == 'кость':
        tech = 'резьба'
    elif result[0] == 'медь':
        tech = 'литье'
    
    os.remove(temp_file)
    
    
    material = result[0]
    technique = tech
    probability = f"{round(perc_pred * 100, 0)}%"

    return templates.TemplateResponse('index.html', {'request': request, 'material': material, 'technique': technique, 'probability': probability})
