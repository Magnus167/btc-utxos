from bloxplorer import bitcoin_explorer as explorer
from bitcash import PrivateKey
import bitsv
import json
import requests
from bs4 import BeautifulSoup 

#https://github.com/sporestack/bitcash
#https://github.com/valinsky/bloxplorer
#https://github.com/AustEcon/bitsv
# ye logo ko thoda thoda inaam banta he <3

def get_bal_from_BTG_page_content(tableStr):
    cont = []
    tempStr = ''
    f = False
    for char in tableStr:
        if char == '<':
            if tempStr!='':
                cont.append(tempStr)
                tempStr = ''
            f = False
        if f:
            if char!=' ':
                tempStr = tempStr + char
        if char=='>':
            f = True
            
            
    tempStr = ''         
    f = False
    for elem in cont:
        if elem=='BTG':
            f=False
        if f:
            tempStr = tempStr + elem
        if elem=='Balance:':
            f = True
            
    return tempStr
      
def get_BTG_balance_bitinfo(address):
    
    default_Parser = 'lxml'
    
    tokenviewURL = 'https://bitinfocharts.com/bitcoin%20gold/address/' + address
    #https://bitinfocharts.com/bitcoin%20gold/address/1ErMsR99tfkp8tBANRV5iyn1W3QdLsWaS6
    raw_html = requests.get(tokenviewURL) 
    soup = BeautifulSoup(raw_html.content, default_Parser) 
    
    tables = soup.find_all('table')
    if len(tables)==0:
        return -1 
        
    else:
        extrStr = str(tables[0])
        return (get_bal_from_BTG_page_content(extrStr))   
    # if the page returns an empty html, return -1. 
    # not returning 0, 
    # as it can be confused with a 0 balance wallet.
    # this is the case where the given wallet doesn't exist on the fork
    
def get_BTG_Balance(pub_key, sec_key):
    return (get_BTG_balance_bitinfo(pub_key))


def get_BSV_Balance(pub_key, sec_key):
    tK = bitsv.Key(sec_key)
    return (tK.balance)

def get_BCH_Balance(pub_key, sec_key):
    tK = PrivateKey(sec_key)
    return (tK.balance)  


def get_BTC_UTXO(pub_key, sec_key):    
    blx_api_response = explorer.addr.get_utxo(pub_key) 
    blx_response_dict = blx_api_response.data    
    return (len(blx_response_dict))

    # utxo_list = []  // can have a method to return the utxo list. seems intriguing, gonna leave this here    


def get_All_Bals(pub_key, sec_key):
    output = []
  
    output.append(get_BTC_UTXO(pub_key, sec_key))
    output.append(get_BCH_Balance(pub_key, sec_key))   
    output.append(get_BSV_Balance(pub_key, sec_key))
    output.append(get_BTG_Balance(pub_key, sec_key))
    
    return output
         

#125GHz Wallet is love. It's just cool is all;
    
jsonFile = open('privKeys.json',)

wallets = json.load(jsonFile)

jsonFile.close()

test_wallets = wallets

#public_kw_list = test_wallets.keys()

for iter_pub_key, iter_secret_key in test_wallets.items():
    secret_key_sliced = iter_secret_key[6:]
    print (get_All_Bals(iter_pub_key, secret_key_sliced)   )                           
  
    






