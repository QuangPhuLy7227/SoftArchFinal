import argparse
import understand
from detectors import adapter

def main():
    parser = argparse.ArgumentParser(description="Simple Design Pattern Detector")
    parser.add_argument(
        "--udb", "-u", required=True,
        help="Path to the Understand .und file"
    )
    args = parser.parse_args()

    # Open the Understand database
    db = understand.open(args.udb)

    # Run the Adapter detector
    matches = adapter.find(db).get("adapter", [])
    print("\n=== Adapter Pattern Detection Results ===")
    if not matches:
        print("No Adapter patterns found.")
        return

    for m in matches:
        print(f"Adapter class: {m['adapter']}")
        print(f"  ↳ Target interface: {m['target']}")
        print(f"  ↳ Adaptee class:   {m['adaptee']}\n")

if __name__ == "__main__":
    main()