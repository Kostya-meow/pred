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
from fastapi import FastAPI, Body, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer


plt = platform.system()
if plt == 'Linux': pathlib.WindowsPath = pathlib.PosixPath



app = FastAPI()


@app.post('/predict')

async def root(file: bytes = File()):

    learner = load_learner("app/model.pkl")

    result = list(learner.predict(file))
    name_pred = str(result[1])
    name_pred = int(name_pred[name_pred.find('(')+1:name_pred.find(')')])
    perc_pred = str(result[2][name_pred])
    perc_pred = round(float(perc_pred[perc_pred.find('(')+1:perc_pred.find(')')]),2)

    if result[0] == 'бронза':
        tech = 'литье'
    elif result[0] == 'глина':
        tech = 'лепка'
    elif result[0] == 'железо':
        tech = 'ловка'
    elif result[0] == 'камень':
        tech = 'скалывание'
    elif result[0] == 'керамика':
        tech = 'лепка'
    elif result[0] == 'кость':
        tech = 'лезьба'
    elif result[0] == 'медь':
        tech = 'литье'

    return {
        "confidence": perc_pred,
        "medium": result[0],
        "tech": tech
        }

