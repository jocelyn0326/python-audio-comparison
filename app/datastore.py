import logging
from collections import defaultdict
from datetime import datetime
from threading import Lock
from typing import Optional

from bson import Binary
from pydantic import BaseModel

from .constants import BLOCK_SIZE
from .db.models import CiModel
from .utils import acquire_timeout

logger = logging.getLogger(__name__)


class Block(BaseModel):
    timestamp: int
    raw_data: bytes


class DataStore:
    def __init__(self) -> None:
        self.map: defaultdict[str, Block] = defaultdict(Block)
        self.locks: defaultdict[str, Lock] = defaultdict(Lock)

    def _validate(self, new_block: Block, last_block: Optional[Block] = None) -> None:
        if last_block and last_block.timestamp + 1 != new_block.timestamp:
            raise ValueError("Invalid timestamp order")

        if len(new_block.raw_data) != BLOCK_SIZE:
            raise ValueError("Invalid raw data size")

    def calculate_ci_value(self, new_raw_data: bytes, last_raw_data: bytes) -> bytes:
        
        return bytes(a ^ b for a, b in zip(new_raw_data, last_raw_data))

    async def add(self, channel: str, timestamp: int, raw_data: bytes) -> CiModel:
        lock = self.locks[channel]
        # When the deque is locked, wait for 10 seconds and then raise timeout.
        with acquire_timeout(lock, 10) as acquired:
            if not acquired:
                raise Exception(f"Get lock of channel ({channel}) timeout.")

            new_block: Block = Block(timestamp=timestamp, raw_data=raw_data)
            last_block: Optional[Block] = self.map.get(channel)
            ci_value_bytes: bytes = b""

            # Validate blocks
            self._validate(new_block, last_block)
    
            if last_block:
                ci_value_bytes = self.calculate_ci_value(
                    new_block.raw_data, last_block.raw_data
                )
                
                # TODO: Complete the second and third formulas later.

            self.map[channel] = new_block

            now = datetime.now()
            return CiModel(
                channel=channel,
                timestamp=timestamp,
                ci_value=Binary(ci_value_bytes),
                created_at=now,
                updated_at=now,
            )


ds = DataStore()
