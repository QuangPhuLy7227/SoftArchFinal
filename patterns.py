import argparse
import understand
from detectors import adapter, observer, factory, singleton, iterator, proxy, strategy, template

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
            
    # Template Method Detection
    template_matches = template.find(db).get("template", [])
    print("\n=== Template Method Pattern ===")
    if not template_matches:
        print("No Template Method patterns found.")
    else:
        for e in template_matches:
            print(f"TemplateClass:        {e['template_class']}")
            print(f"  PrimitiveOperations: {e['primitive_operations']}")
            print(f"  TemplateMethods:     {e['template_methods']}\n")
            
    # Strategy Detection
    strategy_matches = strategy.find(db).get("strategy", [])
    print("\n=== Strategy Pattern ===")
    if not strategy_matches:
        print("No Strategy patterns found.")
    else:
        for e in strategy_matches:
            print(f"Context:              {e['context']}")
            print(f"  Strategy Interface:  {e['strategy_interface']}")
            print(f"  Field:               {e['field']}")
            print(f"  Usage methods:       {e['usage_methods']}\n")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# patterns.py

# patterns.py
# import argparse
# import understand
# from detectors import adapter, observer, factory, singleton, iterator, proxy, strategy, template
# from collections import defaultdict

# def main():
#     parser = argparse.ArgumentParser(
#         description="Detect Design Patterns via DSM"
#     )
#     parser.add_argument(
#         "-u", "--udb", required=True,
#         help="Path to the Understand .und file"
#     )
#     args = parser.parse_args()

#     dsm = load_dsm(args.dsm)

#     print("=== Observer Pattern ===")
#     obs = find_observer(dsm)
#     any_found = any(obs[role] for role in obs)
#     if not any_found:
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

#     # Factory Pattern
#     factory_matches = factory.find(db).get("factory", [])
#     grouped_factories = defaultdict(set)
#     for e in factory_matches:
#         grouped_factories[e["class"]].add((e["factory_method"], e["return_type"]))

#     print("\n=== Factory Method Pattern ===")
#     if not grouped_factories:
#         print("No Factory patterns found.")
#     else:
#         for class_name, methods in grouped_factories.items():
#             print(f"Factory Class: {class_name}")
#             for method, return_type in sorted(methods):
#                 print(f"  → Method: {method}, Returns: {return_type}")
#             print()

#     # Iterator Pattern
#     iterator_matches = iterator.find(db).get("iterator", [])
#     print("\n=== Iterator Pattern ===")
#     if not iterator_matches:
#         print("No Iterator patterns found.")
#     else:
#         for match in iterator_matches:
#             print(f"Iterator Class: {match['iterator_class']}")
#             print(f"  Methods: {match['methods']}")

#     # Proxy Pattern
#     try:
#         proxy_matches = proxy.find(db).get("proxy", [])
#         print("\n=== Proxy Pattern ===")
#         if not proxy_matches:
#             print("No Proxy patterns found.")
#         else:
#             for p in proxy_matches:
#                 print(f"Proxy Class: {p['proxy_class']}")
#                 print(f"  Delegates To: {p.get('delegates_to', [])}")
#                 print(f"  Forwarded Methods: {p.get('forwarded_methods', [])}\n")
#     except Exception as e:
#         print("\n=== Proxy Pattern ===")
#         print(f"Error detecting proxy pattern: {e}")

#     # Singleton Pattern
#     singleton_matches = singleton.find(db).get("singleton", [])
#     print("\n=== Singleton Pattern ===")
#     if not singleton_matches:
#         print("No Singleton patterns found.")
#     else:
#         for s in singleton_matches:
#             print(f"Singleton Class: {s['singleton_class']}")
#             if s.get("from_fallback"):
#                 print("  (Detected via source code fallback)")
#                 print(f"  Has Static Final Field: {s.get('has_static_final_field', False)}")
#                 print(f"  Accessed Externally: {s.get('accessed_externally', False)}")
#             else:
#                 print(f"  Static Field(s): {s.get('static_fields', [])}")
#                 print(f"  Accessors: {s.get('accessors', [])}")
#                 print(f"  Has Private Constructor: {s.get('has_private_constructor', False)}")

# if __name__ == "__main__":
#     main()
