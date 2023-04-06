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
api.initialize(sensor_mode=1)
fd = api.get_device()
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
for ind in range(req.count):
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

print(">> Start streaming")
buf_type = v4l2.v4l2_buf_type(v4l2.V4L2_BUF_TYPE_VIDEO_CAPTURE)
fcntl.ioctl(fd, v4l2.VIDIOC_STREAMON, buf_type)

def take_image(image_name):
    # IMPORTANT : Just bellow you can uncomment to clean the insternal queue of the driver
#    for i in range(3):
#        buf = v4l2.v4l2_buffer()
#        buf.type = v4l2.V4L2_BUF_TYPE_VIDEO_CAPTURE
#        buf.memory = v4l2.V4L2_MEMORY_MMAP
#        fcntl.ioctl(fd, v4l2.VIDIOC_DQBUF, buf)  # get image from the driver queue
#        mm = buffers[buf.index]
#        mm.read(len(mm))
#        mm.seek(0)
#        fcntl.ioctl(fd, v4l2.VIDIOC_QBUF, buf)
    # Reactivate streaming
    with open(image_name, "wb") as binary_file:
        buf = v4l2.v4l2_buffer()
        buf.type = v4l2.V4L2_BUF_TYPE_VIDEO_CAPTURE
        buf.memory = v4l2.V4L2_MEMORY_MMAP
        fcntl.ioctl(fd, v4l2.VIDIOC_DQBUF, buf)  # get image from the driver queue
        mm = buffers[buf.index]
        binary_file.write(mm.read(len(mm)))
        mm.seek(0)
        fcntl.ioctl(fd, v4l2.VIDIOC_QBUF, buf)

api.set_control_value("test_pattern",1)
time.sleep(0.2)
for i in range(1,10):
    api.set_control_value("test_pattern",i%2+1)
    time.sleep(0.2)
    take_image("10bit_"+str(i)+".raw")
    

print(">> Stop streaming")
fcntl.ioctl(fd, v4l2.VIDIOC_STREAMOFF, buf_type)
for i in buffers:
    i.close()
api.close()

  
     