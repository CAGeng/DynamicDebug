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
begin = False
debug_port = 7002
ip = "10.176.36.27"

def debug():
    global begin, debug_port, debug_lock, finish
    client = JdbClient.JdbProcess(ip, debug_port)
    
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
    output_processor.parse_breakpoint_from_file_taint_alloc_size("/mnt/f/code/webdetect/output/2-7/run/scroll-stack.txt")
    # output_processor.parse_breakpoint_from_file_system_out("/mnt/f/code/webdetect/output/out13.txt")
    # output_processor.parse_breakpoint_from_linger_extend("/mnt/f/code/webdetect/output/ES-output/output-8.4.2/longlifeExtend.txt")
    # output_processor.parse_breakpoint_from_file_system_out("/mnt/f/code/webdetect/output/tomcat-output/out-tomcat-raw.txt")
    # output_processor.parse_breakpoint_from_RCE_output("/mnt/f/web module/dubbo-bfei/Dubbo3.1.1.txt")
    # output_processor.parse_breakpoint_from_simple_list("/mnt/f/code/webdetect/output/1-31/es-test-1/debug/exp-readstring.txt")
    output_processor.add_breakpoints(client)
    debug_lock.release()
    begin = True
    
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
        finally:      
            client.finish_this_turn()
        debug_lock.release()
        if client.extract_breakpoint_method != None:      
            hit_breakpoints.append(client.extract_breakpoint_method)
        hit_map_request[client.extract_breakpoint_method] = myrequest.func_con

    finish = True
    with open("./output/hit_breakpoints.txt", "w") as f:
        for b in hit_breakpoints:
            if hit_map_request[b] == None:
                 f.write(b + "\n")
            else:
                f.write(b + "  :  [request id]" + str(hit_map_request[b]) + "\n")

def send_my_request():
    global finish, begin
    while True:
        time.sleep(1)
        if begin:
            break
    print("-------------------- begin sending -----------------------------")
    con = 0
    while con < 10:
        con += 1
        if finish:
            print("finish send")
            break
        time.sleep(1)
        debug_lock.acquire()
        debug_lock.release()
        myrequest.send()

thread = threading.Thread(name='t1',target= debug,args=())
thread.start()
# begin = True
thread = threading.Thread(name='t2',target= send_my_request,args=())
thread.start()


@func_set_timeout(10)
def loop(client):
    client.wait()