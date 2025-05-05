#!/usr/bin/env python3
"""
Test script for verifying lightbulb control functionality
"""
import time
import lightbulb

print("Testing lightbulb functions...")

try:
    # Get current status
    print("Getting current status...")
    status = lightbulb.get_status()
    print(f"Status: {status}")

    # Turn on the light
    print("\nTurning on the light...")
    result = lightbulb.turn_on()
    print(f"Result: {result}")
    time.sleep(2)

    # Set to red
    print("\nSetting color to red...")
    result = lightbulb.set_color(255, 0, 0)
    print(f"Result: {result}")
    time.sleep(2)

    # Set to green
    print("\nSetting color to green...")
    result = lightbulb.set_color(0, 255, 0)
    print(f"Result: {result}")
    time.sleep(2)

    # Set to blue
    print("\nSetting color to blue...")
    result = lightbulb.set_color(0, 0, 255)
    print(f"Result: {result}")
    time.sleep(2)

    # Turn off the light
    print("\nTurning off the light...")
    result = lightbulb.turn_off()
    print(f"Result: {result}")

    print("\nAll tests completed successfully!")

except Exception as e:
    print(f"Error during testing: {e}") 