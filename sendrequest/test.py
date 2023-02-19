import requests
import json
import random

def f(s1, s2):
    index_name = "sft_index" + s1
    type_name = "sft_type" + s2
    address = "10.176.36.27:9002"
    url="http://{address}/{index_name}".format(address=address, index_name=index_name)
    body={
        "mappings": {
            type_name: {
                "properties": {
                    "title": {
                        "type": "text"
                    }
                }
            }
        }
    }
    headers = {'content-type': "application/json"}
    response = requests.put(url, data = json.dumps(body), headers = headers) 
    print(response.text) 
    
def generate_random_str(randomlength=16):
  """
  生成一个指定长度的随机字符串
  """
  random_str =''
  base_str ='ABCDEFGHIGKLMNOPQRSTUVWXYZabcdefghigklmnopqrstuvwxyz0123456789'
  length =len(base_str) -1
  for i in range(randomlength):
    random_str +=base_str[random.randint(0, length)]
  return random_str

for i in range(10000):
    print(str(i))
    i = i + 1
    s = generate_random_str(10000)
    f(str(i), s)
    