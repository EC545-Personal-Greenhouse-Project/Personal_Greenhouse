import threading
from tplinkcloud import TPLinkDeviceManager

def toggle_plug(on, name):
  '''turn smart plugs on and off'''
    username=''
    password=''

    device_manager = TPLinkDeviceManager(username, password)
    device = device_manager.find_device(name)
    if device:
      #print(f'Found {device.model_type.name} device: {device.get_alias()}')
      if on: device.power_on()
      else: device.power_off()
    else:  
      print(f'Could not find {name}')
