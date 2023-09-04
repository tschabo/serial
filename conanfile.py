from conan import ConanFile
from conan.tools.cmake import CMakeToolchain, CMake, cmake_layout, CMakeDeps
from conan.tools.files import copy
from conan.tools.apple import is_apple_os
import os

class serialRecipe(ConanFile):
    name = "serial"
    package_type = "library"

    license = "MIT"
    homepage = "http://wjwwood.io/serial/"
    url = "https://github.com/conan-io/conan-center-index"
    description = "Cross-platform library for interfacing with rs-232 serial like ports"
    topics = ("serial", "rs-232", "com")

    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}

    exports_sources = exports_sources = "CMakeLists.txt", "src/*", "include/*"

    def config_options(self):
        if self.settings.os == "Windows":
            self.options.rm_safe("fPIC")

    def configure(self):
        if self.options.shared:
            self.options.rm_safe("fPIC")

    def layout(self):
        cmake_layout(self)

    def generate(self):
        deps = CMakeDeps(self)
        deps.generate()
        tc = CMakeToolchain(self)
        tc.cache_variables["CMAKE_WINDOWS_EXPORT_ALL_SYMBOLS"] = self.options.shared
        tc.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()
        copy(self, "LICENSE", src=self.source_folder, dst=os.path.join(self.package_folder,"licenses"))

    def package_info(self):
        self.cpp_info.libs = ["serial"]
        if self.settings.os == "Windows":
            self.cpp_info.system_libs = ["setupapi"]
        elif self.settings.os == "Linux":
            self.cpp_info.system_libs = ["rt", "pthread"]
        elif is_apple_os(self):
            self.cpp_info.frameworks = ["IOKit", "Foundation"]