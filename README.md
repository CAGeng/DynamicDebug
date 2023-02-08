# DynamicDebug

利用Java调试工具JDB自动化处理静态分析输出，用断点拦截请求，寻找真正可触发的代码段

仅支持Unix

```
python3 ./main.py 
```



**自动化的流程**

```
 jdb -connect com.sun.jdi.SocketAttach:hostname=10.176.36.27,port=7002
 
 methods org.elasticsearch.rest.RestController
 
 stop in org.elasticsearch.rest.RestController.dispatchRequest(org.elasticsearch.rest.RestRequest, org.elasticsearch.rest.RestChannel, org.elasticsearch.common.util.concurrent.ThreadContext) 
 
 locals
 
 print this
```

