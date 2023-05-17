#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 14 14:30:38 2023

@author: teledyne
"""
import v4l2
import fcntl
import mmap
import time
import api


def take_image(fd,buffers,image_name): # FUNCTION TO TAKE AN IMAGE 
    
    # This clear the buffer of the driver carefull with this code you will use only 1/4 of the images. 
    # Cleaning the buffer is only usefull for taking image not for  video streaming ...
    # If you want to do a more video streaming applicaton just remove the for (the next 10 lines)
    for i in range(3): 
        buf = v4l2.v4l2_buffer()
        buf.type = v4l2.V4L2_BUF_TYPE_VIDEO_CAPTURE
        buf.memory = v4l2.V4L2_MEMORY_MMAP
        fcntl.ioctl(fd, v4l2.VIDIOC_DQBUF, buf)  # get image from the driver queue
        mm = buffers[buf.index]
        mm.read(len(mm))
        mm.seek(0)
        fcntl.ioctl(fd, v4l2.VIDIOC_QBUF, buf)



    with open(image_name, "wb") as binary_file: # Save the new image
        buf = v4l2.v4l2_buffer()
        buf.type = v4l2.V4L2_BUF_TYPE_VIDEO_CAPTURE
        buf.memory = v4l2.V4L2_MEMORY_MMAP
        fcntl.ioctl(fd, v4l2.VIDIOC_DQBUF, buf)  # get image from the driver queue
        mm = buffers[buf.index]

        image = mm.read(len(mm)) 

        # Here you can add process to the image if you want 

        binary_file.write(image) #This is writting your image in the file
        mm.seek(0)
        fcntl.ioctl(fd, v4l2.VIDIOC_QBUF, buf)




def main():


    fd = open("/dev/video0", 'rb+', buffering=0) #open the device


    # sensor mode = 0 => height=1080 width=1920 format=Y10
    # sensor mode = 1 => height=800 width=1920 format=Y10
    # sensor mode = 2 => height=1080 width=1920 format=GRAY8
    # sensor mode = 3 => height=800 width=1920 format=GRAY8

    api.initialize(fd,sensor_mode=0) 




    print(">> get device capabilities")
    cp = v4l2.v4l2_capability()
    fcntl.ioctl(fd, v4l2.VIDIOC_QUERYCAP, cp)


    print(">> device setup")

    print(">> init mmap capture")
    req = v4l2.v4l2_requestbuffers()
    req.type = v4l2.V4L2_BUF_TYPE_VIDEO_CAPTURE
    req.memory = v4l2.V4L2_MEMORY_MMAP
    req.count = 1  # nr of buffer frames
    fcntl.ioctl(fd, v4l2.VIDIOC_REQBUFS, req)  # tell the driver that we want some buffers 
    print("req.count", req.count)
    buffers = []


    print(">>> VIDIOC_QUERYBUF, mmap, VIDIOC_QBUF")
    for ind in range(req.count): #create the buffers storage
        # setup a buffer
        buf = v4l2.v4l2_buffer()
        buf.type = v4l2.V4L2_BUF_TYPE_VIDEO_CAPTURE
        buf.memory = v4l2.V4L2_MEMORY_MMAP
        buf.index = ind
        fcntl.ioctl(fd, v4l2.VIDIOC_QUERYBUF, buf)
        mm = mmap.mmap(fd.fileno(), buf.length, mmap.MAP_SHARED, mmap.PROT_READ | mmap.PROT_WRITE, offset=buf.m.offset)
        buffers.append(mm)
        # queue the buffer for capture
        fcntl.ioctl(fd, v4l2.VIDIOC_QBUF, buf)


    #start video streaming
    print(">> Start streaming")
    buf_type = v4l2.v4l2_buf_type(v4l2.V4L2_BUF_TYPE_VIDEO_CAPTURE)
    fcntl.ioctl(fd, v4l2.VIDIOC_STREAMON, buf_type)


    #all controls initialization
    api.set_control_value(fd,"exposure",20000)
    time.sleep(0.2)


    # the loop taking images

    for i in range(0,10): #this will take 10 images



        # You can add here any changes of the controls for the next image
        # example  : 
        #
        # api.set_control_value(fd,"test_pattern",i%2+1)
        #
        # this example will do an image with the first test pattern, the second image will be with 
        # the second test pattern, the third will be with the first test pattern again ...

        time.sleep(0.2)

        take_image(fd,buffers,"10bit_"+str(i)+".raw") # take image changing the name to save them properly
        

    print(">> Stop streaming")
    fcntl.ioctl(fd, v4l2.VIDIOC_STREAMOFF, buf_type)
    for i in buffers:
        i.close()
    api.close(fd)

if __name__=="__main__":
    main()
        