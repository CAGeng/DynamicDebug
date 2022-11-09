import requests
import json
from sendrequest import es, dubbo

func_con = 0

def send():
    global func_con
    func_con = 0
    for f in es.ES_funcs:
        func_con += 1
        f()
    for f in dubbo.dubbo_funcs:
        func_con += 1
        f()
