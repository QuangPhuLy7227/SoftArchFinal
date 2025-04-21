# import argparse
# import understand
# from detectors import adapter, observer, template, strategy

# def main():
#     parser = argparse.ArgumentParser(description="Design Pattern Detector")
#     parser.add_argument(
#         "-u","--udb", required=True,
#         help="Path to the Understand .und file"
#     )
#     args = parser.parse_args()

#     db = understand.open(args.udb)

#     # Adapter Detection
#     adapter_matches = adapter.find(db).get("adapter", [])
#     print("\n=== Adapter Pattern ===")
#     if not adapter_matches:
#         print("No Adapter patterns found.")
#     else:
#         for e in adapter_matches:
#             print(f"Adapter: {e['adapter']}, Interface: {e['target']}, Adaptee: {e['adaptee']}")

#     # Observer Detection
#     observer_matches = observer.find(db).get("observer", [])
#     print("\n=== Observer Pattern ===")
#     if not observer_matches:
#         print("No Observer patterns found.")
#     else:
#         for e in observer_matches:
#             print(f"Subject: {e['subject']}")
#             print(f"  Listener Interface: {e['listener_interface']}")
#             print(f"  Add methods:         {e['add_methods']}")
#             print(f"  Remove methods:      {e['remove_methods']}")
#             print(f"  Fields:              {e['fields']}\n")
            
#     # Template Method Detection
#     template_matches = template.find(db).get("template", [])
#     print("\n=== Template Method Pattern ===")
#     if not template_matches:
#         print("No Template Method patterns found.")
#     else:
#         for e in template_matches:
#             print(f"TemplateClass:        {e['template_class']}")
#             print(f"  PrimitiveOperations: {e['primitive_operations']}")
#             print(f"  TemplateMethods:     {e['template_methods']}\n")
            
#     # Strategy Detection
#     strategy_matches = strategy.find(db).get("strategy", [])
#     print("\n=== Strategy Pattern ===")
#     if not strategy_matches:
#         print("No Strategy patterns found.")
#     else:
#         for e in strategy_matches:
#             print(f"Context:              {e['context']}")
#             print(f"  Strategy Interface:  {e['strategy_interface']}")
#             print(f"  Field:               {e['field']}")
#             print(f"  Usage methods:       {e['usage_methods']}\n")

# if __name__ == "__main__":
#     main()

#!/usr/bin/env python3
# patterns.py

# patterns.py
import argparse
from dsm import load_dsm
from detectors.observer import find as find_observer

def main():
    parser = argparse.ArgumentParser(
        description="Detect Design Patterns via DSM"
    )
    parser.add_argument(
        "-d", "--dsm", required=True,
        help="Path to the deps.csv file"
    )
    args = parser.parse_args()

    dsm = load_dsm(args.dsm)

    print("=== Observer Pattern ===")
    obs = find_observer(dsm)
    any_found = any(obs[role] for role in obs)
    if not any_found:
        print("No Observer patterns found.")
    else:
        for role, classes in obs.items():
            print(f"{role}:")
            for c in classes:
                print(f"  - {c}")

if __name__ == "__main__":
    main()
