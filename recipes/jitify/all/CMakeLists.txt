cmake_minimum_required(VERSION 3.15)
project(jitify LANGUAGES CXX)

install (FILES "${JITIFY_SOURCE_DIR}/jitify/jitify.hpp" DESTINATION "include/jitify" RENAME jitify.hpp)
