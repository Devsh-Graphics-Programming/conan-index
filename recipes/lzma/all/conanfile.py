from conan import ConanFile
from conan.tools.cmake import CMake, CMakeToolchain, cmake_layout
from conan.tools.files import copy, get, rmdir
from conan.tools.scm import Version
import os

required_conan_version = ">=2.32.0"


class LzmaConan(ConanFile):
    name = "lzma"
    homepage = "https://github.com/ip7z/7zip"
    description = "LZMA SDK for 7zip"
    license = "LGPL"
    topics = ("compression")
    url = "https://github.com/Devsh-Graphics-Programming/conan-index"
    settings = "os", "arch", "compiler", "build_type"

    def export_sources(self):
        copy(self, "CMakeLists.txt", self.recipe_folder, self.export_sources_folder)

    def layout(self):
        cmake_layout(self, src_folder="src")

    def source(self):
        get(self, **self.conan_data["sources"][self.version], strip_root=True, destination="lzma")

    def generate(self):
        tc = CMakeToolchain(self)
        tc.variables["LZMA_SOURCE_DIR"] = self.source_folder.replace("\\", "/")
        tc.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure(build_script_folder=os.path.join(self.source_folder, os.pardir))
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        self.cpp_info.set_property("cmake_file_name", "lzma")
        self.cpp_info.set_property("cmake_target_name", "lzma::lzma")
        self.cpp_info.set_property("pkg_config_name", "lzma")
        self.cpp_info.components["lzma"].libs = ["lzma"]
