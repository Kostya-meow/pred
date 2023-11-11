from fastapi import FastAPI, Body, Depends, HTTPException, status, File
from fastapi.security import OAuth2PasswordBearer

api_keys = [
    "akljnv13bvi2vfo0b0bw"
]  # This is encrypted in the database

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")  # use token authentication


def api_key_auth(api_key: str = Depends(oauth2_scheme)):
    if api_key not in api_keys:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Forbidden"
        )


app = FastAPI()


@app.get("/test", dependencies=[Depends(api_key_auth)])
def add_post() -> dict:
    return {
        "data": "You used a valid API key"
    }


@app.post('/predict', dependencies=[Depends(api_key_auth)])

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
