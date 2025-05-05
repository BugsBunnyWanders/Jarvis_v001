import tinytuya

# Lightbulb device configuration
DEVICE_ID = 'd7b096d501f14803e9k9xf (len:22)'
DEVICE_IP = '192.168.29.238'
LOCAL_KEY = '.U=`B3gl$Em6^A9='
VERSION = 3.5

def get_bulb():
    """Create and return a configured BulbDevice instance"""
    bulb = tinytuya.BulbDevice(DEVICE_ID, DEVICE_IP, LOCAL_KEY)
    bulb.set_version(VERSION)
    return bulb

def turn_on():
    """Turn the light bulb on"""
    bulb = get_bulb()
    result = bulb.turn_on()
    return result

def turn_off():
    """Turn the light bulb off"""
    bulb = get_bulb()
    result = bulb.turn_off()
    return result

def set_color(r, g, b):
    """Set the light bulb color using RGB values
    
    Args:
        r (int): Red component (0-255)
        g (int): Green component (0-255)
        b (int): Blue component (0-255)
    
    Returns:
        dict: Response from the device
    """
    bulb = get_bulb()
    result = bulb.set_colour(r, g, b)
    return result

def get_status():
    """Get the current status of the light bulb"""
    bulb = get_bulb()
    return bulb.status()

# Test code (uncomment to test)
# print(get_status())
# turn_on()
# set_color(255, 0, 0)  # Set to red
# turn_off()