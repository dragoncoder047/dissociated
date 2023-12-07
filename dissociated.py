#! /usr/bin/env python3

# https://norvig.com/big.txt

import sys
import random
import argparse

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
    token = random.choice(tuple(index.keys()))
    while True:
        nc = random.choice(index.get(token, "\0"))
        if nc != "\0":
            yield nc
        token = token[1:] + nc
        if token == allzeros:
            return

def main():
    parser = argparse.ArgumentParser("dissociated")
    parser.add_argument("-w", "--windowsize", type=int, default=10, metavar="SIZE", help="Length of sliding window to scan the input with.")
    parser.add_argument("-n", "--length", type=int, default=1024, metavar="LENGTH", help="Number of output bytes.")
    parser.add_argument("file", type=str, help="File to read from or - for stdin.")
    opts = parser.parse_args()
    if opts.file == "-":
        index = build_index(tokenize_file(sys.stdin, opts.windowsize))
    else:
        with open(opts.file) as f:
            index = build_index(tokenize_file(f, opts.windowsize))
    for ch, _ in zip(generate_text(index, opts.windowsize), range(opts.length)):
        print(ch, end="", flush=True)

main()
