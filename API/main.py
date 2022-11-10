from fastapi import FastAPI,Query,Body
from requests import get
from typing import Union,Dict

app = FastAPI()

@app.post("/",tags=['Telegram API'])
async def API(
    method,
    token:str=Query(None,max_lenght=46,min_leght=46),
    params:dict=Body(...,embed=False)
    ):
    params = dict(params)
    url = f'https://api.telegram.org/bot{token}/{method}'
    if params:
        url += str('?'+''.join([str(i)+'='+str(params[i])+'&' for i in params]))[:-1:]
    return get(url).json()