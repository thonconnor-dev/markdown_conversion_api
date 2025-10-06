import logging
from fastapi import FastAPI

from app.core.database import get_db
from app.core.logging import setup_logging

setup_logging(json_output=False)
LOG = logging.getLogger(__name__)

app = FastAPI()



@app.get("/")
def hello():
    # get_db()
    LOG.info("hello start")
    return "hello"



