import os

from conan import ConanFile
from conan.tools.cmake import CMake, CMakeDeps, CMakeToolchain, cmake_layout
from conan.tools.files import copy, download, get

required_conan_version = ">=2.32.0"


class NablaImguiConan(ConanFile):
    name = "nabla_imgui"
    description = "Dear ImGui, Dear ImGui Test Engine, ImPlot and ImGuizmo built with Nabla's nabla_imconfig.h"
    license = ("MIT", "LicenseRef-Dear-ImGui-Test-Engine-License-1.04")
    url = "https://github.com/Devsh-Graphics-Programming/conan-index"
    homepage = "https://github.com/ocornut/imgui"
    topics = ("imgui", "imgui-test-engine", "implot", "imguizmo", "gui", "nabla")

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
        sources = self.conan_data["sources"][self.version]
        get(self, **sources["imgui"], strip_root=True, destination="imgui")
        download(self, **sources["nabla_imconfig"], filename=os.path.join("imgui", "nabla_imconfig.h"))
        get(self, **sources["imgui_test_engine"], strip_root=True, destination="imgui_test_engine")
        get(self, **sources["implot"], strip_root=True,
            destination=os.path.join("imgui_test_engine", "imgui_test_suite", "thirdparty", "implot"))
        get(self, **sources["imguizmo"], strip_root=True, destination="imguizmo")

    def generate(self):
        tc = CMakeToolchain(self)
        tc.variables["NABLA_IMGUI_SOURCE_DIR"] = self.source_folder.replace("\\", "/")
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
        imgui = os.path.join(self.source_folder, "imgui")
        test_engine_project = os.path.join(self.source_folder, "imgui_test_engine")
        test_engine = os.path.join(test_engine_project, "imgui_test_engine")
        test_suite = os.path.join(test_engine_project, "imgui_test_suite")
        implot = os.path.join(test_suite, "thirdparty", "implot")
        imguizmo = os.path.join(self.source_folder, "imguizmo")

        copy(self, "LICENSE.txt", imgui, os.path.join(licenses, "imgui"))
        copy(self, "LICENSE.txt", test_engine, os.path.join(licenses, "imgui_test_engine"))
        copy(self, "LICENSE.txt", test_suite, os.path.join(licenses, "imgui_test_suite"))
        copy(self, "LICENSE.txt", os.path.join(test_engine_project, "shared"), os.path.join(licenses, "imgui_test_engine_shared"))
        copy(self, "LICENSE", implot, os.path.join(licenses, "implot"))
        copy(self, "LICENSE", imguizmo, os.path.join(licenses, "imguizmo"))

        copy(self, "*.h", imgui, os.path.join(include, "imgui"), excludes=("examples/*", "docs/*"))
        copy(self, "*.h", test_engine, os.path.join(include, "imgui_test_engine"))
        copy(self, "*.h", test_suite, os.path.join(include, "imgui_test_suite"))
        copy(self, "*.h", imguizmo, os.path.join(include, "imguizmo"), excludes=("example/*", "vcpkg-example/*", "bin/*"))

        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        self.cpp_info.set_property("cmake_file_name", "nabla_imgui")

        imgui = self.cpp_info.components["imgui"]
        imgui.set_property("cmake_target_name", "nabla_imgui::imgui")
        imgui.libs = ["imgui"]
        imgui.includedirs = [
            "include",
            os.path.join("include", "imgui"),
            os.path.join("include", "imgui", "misc", "cpp"),
            os.path.join("include", "imgui", "backends"),
            os.path.join("include", "imgui_test_suite"),
        ]
        imgui.defines = ['IMGUI_USER_CONFIG="nabla_imconfig.h"']
        imgui.requires = ["freetype::freetype"]
        if self.settings.os == "Windows":
            imgui.system_libs = ["imm32", "shell32"]
        elif self.settings.os in ("Linux", "FreeBSD"):
            imgui.system_libs = ["m"]

        implot = self.cpp_info.components["implot"]
        implot.set_property("cmake_target_name", "nabla_imgui::implot")
        implot.libs = ["implot"]
        implot.includedirs = [os.path.join("include", "imgui_test_suite", "thirdparty", "implot")]
        implot.defines = ["IMPLOT_DEBUG", "IMPLOT_DLL_EXPORT"]
        implot.requires = ["imgui"]

        test_engine_includedirs = [
            "include",
            os.path.join("include", "imgui_test_engine"),
            os.path.join("include", "imgui_test_suite"),
        ]

        imtestsuite = self.cpp_info.components["imtestsuite"]
        imtestsuite.set_property("cmake_target_name", "nabla_imgui::imtestsuite")
        imtestsuite.libs = ["imtestsuite"]
        imtestsuite.includedirs = list(test_engine_includedirs)
        imtestsuite.requires = ["implot"]

        imtestengine = self.cpp_info.components["imtestengine"]
        imtestengine.set_property("cmake_target_name", "nabla_imgui::imtestengine")
        imtestengine.libs = ["imtestengine"]
        imtestengine.includedirs = list(test_engine_includedirs)
        imtestengine.requires = ["imtestsuite"]
        if self.settings.os == "Windows":
            imtestengine.system_libs = ["shell32"]
        elif self.settings.os in ("Linux", "FreeBSD"):
            imtestengine.system_libs = ["pthread"]

        imguizmo = self.cpp_info.components["imguizmo"]
        imguizmo.set_property("cmake_target_name", "nabla_imgui::imguizmo")
        imguizmo.libs = ["imguizmo"]
        imguizmo.includedirs = [os.path.join("include", "imguizmo")]
        imguizmo.requires = ["imgui"]
