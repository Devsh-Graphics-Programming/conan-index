import os

from conan import ConanFile
from conan.tools.cmake import CMake, CMakeDeps, CMakeToolchain, cmake_layout
from conan.tools.files import copy, get, rmdir, replace_in_file

required_conan_version = ">=2"


class VulkanToolsConan(ConanFile):
    name = "vulkan-tools"
    description = "Vulkan Development Tools"
    license = "Apache-2.0"
    topics = ("vulkan-tools", "vulkan")
    homepage = "https://github.com/Devsh-Graphics-Programming/Vulkan-Tools"
    url = "https://github.com/Devsh-Graphics-Programming/conan-index"
    package_id_embed_mode = "patch_mode"
    settings = "os", "arch", "compiler", "build_type"
    no_copy_source = True

    def layout(self):
        cmake_layout(self, src_folder="src")

    def requirements(self):
        devsh_version_suffix = self.version.find("-devsh")
        vulkan_version = self.version[:devsh_version_suffix]
        self.requires(f"vulkan-headers/{vulkan_version}", transitive_headers=True)

    def source(self):
        get(self, **self.conan_data["sources"][self.version], strip_root=True)
        self._patch_sources()

    def _patch_sources(self):
        replace_in_file(self, os.path.join(self.source_folder, "CMakeLists.txt"), "set(CMAKE_CXX_STANDARD 17)", "set(CMAKE_CXX_STANDARD 20)")
        replace_in_file(self, os.path.join(self.source_folder, "CMakeLists.txt"), "find_package(VulkanHeaders ${PROJECT_VERSION} QUIET REQUIRED CONFIG)", "find_package(VulkanHeaders REQUIRED CONFIG)")
        replace_in_file(self, os.path.join(self.source_folder, "CMakeLists.txt"), "set(CMAKE_MSVC_RUNTIME_LIBRARY \"MultiThreaded$<$<CONFIG:Debug>:Debug>\")", "")
        replace_in_file(self, os.path.join(self.source_folder, "vulkaninfo", "CMakeLists.txt"), "add_library(vulkaninfo OBJECT)", "add_library(vulkaninfo STATIC)")
        replace_in_file(self, os.path.join(self.source_folder, "vulkaninfo", "CMakeLists.txt"), "    Vulkan-Headers", "    vulkan-headers::vulkan-headers")
        replace_in_file(self, os.path.join(self.source_folder, "vulkaninfo", "CMakeLists.txt"), "install(TARGETS vulkaninfo)", "install(TARGETS vulkaninfo ARCHIVE DESTINATION lib)")

    def generate(self):
        tc = CMakeToolchain(self)
        tc.variables["BUILD_CUBE"] = False
        tc.variables["BUILD_VULKANINFO"] = True
        tc.variables["BUILD_ICD"] = False
        tc.variables["BUILD_TESTS"] = False
        tc.variables["BUILD_WERROR"] = False
        tc.generate()
        deps = CMakeDeps(self)
        deps.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        copy(self, "LICENSE*", src=self.source_folder, dst=os.path.join(self.package_folder, "licenses"))
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        self.cpp_info.set_property("cmake_file_name", "VulkanTools")
        self.cpp_info.components["vulkaninfo"].set_property("cmake_target_name", "vulkan-tools::vulkaninfo")
        self.cpp_info.components["vulkaninfo"].libs = ["vulkaninfo"]
        self.cpp_info.components["vulkaninfo"].requires = ["vulkan-headers::vulkan-headers"]
        self.cpp_info.components["vulkaninfo"].includedirs = []
