import re

def parse_method_sig(signature):
    matchObj = re.match( r'.*<(.*)>.*', signature, re.M|re.I)
    if matchObj != None:
        try:          
            s = matchObj.group(1)
            sp = s.split(": ")
            class_name = sp[0]
            method_name = sp[1].split()[1]
            return class_name, method_name
        except Exception as e :
            return None, None
    return None, None
        
if __name__ == '__main__':
    parse_method_sig("<org.elasticsearch.common.util.BigByteArray: boolean get(long,int,org.apache.lucene.util.BytesRef)>")