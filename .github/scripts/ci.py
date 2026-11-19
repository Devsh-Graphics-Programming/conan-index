from subprocess import check_call, check_output
import os
import sys
from pathlib import Path
import yaml
import json
import argparse

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

    parser = argparse.ArgumentParser()
    parser.add_argument("--host-profile", required=True)
    parser.add_argument("--build-profile", required=True)
    parser.add_argument("--build-type", required=True, choices=["Debug", "Release", "RelWithDebInfo"])
    parser.add_argument("--full-rebuild", action="store_true", default=os.environ.get("CONAN_FULL_REBUILD", "").lower() in ("true", "1"))

    args = parser.parse_args()
    profile_host = args.host_profile
    profile_build = args.build_profile
    build_type = args.build_type
    do_full_rebuild = args.full_rebuild

    # make all recipes known to cache
    for name in recipes:
        for version in recipes[name]:
            check_call(f"conan export --version {version} ./recipes/{name}/all/", shell=True)

    # create and upload
    requires = [f"--requires={name}/{version}" for name, versions in recipes.items() for version in versions]
    build_args = [f"--build=\"*\"" if do_full_rebuild else f"--build=missing"]
    try:
        check_call([
            "conan", "install", *requires,
            f"-pr:h={profile_host}", f"-pr:b={profile_build}",
            f"-s:h=build_type={build_type}", *build_args,
            f"-of=build/{build_type}",
        ], shell=True)
    finally:
        if os.environ.get("CONAN_UPLOAD_PACKAGES", "").lower() in ("true", "1"):
            upload = ["conan", "upload", "*", "-r=devsh", "--confirm", "--check"]
            if os.environ.get("UPLOAD_ALL", "").lower() not in ("true", "1"):
                upload.append("--only-recipe")
            check_call(upload, shell=True)

    print("-----Finished-----")
