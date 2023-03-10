""" Simple Shop """
import base64                     # Encrypting
import binascii                   # Encrypting
import sys                        # General
import os                         # General
from csv import DictReader,reader # CSV Reader
from ast import literal_eval      # String dict to Dict
import random as rand             # To generate the terminal code for payment
import webbrowser as wb           # open the checkout page
import requests                   # Getting the image
import border as b                # local lib for table border
import db                         # local lib for loading the database
from texttable import Texttable   # Print The table
import climage                    # Print Image in Terminal
print("Loading...")

# Default vars
appdata_path:str = 'data.appdata'
prdata_path = 'db/products.csv'

with open(prdata_path, encoding="utf8") as f:
    prd_list = [*DictReader(f)]
with open(prdata_path, encoding="utf8") as fi:
    prdlist_lstInFor = list(reader(fi))

numb=0
prdlist_lst=[]
prdlist_lstInFor = prdlist_lstInFor[1:]
for pinfo in prdlist_lstInFor:
    ls=[numb]
    ls.extend(pinfo[:3])
    prdlist_lst.append(ls)
    numb+=1

# Functions
def printimage(path):
    ''' converts the image to print in terminal
     inform of ANSI Escape codes '''
    print(climage.convert(path, is_256color=True))

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

def print_prd(num:int=1, sort:str="", rev_sort:bool=False, count=10):
    """ prints the products list """
    if num > (len(prd_list)//count):
        print('The page number is too large.')
        return

    if sort=="":
        prdlist_sorted=prdlist_lst[:]
    else:
        if sort == "price":
            prdlist_sorted = sorted(prdlist_lst, key=lambda d: int(d[2]), reverse=rev_sort)
        elif sort in("sell count", "sellcount"):
            prdlist_sorted = sorted(prdlist_lst, key=lambda d: int(d[3]), reverse=rev_sort)
        else:
            prdlist_sorted = prdlist_lst[:]

    if len(prd_list) < count:
        prdlst_cut = prdlist_sorted[:]
    else:
        prdlst_cut = prdlist_sorted[num*count-count : num*count]

    prdlst_cut.insert(0,["ID", "Name", "Price", "Sell Count"])

    print("Page "+str(num)+"\n=== === === === ===")

    table = Texttable()
    table.set_deco(Texttable.HEADER)
    table.set_cols_dtype(['i', 't', 't', 'i'])
    # 't' = text
    # 'f' = float (decimal)
    # 'e' = float (exponent)
    # 'i' = integer
    # 'a' = automatic

    table.set_cols_align(["l", "l", "l", "l"])
    table.add_rows(prdlst_cut)
    print("\n"+table.draw()+"\n")

print("=== === === === ===")
# Actual program
# 6533303d
# {'parsa1': {'name': 'Parsa', 'pass': '1234'} ...}
if __name__ == '__main__':
    if appdata_iskeyexist('name'):
        print(f'Hello, {appdata_read("name")}!')
    else:
        print("You must login to use some other features!")

    print('Welcome!\n To see all commands, type "helpme".')
    print_prd(1)
    while True:
        c1 = input("What to do? ")
        
        #@add command
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
                    continue
            else:
                print("Please put the product id.")
                continue

        #@info command
        elif c1[:4] == 'info':

            if len(c1)>4:
                pid = int(c1[5:])
                if pid < len(prd_list):
                    pname   = prd_list[pid]["name"]
                    pprice  = prd_list[pid]["price"]
                    pdesc   = prd_list[pid]["description"]
                    psellc  = prd_list[pid]["sell_count"]
                    pseller = prd_list[pid]["seller"]
                    pimg    = prd_list[pid]["imgurl"]
                    response = requests.get(pimg, timeout=1000)
                    if response.status_code:
                        fn = "tmp.png"
                        with open(fn, 'wb') as fp:
                            fp.write(response.content)
                    printimage(fn)
                    os.remove(fn)
                    print(f"""{b.dr} {pname} {pprice}T\n\n{b.ud} {pdesc}\n{b.ur} {psellc} times | Seller: {pseller}""")

                else:
                    print("Wrong Id. Try again.")
                    continue
            else:
                print("Please type the product id.")
                continue

        #@buylist command
        elif c1[:7] == 'buylist' or c1[:8] == 'buy list' or c1[:8] == 'buy-list' or c1[:8] == 'buy_list':
            if not appdata_iskeyexist('name'):
                print("You must login to use this feature!")
                continue

            buylst = appdata_read("buylist")
            o:str=''
            a:str=0
            for i in buylst:
                o+=f"\n{i} | "+prd_list[i]["name"]
                a+=int(prd_list[i]["price"])
            print(o.strip())
            print(f"The sum of all products: {a}")

        #@page command
        elif c1[:4] == 'page':
            if len(c1)>4:
                print_prd(int(c1[5:]))
            else:
                print("Please put the page number.")

        #@sort command
        elif c1[:4] == 'sort':
            print("EXPERIMENTAL FEATURE!!")
            if len(c1)>4:
                args = c1.split()

                if len(args) == 2:
                    print_prd(1, args[1])

                elif len(args) == 3:
                    if args[2] == 'asc':
                        print_prd(1, args[1], False)
                    elif args[2] == 'des':
                        print_prd(1, args[1], True)
                    else:
                        print_prd(1, args[1])

                elif len(args) == 4:
                    if args[2] == 'asc':
                        sortmet = False
                    elif args[2] == 'des':
                        sortmet = True
                    else:
                        print_prd(args[3], args[1])
                    print_prd(args[3], args[1], sortmet)
                else:
                    print("Wrong arg. Try again.")
                    continue
            else:
                print("Please put the page number.")
                continue

        #@checkout command
        elif c1 == "checkout":
            print("INCOMPLETE. for now, focusing in other things.")
            c2 = input("Are you sure about that(Yes/No)?").lower()
            if c2 == "yes":
                terminal=rand.randint(1000000, 9999999)

                buylst:list = appdata_read("buylist")
                all_price=0
                for i in buylst:
                    all_price+=int(prd_list[i]["price"])

                wb.open(f"http://localhost/payment/?terminal={terminal}&site=github.com/parsa-gp&pazirande=123456&name=ParsaGP&price={all_price}", new=0, autoraise=True)
                
                checkout_completed=False

                while not checkout_completed:
                    requ=requests.get(f"http://localhost/payment/status/{terminal}", timeout=5)
                    if requ.status_code==200:
                        if requ.text=="true":
                            checkout_completed=True
                
                if checkout_completed:
                    appdata_write("buylist", [])
                    print("Payment was successful!")
                else:
                    print("You canceled the payment!")

        #@remove command
        elif c1[:6] == 'remove':
            if not appdata_iskeyexist('name'):
                print("You must login to use this feature!")

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
                    continue
            else:
                print("Please put the product id.")
                continue

        #@login command
        elif c1 == 'login':
            if appdata_iskeyexist("name"):
                print("You are already logged in to the system. you don\'t need to login again.")
                continue
            print('You can exit the login menu by typing "exit" in the "What\'s your username" section.')
            
            while True:
                    lu = input(f'{b.ud} What\'s your username? ')
                    
                    if lu == 'debug':
                        print(literal_eval(dec(read_file(db.db_path))))
                        continue
                    if lu == 'exit':
                        sys.exit()

                    if db.iskeyexist(lu):
                        lp = input(f'{b.ud} What\'s your password, {lu}? ')
                        if db.read(lu)['pass'] == lp:
                            print(f"{b.ur} Correct! Logging in...")
                            appdata_write('name', db.read(lu)["name"])
                            appdata_write('username', lu)
                            appdata_write("buylist", [])
                            break
                        print(f'{b.ur} The Password is incorrect.')
                        continue
                    print(f'{b.ur} The Username is incorrect.')
                    continue

        #@signup command
        elif c1 == 'signup':
            if not appdata_iskeyexist("name"):
                print("You are already logged in to the system. you don\'t need to login again.")
                continue
            print('You can exit the login menu by typing "exit" in the "What\'s your username" section.')

            su = input(f'{b.ud} Type your username: ')
            sp1 = input(f'{b.ud} Type your password: ')
            sp2 = input(f'{b.ud} Type your password, again: ')
            if sp1==sp2:
                if not db.iskeyexist(su):
                    sn = input(f'{b.ud} Type your display name: ')
                    db.write(su, {"name":sn, "pass":sp1})
                    print(f"{b.ur} Signed up! Logging in...")
                    appdata_write('name', sn)
                    appdata_write('username', su)
                    appdata_write("buylist", [])
                    break
                print(f'{b.ur} The username is already taken.')
                continue
            print(f'{b.ur} The passwords is not the same.')
            continue

        #@logout command
        elif c1 == "logout":
            if not appdata_iskeyexist('name'):
                print("You must login to use this feature!")

            if input("Are you sure about that? (y,n)").lower() == 'y':
                appdata_rem("name")
                appdata_rem("username")
                appdata_rem("buylist")
                sys.exit()
            else:
                continue

        #@delacc command
        elif c1 == "delacc":
            if not appdata_iskeyexist('name'):
                print("You must login to use this feature!")

            if input("Are you sure about that? (y,n)").lower() == 'y':
                db.rem(appdata_read("username"))
                appdata_rem("name")
                appdata_rem("username")
                appdata_rem("buylist")
                sys.exit()
            continue

        #@exit command
        elif c1 == "exit":
            sys.exit()

        #@helpme command
        elif c1 == "helpme":
            print(f'''
{b.dr} command (required) [additional]
{b.ud} 
{b.ud} Command(*=Need Acc)             {b.ud} Description
{b.udr}{b.lr*33}{b.udlr}{b.lr*45}
{b.ud} - Account Settings:             {b.ud}
{b.ud} login                           {b.ud} Login to System.
{b.ud} signin                          {b.ud} Sign in to System.
{b.ud} logout*                         {b.ud} Logout from System.
{b.ud} delacc*                         {b.ud} Delete the Account from System.
{b.ud}                                 {b.ud} 
{b.ud} buylist*                        {b.ud} Show the Buy list.
{b.ud} info (prod id)                  {b.ud} Show more detail about given product.
{b.ud} page (page num)                 {b.ud} Scrolling through the list of products.
{b.ud} sort (q) [asc/des] [PageNumber] {b.ud} Sort the product list. q=price / sellcount
{b.ud} add (prod id)*                  {b.ud} Add a product to Buy list.
{b.ud} remove (prod id)*                {b.ud} Remove a product from Buy list.
{b.ud} exit                            {b.ud} Exit from app.
{b.ur} helpme                          {b.ud} Show this thing.
'''.strip())
