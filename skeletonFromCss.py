# python3^

import json
from splicer import jload, jdump

def main():
    skele = jload("Radon_Skeleton.json")
    css = [ln for ln in getFileData("Radon.css").split("\n")]

    d = {}
    for line in css:
        ln = line.split("{")
        left = ln[0].strip()
        rt = ln[1].split(":")[1].replace("}", "").strip()
        d[left] = rt

    skele["colors"] = d
    jdump(skele, "Radon_Skeleton.json")


def getFileData(path: str) -> str:
    with open(path, "r") as f:
        return f.read()

if __name__ == "__main__":
    main()