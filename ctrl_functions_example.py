import v4l2
from fcntl import ioctl 
#fd = open('/dev/video0', 'rw')
#cp = v4l2.v4l2_capability()
#ioctl(fd, v4l2.VIDIOC_QUERYCAP, cp)
#print(cp.driver)
#print(cp.card)

def control_set(device,code,value):
    ecs = v4l2.v4l2_ext_controls(v4l2.V4L2_CTRL_CLASS_CAMERA, 1)
    ec = (v4l2.v4l2_ext_control * 1)()
    ec[0].id = code
    ecs.count = 1
    ecs.ctrl_class = v4l2.V4L2_CTRL_CLASS_CAMERA
    ec[0].value = value
    ec[0].value64 = value
    ec[0].size = 0
    ecs.controls = ec
    ioctl(device, v4l2.VIDIOC_S_EXT_CTRLS, ecs) #set the control using v4l2 drivers

def control_get(device,code):
    ecs = v4l2.v4l2_ext_controls(v4l2.V4L2_CTRL_CLASS_CAMERA, 1)
    ec = (v4l2.v4l2_ext_control * 1)()
    ec[0].id = code
    ecs.count = 1
    ecs.ctrl_class = v4l2.V4L2_CTRL_CLASS_CAMERA
    ec[0].size = 0
    ecs.controls = ec
    ioctl(device, v4l2.VIDIOC_G_EXT_CTRLS, ecs) #set the control using v4l2 drivers
    return ecs.controls[0].value64

# control the analog gain
def set_analog_gain(device,value):
    control_set(device,0x009a206f,value)

# control the exposure
def set_exposure(device,value):
    control_set(device,0x009a200a,value)

# control the framerate
def set_frame_rate(device,value):
    control_set(device,0x009a200b,value)

# control the digital gain
def set_digital_gain(device,value):
    control_set(device, 0x009a2070, value)

# control the sensor mode
def set_sensor_mode(device,value):
    control_set(device, 0x009a2008, value)

# control the gain
def set_gain(device,value):
    control_set(device, 0x009a2009, value)

# control the gain
def set_test_pattern(device,value):
    control_set(device, 0x009a2071, value)

# control the gain
def set_flip(device,value):
    control_set(device, 0x009a2072, value)
    
# control the gain
def set_height_align(device,value):
    control_set(device, 0x009a2066, value)

# control the gain
def set_preferred_stride(device,value):
    control_set(device, 0x009a206e, value)

# control the gain
def set_sensor_modes(device,value):
    control_set(device, 0x009a2082, value)
    
# get the analog gain
def get_analog_gain(device,value):
    control_get(device,0x009a206f)

# get the exposure
def get_exposure(device,value):
    control_get(device,0x009a200a)

# get the framerate
def get_frame_rate(device,value):
    control_get(device,0x009a200b)

# get the digital gain
def get_digital_gain(device,value):
    control_get(device, 0x009a2070)

# get the sensor mode
def get_sensor_mode(device,value):
    control_get(device, 0x009a2008)

# get the gain
def get_gain(device,value):
    control_get(device, 0x009a2009)

# get the test pattern
def get_test_pattern(device,value):
    control_get(device, 0x009a2071)
    
# get the test pattern
def get_flip(device,value):
    control_get(device, 0x009a2072)

# get the test pattern
def get_height_align(device,value):
    control_get(device, 0x009a2066)

# get the test pattern
def get_preferred_stride(device,value):
    control_get(device, 0x009a206e)

# get the test pattern
def get_sensor_modes(device,value):
    control_get(device, 0x009a2082)
    
