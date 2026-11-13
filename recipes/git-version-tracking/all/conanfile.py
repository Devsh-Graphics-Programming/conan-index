from conan import ConanFile
from conan.tools.files import copy, get, rmdir
from conan.tools.scm import Version
import os

required_conan_version = ">=2.32.0"


class GitVersionTrackingConan(ConanFile):
    name = "git-version-tracking"
    homepage = "https://github.com/Devsh-Graphics-Programming/cmake-git-version-tracking"
    description = "Embed Git metadata in a C/C++ compatible static library using CMake"
    license = "MIT"
    topics = ("git", "cmake")
    url = "https://github.com/Devsh-Graphics-Programming/conan-index"
    package_type = "build-scripts"
    settings = "os", "arch", "compiler", "build_type"

    def source(self):
        get(self, **self.conan_data["sources"][self.version], strip_root=True)

    def package(self):
        copy(self, "LICENSE*", src=self.source_folder, dst=os.path.join(self.package_folder, "licenses"))
        copy(self, "*.cmake", src=self.source_folder, dst=os.path.join(self.package_folder, "cmake"))
        copy(self, "CMakeLists.txt", src=self.source_folder, dst=os.path.join(self.package_folder, "cmake"))
        copy(self, "*.in", src=self.source_folder, dst=os.path.join(self.package_folder, "cmake"))

    def package_info(self):
        self.cpp_info.set_property("cmake_file_name", "git-version-tracking")
        self.cpp_info.set_property("cmake_target_name", "git-version-tracking")
        self.cpp_info.set_property("pkg_config_name", "git-version-tracking")
        self.cpp_info.bindirs = []
        self.cpp_info.libdirs = []
        self.cpp_info.includedirs = []
        self.cpp_info.builddirs = ["cmake"]
        self.cpp_info.set_property("cmake_build_modules", [os.path.join(self.package_folder, "cmake", "CMakeLists.txt")])
