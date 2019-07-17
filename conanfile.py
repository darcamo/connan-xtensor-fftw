from conans import ConanFile, CMake, tools
import os
import shutil


class XtensorfftwConan(ConanFile):
    name = "xtensor-fftw"
    version = "0.2.5"
    license = "BSD-3"
    url = "https://github.com/darcamo/connan-xtensor-fftw"
    description = "FFTW bindings for xtensor "
    no_copy_source = True
    generators = "cmake"
    # No settings/options are necessary, this is header only

    def requirements(self):
        self.requires("fftw3/3.3.8@darcamo/stable")
        self.requires("xtensor/[>=0.16.4]@darcamo/stable")

    def source(self):
        tools.get(
            "https://github.com/egpbos/xtensor-fftw/archive/{0}.zip".format(
                self.version))
        shutil.move("xtensor-fftw-{0}".format(self.version), "sources")

        tools.replace_in_file(
            "sources/CMakeLists.txt", "project(xtensor-fftw)",
            """project(xtensor-fftw)
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()""")

    def build(self):
        os.mkdir("build")
        shutil.move("conanbuildinfo.cmake", "build/")

        cmake = CMake(self)
        cmake.configure(source_folder="sources", build_folder="build")
        cmake.install()

    def package_info(self):
        self.cpp_info.libdirs = ["lib64", "lib"]
