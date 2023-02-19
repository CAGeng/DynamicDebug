**multi query** 已整合

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

**bulk**查询  已整合

```
POST _bulk
{ "index" : { "_index" : "test", "_type" : "type1", "_id" : "1" } }
{ "field1" : "value1" }
{ "delete" : { "_index" : "test", "_type" : "type1", "_id" : "2" } }
{ "create" : { "_index" : "test", "_type" : "type1", "_id" : "3" } }
{ "field1" : "value3" }
```

父子文档
```
DELETE user_address

PUT user_address
{
  "mappings": {
    "hahaha" : {
      "properties": {
        "user_address_relation": {
          "type": "join",
          "relations": {
            "user": "address"
          }
        },
       "user_name": {
          "type": "keyword"
        },
        "age ": {
          "type": "short"
        }
      }
    }
  }
}

PUT user_address/_doc/user1
{
  "user_name": "jack",
  "age": "25",
  "user_address_relation": {
    "name": "user"
  }
}

PUT user_address/_doc/user2
{
  "user_name": "rose",
  "age": "23",
  "user_address_relation": {
    "name": "user"
  }
}

PUT user_address/_doc/address1?routing=user1
{
  "province": "北京",
  "city": "北京",
  "street": "枫林三路",
  "user_address_relation": {
    "name": "address",
    "parent": "user1"
  }
}

PUT user_address/_doc/address2?routing=user1
{
  "province": "天津",
  "city": "天津",
  "street": "华夏路",
  "user_address_relation": {
    "name": "address",
    "parent": "user1"
  }
}

PUT user_address/_doc/address3?routing=user2
{
  "province": "河北",
  "city": "廊坊",
  "street": "燕郊经济开发区",
  "user_address_relation": {
    "name": "address",
    "parent": "user2"
  }
}



PUT user_address/_doc/address4?routing=user2
{
  "province": "天津",
  "city": "天津",
  "street": "华夏路",
  "user_address_relation": {
    "name": "address",
    "parent": "user2"
  }
}

GET user_address/_doc/user1

POST user_address/_search
{
  "query": {
    "has_child": {
      "type": "address",
      "query": {
        "match": {
          "province": "北京"
        }
      }
    }
  }
}

POST user_address/_search
{
  "query": {
    "parent_id": {
      "type": "address",
      "id": "user1"
    }
  }
}

POST user_address/_search
{
  "query": {
    "has_parent": {
      "parent_type": "user",
      "query": {
        "match": {
          "user_name": "jack"
        }
      }
    }
  }
}

GET user_address/_doc/address1?routing=user1

POST user_address/_search
{}
```