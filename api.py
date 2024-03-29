#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 15 14:33:59 2023

@author: teledyne
"""
import v4l2
import fcntl
import os


ctrl_list=dict()

def initialize(fd,sensor_mode=2): # start the driver with a configurable sensor mode. (Initialization is necessary before using any other function)
    
    if(fd.closed): #check if it opened well
        print("error : can't open ",v4l2_flux)
        exit(0)
    
    os.system("v4l2-ctl -l > /tmp/ctrls_list.txt") # save the v4l2-ctrl in a tmp file 
    
    ctrls= open('/tmp/ctrls_list.txt', 'r') # open this file
    line=ctrls.readline()
    while(line): # Parse the file to get informations
        infos=dict()
        
        splited=line.split()
        if len(splited)>2 and len(splited[1])>2:
            if splited[1][0:2]=="0x":
                infos["id"]=splited[1]
                for i in splited:
                    if(len(i)>4 and i[0]=="(" and i[-1]==")"):
                        infos["type"]=i[1:-1]
                        if(infos["type"]=="bool"):
                            infos["minimum"]=0
                            infos["maximum"]=1
                            infos["step"]=1
                    elif(len(i)>8 and i[0:8]=="default="):
                        infos["default"]=int(i[8:])
                    elif(len(i)>4 and i[0:4]=="min="):
                        infos["minimum"]=int(i[4:])
                    elif(len(i)>4 and i[0:4]=="max="):
                        infos["maximum"]=int(i[4:])
                    elif(len(i)>5 and i[0:5]=="step="):
                        infos["step"]=int(i[5:])
                    
                ctrl_list[splited[0]]=infos.copy()
        line=ctrls.readline()
    
    fmt = v4l2.v4l2_format()
    fmt.type = v4l2.V4L2_BUF_TYPE_VIDEO_CAPTURE
    fmt.fmt.pix.field = v4l2.V4L2_FIELD_NONE
    if(sensor_mode==2):
        fmt.fmt.pix.width = 1920
        fmt.fmt.pix.height = 1080
        fmt.fmt.pix.pixelformat = v4l2.V4L2_PIX_FMT_GREY
        set_control_value(fd,"sensor_mode",2)
    elif(sensor_mode==0):
        fmt.fmt.pix.width = 1920
        fmt.fmt.pix.height = 1080
        fmt.fmt.pix.pixelformat = v4l2.V4L2_PIX_FMT_Y10
        set_control_value(fd,"sensor_mode",0)
    elif(sensor_mode==1):
        fmt.fmt.pix.width = 1920
        fmt.fmt.pix.height = 800
        fmt.fmt.pix.pixelformat = v4l2.V4L2_PIX_FMT_Y10
        set_control_value(fd,"sensor_mode",1)
    elif(sensor_mode==3):
        fmt.fmt.pix.width = 1920
        fmt.fmt.pix.height = 80
        fmt.fmt.pix.pixelformat = v4l2.V4L2_PIX_FMT_GREY
        set_control_value(fd,"sensor_mode",3)
    fcntl.ioctl(fd, v4l2.VIDIOC_S_FMT, fmt)

def close(fd): # closes the access to the driver, must be used last, no other function must be called after this one (except if you want to do an initialization again)
    if(fd == None):
        print("error : flux closed")
        exit(0)
    fd.close()


def get_device_controls(fd): # return all names of controls in an array
    return ctrl_list.keys()

def get_control_info(fd,control_name): # return all information about control example (min, max, default value ...) in a dict.
    return ctrl_list[control_name]


def set_controls(fd,controls_dict): # use a dictionary to set controls to value
    
    if(fd ==None or fd.closed): #check if file opened
        print("error : initialize the connection with the function initialize()")
        exit(0)
    ecs = v4l2.v4l2_ext_controls(v4l2.V4L2_CTRL_CLASS_CAMERA, 1) #create the structure used by v4l2
    ecs.count = len(controls_dict.keys()) #set the number of controls 
    ecs.ctrl_class = v4l2.V4L2_CTRL_CLASS_CAMERA # set the class containing the controls
    ec = (v4l2.v4l2_ext_control * len(controls_dict.keys()))() #list of controls 
    i=0
    for ctrl in controls_dict.keys():
        controls_dict[ctrl]
        if(controls_dict[ctrl]>ctrl_list[ctrl]["maximum"]): #check maximum
            print("value is above maxium, take a look at control informations with the function get_control_info(control_name), value set to maximum")
            controls_dict[ctrl]=ctrl_list[ctrl]["maximum"]
        elif(controls_dict[ctrl]<ctrl_list[ctrl]["minimum"]): #check minimum
            print("value is under minimum, take a look at control informations with the function get_control_info(control_name), value set to minimum")
            controls_dict[ctrl]=ctrl_list[ctrl]["minimum"]
        if (ctrl_list[ctrl]["maximum"] - controls_dict[ctrl]) % ctrl_list[ctrl]["step"]!=0: #check step
            print("value isn't in the steps, take a look at control informations with the function get_control_info(control_name), value decreased to match step")
            controls_dict[ctrl]-=(ctrl_list[ctrl]["maximum"] - controls_dict[ctrl]) % ctrl_list[ctrl]["step"]        
        
        ec[i].id = int(ctrl_list[ctrl]["id"][2:],16)#set the id of the control
        ec[i].value = controls_dict[ctrl]
        ec[i].value64 = controls_dict[ctrl]
        ec[i].size = 0 # initialisation (not important)
        i+=1
    ecs.controls = ec # set control list into the structure 
    fcntl.ioctl(fd, v4l2.VIDIOC_S_EXT_CTRLS, ecs) #set the control using v4l2 drivers
        
    

def get_controls_info(fd): # return the dictionary with all controls informations 
    return ctrl_list

def set_control_value(fd,control_name,value): # Allows to retrieve the whole value of a control from its name.
    if(fd ==None or fd.closed): #check if file opened
        print("error : initialize the connection with the function initialize()")
        exit(0)
    if(value>ctrl_list[control_name]["maximum"]): #check maximum
        print("value is above maxium, take a look at control informations with the function get_control_info(control_name), value set to maximum")
        value=ctrl_list[control_name]["maximum"]
    elif(value<ctrl_list[control_name]["minimum"]): #check minimum
        print("value is under minimum, take a look at control informations with the function get_control_info(control_name), value set to minimum")
        value=ctrl_list[control_name]["minimum"]
    
    if (ctrl_list[control_name]["maximum"] - value) % ctrl_list[control_name]["step"]!=0: #check step
        print("value isn't in the steps, take a look at control informations with the function get_control_info(control_name), value decreased to match step")

        value-=(ctrl_list[control_name]["maximum"] - value) % ctrl_list[control_name]["step"]
    
    ecs = v4l2.v4l2_ext_controls(v4l2.V4L2_CTRL_CLASS_CAMERA, 1) #create the structure used by v4l2
    ec = (v4l2.v4l2_ext_control * 1)() #list of controls 
    ec[0].id = int(ctrl_list[control_name]["id"][2:],16)#set the id of the control
    ecs.count = 1 #set the number of controls 
    ecs.ctrl_class = v4l2.V4L2_CTRL_CLASS_CAMERA # set the class containing the controls
    ec[0].value = value
    ec[0].value64 = value
    ec[0].size = 0 # initialisation (not important)
    ecs.controls = ec # set control list into the structure
    fcntl.ioctl(fd, v4l2.VIDIOC_S_EXT_CTRLS, ecs) #set the control using v4l2 drivers
    
def get_control_value(fd,control_name): # Allows to assign a value to a control from its name.
    if(fd == None or fd.closed):
        print("error : initialize the connection with the function initialize()")
        exit(0)
    
    ecs = v4l2.v4l2_ext_controls(v4l2.V4L2_CTRL_CLASS_CAMERA, 1)#create the structure used by v4l2
    ec = (v4l2.v4l2_ext_control * 1)()#list of controls 
    ec[0].id = int(ctrl_list[control_name]["id"][2:],16)#set the id of the control
    ecs.count = 1 #set the number of controls 
    ecs.ctrl_class = v4l2.V4L2_CTRL_CLASS_CAMERA# set the class containing the controls
    ec[0].size = 0 # initialisation (not important)
    ecs.controls = ec# set control list into the structure
    fcntl.ioctl(fd, v4l2.VIDIOC_G_EXT_CTRLS, ecs) #set the control using v4l2 drivers
    return ecs.controls[0].value64
    
