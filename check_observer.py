# import argparse
# from dsm import load_dsm
# from detectors.observer import find as find_observer

# def main():
#     parser = argparse.ArgumentParser(
#         description="Detect Design Patterns via DSM"
#     )
#     parser.add_argument(
#         "-d", "--dsm", required=True,
#         help="Path to the deps.csv file"
#     )
#     args = parser.parse_args()

#     dsm = load_dsm(args.dsm)

#     print("=== Observer Pattern ===")
#     obs = find_observer(dsm)
#     any_found = any(obs[role] for role in obs)
#     if not any_found:
#         print("No Observer patterns found.")
#     else:
#         for role, classes in obs.items():
#             print(f"{role}:")
#             for c in classes:
#                 print(f"  - {c}")

# if __name__ == "__main__":
#     main()

#!/usr/bin/env python
import argparse
from dsm               import load_dsm
from detectors.observer import find

def main():
    p = argparse.ArgumentParser()
    p.add_argument("-d","--dsm", required=True, help="path to deps.csv")
    args = p.parse_args()

    d = load_dsm(args.dsm)
    roles = find(d)

    print("=== Observer Pattern ===")
    if not any(roles.values()):
        print("No Observer patterns found.")
        return

    for role, clist in roles.items():
        print(f"{role}:")
        for c in clist:
            print("  -", c)

if __name__=="__main__":
    main()