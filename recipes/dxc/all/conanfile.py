import os

from conan import ConanFile
from conan.tools.cmake import CMake, CMakeDeps, CMakeToolchain, cmake_layout
from conan.tools.files import copy, download, get
from conan.tools.files import apply_conandata_patches, copy, export_conandata_patches, get, rmdir

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
        export_conandata_patches(self)

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def layout(self):
        cmake_layout(self, src_folder="src")

    def requirements(self):
        if self.settings.os == "Linux":
            self.requires("directx-headers/1.619.1")
        self.requires("spirv-headers/1.4.363.0-devsh.1")
        self.requires("spirv-tools/1.4.363.0-devsh.1", options={"shared": False})

    def source(self):
        get(self, **self.conan_data["sources"][self.version], strip_root=True, destination="dxc")
        apply_conandata_patches(self)

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
        copy(self, "*.h", dxc, os.path.join(include, "dxc"), excludes=("examples/*", "docs/*"))

        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        self.cpp_info.set_property("cmake_file_name", "dxc")

        dxc = self.cpp_info.components["dxcompiler"]
        dxc.set_property("cmake_target_name", "dxc::dxcompiler")
        dxc.libs = ["dxcompiler"]
        dxc.includedirs.append(os.path.join("include", "dxc"))
        dxc.libdirs = ["lib"]
