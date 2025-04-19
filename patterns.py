import argparse
import understand
from detectors import adapter, observer

def main():
    parser = argparse.ArgumentParser(description="Design Pattern Detector")
    parser.add_argument(
        "-u","--udb", required=True,
        help="Path to the Understand .und file"
    )
    args = parser.parse_args()

    db = understand.open(args.udb)

    # Adapter Detection
    adapter_matches = adapter.find(db).get("adapter", [])
    print("\n=== Adapter Pattern ===")
    if not adapter_matches:
        print("No Adapter patterns found.")
    else:
        for e in adapter_matches:
            print(f"Adapter: {e['adapter']}, Interface: {e['target']}, Adaptee: {e['adaptee']}")

    # Observer Detection
    observer_matches = observer.find(db).get("observer", [])
    print("\n=== Observer Pattern ===")
    if not observer_matches:
        print("No Observer patterns found.")
    else:
        for e in observer_matches:
            print(f"Subject: {e['subject']}")
            print(f"  Listener Interface: {e['listener_interface']}")
            print(f"  Add methods:         {e['add_methods']}")
            print(f"  Remove methods:      {e['remove_methods']}")
            print(f"  Fields:              {e['fields']}\n")

if __name__ == "__main__":
    main()