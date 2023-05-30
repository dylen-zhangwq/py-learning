"""Handles creating a release PR"""
from __future__ import annotations

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(prog="release")
    parser.add_argument("--version", required=True)
    options = parser.parse_args()
    print(options.version)
