import json
from typing import Union
from fastapi.responses import HTMLResponse
from fastapi import FastAPI, Request, BackgroundTasks, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from schemas import TaskResponse, TranslationStatus, TranslationPost
from fastapi.middleware.cors import CORSMiddleware
from translation import Translation
from sqlalchemy.orm import Session
import sys
import asyncio
import uvicorn
from db import getDB

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.mount("/static", StaticFiles(directory="static"), name="static")


templates = Jinja2Templates(directory="templates")


@app.get('/', response_class=HTMLResponse)
def index(req: Request):
    return templates.TemplateResponse(req, "index.html", )


@app.post('/translate', response_model=TaskResponse)
def translate(req: TranslationPost, background_tasks: BackgroundTasks, db_session: Session = Depends(getDB)):

    try:
        translation = Translation(db_session, json.loads(req.json()))
        saved_translation = translation.save_translation()

        background_tasks.add_task(translation.translate,
                                  saved_translation.id,
                                  saved_translation.text,
                                  saved_translation.languages)

        return {"task_id": saved_translation.id}

    except:

        return {"message": "Something went wrong."}, 500


@app.get('/translate/{task_id}', response_model=Union[TranslationStatus, object])
def translate(task_id: Union[str, int], db_session: Session = Depends(getDB)):

    try:
        translation = Translation(db_session, {"task_id": task_id})
        res = translation.get_translation()

        if res is None:
            return {}
        return {"task_id": res.id, 'text': res.text, 'status': res.status, 'translation': res.translation}

    except:
        return HTMLResponse(content={"message": "Something went wrong."}, status_code=500)


if sys.platform == "win32" and (3, 8, 0) <= sys.version_info < (3, 9, 0):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


if __name__ == "__main__":
    uvicorn.run(app, port=8080, host="127.0.0.1")
