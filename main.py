from jdbclient import JdbClient
from sendrequest import myrequest
import sendrequest
import time
import threading
from func_timeout import func_set_timeout
import func_timeout
from parse import OutputProcessor, ParseUtil

debug_lock = threading.Lock()
finish = False

def debug():
    client = JdbClient.JdbProcess(8888)
    
    # 基础使用 demo
    # client.add_breakpoint(
    #     class_name="org.elasticsearch.rest.RestController", 
    #     method_name="dispatchRequest(org.elasticsearch.rest.RestRequest, org.elasticsearch.rest.RestChannel, org.elasticsearch.rest.RestHandler)"
    # )
    # client.wait()
    # client.parse_raw()
    # client.check_vals()
    
    debug_lock.acquire()
    output_processor = OutputProcessor.MyProcessor("")
    # output_processor.parse_breakpoint_from_file_taint_alloc_size("/mnt/f/code/webdetect/output/ES-output/output/taint-alloc-size.txt")
    output_processor.parse_breakpoint_from_file_system_out("/mnt/f/code/webdetect/output/out12.txt")
    output_processor.add_breakpoints(client)
    debug_lock.release()
    
    hit_breakpoints = []
    hit_map_request = {}
    while True:
        try:
            loop(client)
        except func_timeout.exceptions.FunctionTimedOut as e:
            print("debug waiting timeout, so we think it has finished")
            break
        
        debug_lock.acquire()
        client.parse_raw()
        try:
            client.check_vals()
        except func_timeout.exceptions.FunctionTimedOut as e:
            print("taint field check time out, skip")
        client.finish_this_turn()
        debug_lock.release()
        hit_breakpoints.append(client.extract_breakpoint_method)
        hit_map_request[client.extract_breakpoint_method] = myrequest.func_con
        
    global finish
    finish = True
    with open("./output/hit_breakpoints.txt", "w") as f:
        for b in hit_breakpoints:
            if hit_map_request[b] == None:
                 f.write(b + "\n")
            else:
                f.write(b + "  :  [request id]" + str(hit_map_request[b]) + "\n")

def send_my_request():
    global finish
    while True:
        if finish:
            break
        time.sleep(1)
        debug_lock.acquire()
        debug_lock.release()
        myrequest.send()

thread = threading.Thread(name='t1',target= debug,args=())
thread.start()
thread = threading.Thread(name='t2',target= send_my_request,args=())
thread.start()


@func_set_timeout(6)
def loop(client):
    client.wait()