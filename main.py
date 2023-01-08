""" Simple Shop """
import base64
import binascii
import sys
from ast import literal_eval
import border as b
import db

# Default vars
appdata_path:str = 'data.appdata'

prd_list:list = [
    {"name":"sib", "price":28_000, "description":"A delicious fruit", "sell_count":9, "seller":"Mive va tarebar e Avang"},
    {"name":"medad", "price":4_000, "description":"Pencil.", "sell_count":7, "seller":"Lavazem tahrir e mamad"},
    {"name":"gheychi", "price":200_000, "description":"scissors!", "sell_count":16, "seller":"Bahman chaman zan"},
    {"name":"mug", "price":59_000, "description":"livan but MOHKAM", "sell_count":3, "seller":"zarf & zorofe mamadi"},
    {"name":"chips (chili)", "price":9_600, "description":"chips chasp SOS", "sell_count":46, "seller":"Super market Arshia"},
    {"name":"pofak", "price":13_500, "description":"polimere to por", "sell_count":38, "seller":"Super market Arshia"},
    {"name":"mohz", "price":44_200, "description":"khiyare zard", "sell_count":8, "seller":"Mive va tarebar e Avang"},
    {"name":"rob e anar", "price":159_000, "description":"Torshak level 2", "sell_count":13, "seller":"Mive va tarebar e Avang"},
    {"name":"narengi", "price":35_000, "description":"porteghale kochik", "sell_count":4, "seller":"Mive va tarebar e Avang"},
    {"name":"ravan nevis", "price":16_000, "description":"Khodkar lvl 2", "sell_count":18, "seller":"lavazem tahririye yaser"},
    {"name":"bastani arosaki", "price":7_000, "description":"hichvaght mesle coveresh nemishe :(", "sell_count":35, "seller":"Super market Arshia"},
    {"name":"dough e ab-ali", "price":14_800, "description":"gaz dar", "sell_count":21, "seller":"Super market Arshia"},
    {"name":"joorab", "price":29_000, "description":"pif pif!", "sell_count":62, "seller":"poshake vaziri"},
    {"name":"estaminofen", "price":72_500, "description":"daroo", "sell_count":95, "seller":"darokhoneye kazemi"},
    {"name":"ghooti noshabe", "price":9_600, "description":"A delicious drink", "sell_count":4, "seller":"Super market Arshia"}
]

# Functions
def enc(text:str) -> str:
    """ Encode the given text to base64 """
    # https://www.scopulus.co.uk/tools/hexconverter.htm
    # convert to BASE64
    b64_bytes = base64.b64encode(text.encode('ascii'))
    # convert to HEX-ASCII and return the result
    return binascii.hexlify(b64_bytes.decode('ascii').encode())

def dec(text:str) -> str:
    """ Encode the given text to base64 """
    hex_bytes = bytearray.fromhex(text).decode()
    return base64.b64decode(hex_bytes).decode()

def read_file(path:str) -> str:
    """ Read and return the file text """
    with open(path, encoding='utf8') as file:
        return file.read()

def write_file(path:str, text:str) -> int:
    """ Write text to the given file """
    with open(path, 'w', encoding='utf8') as file:
        return file.write(text)

def appdata_iskeyexist(key:str) -> bool:
    """ Check if key is in appdata """
    file = read_file(appdata_path)
    data:dict = literal_eval(dec(file))
    return key in data.keys()

def appdata_write(key:str, value:str) -> None:
    """ Write value from appdata """
    file = read_file(appdata_path)
    data:dict = literal_eval(dec(file))
    data[key] = value
    write_file(appdata_path, str(enc(str(data)))[2:-1])

def appdata_rem(key:str) -> None:
    """ Remove value from appdata """
    file = read_file(appdata_path)
    data:dict = literal_eval(dec(file))
    data.pop(key)
    write_file(appdata_path, str(enc(str(data)))[2:-1])

def appdata_read(key:str) -> str:
    """ Read value from appdata """
    data = literal_eval(dec(read_file(appdata_path)))
    write_file(appdata_path, str(enc(str(data)))[2:-1])
    return data[key]

def print_prd(num:int=1, sort:str="", rev_sort:bool=False) -> str:
    """ prints the products list """
    if sort == "":
        prdlist = prd_list[:]
    else:
        if sort == "name":
            prdlist = sorted(prd_list, key=lambda d: d['name'], reverse=rev_sort) 

        elif sort == "price":
            prdlist = sorted(prd_list, key=lambda d: d['price'], reverse=rev_sort) 

        elif sort == "sell count":
            prdlist = sorted(prd_list, key=lambda d: d['sell_count'], reverse=rev_sort) 
        

    if len(prd_list) < 5:
        prdlst_cut = prdlist[:]
    else:
        prdlst_cut = prdlist[num*5-5:num*5]

    output:str=''
    longstrlen:int = 0
    longnumlen:int = 0
    for l in prdlst_cut:
        name:str = l['name']
        price:str = str(l['price'])
        if len(f"{name} {price}T") > longstrlen:
            longstrlen = len(f"{name} {price}T")
        if len(str(prd_list.index(l))) > longnumlen:
            longnumlen = len(str(prd_list.index(l)))
    longstrlen+=2

    for j in prdlst_cut:
        name:str = j['name']
        price:str = str(j['price'])
        prid:str = prd_list.index(j)
        namelen = longstrlen - len(f"{name} {price}") - 2
        output+=f"\n{b.ud} {prid}{' '*(longnumlen+1-len(str(prid)))}{b.ud} {name} {price}T{' '*namelen}{b.ud}\n{b.udr}{b.lr*(longnumlen+2)}{b.udlr}{b.lr*longstrlen}{b.udl}"
    cutlen = -(len(str(prid)) + longstrlen+6)
    output=output[:cutlen]
    print(f"{b.dr}{b.lr*(len(str(prid))+longnumlen+1)}{b.dlr}{b.lr*longstrlen}{b.dl}\n"+output.strip()+f"\n{b.ur}{b.lr*(len(str(prid))+longnumlen+1)}{b.ulr}{b.lr*longstrlen}{b.ul}")

