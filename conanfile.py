from conans import ConanFile, CMake, tools
import os
import shutil


class XtensorfftwConan(ConanFile):
    name = "xtensor-fftw"
    version = "0.2.4"
    license = "<Put the package license here>"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "<Description of Xtensorfftw here>"
    no_copy_source = True
    generators = "cmake"
    # No settings/options are necessary, this is header only

    def requirements(self):
        self.requires("fftw3/3.3.8@darcamo/stable")
        self.requires("xtensor/0.16.4@darcamo/stable")

    def source(self):
        tools.get("https://github.com/egpbos/xtensor-fftw/archive/{0}.zip".format(self.version))
        shutil.move("xtensor-fftw-{0}".format(self.version), "sources")

        tools.replace_in_file("sources/CMakeLists.txt", "project(xtensor-fftw)",
                              """project(xtensor-fftw)
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()""")

        # Hack: For some reason we can't find the required components even
        # though we have included them in the FFTW recipe (the dependency) ->
        # Change the find_package to remove the explicit components
        tools.replace_in_file("sources/CMakeLists.txt", """    find_package(FFTW REQUIRED
            COMPONENTS FLOAT_LIB DOUBLE_LIB LONGDOUBLE_LIB)""",
                              '''    find_package(FFTW REQUIRED)''')

    def build(self):
        os.mkdir("build")
        shutil.move("conanbuildinfo.cmake", "build/")

        cmake = CMake(self)
        cmake.configure(source_folder="sources", build_folder="build")
        cmake.install()

    def package_info(self):
        self.cpp_info.libdirs = ["lib64", "lib"]
