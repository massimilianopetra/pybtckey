"""
 * bitcoin_utils.py
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
import random
import ecdsa

ALPHABET = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'


def base58encode(v):
    result = ''

    if isinstance(v,int):
        while v > 0:
            result = ALPHABET[v%58] + result
            v //= 58
    elif isinstance(v,bytes):
        result = base58encode(int.from_bytes(v, byteorder='big', signed=False))
        
    return result

def base58decode(s):
    result = 0
    for i in range(0, len(s)):
        result = result * 58 + ALPHABET.index(s[i])
    return result.to_bytes(37, 'big')

def base58CheckEncode(a,v):
    v = a+v
    digest = hashlib.sha256(hashlib.sha256(v).digest()).digest()
    return base58encode(v + digest[:4])


def base58CheckDecode(v):

    result = base58decode(v)
    result, check = result[:-4], result[-4:]
    digest = hashlib.sha256(hashlib.sha256(result).digest()).digest()

    if check != digest[:4]:
        raise ValueError("Invalid checksum")

    return result

def generatePrivateKey():
    key = ''.join(['%x' % random.randrange(16) for x in range(0, 64)])
    return key

def privateKeyToWif(key_hex):    
    return base58CheckEncode(bytes([0x80]),bytes.fromhex(key_hex))

def integerToWif(i):    
    return base58CheckEncode(bytes([0x80]),i.to_bytes(32, 'big'))

def integerToPublicKey(i):
    sk = ecdsa.SigningKey.from_string(i.to_bytes(32, 'big'), curve=ecdsa.SECP256k1)
    vk = sk.verifying_key
    return '04'+vk.to_string().hex()

def privateKeyToPublicKey(key_hex):
    sk = ecdsa.SigningKey.from_string(bytes.fromhex(key_hex), curve=ecdsa.SECP256k1)
    vk = sk.verifying_key
    return '04'+vk.to_string().hex()

def pubKeyToAddr(s):
    ripemd160 = hashlib.new('ripemd160')
    ripemd160.update(hashlib.sha256(bytes.fromhex(s)).digest())
    return "1"+base58CheckEncode(bytes([0x00]), ripemd160.digest())

def ripemd160(s):
    ripemd160 = hashlib.new('ripemd160')
    ripemd160.update(hashlib.sha256(bytes.fromhex(s)).digest())
    return ripemd160.digest().hex()

if __name__ == '__main__':
    hexstring= "00010966776006953D5567439E5E39F86A0D273BEED61967F6"
    unencoded_bytes = bytes.fromhex(hexstring)
    encoded_string = base58encode(unencoded_bytes)
    if "6UwLL9Risc3QfPqBUvKofHmBQ7wMtjvM" == encoded_string:
        print("test ok:", encoded_string)
    else:
        print("test error 1")
    print("Private key:",generatePrivateKey())
