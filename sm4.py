from gmssl.sm4 import CryptSM4, SM4_ENCRYPT, SM4_DECRYPT
import base64

_key = b'3l5butlj26hvv313'
_value = b'111kkkl'  # bytes类型
_iv = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'  # bytes类型


#
# iv = '25F76FF022A0732A'
# value = base64.b64decode('7WnCpnhfHjunk6nWo+/5SA==')
# key = '6hcy!zAAHS_DT!T%'.encode('utf-8')


def encrypt_sm4(iv, value, key):
    iv = iv.encode('utf-8')
    value = base64.b64decode(value)
    key = key.encode('utf-8')

    crypt_sm4 = CryptSM4()
    # key = '{:032x}'.format(int(key.encode('utf-8'), 16))
    crypt_sm4.set_key(key, SM4_ENCRYPT)
    encrypt_value = crypt_sm4.crypt_cbc(iv, value)  # bytes类型
    return base64.b64encode(encrypt_value).decode()


def decrypt_sm4(iv, key, value):
    iv = iv.encode('utf-8')
    value = base64.b64decode(value)
    key = key.encode('utf-8')
    crypt_sm4 = CryptSM4()
    # key = '{:032x}'.format(int(key.encode('utf-8'), 16))
    crypt_sm4.set_key(key, SM4_DECRYPT)
    decrypt_value = crypt_sm4.crypt_cbc(iv,value)  # bytes类型
    # print(decrypt_value)
    return decrypt_value


'''
crypt_sm4.set_key(key, SM4_ENCRYPT)
encrypt_value = crypt_sm4.crypt_cbc(iv , value) #  bytes类型
crypt_sm4.set_key(key, SM4_DECRYPT)
decrypt_value = crypt_sm4.crypt_cbc(iv , encrypt_value) #  bytes类型
assert value == decrypt_value
'''

# encrypt_sm4(iv, value, key)
# decrypt_sm4(iv, key, encrypt_sm4(iv, value, key))

# encrypt_sm4("25F76FF022A0732A", "7WnCpnhfHjunk6nWo+/5SA==", "6hcy!zAAHS_DT!T%")
