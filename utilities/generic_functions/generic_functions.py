import logging, string, random, os, json

import datetime as dt 

from typing import Callable

def json_processor(file_name: str, operation_type: str = "r", json_object: dict = None):
    with open(file_name, operation_type, encoding = "utf-8") as f:
        if (operation_type == "r"):
            return json.load(f)
        else:
            json.dump(json_object, f, indent = 4)

def file_processor(file_name: str, operation_type: str = "rb", file_object: bytes = None, yield_yn: bool = False):
    with open(file_name, operation_type) as f:
        if (operation_type == "rb"):
            if (yield_yn == False):
                return f.read()
            else:
                yield from f
        else:
            f.write(file_object)

def operation_indicator(indicator_string: str):
    def wrapper_function(inner_function: Callable):
        def wrapped_function(self, *args, **kwargs):
            try:
                result  = inner_function(self, *args, **kwargs)
                message = f"{str(dt.datetime.now())} - {indicator_string} operation successful"
                self.data_log_object.info(message)
                return result

            except Exception as E:
                message = f"{str(dt.datetime.now())} - {indicator_string} operation failure, exception: {E}"
                self.data_log_object.error(message)
            
        return wrapped_function 
    
    return wrapper_function

def logger_initialization(file_name: str, initial_log_string: str):
    logging.basicConfig(filename = file_name, filemode = "a", format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s", encoding = "utf-8")
    data_log_object = logging.getLogger(initial_log_string)
    data_log_object.setLevel(logging.DEBUG)

    return data_log_object    

def logging_function(log_string: str, data_log_object: logging, log_type: str = "info"):
    match (log_type):
        case "info"  : data_log_object.info(f"{dt.datetime.strftime(dt.datetime.now(), '%Y%m%d_%H%M%S')} - {log_string}")
        case "debug" : data_log_object.error(f"{dt.datetime.strftime(dt.datetime.now(), '%Y%m%d_%H%M%S')} - {log_string}")