import understand

def print_all_classes_and_methods(udb_path):
    # 1) Open the DB
    db = understand.open(udb_path)
    if not db:
        raise RuntimeError(f"Couldn't open UDB at {udb_path}")

    # 2) Fetch every class entity
    classes = db.ents("Class")
    if not classes:
        print("⚠️  No classes found in the UDB. Check that your .und was created with Java files included.")
        return

    # 3) For each class, list the methods it defines
    for cls in classes:
        print(f"\nClass: {cls.longname()}")
        methods = cls.ents("Define", "Method")
        if not methods:
            print("  (no defined methods)")
        else:
            for m in methods:
                print(f"  - {m.name()}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-u", "--udb", required=True,
        help="path to your Understand .und file"
    )
    args = parser.parse_args()
    print_all_classes_and_methods(args.udb)