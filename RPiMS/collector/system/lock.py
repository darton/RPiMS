import logging
import sys
import fcntl

logger = logging.getLogger(__name__)

def acquire_lock(lock_path="/run/lock/rpims.lock"):
    try:
        fp = open(lock_path, "w") # pylint: disable=consider-using-with
    except PermissionError:
        logger.error("Cannot open lock file %s. Check permissions.", lock_path)
        sys.exit(255)

    try:
        fcntl.flock(fp, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        logger.error("Another instance of RPiMS is already running. Exiting.")
        sys.exit(255)

    return fp  # keep file descriptor open!
