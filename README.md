#### The purpose of this code is to provide a simple example of using the V4L2 driver of the Topaz module in python.
#### These codes are only examples, a better implementation is probably possible.

# API

api.py provide an example of driver control by automatically retrieving the driver controls produced by the v4l2-ctl -l command. 
It can be used as an api to simplify your acces to the sensor controls in C.



This api provides several functions: 

- initialize(v4l2_device, sensor_mode) start the driver with a configurable sensor mode. (Initialization is necessary before using any other function)

- close() closes the access to the driver, must be used last, no other function must be called after this one (except if you want to do an initialization again)

- get_device() return the device 

- get_device_controls() return all names of controls in an array

- get_control_info() return all information about control example (min, max, default value ...) in a dict.

- set_controls() use a dictionary to set list of controls to values

- get_controls_info() return the dictionary with all controls informations 

- get_control_value(control_name): Allows to retrieve the whole value of a control from its name.

- set_control_value(control_name,value) : Allows to assign a value to a control from its name.

# GPIO

GPIO_example.py brings an example of control of the pins of the nano jetson allowing with an adjustment of the frequency. This is using RPi to control GPIO. See the code for more information.


# Image Capture

image_capture_example.py provides an example of taking a sequence of images by changing some sensor parameters between each image. In this file you can also find functions to drive the sensor which are different from the api (less complex, address of the controls defined in static).
The program will take a sequence of RAW images and customize the controls applied to each image as you wish.
It is also possible to change the format to take picture in Y10 or GRAY8. Y10 images will be saved in 16bit GRAY raw image.

# Video display with matplolib

video_flux_and_capture_numpy_matplotlib.py provides an example of streaming the video flux using matplotlib, you can also see in the code how to put the images in a numpy array. This codes provides really bad streaming performances with a maxmum of 5/10 fps this is due to the usage of matplotlib, it hasn't been develop for video streaming, we are using it only to show how to use the driver with numpy.