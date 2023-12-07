#! /usr/bin/env python3

# These are the settings
FILE = "big.txt"
FILE_URL = "https://norvig.com/big.txt"
WINDOW_SIZE = 100
LENGTH = 1024

import sys
import random
import os

def tokenize_file(f, window_size):
    allzeros = "\0" * window_size
    token = allzeros
    while True:
        yield token
        ch = f.read(1)
        if not ch:
            break
        token = token[1:] + ch
    while token != allzeros:
        yield token
        token = token[1:] + "\0"
    yield allzeros

def build_index(token_stream):
    index = {}
    prev_token = next(token_stream)
    for token in token_stream:
        if prev_token in index:
            index[prev_token].append(token[-1])
        else:
            index[prev_token] = [token[-1]]
        prev_token = token
    return index

def generate_text(index, window_size):
    allzeros = "\0" * window_size
    token = random.choice(index)
    while True:
        nc = random.choice(index.get(token, "\0"))
        if nc != "\0":
            yield nc
        token = token[1:] + nc
        if token == allzeros:
            return

def main():
    try:
        with open(FILE): pass
    except FileNotFoundError:
        os.system(f"curl \"{FILE_URL}\" > {FILE}")
    with open(FILE) as f:
        index = build_index(tokenize_file(f, WINDOW_SIZE))
    for ch, _ in zip(generate_text(index, WINDOW_SIZE), range(LENGTH)):
        print(ch, end="", flush=True)

main()
