#!/bin/env python3
import sys
import json

from config import TEXT_FILE
import csv2json, chain

if __name__ == "__main__":

    data = csv2json.read_text(TEXT_FILE)
    #print(json.dumps(data, ensure_ascii=False, indent=4))  # utf8

    with open("cardchain.json", "r") as f:
        cardchain = json.load(f)

    data_keys = set(data.keys())
    chain_keys = set(cardchain.keys())

    new_cards = list(data_keys.difference(chain_keys))
    if not new_cards:
        print("No new cards")
        sys.exit(0)

    print(new_cards)

    for num in new_cards:

        cards_len = len(chain_keys)
        res = input("%d cards. Add card number %s? (y/N): " % (cards_len, num))
        if res != "y":
            sys.exit(0)

        last_card = str(int(num) - 1)
        cardchain[num] = chain.make_chain(data[num], cardchain[last_card]["card_hash"])
        print(cardchain[num])

    with open("cardchain.json", "w") as f:
        f.write(json.dumps(cardchain, ensure_ascii=False, indent=4))