# Actual program
# 6533303d
# {'parsa1': {'name': 'Parsa', 'pass': '1234'}}
if __name__ == '__main__':
    if appdata_iskeyexist('name'):
        print(f'Hello, {appdata_read("name")}!')
    else:
        while True:
            inpl=input(f"{b.dr} l=Login s=Signup > ").lower()
            if inpl == "l":
                lu = input(f'{b.ud} What\'s your username? ')
                if db.iskeyexist(lu):
                    lp = input(f'{b.ud} What\'s your password, {lu}? ')
                    if db.read(lu)['pass'] == lp:
                        print(f"{b.ur} Correct! Logging in...")
                        appdata_write('name', db.read(lu)["name"])
                        appdata_write('username', lu)
                        appdata_write("buylist", [])
                        break
                    print(f'{b.ur} The Password is incorrect.')
                else:
                    print(f'{b.ur} The Username is incorrect.')
            elif inpl == 's':
                su = input(f'{b.ud} Type your username: ')
                sp1 = input(f'{b.ud} Type your password: ')
                sp2 = input(f'{b.ud} Type your password, again: ')
                if sp1==sp2:
                    if not db.iskeyexist(su):
                        sn = input(f'{b.ud} Type your display name: ')
                        db.write(su, {"name":sn, "pass":sp1})
                        print(f"{b.ur} Logging in...")
                        appdata_write('name', sn)
                        appdata_write('username', su)
                        appdata_write("buylist", [])
                        break
                    print(f'{b.ur} The username is already taken.')
                else:
                    print(f'{b.ur} The passwords is not the same.')
            elif inpl == 'debug':
                print(literal_eval(dec(read_file(db.db_path))))

            elif inpl == 'e':
                sys.exit()

    print('Welcome!')
    print_prd(1)
    while True:
        c1 = input("What to do? ")

        if c1[:3] == 'add':
            if len(c1)>4:
                pid = int(c1[4:])
                if pid < len(prd_list):
                    buylst:dict = appdata_read("buylist")
                    buylst.append(pid)
                    appdata_write("buylist", buylst)
                    pname = prd_list[pid]["name"]
                    print(f"The {pname} has successfully added.")
                else:
                    print("Wrong Id. Try again.")
            else:
                print("Please put the product id.")

        elif c1[:4] == 'info':
            if len(c1)>4:
                pid = int(c1[5:])
                if pid < len(prd_list):
                    pname   = prd_list[pid]["name"]
                    pprice  = prd_list[pid]["price"]
                    pdesc   = prd_list[pid]["description"]
                    psellc  = prd_list[pid]["sell_count"]
                    pseller = prd_list[pid]["seller"]
                    print(f"""{b.dr} {pname} {pprice}T
{b.ud} {pdesc}
{b.ur} {psellc} times | Seller: {pseller}""")

                else:
                    print("Wrong Id. Try again.")
            else:
                print("Please type the product id.")

        elif c1[:4] == 'list':
            buylst = appdata_read("buylist")
            o:str=''
            a:str=0
            for i in buylst:
                o+=f"\n{i} | "+prd_list[i]["name"]
                a+=prd_list[i]["price"]
            print(o.strip())
            print(f"The sum of all products: {a}")

        elif c1[:4] == 'page':
            if len(c1)>4:
                print_prd(int(c1[5:]))
            else:
                print("Please put the page number.")

        elif c1[:4] == 'sort':
            if len(c1)>4:
                args = c1.split()
                if len(args) == 2:
                    print_prd(1, args[1])
                elif len(args) == 3:
                    print_prd(1, args[1], bool(args[2]))
                else:
                    print("Wrong arg. Try again.")
            else:
                print("Please put the page number.")

        elif c1[:6] == 'remove':
            if len(c1)>4:
                pid = int(c1[7:])
                buylst:dict = appdata_read("buylist")
                if pid in buylst:
                    buylst.remove(pid)
                    appdata_write("buylist", buylst)
                    pname = prd_list[pid]["name"]
                    print(f"The {pname} has successfully removed.")
                else:
                    print("Wrong Id. Try again.")
            else:
                print("Please put the product id.")

        elif c1 == "logout":
            appdata_rem("name")
            appdata_rem("buylist")
            sys.exit()

        elif c1 == "delacc":
            if input("Are you sure about that? (y, n)").lower() == 'y':
                db.rem(appdata_read("username"))
                appdata_rem("name")
                appdata_rem("username")
                appdata_rem("buylist")
                sys.exit()

        elif c1 == "exit":
            sys.exit()

        elif c1 == "helpme":
            print(f'''
{b.dr} command (required) [additional]
{b.ud} 
{b.ud} Command         {b.ud} Description
{b.udr}{b.lr*17}{b.udlr}{b.lr*48}
{b.ud} add (prod id)   {b.ud} Add a product to Buy list.
{b.ud} list            {b.ud} Show the Buy list.
{b.ud} info (prod id)  {b.ud} Show more detail about given product.
{b.ud} page (page num) {b.ud} Scrolling through the list of products.
{b.ud} remove (prodid) {b.ud} Remove a product from Buy list.
{b.ud} logout          {b.ud} Logout from System.
{b.ud} delacc          {b.ud} Delete the Account from System.
{b.ud} exit            {b.ud} Exit from app.
{b.ur} helpme          {b.ud} Show this thing.'''.strip())
