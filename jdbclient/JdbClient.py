import pexpect
import re
from func_timeout import func_set_timeout
import func_timeout

Taint_Tag = "SftVeryNiceSftVeryNice"

class JdbProcess(object):
    def __init__(self, ip, port):
        self.process = pexpect.spawn("jdb -connect com.sun.jdi.SocketAttach:hostname={ip},port={port}".format(port=port, ip=ip), timeout=600)
        self.port = port
        self.taint_tags = ["SftVeryNiceSftVeryNice", "sft_index", "_search/scroll", "383838383838"]
        self.file = open("./output/jdbout.txt", "w")
        self.filepath = "./output/jdbout.txt"
        self.filepath2 = "./output/tainted_class_type.txt"
        open(self.filepath2, "w")
        self.break_points = []
        self.check_field_limit = 2
        self.all_tainted_type = []
        
    @func_set_timeout(3)
    def add_breakpoint(self, class_name, method_name):
        s = "{class_name}.{entry_method}".format(class_name=class_name, entry_method=method_name)
        if s in self.break_points:
            return
        self.process.sendline("stop in " + s)
        print("add breakpoint: " + s + "  size: " + str(len(self.break_points)))
        self.break_points.append(s)
        
        # output may be out of place , we do not try to parse it
        
        # self.process.expect(pexpect.EOF)
        # result = self.process.before.decode()
        # print(result)
        # if "Set breakpoint" in result:
        #     print("Succeed")
        # if "It will be set after the class is loaded." in result:
        #     print("Fail")
        
            
    def wait(self):
        self.process.sendline("run")
        self.process.expect(".*Breakpoint hit:")
        self.process.expect(r".*\[.*\] ")
        self.raw_breakpoint_hit = self.process.after.decode()
        self.printLog(">>>>>>>> breakpoint hit\n")

        self.process.sendline("locals")
        self.process.expect(r".*\[.*\] ")
        self.raw_locals_result = self.process.after.decode()
        
        # self.process.sendline("print this")
        # self.process.expect(r".*\[.*\] ")
        # # self.raw_print_this = self.process.after.decode()
        # lines = self.process.after.decode()
        # for line in lines.split("\n"):
        #     if "this = " in line:
        #         self.raw_print_this = line
        
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
        self.val_map_class = {}
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
                    class_name = self.get_class_name(sp[1])
                    if class_name != None:
                        self.val_map_class[val_name] = class_name
        except Exception as e :
            self.parsed_breakpoint_method = "[parse error] raw is : " + self.raw_locals_result
            
            
        # 找this类型
        # org.apache.lucene.codecs.blocktree.BlockTreeTermsWriter$TermsWriter.pushTerm()
        matchObj = re.match( r'(.*)\.[^.]*', self.parsed_breakpoint_method, re.M|re.I)
        if matchObj != None:
            try:          
                clas = matchObj.group(1)
                self.this_type = clas
            except Exception as e :
                pass
            
        self.printLog("---------- args name ----------------------")
        self.printLog(self.arg_vals)
    
    @func_set_timeout(5)   
    def check_vals(self):
        self.tainted_vals = []
        self.taint_types = []
        self.tainted_vals_detail = []
        for val in self.arg_vals:
            ret = self.check_val_recurse(val, self.check_field_limit)
            taint = ret[0]
            taint_field = ret[1]
            if taint:
                self.tainted_vals.append(val) 
                self.tainted_vals_detail.append(val + "  " + str(taint_field))        
                if val in self.val_map_class.keys():
                    self.taint_types.append(self.val_map_class[val])
                else:
                    self.taint_types.append("[basic type] " + val)
        # this
        ret = self.check_val_recurse("this", self.check_field_limit)
        taint = ret[0]
        taint_field = ret[1]
        if taint:
            self.tainted_vals.append("[this]")
            self.tainted_vals_detail.append("[this] " + str(taint_field))
            if self.this_type != None:
                self.taint_types.append(self.this_type)
        self.printLog("---------- tainted args ----------------------")
        self.printLog(self.tainted_vals)
        self.printLog(self.tainted_vals_detail)
                
    def check_val_recurse(self, val, limit):
        try:
            self.process.sendline("dump {val}".format(val = val))
            self.process.expect(r".*\[.*\] ")
            # print(self.process.after.decode())
            out = self.process.after.decode()
            parse_fields = False
            for line in out.split("\n"):
                # eg. 这样的情况 scrollId = "SftVeryNiceSftVeryNice"
                for tag in self.taint_tags:
                    if tag in line:
                        if parse_fields:
                            sp = line.split(": ")
                            field = sp[0].strip()
                            now_field = val + "." + field
                        else:
                            now_field = val
                        return True, [now_field, tag]
                
                # field包裹在花括号里
                if "= {" in line:
                    parse_fields = True
                    continue
                if "}" in line:
                    parse_fields = False
                    break
                if(parse_fields):
                    if limit > 0:
                        sp = line.split(": ")
                        field = sp[0].strip()
                        ret = self.check_val_recurse(val + "." + field, limit - 1)
                        taint = ret[0]
                        taint_field = ret[1]
                        if taint:
                            return True, taint_field
            return False, None
                             
        except Exception as e :
            self.printLog("!! check vals fail for value " + val)
            self.printLog(e)
            return False
        
    def finish_this_turn(self):
        self.extract_breakpoint_method = self.get_extract_method_breakpoint()
        # print(self.extract_breakpoint_method)
        
        if self.extract_breakpoint_method == None:
            self.printLog("cannot find this method in breakpoint list!?")
            self.process.sendline("clear {method}".format(method=self.parsed_breakpoint_method))
            print("[clear] " + "clear {method}".format(method=self.parsed_breakpoint_method))
        else:
            self.process.sendline("clear {method}".format(method=self.extract_breakpoint_method))
            self.break_points.remove(self.extract_breakpoint_method)
            self.printLog("clear this breakpoint after hit")
            print("[clear] " + "clear {method}".format(method=self.extract_breakpoint_method))
            
        file = open(self.filepath2, "a")
        for s in self.taint_types:
            if not s in self.all_tainted_type:
                file.write(s + "\n")
            self.all_tainted_type.append(s)
        
        file.close()
        
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
        
    def get_class_name(self, s):
        # eg. instance of org.apache.lucene.store.BufferedChecksumIndexInput(id=15182)
        matchObj = re.match( r'.*instance of (.*)\(', s, re.M|re.I)
        if matchObj != None:
            try:          
                clas = matchObj.group(1)
                return clas
            except Exception as e :
                return None
        return None
        
if __name__=='__main__':
    pexpect.spawn("ls", timeout=600)