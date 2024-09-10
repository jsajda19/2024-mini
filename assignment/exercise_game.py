"""
Response time - single-threaded
"""

#from machine import Pin
import time
import random
import json
import os

class Pin:
    OUT = 0
    IN = 1
    PULL_UP = 2

    def __init__(self, pin_number, mode, pull=None):
        self.pin_number = pin_number
        self.mode = mode
        self.state = 0

    def high(self):
        self.state = 1
        print(f"Pin {self.pin_number} set HIGH")

    def low(self):
        self.state = 0
        print(f"Pin {self.pin_number} set LOW")

    def value(self):
        return random.choice([0, 1])


N: int = 3
sample_ms = 10.0
on_ms = 500


def random_time_interval(tmin: float, tmax: float) -> float:
    """return a random time interval between max and min"""
    return random.uniform(tmin, tmax)


def blinker(N: int, led: Pin) -> None:
    # %% let user know game started / is over

    for _ in range(N):
        led.high()
        time.sleep(0.1)
        led.low()
        time.sleep(0.1)


def write_json(json_filename: str, data: dict) -> None:
    """Writes data to a JSON file.

    Parameters
    ----------

    json_filename: str
        The name of the file to write to. This will overwrite any existing file.

    data: dict
        Dictionary data to write to the file.
    """

    with open(json_filename, "w") as f:
        json.dump(data, f)


def scorer(t: list[int | None]) -> None:
    # %% collate results
    misses = t.count(None)
    print(f"You missed the light {misses} / {len(t)} times")

    t_good = [x for x in t if x is not None]
    
    if t_good:
        min_time = min(t_good)
        max_time = max(t_good)
        avg_time = sum(t_good) / len(t_good)
    else:
        min_time = max_time = avg_time = None

    score = (len(t) - misses) / len(t)

    print(t_good)

    # add key, value to this dict to store the minimum, maximum, average response time
    # and score (non-misses / total flashes) i.e. the score a floating point number
    # is in range [0..1]
    data = {
        "min_time": min_time,
        "max_time": max_time,
        "average_time": avg_time,
        "score": score,
        "misses": misses
    }

    # %% make dynamic filename and write JSON

    now: tuple[int] = time.localtime()

    now_str = "-".join(map(str, now[:3])) + "T" + "_".join(map(str, now[3:6]))
    directory = '/Users/helen/Desktop/2024-mini/json_file/' 

    filename = os.path.join(directory, f"score-{now_str}.json")

    if not os.path.exists(directory):
        os.makedirs(directory)
    
    print("write", filename)

    write_json(filename, data)


if __name__ == "__main__":
    # using "if __name__" allows us to reuse functions in other script files

    led = Pin(15, Pin.OUT)
    button = Pin(15, Pin.IN, Pin.PULL_UP)

    t: list[int | None] = []

    blinker(3, led)

    for i in range(N):
        time.sleep(random_time_interval(0.5, 5.0))

        led.high()

        tic = time.time() * 1000 
        t0 = None
        while (time.time() * 1000 - tic) < on_ms:
            if button.value() == 0:
                t0 = time.time() * 1000 - tic
                led.low()
                break
        t.append(t0)

        led.low()

    blinker(5, led)

    scorer(t)
