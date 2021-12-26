import time
import os
import inspect
from functools import wraps
import traceback


# a function logger not in user - would be implemented later
def LoggingTime(unit):
    def logger(func):
        @wraps(func)
        def inner_logger(*args, **kwargs):
            start = time.time()
            try:
                return_values = func(*args, **kwargs)
            except TypeError:
                return_values = func(*args)
            end = time.time()
            scaling = 1000 if unit == "ms" else 1
            duration = (end - start) * scaling

            main_dir = os.path.dirname(os.path.abspath("__main__"))     # the project dir
            func_complete_dir = f'{os.path.abspath(inspect.getfile(func))}\{func.__name__}'     # the function Route
            func_dir = func_complete_dir.replace(main_dir,"")    # the shortened function Route - from the project dir

            LOG = f'Calling - {func_dir} || <{duration} {unit}> \n'
            # print(traceback.extract_stack(limit=2)[-2][2])
            with open(f"CrashLog/Crash Report {PROGRAM_BEGINNING_DATE_TIME}.txt", "a") as file_object:
                file_object.write(LOG)

            return return_values

        return inner_logger

    return logger
