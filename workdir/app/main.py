from fastapi import FastAPI
from pydantic import BaseModel
import pickle
import pandas as pd
from fastai.vision.all import *
from fastapi import FastAPI, UploadFile, File, Body, Depends, HTTPException, status
import shutil
import os
from fastapi.security import OAuth2PasswordBearer
import pathlib
from fastapi.middleware.cors import CORSMiddleware


device = torch.device('cuda:0')
torch.cuda.set_device(0)

plt = platform.system()
if plt == 'Linux': pathlib.WindowsPath = pathlib.PosixPath


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post('/predict')

async def root(file: bytes = File()):

    learner = load_learner("app/model.pkl")

    result = list(learner.predict(file))
    name_pred = str(result[1])
    name_pred = int(name_pred[name_pred.find('(')+1:name_pred.find(')')])
    perc_pred = str(result[2][name_pred])
    perc_pred = round(float(perc_pred[perc_pred.find('(')+1:perc_pred.find(')')]),2)

    if result[0] == 'бронза':
        id_value = 3
    elif result[0] == 'глина':
        id_value = 11
    elif result[0] == 'железо':
        id_value = 9
    elif result[0] == 'камень':
        id_value = 1
    elif result[0] == 'керамика':
        id_value = 2
    elif result[0] == 'кость':
        id_value = 12
    elif result[0] == 'медь':
        id_value = 10

    return {
        "confidence":perc_pred,
        "medium": {
            "value": id_value,
            "label": result[0].title()
        }}

    
