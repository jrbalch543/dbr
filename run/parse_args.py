import argparse

def build_parser():
    parser = argparse.ArgumentParser(prog="DBR")
    parser.add_argument("db_path")
    return parser

def parse():
    args = build_parser().parse_args()
    return args
