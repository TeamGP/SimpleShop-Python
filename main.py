import base64

def enc_b64(text):
    t_bytes = text.encode('ascii')
    b64_bytes = base64.b64encode(t_bytes)
    return b64_bytes.decode('ascii')

prd_list = [
    {"name":"sib", "price":12_000, "description":"A delicious fruit", "sell_count":9, "seller":"Mive va tarebar e Avang"},
    {"name":"medad", "price":9_000, "description":"Pencil.", "sell_count":7, "seller":"Lavazem tahrir e mamad"},
    {"name":"gheychi", "price":25_000, "description":"scissors!", "sell_count":16, "seller":"Bahman chaman zan"},
    {"name":"noshabe", "price":37_000, "description":"A delicious drink", "sell_count":4, "seller":"Super market Arshia"}
]
users_list = {
    "parsa1":{"name":"Parsa", "pass":"1234"}
}

def print_prd(num):
    """ prints the products list """
    if len(prd_list) < 10:
        prdlst_cut = prd_list
    else:
        prdlst_cut = prd_list[num*10-10:num*10]

    for i in prdlst_cut:
        name = i['name']
        price = str(i['price'])
        desc = i['description']
        sell_count = i['sell_count']
        seller = i['seller']

        print(f"""==========
{name} | bought {sell_count} times | {price}$
{desc}
{seller}
""")
    print('='*10)
print_prd(1)