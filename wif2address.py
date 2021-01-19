"""
 * wif2address.py
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

import random
import hashlib
import bitcoin_utils
import ecdsa
import pyqrcode
from tkinter import *

def showGui(priv,wif,pub,address):

    master = Tk()
    master.title("Wif Key To Address Generator")
     
    Label(master, text="Private Key").grid(row=0)
    Label(master, text="Wif Key").grid(row=1)
    Label(master, text="Pub Key").grid(row=2)
    Label(master, text="BTC Address").grid(row=3)

    ePrivateKey = Entry(master, width=140)
    eWif = Entry(master, width=140)
    ePub = Entry(master, width=140)
    eAddress = Entry(master, width=140)

    ePrivateKey.grid(row=0, column=1)
    eWif.grid(row=1, column=1)
    ePub.grid(row=2, column=1)
    eAddress.grid(row=3, column=1)


    ePrivateKey.delete(0, END)
    ePrivateKey.insert(0, priv)
    eWif.delete(0, END)
    eWif.insert(0, wif)
    ePub.delete(0, END)
    ePub.insert(0, pub)
    eAddress.delete(0, END)
    eAddress.insert(0, address)

    # BTC Address qr-code 
    code = pyqrcode.create(address)
    code_xbm = code.xbm(scale=5)

    code_bmp1 = BitmapImage(data=code_xbm)
    code_bmp1.config(foreground="black")
    code_bmp1.config(background="white")
    qraddress = Label(image=code_bmp1)
    qraddress.grid(row=4,column=0)

    # Wif qr-code 
    code = pyqrcode.create(wif)
    code_xbm = code.xbm(scale=5)

    code_bmp2 = BitmapImage(data=code_xbm)
    code_bmp2.config(foreground="black")
    code_bmp2.config(background="white")
    qrwifkey = Label(image=code_bmp2)
    qrwifkey.grid(row=4,column=1)

    mainloop( )

# PrivateKey with insicure random generator
print("--- Wif Key To Address Generator ---")

k = "5HpHagT65TZzG1PH3CSu63k8DbpvD8s5ip4nEB3kEsreAnchuDf"
private_key = bitcoin_utils.base58CheckDecode(k)[1:].hex()
wif_key = bitcoin_utils.privateKeyToWif(private_key)
if k == wif_key:
    print("Wif Check OK")
else:
    print("Wif Check FAIL")
pub_key = bitcoin_utils.privateKeyToPublicKey(private_key)
ripemd = bitcoin_utils.ripemd160(pub_key)
btc_address = bitcoin_utils.pubKeyToAddr(pub_key)


print ("Private Key: %s" % private_key)
print ("Wif Key: %s" % wif_key)
print ("Public Key: %s" % pub_key)
print ("Ripemd160: %s" % ripemd)
print ("BTC Address: %s" % btc_address)



showGui(private_key,wif_key,pub_key,btc_address)
