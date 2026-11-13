#include <iostream>
#include "jitify/jitify.hpp"

int main(int argc, char ** argv)
{
    for (const auto& it : jitify::detail::get_jitsafe_headers_map())
	{
        std::cout << it.first << " " << it.second << "\n";
	}

    return 0;
}
