""" Simple Shop """
import base64
import binascii
from ast import literal_eval
import border
import db

# Default vars
appdata_path = 'data.appdata'


prd_list:list = [
    {"name":"sib", "price":12_000, "description":"A delicious fruit", "sell_count":9, "seller":"Mive va tarebar e Avang"},
    {"name":"medad", "price":9_000, "description":"Pencil.", "sell_count":7, "seller":"Lavazem tahrir e mamad"},
    {"name":"gheychi", "price":25_000, "description":"scissors!", "sell_count":16, "seller":"Bahman chaman zan"},
    {"name":"noshabe", "price":37_000, "description":"A delicious drink", "sell_count":4, "seller":"Super market Arshia"}
]

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
        prdlst_cut = prd_list[:]
    else:
        prdlst_cut = prd_list[num*5-5:num*5]

    for i in prdlst_cut:
        name = i['name']
        price = str(i['price'])
        pid = prd_list.index(i)
        print(f"""==========\n{pid} | {name} {price}T""")
    print('='*10)

# Actual program
# 6533303d
# {'parsa1': {'name': 'Parsa', 'pass': '1234'}}
if __name__ == '__main__':
    if appdata_iskeyexist('name'):
        print(f'Hello, {appdata_read("name")}!')
    else:
        while True:
            inpl=input(f"{border.dr} l=Login s=Signup > ").lower()
            if inpl == "l":
                lu = input(f'{border.ud} What\'s your username? ')
                if db.iskeyexist(lu):
                    lp = input(f'{border.ud} What\'s your password, {lu}? ')
                    if db.read(lu)['pass'] == lp:
                        print(f"{border.ur} Correct! Logging in...")
                        appdata_write('name', db.read(lu)["name"])
                        appdata_write('username', lu)
                        appdata_write("buylist", [])
                        break

                    else:
                        print(f'{border.ur} The Password is incorrect.')
                else:
                    print(f'{border.ur} The Username is incorrect.')
            elif inpl == 's':
                su = input(f'{border.ud} Type your username: ')
                sp1 = input(f'{border.ud} Type your password: ')
                sp2 = input(f'{border.ud} Type your password, again: ')
                if sp1==sp2:
                    if not db.iskeyexist(su):
                        sn = input('{border.ud} Type your display name: ')
                        db.write(su, {"name":sn, "pass":sp1})
                        print(f"{border.ur} Logging in...")
                        appdata_write('name', sn)
                        appdata_write('username', su)
                        appdata_write("buylist", [])
                        break
                    else:
                        print(f'{border.ur} The username is already taken.')
                else:
                    print(f'{border.ur} The passwords is not the same.')
            elif inpl == 'debug':
                print(literal_eval(dec(read_file(db.db_path))))

            elif inpl == 'e':
                exit()

    print('Welcome!')
    print_prd(1)
    while True:
        c1 = input("What to do? ")

        if c1[:3] == 'add':
            pid = int(c1[4:])
            if pid < len(prd_list):
                buylst:dict = appdata_read("buylist")
                buylst.append(pid)
                appdata_write("buylist", buylst)
                pname = prd_list[pid]["name"]
                print(f"The {pname} has successfully added.")
            else:
                print("Wrong Id. Try again.")

        elif c1[:4] == 'list':
            buylst = appdata_read("buylist")
            o:str=''
            a:str=0
            for i in buylst:
                o+=f"\n{i} | "+prd_list[i]["name"]
                a+=prd_list[i]["price"]
            print(o.strip())
            print(f"The sum of all products: {a}")

        elif c1[:6] == 'remove':
            pid = int(c1[7:])
            buylst:dict = appdata_read("buylist")
            if pid in buylst:
                buylst.remove(pid)
                appdata_write("buylist", buylst)
                pname = prd_list[pid]["name"]
                print(f"The {pname} has successfully removed.")
            else:
                print("Wrong Id. Try again.")

        elif c1 == "logout":
            appdata_rem("name")
            appdata_rem("buylist")
            exit()

        elif c1 == "delacc":
            if input("Are you sure about that? (y, n)").lower() == 'y':
                db.rem(appdata_read("username"))
                appdata_rem("name")
                appdata_rem("username")
                appdata_rem("buylist")
                exit()

        elif c1 == "exit":
            exit()

        elif c1 == "helpme":
            print('''
command (required) [additional]

Command         | Description
____________________________________________
add (prod id)   | Add a product to Buy list
list            | Show the Buy list
remove (prodid) | Remove a product from Buy list
logout          | Logout from System
delacc          | Delete the Account from System
exit            | Exit from app
helpme          | Show this thing
                '''.strip())
