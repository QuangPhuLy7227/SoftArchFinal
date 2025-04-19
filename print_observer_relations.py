import argparse
import understand

class ObserverRelationshipPrinter:
    def __init__(self, udb_path):
        self.db = understand.open(udb_path)
        if not self.db:
            raise RuntimeError(f"Failed to open UDB at {udb_path}")

    def print_relationships(self):
        # 1) Lookup the core interface
        ifaces = self.db.lookup("org.apache.commons.net.io.CopyStreamListener", "Interface")
        if not ifaces:
            print("❌  CopyStreamListener interface not found.")
            return
        iface = ifaces[0]
        print(f"\nObserver Interface:\n  • {iface.longname()}")

        # 2) Lookup the adapter/subject class
        subjects = self.db.lookup("org.apache.commons.net.io.CopyStreamAdapter", "Class")
        if not subjects:
            print("❌  CopyStreamAdapter class not found.")
            return
        subj = subjects[0]
        print(f"\nSubject (also implements that interface):\n  • {subj.longname()}")

        #   a) check that it truly implements the interface
        impls = [r.ent().longname()
                 for r in subj.refs("Inheritance")
                 if r.kindname()=="Implements"]
        print("    implements:", impls or "⚠️  none")

        #   b) show its add/remove methods
        adds = [m.longname() for m in subj.ents("Define","Method")
                if m.name()=="addCopyStreamListener"]
        rems = [m.longname() for m in subj.ents("Define","Method")
                if m.name()=="removeCopyStreamListener"]
        print("    add methods:   ", adds or "⚠️  none")
        print("    remove methods:", rems or "⚠️  none")

        #   c) show the backing listener‐list field
        fields = [f.longname() for f in subj.ents("Define","Member")
                  if "ListenerList" in (f.type() or "")]
        print("    backing fields:", fields or "⚠️  none")

        # 3) Lookup the ListenerList class itself
        lists = self.db.lookup("org.apache.commons.net.util.ListenerList", "Class")
        if lists:
            ll = lists[0]
            print(f"\nBacking List Class:\n  • {ll.longname()}")
        else:
            print("\n❌  ListenerList class not found.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--udb","-u", required=True, help="path to .und file")
    args = parser.parse_args()

    printer = ObserverRelationshipPrinter(args.udb)
    printer.print_relationships()