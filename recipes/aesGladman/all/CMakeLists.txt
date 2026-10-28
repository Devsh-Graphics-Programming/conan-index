cmake_minimum_required(VERSION 3.15)
project(nabla_aesGladman LANGUAGES C CXX)

set(AES_ROOT "${AES_SOURCE_DIR}/aesGladman")

add_library(aesGladman STATIC
	"${AES_ROOT}/aes_ni.c"
	"${AES_ROOT}/aescrypt.c"
	"${AES_ROOT}/aeskey.c"
	"${AES_ROOT}/aestab.c"
	"${AES_ROOT}/fileenc.c"
	"${AES_ROOT}/hmac.c"
	"${AES_ROOT}/prng.c"
	"${AES_ROOT}/pwd2key.c"
	"${AES_ROOT}/sha1.c"
)
target_include_directories(aesGladman PUBLIC
    $<BUILD_INTERFACE:${AES_SOURCE_DIR}>
    $<INSTALL_INTERFACE:include>
)

install(TARGETS aesGladman ARCHIVE DESTINATION lib)
install(DIRECTORY "${AES_ROOT}/"
	DESTINATION include/aesGladman
	FILES_MATCHING PATTERN "*.h"
)
