# python3^
from sys import argv
from pathlib import Path
import json


class Theme:

    def jload(filePath: str) -> str:
            with open(f"{filePath}", "r") as possibleMatch:
                dat = json.load(possibleMatch)
            return dat

    def isTheme(filePath: str) -> bool:

        dat = Theme.jload(filePath)        

        try:
            dat = Theme.jload(filePath)
            if "tokenColors" in dat.keys():
                  return True
            else: return False

        except: IsADirectoryError

    def splice(filePath: str):

        dat = Theme.jload(filePath)
        radon = Theme.jload("Radon_Skeleton.json")
        radon["tokenColors"] = dat["tokenColors"]

        if confirm("Done. Saving file?"):
            print("(don't have to put .json on the end)")
            name = "Radon-" + input("Spliced theme name? :  Radon-")

            if name.__contains__("json"):
                name = name.replace("json", "")

            with open(f"themes/{name}.json", "w+") as output:
                json.dump(radon, output)

            with open("package_skeleton.json", "r") as package:
                dat = json.load(package)    
            
            dat["contributes"]["themes"].append({
                "label": f"{name}",
                "uiTheme": "vs-dark",
                "path": f"./themes/{name}.json"
            })

            with open("package.json", "w+") as package:
                json.dump(dat, package)


def confirm(msg: str):
    print(msg); inp = input().strip()
    if inp == "y": return True
    else: return False


def check(filePath: str):
    if Theme.isTheme(filePath) == True:
        if confirm(f"Is {filePath} a VSCode theme .json?"):
            if confirm(f"Splice {filePath}'s syntax into a Radon theme?"):
                Theme.splice(filePath)


def dirTrav(filePath: str):

    if not Path.is_dir(Path(filePath)):
        check(filePath)

    else:
        for ith_file in Path.iterdir(Path(filePath)):

            if str(ith_file).__contains__(".json"):
                check(ith_file)
            
            elif Path.is_dir(ith_file):
                dirTrav(ith_file)
        

def main():
    if len(argv) > 1:
        ls = []
        [ls.append(argv[x]) for x in range(1, (len(argv)))]
        [dirTrav(i) for i in ls]

    else:
        hm = Path.home()
        msg = "Is <" + str(hm) + "> your home dir?  (y | n)\n"
        if confirm(msg):
            msg = "Search in ~/.vscode/extensions/* for themes to splice?"
            if confirm(msg):
                pth = Path(str(hm) + "/.vscode/extensions/")
                dirTrav(pth)

        else: print("closing out, then"); exit(0)

main()