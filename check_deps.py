import csv

with open('deps.csv', newline='') as f:
    reader = csv.reader(f)
    header = next(reader)
    n_cols = len(header)
    bad = []
    for i, row in enumerate(reader, start=2):
        if len(row) != n_cols:
            bad.append((i, len(row)))
    if not bad:
        print(f"✅ All {i} rows have the expected {n_cols} columns.")
    else:
        print("❌ Found rows with wrong column counts:")
        for line_num, count in bad:
            print(f"  • Line {line_num}: {count} columns (expected {n_cols})")