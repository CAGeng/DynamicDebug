import requests
import json
from sendrequest import es, dubbo, tomcat

func_con = 0

def send():
    global func_con
    func_con = 0
    for f in es.ES_funcs:
        func_con += 1
        # print("func: " + str(func_con))
        try:
            f()
        except Exception as e:
            continue
    # func_con = 0
    # for f in dubbo.dubbo_funcs:
    #     func_con += 1
    #     try:
    #         f()
    #     except Exception as e:
    #         continue
    # func_con = 0
    # for f in tomcat.funcs:
    #     func_con += 1
    #     try:
    #         f()
    #     except Exception as e:
    #         print(e)
    #         continue
