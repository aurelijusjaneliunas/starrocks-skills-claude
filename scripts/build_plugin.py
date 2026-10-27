#!/usr/bin/env python3
import os
import sys
import zipfile


def add(zf, path):
    if os.path.isdir(path):
        for root, _, files in os.walk(path):
            for name in files:
                full = os.path.join(root, name)
                zf.write(full, full.replace(os.sep, "/"))
    else:
        zf.write(path, path.replace(os.sep, "/"))


def main():
    out, *sources = sys.argv[1:]
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as zf:
        for src in sources:
            add(zf, src)


if __name__ == "__main__":
    main()
