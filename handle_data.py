import base64
import time
import sm3, sm4
from hashlib import md5
import requests, json
import aes
from Crypto.Cipher import AES
import getopt
import sys
from urllib import parse

t = int(time.time())
# t = 1640966400
# t = 1669017313
# key = 'VILv&y&PB%h^ATND6hcy!zAAHS_DT!T%'
key = 'RILv&y&PB%h^ATND6hcy!zAAHS_DT!T%'

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

t_str = t_key + t_hex
md5_str = md5(bytes.fromhex(t_str)).hexdigest().upper()
aes_key = key[0:16].encode('utf-8')
aes_iv = md5_str[0:16].encode("utf-8")
sm4_key = key[16:32]
sm4_iv = md5_str[16:32]


# print(bytes.fromhex(vid_target))


def method_request(method_code):
    # VILv&y&P9E30D7006hcy!zAA
    t_vid = md5(bytes.fromhex(vid_target)).hexdigest().upper()
    js_heartbeat = {
        "SID": '5301020001',
        "FID": method_code,
        "TID": t_key,
        "VID": t_vid
    }
    payload = parse.urlencode(js_heartbeat)
    return payload


def encryption_data(data):
    aes_data = aes.AEScryptor(aes_key, AES.MODE_CBC, aes_iv, paddingMode="PKCS7Padding", characterSet='utf-8')
    rData = aes_data.encryptFromString(str(data))
    encryption_aes = rData.toBase64()
    sm4_data = sm4.encrypt_sm4(sm4_iv, encryption_aes, sm4_key)
    return str(sm4_data)


def decryption_data(msg):
    js_data = json.loads(msg)
    # print(js_data)
    data = js_data[0]['Data']
    # data = base64.b64decode(data)
    decrypt_sm4_data = sm4.decrypt_sm4(sm4_iv, sm4_key, data)
    # print(decrypt_sm4_data)
    aes_de = aes.AEScryptor(aes_key, AES.MODE_CBC, aes_iv, paddingMode="PKCS7Padding", characterSet='utf-8')
    decrypt_aes_data = aes_de.decryptFromBytes(decrypt_sm4_data)
    # print(decrypt_aes_data)
    return decrypt_aes_data


def sensor_data():
    sensorData = {
        "Host": [{
            "P1": 2000,
            "P2": 0,
            "P3": 0,
            "P4": 55.1,
            "P5": 0,
            "P6": 0,
            "P7": 12.6
        }]
        ,
        "Terminal": [
            {
                "P1": "530102A001",
                "P2": 0,
                "P3": 13.3
            }, {
                "P1": "530102A002",
                "P2": 0,
                "P3": 13.3
            },
            {
                "P1": "530102A003",
                "P2": 0,
                "P3": 13.3
            },
            {
                "P1": "530102A004",
                "P2": 0,
                "P3": 13.3
            },
            {
                "P1": "530102A005",
                "P2": 0,
                "P3": 13.3
            },
            {
                "P1": "530102A006",
                "P2": 0,
                "P3": 13.3
            },
            {
                "P1": "530102A007",
                "P2": 0,
                "P3": 13.3
            },
            {
                "P1": "530102A008",
                "P2": 0,
                "P3": 13.3
            },
            {
                "P1": "530102A009",
                "P2": 0,
                "P3": 13.3
            },
            {
                "P1": "530102A010",
                "P2": 0,
                "P3": 13.3
            },
            {
                "P1": "530102B001",
                "P2": 0,
                "P3": 13.3
            }
        ]
    }

    js_str = json.dumps(sensorData)
    # print(js_str)
    vid3 = sm3.sm3(encryption_data(js_str)).upper()
    d_vid_target = vid1 + vid2 + vid3
    d_vid = md5(bytes.fromhex(d_vid_target)).hexdigest().upper()

    msg = {
        "SID": '5301020001',
        "FID": 1002,
        "TID": t_key,
        "VID": d_vid,
        "Data": encryption_data(js_str)
    }
    # print(json.dumps(msg))
    payload = parse.urlencode(msg)
    return payload


def post_msg(msg):
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    url = 'https://demo.ynyrkj.cn:20016/HostSiteApi.ashx'
    res = requests.post(url, headers=headers, data=msg)
    return res.text


# print(json.dumps(d))
# heartbeat()
# encryption_data("hello")
if __name__ == '__main__':
    # print(heartbeat())
    print(method_request(3001))
    res = post_msg(method_request(3001))
    # res = post_msg(sensor_data())
    print(res)
    # print(decryption_data(res))

# try:
#     opts, args = getopt.getopt(sys.argv[1:], 'td:')
#     # print(opts)
#     # print(args)
#     for opt, arg in opts:
#         if opt == '-t':
#             heartbeat()
#         elif opt == '-d':
#             print(arg)
#             encryption_data(arg)
# except getopt.GetoptError as e:
#     print('getopt error:', e)
