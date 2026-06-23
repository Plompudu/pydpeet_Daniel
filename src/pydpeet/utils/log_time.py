import logging
from contextlib import contextmanager
from time import perf_counter


@contextmanager
def _log_time(
    description: str = "",
    show_runtime: bool = True,
):
    start = perf_counter()
    yield
    end = perf_counter()
    if show_runtime:
        logging.info(f"{end - start:.4f}s {description}")
