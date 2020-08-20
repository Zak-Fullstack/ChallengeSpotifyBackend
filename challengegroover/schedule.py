import time
from pathlib import Path

def should_update(filename):
    path = Path(filename)
    modification_time = path.stat().st_mtime
    now = time.time()
    one_day = 86400
    if abs(now - modification_time):
        return True
    else:
        return False