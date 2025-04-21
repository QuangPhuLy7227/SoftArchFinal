# check_decorator.py

import argparse
from dsm import load_dsm
from detectors.decorator import find_decorator

def _print(name: str, roles: dict):
    print(f"=== {name} Pattern ===")
    if not any(roles.values()):
        print(f"No {name} patterns found.\n")
        return
    for role, classes in roles.items():
        print(f"{role}:")
        for c in classes:
            print(f"  - {c}")
    print()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
      "-d","--dsm", required=True,
      help="Path to your CSV-style DSM (export from Understand)"
    )
    args = parser.parse_args()

    dsm = load_dsm(args.dsm)
    roles = find_decorator(dsm)
    _print("Decorator", roles)

if __name__ == "__main__":
    main()