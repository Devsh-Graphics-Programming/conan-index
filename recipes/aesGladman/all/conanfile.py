from conan import ConanFile
from conan.tools.cmake import CMake, CMakeToolchain, cmake_layout
from conan.tools.files import copy, get, rmdir
from conan.tools.scm import Version
import os

required_conan_version = ">=2.32.0"


class AesGladmanConan(ConanFile):
    name = "aesGladman"
    homepage = "https://github.com/Devsh-Graphics-Programming/aes"
    description = "AES code"
    license = "Copyright-BrianGladman"
    topics = ("encryption")
    url = "https://github.com/Devsh-Graphics-Programming/conan-index"
    settings = "os", "arch", "compiler", "build_type"

    def export_sources(self):
        copy(self, "CMakeLists.txt", self.recipe_folder, self.export_sources_folder)

    def layout(self):
        cmake_layout(self, src_folder="src")

    def source(self):
        get(self, **self.conan_data["sources"][self.version], strip_root=True, destination="aesGladman")

    def generate(self):
        tc = CMakeToolchain(self)
        tc.variables["AES_SOURCE_DIR"] = self.source_folder.replace("\\", "/")
        tc.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure(build_script_folder=os.path.join(self.source_folder, os.pardir))
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        self.cpp_info.set_property("cmake_file_name", "aesGladman")
        self.cpp_info.set_property("cmake_target_name", "aesGladman::aes")
        self.cpp_info.set_property("pkg_config_name", "aesGladman")
        self.cpp_info.components["aesGladman"].libs = ["aesGladman"]
