#include <string>
#include <iostream>

#include <aesGladman/fileenc.h>

int main(int argc, char ** argv)
{
    std::string password = "deadbeef";
    uint8_t salt_val = 2;
    const uint8_t* salt = &salt_val;
    uint16_t pwVerificationFile;

    fcrypt_ctx zctx;
    int rc = fcrypt_init(
        1u, // random mode
        (const unsigned char*)password.c_str(),
        password.size(),
        salt,
        (unsigned char*)&pwVerificationFile,
        &zctx
    );

    std::cout << "Created file encryption context " << rc << "\n";
    return 0;
}
