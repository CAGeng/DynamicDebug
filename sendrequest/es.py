import requests
import json

ES_funcs = []

def f():
    url="http://127.0.0.1:9200/sft_index"
    response = requests.put(url)
    # print(response.text)
ES_funcs.append(f)

def f():
    url="http://127.0.0.1:9200/sft_index"
    headers = {'content-type': "application/json"}
    response = requests.get(url, headers = headers)
    # print(response.text)
ES_funcs.append(f)

def f():
    url="http://127.0.0.1:9200/_search/scroll"
    body={"scroll_id" : "SftVeryNiceSftVeryNice"}
    headers = {'content-type': "application/json"}
    response = requests.get(url, data = json.dumps(body), headers = headers)
    # print(response.text)
ES_funcs.append(f)

def f():
    url="http://127.0.0.1:9200/_cat/indices?v"
    response = requests.get(url) 
ES_funcs.append(f)

def f():
    url="http://127.0.0.1:9200/sft_index/_doc/SftVeryNiceSftVeryNice"
    body={
        "title" : "SftVeryNiceSftVeryNice",
        "name" : "SftVeryNiceSftVeryNice",
        "idddd" : "SftVeryNiceSftVeryNice"
    }
    headers = {'content-type': "application/json"}
    response = requests.post(url, data = json.dumps(body), headers = headers)
    # print(response.text)
ES_funcs.append(f)

def f():
    url="http://127.0.0.1:9200/sft_index/_doc/SftVeryNiceSftVeryNice"
    response = requests.get(url) 
    # print(response.text)
ES_funcs.append(f)

def f():
    url="http://127.0.0.1:9200/sft_index/_search"
    response = requests.get(url) 
    # print(response.text)
ES_funcs.append(f)

def f():
    url="http://127.0.0.1:9200/sft_index/_doc/SftVeryNiceSftVeryNice"
    response = requests.delete(url) 
    # print(response.text) 
ES_funcs.append(f)

def f():
    url="http://127.0.0.1:9200/sft_index/_search"
    body={
        "query": {
            "match_all" : {
                    
                    }
        }
    }
    headers = {'content-type': "application/json"}
    response = requests.get(url, data = json.dumps(body), headers = headers) 
    # print(response.text) 
ES_funcs.append(f)

def f():
    url="http://127.0.0.1:9200/_tasks/task_id:SftVeryNiceSftVeryNice/_cancel"
    response = requests.post(url) 
    # print(response.text) 
ES_funcs.append(f)

def f():
    url="http://127.0.0.1:9200/_tasks/task_id:383838383838/_cancel"
    response = requests.post(url) 
    # print(response.text) 
ES_funcs.append(f)

def f():
    url="http://127.0.0.1:9200/_nodes/stats"
    response = requests.get(url) 
    # print(response.text) 
ES_funcs.append(f)

def f():
    url="http://127.0.0.1:9200/_cluster/pending_tasks"
    response = requests.get(url) 
    # print(response.text) 
ES_funcs.append(f) 

def f():
    url="http://127.0.0.1:9200/sft_index/_search?scroll=10m"
    body={
        "query": { "match_all": {}},
        "sort" : ["_doc"], 
        "size":  1
    }
    headers = {'content-type': "application/json"}
    response = requests.get(url, data = json.dumps(body), headers = headers) 
    # print(response.text) 
ES_funcs.append(f)

def f():
    url="http://127.0.0.1:9200/sft_index/_search"
    body={
        "query": {
            "match_all" : {
                    
                    }
        },
        "aggs": {
            "SftVeryNiceSftVeryNice": {
            "date_range": {
                "field": "date",
                "format": "MM-yyyy",
                "ranges": [
                { "to": "now-10M/M" },  
                { "from": "now-10M/M" } 
                ]
            }
            }
        }

    }
    headers = {'content-type': "application/json"}
    response = requests.get(url, data = json.dumps(body), headers = headers) 
    # print(response.text) 
ES_funcs.append(f)

def f():
    url="http://127.0.0.1:9200/_mget"
    body={
    "docs": [
            {
            "_index": "sft_index",
            "_id": "1"
            },
            {
            "_index": "my-index-000001",
            "_id": "2"
            }
        ]
    }
    headers = {'content-type': "application/json"}
    response = requests.get(url, data = json.dumps(body), headers = headers) 
    # print(response.text) 
ES_funcs.append(f)

def f():
    url="http://127.0.0.1:9200/_cat/segments/sft_index?v&h=shard,segment,size,size.menory"
    response = requests.get(url) 
    # print(response.text) 
ES_funcs.append(f)

if __name__=='__main__':
    for f in ES_funcs:
        f()