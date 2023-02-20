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

fd = open('/dev/video0', 'rb+', buffering=0)
print(">> get device capabilities")
cp = v4l2.v4l2_capability()
fcntl.ioctl(fd, v4l2.VIDIOC_QUERYCAP, cp)



print(">> device setup")
api.initialize(sensor_mode=1)

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
    with open(image_name, "wb") as binary_file:
        buf = v4l2.v4l2_buffer()
        buf.type = v4l2.V4L2_BUF_TYPE_VIDEO_CAPTURE
        buf.memory = v4l2.V4L2_MEMORY_MMAP
        fcntl.ioctl(fd, v4l2.VIDIOC_DQBUF, buf)  # get image from the driver queue
        mm = buffers[buf.index]
        binary_file.write(mm.read(len(mm)))
        mm.seek(0)
        fcntl.ioctl(fd, v4l2.VIDIOC_QBUF, buf)
    
    
for i in range(5):
    api.set_control_value("digital_gain",i*500)
    time.sleep(1)
    take_image("test"+str(i)+".raw")
    
  
print(">> Stop streaming")
fcntl.ioctl(fd, v4l2.VIDIOC_STREAMOFF, buf_type)
for i in buffers:
    i.close()
fd.close()

  
     