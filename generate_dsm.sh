#!/usr/bin/env bash
set -e

# 1) UDB path
UDB_PATH=$1
# 2) source directory (where your .java lives)
SRC_DIR=$2
# 3) output .dsm
OUT_DSM=$3

echo "1) Creating/opening Understand DB → $UDB_PATH"
"/c/Program Files/SciTools/bin/pc-win64/und.exe" create -db "$UDB_PATH" -languages java

echo "2) Adding source files from $SRC_DIR"
"/c/Program Files/SciTools/bin/pc-win64/und.exe" -db "$UDB_PATH" add "$SRC_DIR"

echo "3) Analyzing…"
"/c/Program Files/SciTools/bin/pc-win64/und.exe" analyze "$UDB_PATH"

echo "4) Exporting DSM (matrix format) → $OUT_DSM"
"/c/Program Files/SciTools/bin/pc-win64/und.exe" export -dependencies file matrix "$OUT_DSM" "$UDB_PATH"

echo "✅ Done! Your DSM is at $OUT_DSM"