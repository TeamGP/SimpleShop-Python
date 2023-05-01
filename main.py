""" Simple Shop """
from sys import exit as safeExit   # General
from os import path as fpath       # if File is exists
from os import remove as fremove   # Remove a file
from csv import DictReader,reader  # CSV Reader
from ast import literal_eval       # String dict to Dict
import random as rand              # To generate the terminal code for payment
import webbrowser as wb            # open the checkout page
from requests import get           # Getting the image
import border as b                 # local lib for table border
import db                          # local lib for loading the database
from texttable import Texttable    # Print The table
from climage import convert as i2t # Print Image in Terminal
import pickle                      # Load and save file config     
print("Loading...")

# Default vars
appdata_path:str = 'data.appdata'
pickle_path = "data.pickle"
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

# Classes
class File:
    def __init__(self, path):
        self.path = path
    @property
    def content(self):
        with open(self.path, "r", encoding='utf8') as f:
            return f.read()
    @content.setter
    def content(self, new_content):
        with open(self.path, "w", encoding='utf8') as f:
            return f.write(new_content)

class Appdata:
    def __init__(self, path):
        if not fpath.isfile(pickle_path):
            with open(pickle_path, 'wb') as f:
                return pickle.dump({}, f, pickle.HIGHEST_PROTOCOL)
        self.path = path

    @property
    def content(self):
        with open(pickle_path, 'rb') as f:
            return pickle.load(f)

    @content.setter
    def content(self, new_content):
        with open(pickle_path, 'wb') as f:
            return pickle.dump(new_content, f, pickle.HIGHEST_PROTOCOL)
    
    def isKeyExists(self, key):
        with open(pickle_path, 'rb') as f:
            loaded_data = pickle.load(f)
            if isinstance(loaded_data, dict):
                return key in loaded_data.keys()
            else:
                raise TypeError(f"The data is not \"dict\", it\'s {type(loaded_data)}")

    def getKey(self, key):
        return self.content[key]

    def setKey(self, key, value):
        data:dict = self.content
        data[key] = value
        self.content = data

    def remKey(self, key):
        data:dict = self.content
        data.pop(key)
        self.content = data

# Functions
def printimage(path):
    ''' converts the image to print in terminal\n inform of ANSI Escape codes '''
    print(climage.convert(path, is_256color=True))

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
    appdata = Appdata(pickle_path)
    if appdata.isKeyExists('name'):
        print(f'Hello, {appdata.getKey("name")}!')
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
                    buylst:dict = appdata.getKey("buylist")
                    buylst.append(pid)
                    appdata.setKey("buylist", buylst)
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
                    response = get(pimg, timeout=1000)
                    if response.status_code:
                        fn = "tmp.png"
                        with open(fn, 'wb') as fp:
                            fp.write(response.content)
                    printimage(fn)
                    fremove(fn)
                    print(f"""{b.dr} {pname} {pprice}T\n\n{b.ud} {pdesc}\n{b.ur} {psellc} times | Seller: {pseller}""")

                else:
                    print("Wrong Id. Try again.")
                    continue
            else:
                print("Please type the product id.")
                continue

        #@buylist command
        elif c1[:7] == 'buylist' or c1[:8] == 'buy list' or c1[:8] == 'buy-list' or c1[:8] == 'buy_list':
            if not appdata.isKeyExists('name'):
                print("You must login to use this feature!")
                continue

            buylst = appdata.getKey("buylist")
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

                buylst:list = appdata.getKey("buylist")
                all_price=0
                for i in buylst:
                    all_price+=int(prd_list[i]["price"])

                wb.open(f"http://localhost/payment/?terminal={terminal}&site=github.com/parsa-gp&pazirande=123456&name=ParsaGP&price={all_price}", new=0, autoraise=True)
                
                checkout_completed=False

                while not checkout_completed:
                    requ=get(f"http://localhost/payment/status/{terminal}", timeout=5)
                    if requ.status_code==200:
                        if requ.text=="true":
                            checkout_completed=True
                
                if checkout_completed:
                    appdata.setKey("buylist", [])
                    print("Payment was successful!")
                else:
                    print("You canceled the payment!")

        #@remove command
        elif c1[:6] == 'remove':
            if not appdata.isKeyExists('name'):
                print("You must login to use this feature!")

            if len(c1)>4:
                pid = int(c1[7:])
                buylst:dict = appdata.getKey("buylist")
                if pid in buylst:
                    buylst.remove(pid)
                    appdata.setKey("buylist", buylst)
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
            if appdata.isKeyExists("name"):
                print("You are already logged in to the system. you don\'t need to login again.")
                continue
            print('You can exit the login menu by typing "exit" in the "What\'s your username" section.')
            
            while True:
                    lu = input(f'{b.ud} What\'s your username? ')
                    
                    if lu == 'debug':
                        _ = File(db.db_path)
                        print(literal_eval(dec(_.content)))
                        continue
                    if lu == 'exit':
                        safeExit()

                    if db.iskeyexist(lu):
                        lp = input(f'{b.ud} What\'s your password, {lu}? ')
                        if db.read(lu)['pass'] == lp:
                            print(f"{b.ur} Correct! Logging in...")
                            appdata.setKey('name', db.read(lu)["name"])
                            appdata.setKey('username', lu)
                            appdata.setKey("buylist", [])
                            break
                        print(f'{b.ur} The Password is incorrect.')
                        continue
                    print(f'{b.ur} The Username is incorrect.')
                    continue

        #@signup command
        elif c1 == 'signup':
            if not appdata.isKeyExists("name"):
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
                    appdata.setKey('name', sn)
                    appdata.setKey('username', su)
                    appdata.setKey("buylist", [])
                    break
                print(f'{b.ur} The username is already taken.')
                continue
            print(f'{b.ur} The passwords is not the same.')
            continue

        #@logout command
        elif c1 == "logout":
            if not appdata.isKeyExists('name'):
                print("You must login to use this feature!")

            if input("Are you sure about that? (y,n)").lower() == 'y':
                appdata.remKey("name")
                appdata.remKey("username")
                appdata.remKey("buylist")
                safeExit()
            else:
                continue

        #@delacc command
        elif c1 == "delacc":
            if not appdata.isKeyExists('name'):
                print("You must login to use this feature!")

            if input("Are you sure about that? (y,n)").lower() == 'y':
                db.rem(appdata.getKey("username"))
                appdata.remKey("name")
                appdata.remKey("username")
                appdata.remKey("buylist")
                safeExit()
            continue

        #@exit command
        elif c1 == "exit":
            safeExit()

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
