import requests
import json
from jdbclient.JdbClient import Taint_Tag

funcs = []

ip = "localhost"

def f():
    url="http://{}:8080/webapp".format(ip)
    response = requests.get(url)
    # print(response.text)
funcs.append(f)

def f():
    url = "http://{}:8080/webapp/".format(ip) + Taint_Tag
    response = requests.get(url)
    # print(response.text)
funcs.append(f)

def f():
    url = "http://{}:8080".format(ip)
    response = requests.get(url)
    # print(response.text)
funcs.append(f)