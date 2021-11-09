# python3^
from sys import argv
from pathlib import Path
import json


def jload(filePath: str) -> dict:
        with open(f"{filePath}", "r") as possibleMatch:
            return json.load(possibleMatch)

def jdump(data: dict, filePath: str):
    with open(filePath, "w+") as f:
        json.dump(data, f, indent=4)

def isTheme(filePath: str) -> bool:
    try:
        d = jload(filePath)
        return "tokenColors" in d.keys()

    except: 
        IsADirectoryError

def splice(filePath: str):
    d = jload(filePath)
    radon = jload("Radon_Skeleton.json")
    radon["tokenColors"] = d["tokenColors"]

    if confirm("Done. Saving file?"):
        print("(don't have to put .json on the end)")
        name = "Radon-" + input("Spliced theme name? :  Radon-")

        if "json" in name:
            name = name.replace("json", "")

        jdump(radon, f"themes/{name}.json")

        d = jload("package_skeleton.json")
        
        d["contributes"]["themes"].append({
            "label": f"{name}",
            "uiTheme": "vs-dark",
            "path": f"./themes/{name}.json"
        })

        jdump(d, "package.json")


def confirm(msg: str):
    print(msg)
    return input().strip().lower() == "y"


def check(filePath: str):
    if isTheme(filePath):
        if confirm(f"Is {filePath} a VSCode theme .json?"):
            if confirm(f"Splice {filePath}'s syntax into a Radon theme?"):
                splice(filePath)


def dirTrav(filePath: str):
    if not Path.is_dir(Path(filePath)):
        check(filePath)

    else:
        for ith_file in Path.iterdir(Path(filePath)):

            if ".json" in str(ith_file):
                check(ith_file)
            
            elif Path.is_dir(ith_file):
                dirTrav(ith_file)
        

def main():
    if len(argv) > 1:
        ls = []
        (ls.append(argv[x]) for x in range(1, (len(argv))))
        (dirTrav(i) for i in ls)

    else:
        hm = Path.home()
        msg = f"Is <{str(hm)}> your home dir?  (y | n) "
        if confirm(msg):
            msg = "Search in ~/.vscode/extensions/* for themes to splice?"
            if confirm(msg):
                pth = Path(str(hm) + "/.vscode/extensions/")
                dirTrav(pth)

        else: print("closing out, then"); exit(0)

if __name__ == "__main__":
    main()