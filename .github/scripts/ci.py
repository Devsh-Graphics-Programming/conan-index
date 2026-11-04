from subprocess import check_call, check_output
import os
import sys
from pathlib import Path
import yaml
import json

def readYMLForVersions(recipe_dir: Path) -> list:
    with open(recipe_dir / "config.yml", "r") as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    return list(config['versions'].keys())

def getRemoteAvailableRecipes() -> dict:
    available_recipes_bytes = check_output(f"conan list \"*/*:*#*\" -r=devsh --format=json", shell=True)
    available_recipes_string = available_recipes_bytes.decode('UTF-8')
    json_begin_ix = available_recipes_string.find("{")
    recipes_json = json.loads(available_recipes_string[json_begin_ix:])
    devsh_remote_recipes = recipes_json["devsh"]
    available_recipes = {}
    for entry in devsh_remote_recipes:
        name_version = entry.strip().split("/")
        name = name_version[0]
        version = name_version[1]
        platforms = set()
        for rev1 in devsh_remote_recipes[entry]["revisions"]:
            rev = devsh_remote_recipes[entry]["revisions"][rev1]
            for pkg in rev["packages"]:
                setting = rev["packages"][pkg]["info"]["settings"]
                if bool(setting):
                    platforms.add(setting["os"])
        if name in available_recipes:
            available_recipes[name][version] = platforms
        else:
            available_recipes[name] = {version: platforms}
    return available_recipes

if __name__ == "__main__":
    recipes = {}
    for package in os.listdir("./recipes"):
        recipes[package] = readYMLForVersions(Path("./recipes") / package)

    platform = "Windows" if os.environ['PLATFORM'] == "windows-latest" else "Linux"

    do_full_rebuild = "full_rebuild" in sys.argv[1:]
    do_full_rebuild = do_full_rebuild or ('CONAN_FULL_REBUILD' in os.environ and os.environ['CONAN_FULL_REBUILD'])
    if not do_full_rebuild:
        available_recipes = getRemoteAvailableRecipes()
        for name in available_recipes:
            if name in recipes:
                for version in available_recipes[name]:
                    if platform in available_recipes[name][version]:
                        recipes[name].pop(version)

    for name in recipes:
        for version in recipes[name]:
            package_ref = f"{name}/{version}"
            print(f"Building recipe: {package_ref}...")
            check_call(f"conan create --version {version} -s=\"compiler.cppstd=gnu20\" -tf \"\" -u -b missing ./recipes/{name}/all/", shell=True)

    if 'CONAN_UPLOAD_PACKAGES' in os.environ and os.environ['CONAN_UPLOAD_PACKAGES']:
        upload_all = False
        if 'UPLOAD_ALL' in os.environ and os.environ['UPLOAD_ALL'] == 'true':
            upload_all = True

        for name in recipes:
            for version in recipes[name]:
                package_ref = f"{name}/{version}"
                if upload_all:
                    print(f"Uploading recipe and package: {package_ref}")
                    check_call(f"conan upload {package_ref} -r=devsh --confirm --check", shell=True)
                else:
                    print(f"Uploading recipe: {package_ref}")
                    check_call(f"conan upload {package_ref} -r=devsh --confirm --check --only-recipe", shell=True)

    print("-----Finished-----")
