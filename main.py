""" Simple Shop """
import base64
import binascii
from ast import literal_eval
import db

# Default vars
appdata_path = 'data.appdata'

prd_list = [
    {"name":"sib", "price":12_000, "description":"A delicious fruit", "sell_count":9, "seller":"Mive va tarebar e Avang"},
    {"name":"medad", "price":9_000, "description":"Pencil.", "sell_count":7, "seller":"Lavazem tahrir e mamad"},
    {"name":"gheychi", "price":25_000, "description":"scissors!", "sell_count":16, "seller":"Bahman chaman zan"},
    {"name":"noshabe", "price":37_000, "description":"A delicious drink", "sell_count":4, "seller":"Super market Arshia"}
]

users_list = {
#   "USERNAME":{"name":"DISPLAY_NAME", "pass":"ENCRYPTED_PASSWORD"}
    "parsa1":{"name":"Parsa", "pass":"1234"}
}

# Functions
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

def appdata_iskeyexist(key):
    file = read_file(appdata_path)
    data:dict = literal_eval(dec(file))
    return not data.get(key, False) == False

def appdata_write(key, value):
    file = read_file(appdata_path)
    data:dict = literal_eval(dec(file))
    data[key] = value
    write_file(appdata_path, str(enc(str(data)))[2:-1])

def appdata_rem(key):
    file = read_file(appdata_path)
    data:dict = literal_eval(dec(file))
    data.pop(key)
    write_file(appdata_path, str(enc(str(data)))[2:-1])

def appdata_read(key):
    data = literal_eval(dec(read_file(appdata_path)))
    write_file(appdata_path, str(enc(str(data)))[2:-1])
    return data[key]

def iskeyindict(dic, key):
    return key in dic.keys()

def print_prd(num):
    """ prints the products list """
    if len(prd_list) < 5:
        prdlst_cut = prd_list
    else:
        prdlst_cut = prd_list[num*5-5:num*5]

    for i in prdlst_cut:
        name = i['name']
        price = str(i['price'])
        desc = i['description']
        sell_count = i['sell_count']
        seller = i['seller']

        print(f"""==========
{name} | bought {sell_count} times | {price}$
{desc}
{seller}""")
    print('='*10)

# Actual program
# 6533303d
if __name__ == '__main__':
    if appdata_iskeyexist('name'):
        print(f'Hello, {appdata_read("name")}!')
    else:
        appdata_write('name', input('What\'s your name? '))
    print('Welcome!')
    print_prd(1)
