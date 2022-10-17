import time
from spike.operator import equal_to

def wait_for_seconds(seconds):
    time.sleep(seconds)

def wait_until(get_value_function, operator_function=equal_to, target_value=True):
    while not operator_function(get_value_function(), target_value):
        time.sleep(0.001)

class Timer:
    def __init__(self):
        self.start = time.time()
    def reset(self):
        self.start = time.time()
    def now(self):
        return int(time.time() - self.start)
