#include <iostream>
#include <string>
#include <array>

extern int vulkaninfo(int, char**);

int main() {
  auto one = std::to_string(1u);
  std::string arg1 = "--json=" + one;
  std::string arg2 = "-o";
  std::string arg3 = "device_" + one + ".json";

  auto args = std::to_array<const char*>({ arg1.data(), arg2.data(), arg3.data()});
  int res = ::vulkaninfo(args.size(), const_cast<char**>(args.data()));

  std::cout << "vulkaninfo " << res << "\n";

  return 0;
}
