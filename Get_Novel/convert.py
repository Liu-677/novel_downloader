import urllib

def str_encode(str):
    return urllib.parse.quote(str.encode('gb2312'))      # 先进行gb2312编码 再进行urlencode编码

def str_decode(str):
    return urllib.parse.unquote(str,encoding='gb2312')

if __name__=='__main__':
    str1=''
    print(str_encode(str1))
    str2=''
    print(str_decode(str2))