#!/bin/env python3
import random
import json

import hashlib
import binascii
import collections

from config import SEED, COLOR1, COLOR2
from crypting import load_user, sign_mess


def get_rand_color(color1: int, color2: int, hash: str) -> tuple:

    random.seed(hash)

    col = [color1, color2, random.randint(color1,color2)]
    random.shuffle(col)
    #print(col)
    return tuple(col)

def make_chain(chain: dict, prev_hash: str) -> dict:

        credentials = load_user()

        # body
        chain["card"]["body"]["prev_hash"] = prev_hash
        color = get_rand_color(COLOR1, COLOR2, prev_hash)
        chain["card"]["body"]["color"] = color

        # header
        chain["card"]["header"]["pub_key"] = credentials["public"]

        sorted_dict = collections.OrderedDict(sorted(chain["card"]["body"].items(), key=lambda x: x[0]))
        body_dump = json.dumps(sorted_dict, ensure_ascii=False)
        sign = sign_mess(credentials, body_dump)
        chain["card"]["header"]["sign"] = sign
        print("Sign: ", sign)

        # card
        card_dump = json.dumps(chain["card"], ensure_ascii=False)
        #print(card_dump)

        hash256 = hashlib.new("sha256")
        hash256.update(hashlib.sha256(card_dump.encode()).digest())
        ascii_hash = binascii.hexlify(hash256.digest()).decode("ascii")
        chain["card_hash"] = ascii_hash

        print("hash: ", ascii_hash)

        return chain

def chainify(cards: dict) -> dict:

    prev_hash = SEED
    chain = {}

    for num in cards.keys():

        print(num)
        chain[num] = make_chain(cards[num], prev_hash)
        prev_hash = chain[num]["card_hash"]

        print(chain[num]["card"]["body"]["color"])

    return chain

if __name__ == "__main__":

    res = input("Do you want regenerate cardchain? (y/N): ")
    if res != "y":
            sys.exit()

    with open("cardchain.json", "r") as f:
        chain = json.load(f)

    chain = chainify(chain)

    with open("cardchain.json", "w") as f:
        f.write(json.dumps(chain, ensure_ascii=False, indent=4))
