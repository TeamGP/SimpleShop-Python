""" DB """
import base64
import binascii
from ast import literal_eval

db_path = 'db/db'

def enc(text):
    """ Encode the given text to base64 """
    # https://www.scopulus.co.uk/tools/hexconverter.htm
    # convert to BASE64
    b64_bytes = base64.b64encode(text.encode('ascii'))
    # convert to HEX-ASCII and return the result
    return binascii.hexlify(b64_bytes.decode('ascii').encode())

def dec(text):
    """ Encode the given text to base64 """
    hex_bytes = bytearray.fromhex(text).decode()
    return base64.b64decode(hex_bytes).decode()

def read_file(path):
    """ Read and return the file text """
    with open(path, encoding='utf8') as file:
        return file.read()

def write_file(path, text):
    """ Write text to the given file """
    with open(path, 'w', encoding='utf8') as file:
        return file.write(text)

def iskeyexist(key):
    file = read_file(db_path)
    data:dict = literal_eval(dec(file))
    return not data.get(key, False) == False

def write(key, value):
    file = read_file(db_path)
    data:dict = literal_eval(dec(file))
    data[key] = value
    write_file(db_path, str(enc(str(data)))[2:-1])

def rem(key):
    file = read_file(db_path)
    data:dict = literal_eval(dec(file))
    data.pop(key)
    write_file(db_path, str(enc(str(data)))[2:-1])

def read(key):
    data = literal_eval(dec(read_file(db_path)))
    write_file(db_path, str(enc(str(data)))[2:-1])
    return data[key]

def iskeyindict(dic, key):
    return key in dic.keys()
