cmake_minimum_required(VERSION 3.15)
project(nabla_aesGladman LANGUAGES C CXX)

set(LZMA_ROOT "${LZMA_SOURCE_DIR}/lzma")

add_library(lzma STATIC
	"${LZMA_ROOT}/C/Alloc.c"
	"${LZMA_ROOT}/C/CpuArch.c"
	"${LZMA_ROOT}/C/LzFind.c"
	"${LZMA_ROOT}/C/LzmaDec.c"
	"${LZMA_ROOT}/C/LzmaEnc.c"
)
target_compile_definitions(lzma PRIVATE Z7_ST)

target_include_directories(lzma PUBLIC
    $<BUILD_INTERFACE:${AES_SOURCE_DIR}>
    $<INSTALL_INTERFACE:include>
)

install(TARGETS lzma ARCHIVE DESTINATION lib)
install(DIRECTORY "${LZMA_ROOT}/C"
	DESTINATION include/lzma
	FILES_MATCHING PATTERN "*.h"
)
