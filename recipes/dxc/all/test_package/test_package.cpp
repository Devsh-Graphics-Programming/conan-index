#include <iostream>
#include <string>
#include <vector>
#include <cassert>

#include <wrl.h>
#include <dxcapi.h>

int main() {
    Microsoft::WRL::ComPtr<IDxcUtils> m_dxcUtils;
    Microsoft::WRL::ComPtr<IDxcCompiler3> m_dxcCompiler;

    Microsoft::WRL::ComPtr<IDxcUtils> utils;
    auto res = DxcCreateInstance(CLSID_DxcUtils, IID_PPV_ARGS(utils.GetAddressOf()));
    assert(SUCCEEDED(res));

    Microsoft::WRL::ComPtr<IDxcCompiler3> compiler;
    res = DxcCreateInstance(CLSID_DxcCompiler, IID_PPV_ARGS(compiler.GetAddressOf()));
    assert(SUCCEEDED(res));

    return 0;
}
