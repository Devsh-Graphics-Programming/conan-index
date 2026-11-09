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

    platIsWin = os.environ['PLATFORM'] == "windows-latest"
    platform = "Windows" if platIsWin else "Linux"
    profile = "windows-msvc194-x64-mt" if platIsWin else "linux-clang22-x64"

    do_full_rebuild = "full_rebuild" in sys.argv[1:]
    do_full_rebuild = do_full_rebuild or ('CONAN_FULL_REBUILD' in os.environ and os.environ['CONAN_FULL_REBUILD'])
    if not do_full_rebuild:
        # prevent recipes already available on remote being rebuilt
        available_recipes = getRemoteAvailableRecipes()
        for name in available_recipes:
            if name in recipes:
                for version in available_recipes[name]:
                    if platform in available_recipes[name][version]:
                        recipes[name].pop(version)

    # make all recipes known to cache
    for name in recipes:
        for version in recipes[name]:
            check_call(f"conan export --version {version} ./recipes/{name}/all/", shell=True)

    # reorder package create order by dependency
    recipe_dependency_order = []
    for name in recipes:
        for version in recipes[name]:
            recipe_graph_string = check_output(f"conan graph build-order --order-by=recipe --version {version} --format=json --build=missing -pr:a={profile} ./recipes/{name}/all/", shell=True).decode('UTF-8')
            graph_json = json.loads(recipe_graph_string)
            for dep_level in graph_json["order"]:
                for dep in dep_level:
                    dep_ref = dep["ref"]
                    np = dep_ref.split("/")
                    dep_name = np[0]
                    dep_version = np[1].split("#")[0]
                    dep_name_version = (dep_name, dep_version)
                    if dep_name in recipes and dep_name_version not in recipe_dependency_order:
                        recipe_dependency_order.append(dep_name_version)
            name_version = (name, version)
            if name_version not in recipe_dependency_order:
                recipe_dependency_order.append(name_version)

    # create and upload
    for name, version in recipe_dependency_order:
        package_ref = f"{name}/{version}"
        print(f"Building recipe: {package_ref}...")
        check_call(f"conan create --version {version} -tf \"\" -u --build=missing -pr:a={profile} ./recipes/{name}/all/", shell=True)

    if 'CONAN_UPLOAD_PACKAGES' in os.environ and os.environ['CONAN_UPLOAD_PACKAGES']:
        upload_all = False
        if 'UPLOAD_ALL' in os.environ and os.environ['UPLOAD_ALL'] == 'true':
            upload_all = True
        for name, version in recipe_dependency_order:
            package_ref = f"{name}/{version}"
            if upload_all:
                print(f"Uploading recipe and package: {package_ref}")
                check_call(f"conan upload {package_ref} -r=devsh --confirm --check", shell=True)
            else:
                print(f"Uploading recipe: {package_ref}")
                check_call(f"conan upload {package_ref} -r=devsh --confirm --check --only-recipe", shell=True)

    print("-----Finished-----")
