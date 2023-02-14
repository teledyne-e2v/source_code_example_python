#!/usr/bin/env python
from v4l2 import *
import fcntl
import mmap
import select
import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation 

vd = open('/dev/video0', 'rb+', buffering=0)

print(">> get device capabilities")
cp = v4l2_capability()
fcntl.ioctl(vd, VIDIOC_QUERYCAP, cp)

print(">> device setup")
fmt = v4l2_format()
fmt.type = V4L2_BUF_TYPE_VIDEO_CAPTURE

print(">> init mmap capture")
req = v4l2_requestbuffers()
req.type = V4L2_BUF_TYPE_VIDEO_CAPTURE
req.memory = V4L2_MEMORY_MMAP
req.count = 1  # nr of buffer frames
fcntl.ioctl(vd, VIDIOC_REQBUFS, req)  # tell the driver that we want some buffers 
print("req.count", req.count)
buffers = []
print(">>> VIDIOC_QUERYBUF, mmap, VIDIOC_QBUF")
for ind in range(req.count):
    # setup a buffer
    buf = v4l2_buffer()
    buf.type = V4L2_BUF_TYPE_VIDEO_CAPTURE
    buf.memory = V4L2_MEMORY_MMAP
    buf.index = ind
    fcntl.ioctl(vd, VIDIOC_QUERYBUF, buf)

    mm = mmap.mmap(vd.fileno(), buf.length, mmap.MAP_SHARED, mmap.PROT_READ | mmap.PROT_WRITE, offset=buf.m.offset)
    buffers.append(mm)

    # queue the buffer for capture
    fcntl.ioctl(vd, VIDIOC_QBUF, buf)

print(">> Start streaming")
buf_type = v4l2_buf_type(V4L2_BUF_TYPE_VIDEO_CAPTURE)
fcntl.ioctl(vd, VIDIOC_STREAMON, buf_type)

fig = plt.figure()

def f():
    buf = v4l2_buffer()
    buf.type = V4L2_BUF_TYPE_VIDEO_CAPTURE
    buf.memory = V4L2_MEMORY_MMAP
    fcntl.ioctl(vd, VIDIOC_DQBUF, buf)  # get image from the driver queue

    mm = buffers[buf.index]
    image=np.frombuffer(mm.read(len(mm)),dtype=np.ubyte)
    image=image.reshape(1080,1920)
    mm.seek(0)
    fcntl.ioctl(vd, VIDIOC_QBUF, buf)
    #image=np.delete(image, np.s_[::2], 1) compress image by 2
    #image=np.delete(image, np.s_[::2], 0) compress image by 2
    return image
im = plt.imshow(f(), animated=True,cmap='gray', vmin=0, vmax=255)


def updatefig(*args):
    im.set_array(f())
    return im,

ani = animation.FuncAnimation(fig, updatefig, blit=True,interval=1)
plt.show()
  
  
print(">> Stop streaming")
fcntl.ioctl(vd, VIDIOC_STREAMOFF, buf_type)
#vid.close()
vd.close()

  
     

