#!/bin/env python3
import sys
import json

from config import TEXT_FILE, LINK


def read_text(filename: str) -> dict:
    '''
    Read csv "filename" with stroke "|" separator:
    num | picture | author | "text".

    picture - author photo file name in APNG format w/o .png
    '''
    separator = "|"
    lines = {}

    with open("memo.json", "r") as f:
        memo = json.load(f)

    with open(filename) as f:

        while True:

            ln = f.readline()
            if ln == "\n":
                continue

            line = ln.split(separator)
            if line[0] == "":
                break
            elif line[0][0] == "#":
                continue

            num = line[0].strip()
            try:
                mm = memo[num]
            except:
                mm = ""

            #print(line)
            lines[num] = {
                "card_hash": "",
                "card": {
                    "header": {
                        "pub_key": "",
                        "sign": "",
                        "memo": mm
                    },
                    "body": {
                        "number": "N%03d" % int(line[0]),
                        "prev_hash": "",
                        "link": LINK,
                        "picture": line[1].strip(),
                        "tag": "#%s%s" % (line[1].strip()[0].upper(), line[1].strip()[1:]),
                        "author": line[2].strip().replace(r"\n", "\n"),
                        "text": line[3].strip().replace(r"\n", "\n"),
                        "color": ""
                    }
                }
            }
    
    return lines

if __name__ == "__main__":

    res = input("Do you want create all cards from scratch? (y/N): ")
    if res != "y":
            sys.exit()

    data = read_text(TEXT_FILE)
    #print(json.dumps(data, ensure_ascii=False, indent=4))  # utf8

    with open("cardchain.json", "w") as f:
        f.write(json.dumps(data, ensure_ascii=False, indent=4))
