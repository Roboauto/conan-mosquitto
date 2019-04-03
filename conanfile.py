#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
import os


class MosquittoConan(ConanFile):
    name = "mosquitto"
    version = "1.4.15"
    description = "Open source message broker that implements the MQTT protocol"
    url = "https://github.com/bincrafters/conan-mosquitto"
    homepage = "https://mosquitto.org/"
    author = "Bincrafters <bincrafters@gmail.com>"
    license = "EPL", "EDL"
    exports = ["LICENSE.md"]
    exports_sources = ["CMakeLists.txt", "mosquitto.patch"]
    generators = "cmake"
    settings = "os", "arch", "compiler", "build_type"
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
        "with_tls": [True, False],
        "with_mosquittopp": [True, False],
        "with_srv": [True, False],
        "with_binaries": [True, False]
    }
    default_options = ("shared=False", "fPIC=True", "with_tls=True",
                       "with_mosquittopp=True", "with_srv=True",
                       "with_binaries=True")
    source_subfolder = "source_subfolder"
    build_subfolder = "build_subfolder"

    def config_options(self):
        if self.settings.os == 'Windows':
            del self.options.fPIC
        if self.settings.os == "Macos":
            del self.options.with_uuid

    def configure(self):
        if not self.options.with_mosquittopp:
            del self.settings.compiler.libcxx

    def requirements(self):
        if self.options.with_tls:
            self.requires.add("OpenSSL/1.1.0g@conan/stable")
        if self.options.with_srv:
            self.requires.add("c-ares/1.14.0@conan/stable")

    def source(self):
        source_url = "https://github.com/eclipse/mosquitto"
        tools.get("{0}/archive/v{1}.tar.gz".format(source_url, self.version))
        extracted_dir = self.name + "-" + self.version
        os.rename(extracted_dir, self.source_subfolder)
        tools.patch(
            patch_file="mosquitto.patch", base_path=self.source_subfolder)

    def configure_cmake(self):
        cmake = CMake(self)
        cmake.definitions["WITH_SRV"] = self.options.with_srv
        cmake.definitions["WITH_BINARIES"] = self.options.with_binaries
        cmake.definitions["WITH_MOSQUITTOPP"] = self.options.with_mosquittopp
        if self.settings.os == "Windows":
            cmake.definitions["CMAKE_WINDOWS_EXPORT_ALL_SYMBOLS"] = self.options.shared
            cmake.definitions["WITH_THREADING"] = False
        cmake.configure(build_folder=self.build_subfolder)
        return cmake

    def build(self):
        cmake = self.configure_cmake()
        cmake.build()

    def package(self):
        self.copy(pattern="LICENSE.txt", dst="licenses", src=self.source_subfolder)
        self.copy(pattern="edl-v10", dst="licenses", src=self.source_subfolder)
        self.copy(pattern="epl-v10", dst="licenses", src=self.source_subfolder)
        cmake = self.configure_cmake()
        cmake.install()

    def deploy(self):
        self.copy("*", src="bin", dst="bin")
        self.copy("*.dll", src="lib", dst="bin")
        self.copy("*.dylib*", src="lib", dst="bin")
        self.copy_deps("*.dylib*", src="lib", dst="bin")
        self.copy_deps("*.dll", src="lib", dst="bin")
        self.copy("*.so*", src="lib", dst="bin")
        self.copy_deps("*.so*", src="lib", dst="bin")
        self.copy("mosquitto.conf", src="etc/mosquitto/", dst="bin")

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
        if self.settings.os == "Windows":
            self.cpp_info.libs.append("ws2_32")
        elif self.settings.os == "Linux":
            self.cpp_info.libs.extend(["rt", "pthread", "dl"])
