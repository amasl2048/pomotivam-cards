#!/bin/sh
python3 ./csv2json.py
python3 ./chain.py
python3 ./verify.py
python3 ./cards.py
