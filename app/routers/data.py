from cmath import exp
import logging

from fastapi import APIRouter, Depends, Form, HTTPException, UploadFile

from app.constants import BLOCK_SIZE
from app.datastore import ds
from app.db import DatabaseManager, get_database
from app.db.models import CiModel

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/deliver/", status_code=201)
async def deliver(
    file: UploadFile = Form(...),
    channel: str = Form(...),
    timestamp: int = Form(...),
    db: DatabaseManager = Depends(get_database),
):
    raw_data: bytes = await file.read()
    if len(raw_data) != BLOCK_SIZE:
        raise HTTPException(status_code=400, detail="Invalid data size")

    try:
        ci: CiModel = await ds.add(
            channel=channel, timestamp=timestamp, raw_data=raw_data
        )
    except Exception as e:
        logger.error(f"Unexpected error raised: {repr(e)}")
        raise HTTPException(status_code=400, detail="Unknown error")
    try:
        created_ci_id: str = await db.add_ci(ci)
        logger.info(f"Ci ({created_ci_id}) is created.")
    except Exception as e:
        logger.error(f"Unexpected error raised: {repr(e)}")
        raise HTTPException(status_code=400, detail="Unknown error")
