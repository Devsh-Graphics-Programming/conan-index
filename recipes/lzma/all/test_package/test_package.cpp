#include <string>
#include <iostream>

#include <lzma/C/LzmaEnc.h>

int main(int argc, char ** argv)
{
    size_t propsSize = LZMA_PROPS_SIZE;
    CLzmaEncProps props;
    LzmaEncProps_Init(&props);
    props.dictSize = 1 << 16; // 64KB
    props.writeEndMark = 1;

    std::cout << "EncProps reduceSize " << props.reduceSize << "\n";
    return 0;
}
