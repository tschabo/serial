#include "serial.h"
#include <vector>
#include <string>

int main()
{
    const auto devices_found = serial::list_ports();

    for(auto& device : serial::list_ports())
    {
        printf("(%s, %s, %s)\n", device.port.c_str(), device.description.c_str(),
               device.hardware_id.c_str());
    }

    return 0;
}
