import base64

def enc_b64(text):
    t_bytes = text.encode('ascii')
    b64_bytes = base64.b64encode(t_bytes)
    return b64_bytes.decode('ascii')

prd_list = [
    {"name":"sib", "price":12_000, "desription":"A delicious fruit", "sell_count":9, "seller":"Mive va tarebar e Avang"},
    {"name":"medad", "price":9_000, "desription":"Pencil.", "sell_count":7, "seller":"Lavazem tahrir e mamad"},
    {"name":"gheychi", "price":25_000, "desription":"scissors!", "sell_count":16, "seller":"Bahman chaman zan"},
    {"name":"noshabe", "price":37_000, "desription":"A delicious drink", "sell_count":4, "seller":"Super market Arshia"}
]
users_list = {
    "parsa1":{"name":"Parsa", "pass":"1234"}
}

if len(prd_list) < 10:
    print(prd_list)
else:
    print(prd_list[0:10])
