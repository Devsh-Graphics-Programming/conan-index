cmake_minimum_required(VERSION 3.15)
project(renderdoc LANGUAGES CXX)

install (FILES "${RDOC_SOURCE_DIR}/rdoc/renderdoc/api/app/renderdoc_app.h" DESTINATION "include/renderdoc" RENAME renderdoc_app.h)
