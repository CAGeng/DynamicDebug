from parse import ParseUtil

class MyProcessor(object):
    def __init__(self, root_path):
        self.root_dir = root_path
        self.breakpoints_set1 = []
        self.breakpoints_set2 = []
        self.breakpoints_set3 = []
        self.stacks_output1 = []
        self.stacks_output2 = []
        
    
    """
        file format:
        [SINK] <method signature>
            <method signature>
            <method signature>
        [SINK] <method signature>
            <method signature>
            <method signature>
    """
    def parse_breakpoint_from_file_taint_alloc_size(self, path, encoding='utf-8'):
        input_file = open(path, encoding=encoding)
        self.stacks_output1 = []
        stack = []
        lines = input_file.readlines()
        for line in lines:
            if "[SINK]" in line and len(stack) > 0:
                self.stacks_output1.append(stack) 
                stack = []
            
            class_name, method_name = ParseUtil.parse_method_sig(line)
            if class_name != None:
                stack.append({"class" : class_name, "method" : method_name})
        if len(stack) > 0:
            self.stacks_output1.append(stack)
            
            
    """
        file format:
        entry <method signature>
            <method signature>
            <method signature>
            
        entry <method signature>
            <method signature>
            <method signature>
    """
    def parse_breakpoint_from_RCE_output(self, path, encoding='utf-8'):
        input_file = open(path, encoding=encoding)
        self.breakpoints_set2 = []
        lines = input_file.readlines()
        begin = False
        for line in lines:
            if "Risky entries number :" in line:
                begin = True
            
            if begin:
                class_name, method_name = ParseUtil.parse_method_sig(line)
                if class_name != None:
                    self.breakpoints_set2.append({"class" : class_name, "method" : method_name})
            
            
    """
        file format:
        ---------- risky call stack ----------
            <method signature>
            <method signature>
            [sink units]
            
            <method signature>
            <method signature>
            [sink units]
    """
    def parse_breakpoint_from_file_system_out(self, path, encoding='utf-8'):
        input_file = open(path, encoding=encoding)
        self.breakpoints_set1 = []
        lines = input_file.readlines()
        begin = False
        for line in lines:
            if "--- risky call stack ---" in line:
                begin = True
            
            if begin:
                if "[sink units]" in line:
                    continue
                class_name, method_name = ParseUtil.parse_method_sig(line)
                if class_name != None:
                    self.breakpoints_set1.append({"class" : class_name, "method" : method_name})
            
            
    """
        file format:
            <method>  extend long life  <unit>
    """
    def parse_breakpoint_from_linger_extend(self, path, encoding='utf-8'):
        input_file = open(path, encoding=encoding)
        self.breakpoints_set3 = []
        lines = input_file.readlines()
        for line in lines:
            s = line.split("  extend long life  ")[0]
            class_name, method_name = ParseUtil.parse_method_sig(s)
            if class_name != None:
                self.breakpoints_set3.append({"class" : class_name, "method" : method_name})
                
    """
        file format:
            <method>
    """
    def parse_breakpoint_from_simple_list(self, path, encoding='utf-8'):
        input_file = open(path, encoding=encoding)
        self.breakpoints_set3 = []
        lines = input_file.readlines()
        for line in lines:
            class_name, method_name = ParseUtil.parse_method_sig(line)
            if class_name != None:
                self.breakpoints_set3.append({"class" : class_name, "method" : method_name})
            
    def add_breakpoints(self, jdbclient):
        print("stacks from taint_alloc_size: " + str(len(self.stacks_output1)))
        breakpoints = []
        for stack in self.stacks_output1:
            for dic in stack:
                # jdbclient.add_breakpoint(class_name=dic['class'], method_name=dic['method'])
                breakpoints.append(dic)
        if len(breakpoints) > 100:
            print("[warning] too many breakpoints maybe puzzling, auto split into size 100, only use 100 breakpoints")
            breakpoints = breakpoints[0:100]
        for dic in breakpoints:
            jdbclient.add_breakpoint(class_name=dic['class'], method_name=dic['method'])
                
        print("breakpoints from system_out: " + str(len(self.breakpoints_set1)))
        breakpoints = self.breakpoints_set1
        if len(breakpoints) > 100:
            print("[warning] too many breakpoints maybe puzzling, auto split into size 100")
            breakpoints = breakpoints[:100]
        for dic in breakpoints:
            jdbclient.add_breakpoint(class_name=dic['class'], method_name=dic['method'])
            
        print("breakpoints from RCE-output: " + str(len(self.breakpoints_set2)))
        for dic in self.breakpoints_set2:
            jdbclient.add_breakpoint(class_name=dic['class'], method_name=dic['method'])
            
        print("breakpoints from linger-extend: " + str(len(self.breakpoints_set3)))
        for dic in self.breakpoints_set3:
            jdbclient.add_breakpoint(class_name=dic['class'], method_name=dic['method'])
                
            
if __name__=='__main__' :
    processor = MyProcessor("")
    processor.parse_breakpoint_from_file_taint_alloc_size("/mnt/f/code/webdetect/output/ES-output/output/taint-alloc-size.txt")