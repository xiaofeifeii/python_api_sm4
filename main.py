import time
import sm3, sm4
from hashlib import md5
import requests,json
import aes
from Crypto.Cipher import AES
import getopt
import sys

t = int(time.time())
# t = 1640966400
key = 'VILv&y&PB%h^ATND6hcy!zAAHS_DT!T%'
t_key = hex(~t ^ 0xffffffff).upper()
a = int(t_key, 16)
a += 1
t_key = hex(a).upper()[3:]
# t_key = t_key[3:]
t_hex = hex(t).upper()[2:]
str1 = key[0:8] + t_key + key[16:24]
str2 = key[8:16] + t_hex + key[24:32]
vid1 = sm3.sm3(str1).upper()
vid2 = sm3.sm3(str2).upper()
vid_target = vid1 + vid2
# print(bytes.fromhex(vid_target))
vid = md5(bytes.fromhex(vid_target)).hexdigest().upper()

def heartbeat():
    # VILv&y&P9E30D7006hcy!zAA

    js_heartbeat = {
        "time": t,
        "TID": t_key,
        "VID": vid
    }
    js_str = json.dumps(js_heartbeat)
    print(js_str)


def encryption_data(data):
    # data = "Hello World"
    t_str = t_key + t_hex
    md5_str = md5(bytes.fromhex(t_str)).hexdigest().upper()
    aes_key = key[0:16].encode('utf-8')
    aes_iv = md5_str[0:16].encode("utf-8")
    # print(f"{aes_key}  {aes_iv}")
    aes_data = aes.AEScryptor(aes_key, AES.MODE_CBC, aes_iv, paddingMode="PKCS7Padding", characterSet='utf-8')
    rData = aes_data.encryptFromString(str(data))

    encryption_aes = rData.toBase64()
    sm4_key = key[16:32]
    sm4_iv = md5_str[16:32]
    # print(f"{sm4_key} and  {sm4_iv}")
    sm4_data = sm4.encrypt_sm4(sm4_iv, encryption_aes, sm4_key)
    js_sm4={
        "time": t,
        "TID": t_key,
        "VID": vid,
        "DATA": sm4_data
    }
    print(json.dumps(js_sm4))

def post_msg(msg):
    url = 'https://demo.ynyrkj.cn:20016/HostSiteApi.ashx'
    requests.post(url,data=[("jsonString", json.dumps(msg))])


# print(json.dumps(d))
# heartbeat()
# encryption_data("hello")

try:
    opts, args = getopt.getopt(sys.argv[1:], 'td:')
    # print(opts)
    # print(args)
    for opt, arg in opts:
        if opt == '-t':
            heartbeat()
        elif opt == '-d':
            print(arg)
            encryption_data(arg)
except getopt.GetoptError as e:
    print('getopt error:', e)
