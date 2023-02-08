import requests
import json

ES_funcs = []

address = "10.176.36.27:9002"

def f():
    url="http://{address}/sft_index".format(address=address)
    response = requests.put(url)
    # print(response.text)
ES_funcs.append(f)

# 2
def f():
    url="http://{address}/sft_index".format(address=address)
    headers = {'content-type': "application/json"}
    response = requests.get(url, headers = headers)
    # print(response.text)
ES_funcs.append(f)

def f():
    url="http://{address}/_search/scroll".format(address=address)
    body={"scroll_id" : "SftVeryNiceSftVeryNice"}
    headers = {'content-type': "application/json"}
    response = requests.get(url, data = json.dumps(body), headers = headers)
    # print(response.text)
ES_funcs.append(f)

def f():
    url="http://{address}/_cat/indices?v".format(address=address)
    response = requests.get(url) 
ES_funcs.append(f)

# 5
def f():
    url="http://{address}/sft_index/_doc/SftVeryNiceSftVeryNice".format(address=address)
    body={
        "title" : "SftVeryNiceSftVeryNice",
        "name" : "SftVeryNiceSftVeryNice",
        "idddd" : "SftVeryNiceSftVeryNice"
    }
    headers = {'content-type': "application/json"}
    response = requests.post(url, data = json.dumps(body), headers = headers)
    # print(response.text)
ES_funcs.append(f)

# 6
def f():
    url="http://{address}/sft_index/_doc/SftVeryNiceSftVeryNice".format(address=address)
    response = requests.get(url) 
    # print(response.text)
ES_funcs.append(f)

# 7
def f():
    url="http://{address}/sft_index/_search".format(address=address)
    response = requests.get(url) 
    # print(response.text)
ES_funcs.append(f)

def f():
    url="http://{address}/sft_index/_doc/SftVeryNiceSftVeryNice".format(address=address)
    response = requests.delete(url) 
    # print(response.text) 
ES_funcs.append(f)

# 9
def f():
    url="http://{address}/sft_index/_search".format(address=address)
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

# 10
def f():
    url="http://{address}/_tasks/task_id:SftVeryNiceSftVeryNice/_cancel".format(address=address)
    response = requests.post(url) 
    # print(response.text) 
ES_funcs.append(f)

# 11
def f():
    url="http://{address}/_tasks/task_id:383838383838/_cancel".format(address=address)
    response = requests.post(url) 
    # print(response.text) 
ES_funcs.append(f)

# 12
def f():
    url="http://{address}/_nodes/stats".format(address=address)
    response = requests.get(url) 
    # print(response.text) 
ES_funcs.append(f)

def f():
    url="http://{address}/_cluster/pending_tasks".format(address=address)
    response = requests.get(url) 
    # print(response.text) 
ES_funcs.append(f) 

def f():
    url="http://{address}/sft_index/_search?scroll=10m".format(address=address)
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
    url="http://{address}/sft_index/_search".format(address=address)
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
    url="http://{address}/_mget".format(address=address)
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

# 17
def f():
    url="http://{address}/_cat/segments/sft_index?v&h=SftVeryNiceSftVeryNice,shard,segment,size,size.menory".format(address=address)
    response = requests.get(url) 
    # print(response.text) 
ES_funcs.append(f)

# 18
def f():
    url="http://{address}/sft_index/_search".format(address=address)
    body={
        "query": {
            "multi_match" : {
                "query":    "this is a test", 
                "type":       "best_fields",
                "fields": [ "subject", "message" ] 
            }
        }
    }
    headers = {'content-type': "application/json"}
    response = requests.get(url, data = json.dumps(body), headers = headers) 
    # print(response.text) 
ES_funcs.append(f)

if __name__=='__main__':
    # for i in range(len(ES_funcs)):
    #     print(i + 1)
    #     if i > 5:
    #         continue
    #     ES_funcs[i]()
    ES_funcs[6]()