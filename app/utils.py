from contextlib import contextmanager


@contextmanager
def acquire_timeout(lock, timeout):
    """Get lock with timeout argument and release it at last."""
    result = lock.acquire(timeout=timeout)
    try:
        yield result
    finally:
        if result:
            lock.release()
