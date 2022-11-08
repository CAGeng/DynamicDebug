import pexpect
import re

class JdbProcess(object):
    def __init__(self, port):
        self.process = pexpect.spawn("jdb -connect com.sun.jdi.SocketAttach:hostname=localhost,port={port}".format(port=port), timeout=600)
        self.port = port
        self.taint_tags = ["SftVeryNiceSftVeryNice", "sft_index", "_search/scroll", "383838383838"]
        self.file = open("./output/jdbout.txt", "w")
        self.filepath = "./output/jdbout.txt"
        self.break_points = []
        
    def add_breakpoint(self, class_name, method_name):
        self.process.sendline("stop in {class_name}.{entry_method}".format(
                class_name=class_name, entry_method=method_name
            ))
        print("add breakpoint: " + "{class_name}.{entry_method}".format(class_name=class_name, entry_method=method_name))
        
        # output may be out of place , we do not try to parse it
        
        # self.process.expect("\n>")
        # result = self.process.before.decode()
        # print(result)
        # if "Set breakpoint" in result:
        #     print("Succeed")
        # if "It will be set after the class is loaded." in result:
        #     print("Fail")
        
        self.break_points.append("{class_name}.{entry_method}".format(class_name=class_name, entry_method=method_name))
            
    def wait(self):
        self.process.sendline("run")
        self.process.expect(".*Breakpoint hit:")
        self.process.expect(r".*\[.*\] ")
        self.raw_breakpoint_hit = self.process.after.decode()
        self.printLog(">>>>>>>> breakpoint hit\n")

        self.process.sendline("locals")
        self.process.expect(r".*\[.*\] ")
        self.raw_locals_result = self.process.after.decode()
        # print("------------ locals------------------")
        # print(self.raw_locals_result)
        # print("-------------------------------------")
        # print("")
        
    def parse_raw(self):
        # print("------------- raw ---------------------")
        # print(self.raw_breakpoint_hit)
        # print("---------------- raw ------------------")
        # print(self.raw_locals_result)
        try :
            sp = self.raw_breakpoint_hit.split(",")
            s = sp[1]
            self.parsed_breakpoint_method = s
        except Exception as e :
            self.parsed_breakpoint_method = "[parse error] raw is : " + self.raw_breakpoint_hit
            
        self.parsed_breakpoint_method = self.parsed_breakpoint_method.strip()
        self.printLog("---------- breakpoint at method ----------------------")
        self.printLog(self.parsed_breakpoint_method)
        
        self.arg_vals = []
        try :
            isArg = False
            for line in self.raw_locals_result.split("\n"):
                if "Method arguments:" in line:
                    isArg = True
                    continue
                if "Local variables:" in line:
                    break
                if isArg:
                    sp = line.split(" = ")
                    val_name = sp[0]
                    self.arg_vals.append(val_name)
        except Exception as e :
            self.parsed_breakpoint_method = "[parse error] raw is : " + self.raw_locals_result
            
        self.printLog("---------- args name ----------------------")
        self.printLog(self.arg_vals)
        
    def check_vals(self):
        self.tainted_vals = []
        for val in self.arg_vals:
            if self.check_val_recurse(val, 3):
                self.tainted_vals.append(val)               
        if self.check_val_recurse("this", 3):
                self.tainted_vals.append("[this]")
        self.printLog("---------- tainted args ----------------------")
        self.printLog(self.tainted_vals)
                
    def check_val_recurse(self, val, limit):
        try:
            self.process.sendline("dump {val}".format(val = val))
            self.process.expect(r".*\[.*\] ")
            # print(self.process.after.decode())
            out = self.process.after.decode()
            parse = False
            for line in out.split("\n"):
                if "= {" in line:
                    parse = True
                    continue
                if "}" in line:
                    parse = False
                    break
                if(parse):
                    for tag in self.taint_tags:
                        if tag in line:
                            return True
                    if limit > 0:
                        sp = line.split(": ")
                        field = sp[0]
                        taint = self.check_val_recurse(val + "." + field, limit - 1)
                        if taint:
                            return True
            return False
                             
        except Exception as e :
            self.printLog("!! check vals fail for value " + val)
            self.printLog(e)
            return False
        
    def finish_this_turn(self):
        self.extract_breakpoint_method = self.get_extract_method_breakpoint()
        # print(self.extract_breakpoint_method)
        
        if self.extract_breakpoint_method == None:
            self.printLog("cannot find this method in breakpoint list!?")
        else:
            self.process.sendline("clear {method}".format(method=self.extract_breakpoint_method))
            self.break_points.remove(self.extract_breakpoint_method)
            self.printLog("clear this breakpoint after hit")
        
    def get_extract_method_breakpoint(self):
        """
        parsed_breakpoint when hit is like: 
            org.elasticsearch.common.compress.CompressorFactory.compressor(), line=41 bci=0
        but we need args list like what we do when add breakpoints: 
            stop in org.elasticsearch.common.compress.CompressorFactory.compressor(org.elasticsearch.common.bytes.BytesReference)
        so we try to parse it through comparing with the breakpoints list
        """
        s = self.parsed_breakpoint_method[:-1]
        one_of_same_name_mathod = None
        for bp in self.break_points:
            if s in bp:
                one_of_same_name_mathod = bp
                # (org.elasticsearch.common.bytes.BytesReference)
                matchObj = re.match( r'.*\((.*)\)', bp, re.M|re.I)
                if matchObj != None:
                    try:          
                        arg_siz = len(matchObj.group(1).split(","))
                        if arg_siz == len(self.arg_vals):
                            return bp
                    except Exception as e :
                       continue
        
        if one_of_same_name_mathod != None:
            self.printLog("cannot get exact method, return one breakpoint methods having the same name")
            return one_of_same_name_mathod
        return None
        
    def printLog(self, object):
        s = str(object)
        print(s)
        file = open(self.filepath, "a")
        file.write(s + "\n")
        file.close()