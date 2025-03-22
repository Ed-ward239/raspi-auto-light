#include <iostream>
#include <libusb-1.0/libusb.h>
#include <chrono>
#include <thread>
#include <iomanip>

// Function to get current time as a formatted string
std::string getCurrentTime()
{
    auto now = std::chrono::system_clock::now();
    auto time = std::chrono::system_clock::to_time_t(now);
    struct tm *localTime = localtime(&time);

    std::ostringstream timeStream;
    timeStream << std::put_time(localTime, "%Y-%m-%d %H:%M:%S"); // Format: YYYY-MM-DD HH:MM:SS
    return timeStream.str();
}

// Init USB Communication
void controlLed(bool turnOn)
{
    libusb_context *ctx = nullptr;
    libusb_device_handle *dev_handle = nullptr;

    libusb_init(&ctx);
    dev_handle = libusb_open_device_with_vid_pid(ctx, 0x1234, 0x5678);

    if (dev_handle == nullptr)
    {
        std::cerr << "Device not found" << std::endl;
        libusb_exit(ctx);
        return;
    }

    unsigned char data[] = {turnOn ? 0x01 : 0x00};
    int actualLength = 0;

    libusb_claim_interface(dev_handle, 0);
    libusb_bulk_transfer(dev_handle, 0x01, data, sizeof(data), &actualLength, 1000);
    libusb_release_interface(dev_handle, 0);

    libusb_close(dev_handle);
    libusb_exit(ctx);
}

// Check Time & Control Lights
bool isDaytime(int hour)
{
    return ((hour >= 6 && hour < 10) || (hour >= 18 && hour < 22));
}

int main()
{
    while (true)
    {
        auto now = std::chrono::system_clock::now();
        auto time = std::chrono::system_clock::to_time_t(now);
        struct tm *localTime = localtime(&time);

        int hour = localTime->tm_hour;
        std::string currentTime = getCurrentTime();

        if (isDaytime(hour))
        {
            std::cout << "Turning lights ON: " << currentTime << std::endl;
            controlLed(true);
        }
        else
        {
            std::cout << "Turning lights OFF: " << currentTime << std::endl;
            controlLed(false);
        }

        std::this_thread::sleep_for(std::chrono::minutes(1));
    }
    return 0;
}