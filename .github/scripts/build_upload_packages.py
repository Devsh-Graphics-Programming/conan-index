from subprocess import check_output, check_call
import os
import string
from pathlib import Path
import yaml # need to pip install pyyaml

def readYMLForVersions(recipe_dir: Path) -> list:
    with open(recipe_dir / "config.yml", "r") as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    return list(config['versions'].keys())

if __name__ == "__main__":
    recipes = {}
    for package in os.listdir("./recipes"):
        recipes[package] = readYMLForVersions(Path("./recipes") / package)

    for name in recipes:
        for version in recipes[name]:
            package_ref = f"{name}/{version}"
            print(f"Building recipe: {package_ref}...")
            check_call(f"conan create --version {version} -tf \"\" -u -b missing ./recipes/{name}/all/", shell=True)

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
