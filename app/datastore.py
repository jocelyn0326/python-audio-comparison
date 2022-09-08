import logging
from collections import defaultdict, deque
from datetime import datetime
from threading import Lock
from typing import Optional

from bson import Binary
from pydantic import BaseModel

from .constants import BLOCK_SIZE, QUEUE_LENGTH
from .db.models import CiModel
from .utils import acquire_timeout

logger = logging.getLogger(__name__)


class Block(BaseModel):
    timestamp: int
    raw_data: bytes


class DataStore:
    DEFAULT_MAX_LENGTH: int = QUEUE_LENGTH

    def __init__(self, max_length: int = DEFAULT_MAX_LENGTH) -> None:
        self.map: defaultdict[str, deque[Block]] = defaultdict(deque)
        self.locks: defaultdict[str, Lock] = defaultdict(Lock)
        self.max_length = max_length

    def _validate(self, new_block: Block, last_block: Optional[Block] = None) -> None:
        if last_block and last_block.timestamp + 1 != new_block.timestamp:
            raise ValueError("Invalid timestamp order")

        if len(new_block.raw_data) != BLOCK_SIZE:
            raise ValueError("Invalid raw data size")

    def get_ci_value(self, new_raw_data: bytes, last_raw_data: bytes) -> bytes:
        return bytes(a ^ b for a, b in zip(new_raw_data, last_raw_data))

    async def add(self, channel: str, timestamp: int, raw_data: bytes) -> CiModel:
        lock = self.locks[channel]
        # When the deque is locked, wait for 10 seconds and then raise timeout.
        with acquire_timeout(lock, 10) as acquired:
            if not acquired:
                raise Exception(f"Get lock of channel ({channel}) timeout.")

            channel_q = self.map[channel]
            new_block: Block = Block(timestamp=timestamp, raw_data=raw_data)
            last_block: Optional[Block] = None
            ci_value_bytes: bytes = b""
            if channel_q:
                last_block = channel_q[-1]

            # Validate blocks
            self._validate(new_block, last_block)

            # Handle queue overflow
            if len(channel_q) >= self.max_length:
                # Pop the oldest block
                logger.info("The oldest data is popped.")
                channel_q.popleft()

            channel_q.append(new_block)

            if last_block:
                ci_value_bytes = self.get_ci_value(
                    new_block.raw_data, last_block.raw_data
                )
                
                # TODO: Complete the second and third formulas later.

            now = datetime.now()
            return CiModel(
                channel=channel,
                timestamp=timestamp,
                ci_value=Binary(ci_value_bytes),
                created_at=now,
                updated_at=now,
            )


ds = DataStore()
