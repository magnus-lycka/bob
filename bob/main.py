
from os import getenv
import subprocess
import logging
import sys

from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel

from . import util

SITE_DIR = getenv("SITE_DIRECTORY")

file_handler = logging.FileHandler(filename=SITE_DIR + '/bob.log')
stdout_handler = logging.StreamHandler(sys.stdout)
handlers = [file_handler, stdout_handler]

logging.basicConfig(
    level=logging.INFO, 
    format='[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s',
    handlers=handlers
)
log = logging.getLogger()


app = FastAPI()


class Build(BaseModel):
    output: str
    error: str


def execute() -> Build:
    result = subprocess.run(
        getenv('BOB'),
        cwd=SITE_DIR,
        shell=True,
        text=True,
        capture_output=True
    )
    if result.returncode:
        log.error('Build failed: %s, %s', result.stderr, result.stdout)
        raise HTTPException(status_code=500, detail=result.stderr)
    log.info('Done building')
    return dict(output=result.stdout, error=result.stderr)


@app.post(
    "/build", 
    response_model=Build, 
    responses={
        204: {"description": "Ignored event type"},
        401: {"description": "Not valid X-Hub-Signature header"},
        500: {"description": "Build failed"},
    }
)
async def build(request: Request) -> Build:
    raw = await request.body()
    signature = request.headers.get("X-Hub-Signature")
    if signature != util.calc_signature(raw):
        log.warn('Reject build attempt')
        raise HTTPException(status_code=401, detail="Unauthorized")

    payload = await request.json()
    event_type = request.headers.get("X-Github-Event")
    match event_type:
        case 'push':
            return execute()
        case _:
            log.info('Ignored event type %s', event_type)
            return dict(output='Ignored', )

