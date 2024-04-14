#!/bin/env python3
import os
from flask import Flask
from flask import request, render_template

import json

APP_PORT = 8888
app = Flask(__name__)
app.config['CARDCHAIN'] = os.path.join("static")
app.config['CARDS_FOLDER'] = os.path.join("static", "output-cards")

with open(app.config['CARDCHAIN'], "r") as f:
    CHAIN = json.load(f)

LEN = len(CHAIN.keys())


def chain_error(card: str):

    error = ""

    if int(card) < 1 or int(card) > LEN:
        card = str(LEN)
        error = "Enter card no. from 1 to %s" % LEN

    try:
        chain_card = CHAIN[card]
    except Exception as e:
        chain_card = CHAIN[str(LEN)]
        error = e

    chain_txt = json.dumps(chain_card, ensure_ascii=False, indent=4)

    return card, chain_txt, error


def taq(card: str):
    tag = CHAIN[card]["card"]["body"]["tag"][1:]
    author = CHAIN[card]["card"]["body"]["author"]
    quote = CHAIN[card]["card"]["body"]["text"]
    return tag, author, quote


def render_card(card: str):

    card, chain_txt, error = chain_error(card)
    filename = os.path.join(app.config['CARDS_FOLDER'], '%s.png' % card)

    if error:
        tag, author, quote = taq(str(LEN))
    else:
        tag, author, quote = taq(card)

    prev = int(card) - 1
    next = int(card) + 1
    if next > LEN:
        next = LEN
    if prev < 1:
        prev = 1

    return render_template("cards.html",
                           len=str(LEN),
                           prev=str(prev),
                           next=str(next),
                           card=card,
                           tag=tag,
                           author=author,
                           quote=quote,
                           image=filename,
                           chain=chain_txt,
                           error=error)


@app.route('/', methods=['GET'])
def root():
    return render_card(LEN)


@app.route('/card', methods=['GET'])
def show_card():
    card = request.args.get("card")
    return render_card(card)


if __name__ == "__main__":
    app.run(debug = True, host = "0.0.0.0", port = APP_PORT)
