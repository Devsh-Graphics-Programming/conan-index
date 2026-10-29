from conan import ConanFile
from conan.tools.cmake import CMake, CMakeToolchain, cmake_layout
from conan.tools.files import copy, get, rmdir
from conan.tools.scm import Version
import os

required_conan_version = ">=2.32.0"


class RenderdocConan(ConanFile):
    name = "renderdoc"
    homepage = "https://github.com/baldurk/renderdoc"
    description = "Renderdoc in-application API header"
    license = "MIT"
    topics = ("vulkan", "opengl")
    url = "https://github.com/Devsh-Graphics-Programming/conan-index"
    package_type = "header-library"
    settings = "os", "arch", "compiler", "build_type"

    def export_sources(self):
        copy(self, "CMakeLists.txt", self.recipe_folder, self.export_sources_folder)

    def layout(self):
        cmake_layout(self, src_folder="src")

    def source(self):
        get(self, **self.conan_data["sources"][self.version], strip_root=True, destination="rdoc")

    def generate(self):
        tc = CMakeToolchain(self)
        tc.variables["RDOC_SOURCE_DIR"] = self.source_folder.replace("\\", "/")
        tc.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure(build_script_folder=os.path.join(self.source_folder, os.pardir))
        cmake.build()

    def package(self):
        copy(self, "LICENSE*", src=self.source_folder, dst=os.path.join(self.package_folder, "licenses"))
        cmake = CMake(self)
        cmake.install()
        rmdir(self, os.path.join(self.package_folder, "lib"))

    def package_info(self):
        self.cpp_info.set_property("cmake_file_name", "renderdoc")
        self.cpp_info.set_property("cmake_target_name", "renderdoc::renderdoc_app")
        self.cpp_info.set_property("pkg_config_name", "renderdoc")
        self.cpp_info.bindirs = []
        self.cpp_info.libdirs = []
