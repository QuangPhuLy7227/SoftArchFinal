# check_factory.py

import argparse
from dsm import load_dsm
from detectors.factory import find_abstract_factory, find_factory_method

def _print(pattern_name, roles):
    print(f"=== {pattern_name} ===")
    if not any(roles.values()):
        print(f"No {pattern_name} patterns found.\n")
        return
    for role, clist in roles.items():
        print(f"{role}:")
        for c in clist:
            print(f"  - {c}")
    print()

def main():
    p = argparse.ArgumentParser()
    p.add_argument("-d","--dsm", required=True, help=".csv export from Understand")
    args = p.parse_args()

    dsm = load_dsm(args.dsm)

    _print("Abstract Factory Pattern", find_abstract_factory(dsm))
    _print("Factory Method Pattern", find_factory_method(dsm))

if __name__ == "__main__":
    main()