
import tinytuya

# Connect to Device
d = tinytuya.OutletDevice(
    dev_id='d7b096d501f14803e9k9xf (len:22)',
    address='192.168.29.238',      # Or set to 'Auto' to auto-discover IP address
    local_key='.U=`B3gl$Em6^A9=', 
    version=3.5)

# Get Status
data = d.status() 
print('set_status() result %r' % data)

bulb = tinytuya.BulbDevice('d7b096d501f14803e9k9xf (len:22)', '192.168.29.238', '.U=`B3gl$Em6^A9=')
bulb.set_version(3.5)

bulb.set_colour(255, 0, 0, nowait=True)