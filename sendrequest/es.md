**multi query**

http://events.jianshu.io/p/783990ca691e

```
# 创建索引
PUT test_multi
{
  "mappings": {
    "properties" : {
      "subject":{
        "type": "text"
      },
      "message":{
        "type": "text"
      }
    }
  }
}

# 创建索引  es6以前有表的概念，加上索引类型good。
PUT test_multi
{
  "mappings": {
    "good":{
      "properties" : {
        "subject":{
          "type": "text"
        },
        "message":{
          "type": "text"
        }
      }
    }
  }
}

# 填充数据
POST test_multi/_doc
{
  "subject":"brown fox",
  "message":"brown is my love" 
}

POST test_multi/_doc
{
  "subject":"fox is sly",
  "message":"brown and blank is color" 
}

# 搜索
GET /_search
{
  "query": {
    "multi_match" : {
      "query":    "this is a test", 
      "fields": [ "subject", "message" ] 
    }
  }
}
```

