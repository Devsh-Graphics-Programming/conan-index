import os

from conan import ConanFile
from conan.tools.cmake import CMake, CMakeDeps, CMakeToolchain, cmake_layout
from conan.tools.files import copy, download, get

required_conan_version = ">=2.32.0"


class DxcConan(ConanFile):
    name = "dxc"
    description = "DirectX Shader Compiler which is based on LLVM/Clang, with adjustments for Nabla usage"
    license = ("LLVM Release License")
    url = "https://github.com/Devsh-Graphics-Programming/conan-index"
    homepage = "https://github.com/Devsh-Graphics-Programming/DirectXShaderCompiler"
    topics = ("dxc", "nabla")

    package_type = "static-library"
    settings = "os", "arch", "compiler", "build_type"
    options = {
        "fPIC": [True, False],
    }
    default_options = {
        "fPIC": True,
    }

    def export_sources(self):
        copy(self, "CMakeLists.txt", self.recipe_folder, self.export_sources_folder)

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def layout(self):
        cmake_layout(self, src_folder="src")

    def requirements(self):
        self.requires("freetype/[>2.14.1]", transitive_headers=True)

    def source(self):
        get(self, **self.conan_data["sources"][self.version], strip_root=True, destination="dxc")

    def generate(self):
        tc = CMakeToolchain(self)
        tc.variables["DXC_SOURCE_DIR"] = self.source_folder.replace("\\", "/")
        tc.variables["COMPILER_DYNAMIC_RUNTIME"] = True
        tc.generate()
        deps = CMakeDeps(self)
        deps.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure(build_script_folder=os.path.join(self.source_folder, os.pardir))
        cmake.build()

    def package(self):
        licenses = os.path.join(self.package_folder, "licenses")
        include = os.path.join(self.package_folder, "include")
        dxc = os.path.join(self.source_folder, "dxc")

        copy(self, "LICENSE.TXT", dxc, os.path.join(licenses, "dxc"))

        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        self.cpp_info.set_property("cmake_file_name", "dxc")

        dxc = self.cpp_info.components["dxcompiler"]
        dxc.set_property("cmake_target_name", "dxc::dxc")
        dxc.libs = ["dxcompiler"]
        dxc.includedirs.append(os.path.join("include", "dxc"))
