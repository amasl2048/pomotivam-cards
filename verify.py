#!/bin/env python3
import json

import hashlib
import binascii
import collections

from crypting import load_user, check_sign

if __name__ == "__main__":

    with open("cardchain.json", "r") as f:
        chain = json.load(f)

    for num in chain.keys():

        # card hash sha256
        card_hash = chain[num]["card_hash"]
        card_dump = json.dumps(chain[num]["card"], ensure_ascii=False)

        hash256 = hashlib.new("sha256")
        hash256.update(hashlib.sha256(card_dump.encode()).digest())

        ascii_hash = binascii.hexlify(hash256.digest()).decode("ascii")

        try:
            assert(card_hash == ascii_hash)
        except:
            print("Wrong hash: ", num, "\n", card_hash, "\n", ascii_hash)

        # body sign
        ascii_key = chain[num]["card"]["header"]["pub_key"]
        ascii_sign = chain[num]["card"]["header"]["sign"]

        credentials = load_user()

        try:
            assert(ascii_key == credentials["public"])
        except:
            print("Wrong key\n", ascii_key, "\n", credentials["public"])

        sorted_dict = collections.OrderedDict(sorted(chain[num]["card"]["body"].items(), key=lambda x: x[0])) 
        body_dump = json.dumps(sorted_dict, ensure_ascii=False)

        try:
            assert check_sign(ascii_sign, body_dump, ascii_key)
        except:
            print("Wrong sign: ", num, "\n", ascii_sign)
