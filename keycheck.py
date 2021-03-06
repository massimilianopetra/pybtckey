"""
 * keycheck.py
 *
 * Author: Massimiliano Petra <massimiliano.petra@gmail.com> January, 2021
 *
 *
 *  This program is free software; you can redistribute it and/or modify
 *  it under the terms of the GNU General Public License as published by
 *  the Free Software Foundation; either version 2 of the License, or
 *  (at your option) any later version.
 *
 *  This program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU General Public License for more details.
 *
 *  You should have received a copy of the GNU General Public License
 *  along with this program; if not, write to the Free Software
 *  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA
 *  02111-1307  USA.
 *
 *
"""


import hashlib
import bitcoin_utils
import ecdsa
import requests
from datetime import datetime


# PrivateKey from integer
print("--- Bitcoin Key Checker ---")
print()

for i in range(1,2):

    wif_key = bitcoin_utils.integerToWif(i)
    pub_key = bitcoin_utils.integerToPublicKey(i)
    btc_address = bitcoin_utils.pubKeyToAddr(pub_key)
    balance = 0
    ntx = 0
    last = ""

    """
    r = requests.get("https://blockchain.info/rawaddr/%s" % btc_address)
    rjson = r.json()
    balance = rjson["final_balance"]
    ntx = rjson["n_tx"]
    """
    
    if ntx > 0:
        dt = datetime.fromtimestamp(rjson["txs"][0]["time"])
        last = dt.strftime("%Y/%m/%d, %H:%M:%S")	
    else:
        last = ""
        
    print("%d\t%s\t%s\t%d\t%d\t%s" % (i,wif_key,btc_address,balance,ntx,last))


input()
