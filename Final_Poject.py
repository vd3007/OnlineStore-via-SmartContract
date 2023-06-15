# -*- coding: utf-8 -*-
"""
Created on Mon Jun 12 16:44:00 2023

@author: Vincent
"""

all_item_dic = { " headphones "  : "1",
                 " microphone "  : "2",
                 " keyboard "  : "3",
                 " polaroid "  : "4",
                 " Switch "  : "5",
                 " PS5 "  : "6",
                 " earings "  : "7",
                 " rings "  : "8",
                 " watch "  : "9",
                 " necklace "  : "10",
                 " tote "  : "11",
                 " backpack "  : "12",
                 " wallet "  : "13",
                 " stachel "  : "14",
 }

from web3 import Web3

# 连接到以太坊节点
w3 = Web3(Web3.HTTPProvider('https://polygon-mumbai-bor.publicnode.com'))
# 读取合约ABI和地址
contract_address = '0x1939c2d09E9c0306B1A1c85686C7F15D874cFcaE'
# 在这里粘贴合约的ABI Remix Compilation Details -> Web3Deploy ( Line 1 )
contract_abi = [{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[{"internalType":"address","name":"walletAddress","type":"address"},{"internalType":"uint256","name":"productId","type":"uint256"}],"name":"checkBuyer","outputs":[{"internalType":"string","name":"","type":"string"},{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"productId","type":"uint256"}],"name":"checkStore","outputs":[{"internalType":"string","name":"","type":"string"},{"internalType":"uint256","name":"","type":"uint256"},{"internalType":"uint256","name":"","type":"uint256"},{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"uint256","name":"","type":"uint256"}],"name":"productBalances","outputs":[{"internalType":"uint256","name":"productId","type":"uint256"},{"internalType":"string","name":"name","type":"string"},{"internalType":"uint256","name":"balance","type":"uint256"},{"internalType":"uint256","name":"price","type":"uint256"},{"internalType":"string","name":"description","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"productId","type":"uint256"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"purchase","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"productId","type":"uint256"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"restock","outputs":[],"stateMutability":"nonpayable","type":"function"}]
# 加载合约
contract = w3.eth.contract(address=contract_address, abi=contract_abi)



#賣家錢包地址
acc_address = contract.functions.owner().call() 
#print ( account_address )





# 调用合约函数
# Check Customer address & Customer private key
def check () :
    interactive.delete ('1.0', 'end')
    
    global cus_address
    global cus_key
    cus_address = customer_address_input.get ()
    cus_key = customer_key_input.get ()
    
    transaction = contract.functions.purchase(15, 1).build_transaction({
        'from': cus_address,
        'nonce': w3.eth.get_transaction_count(cus_address),
        'gas': 200000,  # 设置足够的gas值
        'gasPrice': w3.to_wei('30', 'gwei')  # 设置合适的gas价格
    })
        
    try :
        w3.eth.account.sign_transaction(transaction, private_key=cus_key)
        interactive.insert ('end', "Your address and Your private key can match ~ \n")
    except :
        interactive.insert ('end', "Your address and Your private key can not match!!! \n")

# Restock  
def restock () :
    interactive.delete ('1.0', 'end')
    
    product = choose_item.get ()
    product_id = int ( all_item_dic [ product ] )   
    amount = int ( item_add_cnt.get () )
    
    if cus_address == acc_address :
        # 签署交易
        transaction = contract.functions.restock(product_id, amount).build_transaction({
            'from': acc_address,
            'nonce': w3.eth.get_transaction_count(acc_address),
            'gas': 200000,  # 设置足够的gas值
            'gasPrice': w3.to_wei('30', 'gwei')  # 设置合适的gas价格
        })
        # 发送交易
        signed_txn = w3.eth.account.sign_transaction(transaction, private_key=acc_key)
        tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        # 等待交易确认
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        
        interactive.insert ('end', f"You restock {amount} {product}. \n")
        interactive.insert ('end', f"Restock Transaction Hash: {tx_receipt['transactionHash'].hex()} \n")
    else :
        interactive.insert ('end', "You are not Shop Owner, so you can't Restock product !!! \n")

# Search Item Information
def shop_search () : 
    interactive.delete ('1.0', 'end')
    
    product = choose_item.get ()
    product_id = int ( all_item_dic [ product ] )
    store_info = contract.functions.checkStore( product_id ).call()
    
    price = int ( store_info[2] )/1000000000000000000
    
    item_balance_cnt.config ( text = store_info[1] )
    item_price_cnt.config ( text = price )
    item_description_line.config ( text = store_info[3] )
    
    interactive.insert ('end', f"You search {product} information in the shop. \n")

# Search Item Information
def payable () :
    interactive.delete ('1.0', 'end')
    
    product = choose_item.get ()
    product_id = int ( all_item_dic [ product ] )
    amount = int ( buyer_amount_cnt.get () )
    #payment = float ( buyer_payment_cnt.get () )
    
    store_info = contract.functions.checkStore( product_id ).call()
    price = int ( store_info[2] )/1000000000000000000
    price = price * amount
    #print ( price )
    
    try :
        # 签署交易
        transaction = contract.functions.purchase(product_id, amount).build_transaction({
            'from': cus_address,
            'nonce': w3.eth.get_transaction_count(cus_address),
            'gas': 200000,  # 设置足够的gas值
            'gasPrice': w3.to_wei('30', 'gwei'),  # 设置合适的gas价格
            'value': w3.to_wei(price, 'ether')  # 设置支付的以太币数量
        })
        # 发送交易
        signed_txn = w3.eth.account.sign_transaction(transaction, private_key=cus_key)
        tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        # 等待交易确认
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        
        interactive.insert ('end', f"You pay {price} ether for buy {amount} {product}.  \n")
        interactive.insert ('end', f"Purchase Transaction Hash: {tx_receipt['transactionHash'].hex()} \n")
    except :
        interactive.insert ('end', f"Your wallet hasn't enough money to buy {amount} {product} ({price} ether). \n")
    '''
    if payment >= price :
        dis = payment - price
        payment = payment - dis
        # 签署交易
        transaction = contract.functions.purchase(product_id, amount).build_transaction({
            'from': cus_address,
            'nonce': w3.eth.get_transaction_count(cus_address),
            'gas': 200000,  # 设置足够的gas值
            'gasPrice': w3.to_wei('30', 'gwei'),  # 设置合适的gas价格
            'value': w3.to_wei(payment, 'ether')  # 设置支付的以太币数量
        })
        # 发送交易
        signed_txn = w3.eth.account.sign_transaction(transaction, private_key=cus_key)
        tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        # 等待交易确认
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        
        interactive.insert ('end', f"You buy {amount} {product}, and find you {dis} ether.  \n")
        interactive.insert ('end', f"Purchase Transaction Hash: {tx_receipt['transactionHash'].hex()} \n")
    else :
        interactive.insert ('end', f"Your payment isn't enough to buy {amount} {product}. \n")
    '''
# Buyer Items Balance
def buy_own () :
    interactive.delete ('1.0', 'end')
    
    product = choose_item.get ()
    product_id = int ( all_item_dic [ product ] )
    
    buyer_info = contract.functions.checkBuyer( cus_address , product_id ).call()
    amount = buyer_info[1]
    
    buyer_balance_cnt.config ( text = amount  )
    
    interactive.insert ('end', f"You have {amount} {product}. \n")
    
#------------------------------------------------------------------------------------------------------------------------------
import tkinter as tk
from tkinter import ttk
from tkinter.font import Font
from PIL import Image, ImageTk

root = tk.Tk ()
root.title ( "Vending Store" )
window_width = 1920
window_height = 1000

# font , green , blue  
bold_font = Font ( family="Consolas" , size=11 , weight="bold" )
g = "#22B14C"
b = "#3F48CC"
#root.geometry ( "1300x1000" )



# Background Image
bg = Image.open ( 'D:\Vincent\Desktop\大學壓縮包\區塊鏈\Final\pic/001.jpg' )
bg = bg.resize( (window_width, window_height) )
bg_photo = ImageTk.PhotoImage ( bg )

# Item Image
item_img = []
for i in range ( 0 , 14 ) :
    path = 'pic/' + str ( i+1 ) + '.png'
    img = Image.open ( path )
    img = img.resize( (200, 200) )
    item_img.append ( ImageTk.PhotoImage ( img ) )



#創建畫布 建立控件
# Background
canvas = tk.Canvas ( root  , width = window_width , height = window_height  , highlightthickness = 0 )
canvas.create_image ( 0 , 0 , anchor="nw" , image = bg_photo )

# Shop Owner
shop_owner = tk.Label ( root , text = "Shop Owner Address :" , font = bold_font , bg="black", fg="white" )
account_address_label = tk.Label ( root , text = acc_address , font = bold_font , bg = g , fg="white" )

# Customer address
customer_address = tk.Label ( root , text = "Customer Address   :" , font = bold_font , bg="black", fg="white" )
customer_address_input = tk.Entry ( root , font = bold_font , insertbackground = 'blue' , highlightthickness = 2 )
# Customer key
customer_key = tk.Label ( root , text = "Customer Key       :" , font = bold_font , bg="black", fg="white" )
customer_key_input = tk.Entry ( root , font = bold_font , insertbackground = 'blue' , highlightthickness = 2 )

# Check Customer address & Customer private key
check_wallet = tk.Button ( root , text="Check" , command=check , font = bold_font , bg = b , fg="white" ) 

# Items 
item = tk.Label ( root , text = "Items :" , font = bold_font , bg="black", fg="white" )
choose_item = ttk.Combobox ( root , values = list ( all_item_dic.keys() ) )
choose_item.bind ( "<<ComboboxSelected>>" )
choose_item.configure ( font = bold_font )
# 選單內 字的大小
root.option_add ( "*TCombobox*Listbox*Font" , bold_font )

# Restock    
shop_restock = tk.Button ( root , text="Shop Restock" , command=restock , font = bold_font , bg = b , fg="white" ) 
item_add = tk.Label ( root , text = "Restock Quantity :" , font = bold_font , bg = "black" , fg="white" )
item_add_cnt = tk.Entry ( root , font = bold_font , insertbackground = 'blue' , highlightthickness = 2 )

# Search Item Information
search_information = tk.Button ( root , text="Search Information" , command=shop_search , font = bold_font , bg = b , fg="white" ) 
# Item Information
item_balance = tk.Label ( root , text = "Shop Stock       :" , font = bold_font , bg = "black" , fg="white" )
item_balance_cnt = tk.Label ( root , text = "" , font = bold_font , bg = g , fg="white" )
item_price = tk.Label ( root , text = "Item Price   :" , font = bold_font , bg="black", fg="white" )
item_price_cnt = tk.Label ( root , text = "" , font = bold_font , bg = g , fg="white" )
item_price_unit = tk.Label ( root , text = "ether" , font = bold_font , bg = g , fg="white" )
item_description = tk.Label ( root , text = "Item Description :" , font = bold_font , bg="black", fg="white" )
item_description_line = tk.Label ( root , text = "" , font = bold_font , bg = g , fg="white" )

# Buyer Payable
buyer_payable = tk.Button ( root , text="Buyer_Payable" , command=payable , font = bold_font , bg = b , fg="white" ) 
buyer_amount = tk.Label ( root , text = "Buyer Amount : " , font = bold_font , bg="black", fg="white" )
buyer_amount_cnt = tk.Entry ( root , font = bold_font , insertbackground = 'blue' , highlightthickness = 2 )
#buyer_payment = tk.Label ( root , text = "Buyer Payment : " , font = bold_font , bg="black", fg="white" )
#buyer_payment_cnt = tk.Entry ( root , font = bold_font , insertbackground = 'blue' , highlightthickness = 2 )
#buyer_payment_unit = tk.Label ( root , text = "ether" , font = bold_font , bg = g , fg="white" )

# Buyer Items Balance
buyer_information = tk.Button ( root , text="Search Buyer" , command=buy_own , font = bold_font , bg = b , fg="white"  ) 
buyer_balance = tk.Label ( root , text = "Buyer Balance : " , font = bold_font , bg="black", fg="white" )
buyer_balance_cnt = tk.Label ( root , text = "" , font = bold_font , bg = g , fg="white" )

# Interactive
interactive = tk.Text ( root , font = bold_font )
interactive.insert ('end', " ~~~ Welcome to Shop ~~~ \n")

# Item Name
item1_name = tk.Label ( root , text = " Headphones " , font = bold_font , bg="black", fg="white" )
item2_name = tk.Label ( root , text = " Microphone " , font = bold_font , bg="black", fg="white" )
item3_name = tk.Label ( root , text = " Keyboard " , font = bold_font , bg="black", fg="white" )
item4_name = tk.Label ( root , text = " Polaroid " , font = bold_font , bg="black", fg="white" )
item5_name = tk.Label ( root , text = " Switch " , font = bold_font , bg="black", fg="white" )
item6_name = tk.Label ( root , text = " PS5 " , font = bold_font , bg="black", fg="white" )
item7_name = tk.Label ( root , text = " Earings " , font = bold_font , bg="black", fg="white" )
item8_name = tk.Label ( root , text = " Rings " , font = bold_font , bg="black", fg="white" )
item9_name = tk.Label ( root , text = " Watch " , font = bold_font , bg="black", fg="white" )
item10_name = tk.Label ( root , text = " Necklace " , font = bold_font , bg="black", fg="white" )
item11_name = tk.Label ( root , text = " Tote " , font = bold_font , bg="black", fg="white" )
item12_name = tk.Label ( root , text = " Backpack " , font = bold_font , bg="black", fg="white" )
item13_name = tk.Label ( root , text = " Wallet " , font = bold_font , bg="black", fg="white" )
item14_name = tk.Label ( root , text = " Stachel " , font = bold_font , bg="black", fg="white" )

# Item Image
item1 = tk.Label(root , image=item_img[0] , highlightthickness = 2 )
item2 = tk.Label(root , image=item_img[1] , highlightthickness = 2 )
item3 = tk.Label(root , image=item_img[2] , highlightthickness = 2 )
item4 = tk.Label(root , image=item_img[3] , highlightthickness = 2 )
item5 = tk.Label(root , image=item_img[4] , highlightthickness = 2 )
item6 = tk.Label(root , image=item_img[5] , highlightthickness = 2 )
item7 = tk.Label(root , image=item_img[6] , highlightthickness = 2 )
item8 = tk.Label(root , image=item_img[7] , highlightthickness = 2 )
item9 = tk.Label(root , image=item_img[8] , highlightthickness = 2 )
item10 = tk.Label(root , image=item_img[9] , highlightthickness = 2 )
item11 = tk.Label(root , image=item_img[10] , highlightthickness = 2 )
item12 = tk.Label(root , image=item_img[11] , highlightthickness = 2 )
item13 = tk.Label(root , image=item_img[12] , highlightthickness = 2 )
item14 = tk.Label(root , image=item_img[13] , highlightthickness = 2 )



#介面佈局
# Background
canvas.pack ()

# Shop Owner
shop_owner.pack ()
canvas.create_window ( 100 , 20 , width = 190 , height = 30 , window = shop_owner )
account_address_label.pack ()
canvas.create_window ( 500 , 20 , width = 600 , height = 30 , window = account_address_label )

# Customer address
customer_address.pack ()
canvas.create_window ( 100 , 60 , width = 190 , height = 30 , window = customer_address )
customer_address_input.pack ()
canvas.create_window ( 500 , 60 , width = 600 , height = 30 , window = customer_address_input )
# Customer key
customer_key.pack ()
canvas.create_window ( 100 , 95 , width = 190 , height = 30 , window = customer_key )
customer_key_input.pack ()
canvas.create_window ( 500 , 95 , width = 600 , height = 30 , window = customer_key_input )

# Check Customer address & Customer private key
check_wallet.pack ()
canvas.create_window ( 835 , 77 , width = 60 , height = 66 , window = check_wallet )

# Items
item.pack ()
canvas.create_window ( 860 , 20 , width = 80 , height = 30 , window = item )
choose_item.pack ()
canvas.create_window ( 970 , 20 , width = 130 , height = 30 , window = choose_item )

# Restock
shop_restock.pack ()
canvas.create_window ( 1145 , 20 , width = 180 , height = 30 , window = shop_restock )
item_add.pack ()
canvas.create_window ( 1330 , 20 , width = 180 , height = 30 , window = item_add )
item_add_cnt.pack ()
canvas.create_window ( 1450 , 20 , width = 50 , height = 30 , window = item_add_cnt )

# Search Items Information 
search_information.pack ()
canvas.create_window ( 1145 , 60 , width = 180 , height = 30 , window = search_information )
# Item Information
item_balance.pack ()
canvas.create_window ( 1330 , 60 , width = 180 , height = 30 , window = item_balance )
item_balance_cnt.pack ()
canvas.create_window ( 1450 , 60 , width = 50 , height = 30 , window = item_balance_cnt )
item_price.pack ()
canvas.create_window ( 1585 , 60 , width = 180 , height = 30 , window = item_price )
item_price_cnt.pack ()
canvas.create_window ( 1705 , 60 , width = 50 , height = 30 , window = item_price_cnt )
item_price_unit.pack ()
canvas.create_window ( 1765 , 60 , width = 60 , height = 30 , window = item_price_unit )
item_description.pack ()
canvas.create_window ( 1330 , 95 , width = 180 , height = 30 , window = item_description )
item_description_line.pack ()
canvas.create_window ( 1660 , 95 , width = 470 , height = 30 , window = item_description_line )

# Buyer Payable
buyer_payable.pack ()
canvas.create_window ( 1145, 135 , width = 180 , height = 30 , window = buyer_payable )
buyer_amount.pack ()
canvas.create_window ( 1330 , 135 , width = 180 , height = 30 , window = buyer_amount )
buyer_amount_cnt.pack ()
canvas.create_window ( 1450 , 135 , width = 50 , height = 30 , window = buyer_amount_cnt )
#buyer_payment.pack ()
#canvas.create_window ( 1585 , 135 , width = 180 , height = 30 , window = buyer_payment )
#buyer_payment_cnt.pack ()
#canvas.create_window ( 1705 , 135 , width = 50 , height = 30 , window = buyer_payment_cnt )
#buyer_payment_unit.pack ()
#canvas.create_window ( 1765 , 135 , width = 60 , height = 30 , window = buyer_payment_unit )

# Buyer Items Balance
buyer_information.pack ()
canvas.create_window ( 1145 , 175 , width = 180 , height = 30 , window = buyer_information )
buyer_balance.pack ()
canvas.create_window ( 1330 , 175 , width = 180 , height = 30 , window = buyer_balance )
buyer_balance_cnt.pack ()
canvas.create_window ( 1450 , 175 , width = 50 , height = 30 , window = buyer_balance_cnt )

# Interactive
interactive.pack ()
canvas.create_window ( 402 , 155 , width = 795 , height = 70 , window = interactive )

# Item Name
item1_name.pack()
canvas.create_window ( 270 , 340 , width = 100 , height = 30 , window = item1_name )
item2_name.pack()
canvas.create_window ( 500 , 340 , width = 100 , height = 30 , window = item2_name )
item3_name.pack()
canvas.create_window ( 730 , 340 , width = 100 , height = 30 , window = item3_name )
item4_name.pack()
canvas.create_window ( 960 , 340 , width = 100 , height = 30 , window = item4_name )
item5_name.pack()
canvas.create_window ( 1190 , 340 , width = 100 , height = 30 , window = item5_name )
item6_name.pack()
canvas.create_window ( 1420 , 340 , width = 100 , height = 30 , window = item6_name )
item7_name.pack()
canvas.create_window ( 1650 , 340 , width = 100 , height = 30 , window = item7_name )
item8_name.pack()
canvas.create_window ( 270 , 650 , width = 100 , height = 30 , window = item8_name )
item9_name.pack()
canvas.create_window ( 500 , 650 , width = 100 , height = 30 , window = item9_name )
item10_name.pack()
canvas.create_window ( 730 , 650 , width = 100 , height = 30 , window = item10_name )
item11_name.pack()
canvas.create_window ( 960 , 650 , width = 100 , height = 30 , window = item11_name )
item12_name.pack()
canvas.create_window ( 1190 , 650 , width = 100 , height = 30 , window = item12_name )
item13_name.pack()
canvas.create_window ( 1420 , 650 , width = 100 , height = 30 , window = item13_name )
item14_name.pack()
canvas.create_window ( 1650 , 650 , width = 100 , height = 30 , window = item14_name )

# Item Image
item1.pack()
canvas.create_window ( 270 , 460 , width = 210 , height = 200 , window = item1 )
item2.pack()
canvas.create_window ( 500 , 460 , width = 210 , height = 200 , window = item2 )
item3.pack()
canvas.create_window ( 730 , 460 , width = 210 , height = 200 , window = item3 )
item4.pack()
canvas.create_window ( 960 , 460 , width = 210 , height = 200 , window = item4 )
item5.pack()
canvas.create_window ( 1190 , 460 , width = 210 , height = 200 , window = item5 )
item6.pack()
canvas.create_window ( 1420 , 460 , width = 210 , height = 200 , window = item6 )
item7.pack()
canvas.create_window ( 1650 , 460 , width = 210 , height = 200 , window = item7 )
item8.pack()
canvas.create_window ( 270 , 770 , width = 210 , height = 200 , window = item8 )
item9.pack()
canvas.create_window ( 500 , 770 , width = 210 , height = 200 , window = item9 )
item10.pack()
canvas.create_window ( 730 , 770 , width = 210 , height = 200 , window = item10 )
item11.pack()
canvas.create_window ( 960 , 770 , width = 210 , height = 200 , window = item11 )
item12.pack()
canvas.create_window ( 1190 , 770 , width = 210 , height = 200 , window = item12 )
item13.pack()
canvas.create_window ( 1420 , 770 , width = 210 , height = 200 , window = item13 )
item14.pack()
canvas.create_window ( 1650 , 770 , width = 210 , height = 200 , window = item14 )



# 啟動tkInter的事件循環
root.mainloop()




















































































































































































































































































