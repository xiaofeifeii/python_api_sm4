import time
import sm3, sm4
from hashlib import md5
import json
import aes
from Crypto.Cipher import AES

# t = int(time.time())
t = 1640966400
key = 'VILv&y&PB%h^ATND6hcy!zAAHS_DT!T%'
t_key = hex(~t ^ 0xffffffff).upper()
# a = int(t_key, 16)
# a += 1
# t_key = hex(a).upper()[3:]
t_key = t_key[3:]
t_hex = hex(t).upper()[2:]


def heartbeat():
    # VILv&y&P9E30D7006hcy!zAA
    str1 = key[0:8] + t_key + key[16:24]
    str2 = key[8:16] + t_hex + key[24:32]
    vid1 = sm3.sm3(str1).upper()
    vid2 = sm3.sm3(str2).upper()
    vid_target = vid1 + vid2
    # print(bytes.fromhex(vid_target))
    vid = md5(bytes.fromhex(vid_target)).hexdigest().upper()
    js_heartbeat = {
        "time": t,
        "TID": t_key,
        "VID": vid
    }
    js_str = json.dumps(js_heartbeat)
    print(js_str)


def encryption_data():
    data = "Hello World"
    t_str = t_key + t_hex
    str1 = md5(bytes.fromhex(t_str)).hexdigest().upper()
    aes_key = key[0:16].encode('utf-8')
    aes_iv = str1[0:16].encode("utf-8")

    aes_data = aes.AEScryptor(aes_key, AES.MODE_CBC, aes_iv, paddingMode="ZeroPadding", characterSet='utf-8')
    rData = aes_data.encryptFromString(data)

    encryption_aes = rData.toBase64()

    print(encryption_aes)

    # print(key[15:32])

    # sm4_key = md5(bytes.fromhex(key[15:32])).hexdigest().upper()
    # sm4_iv = bytes.fromhex(str1[15:32])
    # key2 = bytes.fromhex("0123456789ABCDEFFEDCBA9876543210")  # 128bit密钥
    # key2 = bytes.fromhex(sm4_key)  # 128bit密钥
    # plaintext = bytes.fromhex(encryption_aes)  # 128bit明文
    # plaintext = bytes.fromhex("00112233445566778899aabbccddeeff")  # 128bit明文
    # SM4 = sm4.SM4Cipher(key2)
    # print(SM4.encrypt(plaintext).hex())  # 09325c4853832dcb9337a5984f671b9a


# heartbeat()
encryption_data()
