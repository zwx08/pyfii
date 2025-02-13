import cmath
import os
import time
import uuid
import warnings
import shutil

import pyautogui
import cv2
import tqdm
import numpy as np
import pygame
from ffmpy import FFmpeg

from .cv3d import IIID, IIID2


# 视频添加音频
def video_add_audio(video_path: str, audio_path: str,output_path:str):
    _ext_video = os.path.basename(video_path).strip().split('.')[-1]
    _ext_audio = os.path.basename(audio_path).strip().split('.')[-1]
    if _ext_audio not in ['mp3', 'wav']:
        print('No music!')
        shutil.copy(video_path,video_path[0:-12]+'.mp4')
    else:
        _codec = 'copy'
        if _ext_audio == 'wav':
            _codec = 'aac'
        result =output_path.format(uuid.uuid4(), _ext_video)
        ff = FFmpeg(
            inputs={video_path: None, audio_path: None},
            outputs={result: '-map 0:v -map 1:a -c:v copy -c:a {} -shortest'.format(_codec)})
        print(ff.cmd)
        ff.run()
        return result

'''def nothing(x):
    pass'''

def color(n,m=0):
    n=180-n*180/7
    if m>0:
        n=(-abs(n))%180
        h,s,v=int(n),int(255-m),255
    else:
        n=(-abs(n))%180
        h,s,v=int(n),255,int(255+m)
    img=np.zeros((1,1,3),np.uint8)
    img[0][0]=(h,s,v)
    img=cv2.cvtColor(img,cv2.COLOR_HSV2BGR)
    return(int(img[0][0][0]),int(img[0][0][1]),int(img[0][0][2]))

def iiid_rotate(a,g=np.array([0,0,-980])):# 无人机旋转
    wing_force=a-g
    unit_wing_force=wing_force/np.sqrt(wing_force[0]**2+wing_force[1]**2+wing_force[2]**2)
    
    x,y,z=unit_wing_force[0],unit_wing_force[1],unit_wing_force[2]
    if x==0 and y==0:
        rotate_matrix=np.mat([
        [1,0,0],
        [0,1,0],
        [0,0,1]
    ])
    else:
        rotate_matrix=np.mat([
            [(x**2*z+y**2)/(x**2+y**2),-x*y/(z+1),x],
            [-x*y/(z+1),(x**2+y**2*z)/(x**2+y**2),y],
            [-x,-y,z]
        ])

    return rotate_matrix

def draw_drone(img,x,y,color,a=0,led=(-1,-1,-1),up=False,skin=1,device="F400",size=1):
    if device=="F400":
        if skin==0:
            if up:
                cv2.circle(img,(int(x*size),int(y*size)),15*size,color,-1)
            else:
                cv2.rectangle(img,(int((x-15)*size),int((y+5)*size)),(int((x+15)*size),int((y-5)*size)),color,-1)
        elif skin==1:
            if up:
                cv2.circle(img,(int((x-21/2*np.cos(np.pi/4+a))*size),int((y+21/2*np.sin(np.pi/4+a))*size)),8*size,color,size)
                cv2.circle(img,(int((x-21/2*np.cos(3*np.pi/4+a))*size),int((y+21/2*np.sin(3*np.pi/4+a))*size)),8*size,color,size)
                cv2.circle(img,(int((x-21/2*np.cos(-3*np.pi/4+a))*size),int((y+21/2*np.sin(-3*np.pi/4+a))*size)),8*size,color,size)
                cv2.circle(img,(int((x-21/2*np.cos(-np.pi/4+a))*size),int((y+21/2*np.sin(-np.pi/4+a))*size)),8*size,color,size)
                cv2.line(img,(int((x-21/2*np.cos(np.pi/4+a))*size),int((y+21/2*np.sin(np.pi/4+a))*size)),(int((x-21/2*np.cos(-3*np.pi/4+a))*size),int((y+21/2*np.sin(-3*np.pi/4+a))*size)),color,size)
                cv2.line(img,(int((x-21/2*np.cos(-np.pi/4+a))*size),int((y+21/2*np.sin(-np.pi/4+a))*size)),(int((x-21/2*np.cos(3*np.pi/4+a))*size),int((y+21/2*np.sin(3*np.pi/4+a))*size)),color,size)
                if led[0]>-1:
                    cv2.circle(img,(int(x*size),int(y*size)),5*size,led,-1)
            else:
                cv2.ellipse(img,(int((x+21/(2**0.5)/2)*size),int((y-1/4*7.6)*size)),(8*size,2*size),0,0,360,color,size)
                cv2.ellipse(img,(int((x-21/(2**0.5)/2)*size),int((y-1/4*7.6)*size)),(8*size,2*size),0,0,360,color,size)
                cv2.ellipse(img,(int((x-21/(2**0.5)/2)*size),int((y-3/4*7.6)*size)),(8*size,2*size),0,0,360,color,size)
                cv2.ellipse(img,(int((x+21/(2**0.5)/2)*size),int((y-3/4*7.6)*size)),(8*size,2*size),0,0,360,color,size)
                cv2.line(img,(int((x+21/(2**0.5)/2)*size),int((y-1/4*7.6)*size)),(int((x-21/(2**0.5)/2)*size),int((y-3/4*7.6)*size)),color,size)
                cv2.line(img,(int((x-21/(2**0.5)/2)*size),int((y-1/4*7.6)*size)),(int((x+21/(2**0.5)/2)*size),int((y-3/4*7.6)*size)),color,size)
                if led[0]>-1:
                    cv2.circle(img,(int(x*size),int((y-1/2*7.6)*size)),5*size,led,-1)
        elif skin==2:
            if up:
                red_square=np.array([[x+16*np.cos(a),y+16*np.sin(a)],[x+16*np.cos(a+np.pi/2),y+16*np.sin(a+np.pi/2)],[x+16*np.cos(a+np.pi),y+16*np.sin(a+np.pi)],[x+16*np.cos(a-np.pi/2),y+16*np.sin(a-np.pi/2)]],np.int32)
                fu=[np.array([[x+((-7-6j)*cmath.e**(a*1j)).real,y+((-7-6j)*cmath.e**(a*1j)).imag],[x+((-6-5j)*cmath.e**(a*1j)).real,y+((-6-5j)*cmath.e**(a*1j)).imag]],np.int32),
                np.array([[x+((-8-2j)*cmath.e**(a*1j)).real,y+((-8-2j)*cmath.e**(a*1j)).imag],[x+((-5-3j)*cmath.e**(a*1j)).real,y+((-5-3j)*cmath.e**(a*1j)).imag]],np.int32),
                np.array([[x+((-5-3j)*cmath.e**(a*1j)).real,y+((-5-3j)*cmath.e**(a*1j)).imag],[x+((-8+3j)*cmath.e**(a*1j)).real,y+((-8+3j)*cmath.e**(a*1j)).imag]],np.int32),
                np.array([[x+((-6-0j)*cmath.e**(a*1j)).real,y+((-6-0j)*cmath.e**(a*1j)).imag],[x+((-6+6j)*cmath.e**(a*1j)).real,y+((-6+6j)*cmath.e**(a*1j)).imag]],np.int32),
                np.array([[x+((-6+1j)*cmath.e**(a*1j)).real,y+((-6+1j)*cmath.e**(a*1j)).imag],[x+((-5+2j)*cmath.e**(a*1j)).real,y+((-5+2j)*cmath.e**(a*1j)).imag]],np.int32),
                np.array([[x+((-3-5j)*cmath.e**(a*1j)).real,y+((-3-5j)*cmath.e**(a*1j)).imag],[x+((5-5j)*cmath.e**(a*1j)).real,y+((5-5j)*cmath.e**(a*1j)).imag]],np.int32),
                np.array([[x+((-2-3j)*cmath.e**(a*1j)).real,y+((-2-3j)*cmath.e**(a*1j)).imag],[x+((4-3j)*cmath.e**(a*1j)).real,y+((4-3j)*cmath.e**(a*1j)).imag],
                [x+((4-1j)*cmath.e**(a*1j)).real,y+((4-1j)*cmath.e**(a*1j)).imag],[x+((-2-1j)*cmath.e**(a*1j)).real,y+((-2-1j)*cmath.e**(a*1j)).imag]],np.int32),
                np.array([[x+((-3+1j)*cmath.e**(a*1j)).real,y+((-3+1j)*cmath.e**(a*1j)).imag],[x+((5+1j)*cmath.e**(a*1j)).real,y+((5+1j)*cmath.e**(a*1j)).imag],
                [x+((5+5j)*cmath.e**(a*1j)).real,y+((5+5j)*cmath.e**(a*1j)).imag],[x+((-3+5j)*cmath.e**(a*1j)).real,y+((-3+5j)*cmath.e**(a*1j)).imag]],np.int32),
                np.array([[x+((-3+3j)*cmath.e**(a*1j)).real,y+((-3+3j)*cmath.e**(a*1j)).imag],[x+((5+3j)*cmath.e**(a*1j)).real,y+((5+3j)*cmath.e**(a*1j)).imag]],np.int32),
                np.array([[x+((1+1j)*cmath.e**(a*1j)).real,y+((1+1j)*cmath.e**(a*1j)).imag],[(x+(1+5j)*cmath.e**(a*1j)).real,y+((1+5j)*cmath.e**(a*1j)).imag]],np.int32)]
                img=cv2.fillPoly(img,[red_square],color=[0,0,255])
                img=cv2.polylines(img,fu,isClosed=True,color=[0,0,0],thickness=1)
            else:
                cv2.ellipse(img,(int(x+21/(2**0.5)/2),int(y-1/4*7.6)),(8,2),0,0,360,color,1)
                cv2.ellipse(img,(int(x-21/(2**0.5)/2),int(y-1/4*7.6)),(8,2),0,0,360,color,1)
                cv2.ellipse(img,(int(x-21/(2**0.5)/2),int(y-3/4*7.6)),(8,2),0,0,360,color,1)
                cv2.ellipse(img,(int(x+21/(2**0.5)/2),int(y-3/4*7.6)),(8,2),0,0,360,color,1)
                cv2.line(img,(int(x+21/(2**0.5)/2),int(y-1/4*7.6)),(int(x-21/(2**0.5)/2),int(y-3/4*7.6)),color,1)
                cv2.line(img,(int(x-21/(2**0.5)/2),int(y-1/4*7.6)),(int(x+21/(2**0.5)/2),int(y-3/4*7.6)),color,1)
                if led[0]>-1:
                    cv2.circle(img,(int(x),int(y-1/2*7.6)),5,led,-1)
    elif device=="F600":
        if up:
            cv2.circle(img,(int((x-12.6/2*np.cos(np.pi/4+a))*size),int((y+12.6/2*np.sin(np.pi/4+a))*size)),5*size,color,size)
            cv2.circle(img,(int((x-12.6/2*np.cos(3*np.pi/4+a))*size),int((y+12.6/2*np.sin(3*np.pi/4+a))*size)),5*size,color,size)
            cv2.circle(img,(int((x-12.6/2*np.cos(-3*np.pi/4+a))*size),int((y+12.6/2*np.sin(-3*np.pi/4+a))*size)),5*size,color,size)
            cv2.circle(img,(int((x-12.6/2*np.cos(-np.pi/4+a))*size),int((y+12.6/2*np.sin(-np.pi/4+a))*size)),5*size,color,size)
            cv2.line(img,(int((x-12.6/2*np.cos(np.pi/4+a))*size),int((y+12.6/2*np.sin(np.pi/4+a))*size)),(int((x-12.6/2*np.cos(-3*np.pi/4+a))*size),int((y+12.6/2*np.sin(-3*np.pi/4+a))*size)),color,size)
            cv2.line(img,(int((x-12.6/2*np.cos(-np.pi/4+a))*size),int((y+12.6/2*np.sin(-np.pi/4+a))*size)),(int((x-12.6/2*np.cos(3*np.pi/4+a))*size),int((y+12.6/2*np.sin(3*np.pi/4+a))*size)),color,size)
            if led[0]>-1:
                cv2.circle(img,(int(x*size),int(y*size)),3*size,led,-1)
        else:
            cv2.ellipse(img,(int((x+12.6/(2**0.5)/2)*size),int((y-1/4*4.0)*size)),(5*size,2*size),0,0,360,color,size)
            cv2.ellipse(img,(int((x-12.6/(2**0.5)/2)*size),int((y-1/4*4.0)*size)),(5*size,2*size),0,0,360,color,size)
            cv2.ellipse(img,(int((x-12.6/(2**0.5)/2)*size),int((y-3/4*4.0)*size)),(5*size,2*size),0,0,360,color,size)
            cv2.ellipse(img,(int((x+12.6/(2**0.5)/2)*size),int((y-3/4*4.0)*size)),(5*size,2*size),0,0,360,color,size)
            cv2.line(img,(int((x+12.6/(2**0.5)/2)*size),int((y-1/4*4.0)*size)),(int((x-21/(2**0.5)/2)*size),int((y-3/4*4.0)*size)),color,size)
            cv2.line(img,(int((x-12.6/(2**0.5)/2)*size),int((y-1/4*4.0)*size)),(int((x+21/(2**0.5)/2)*size),int((y-3/4*4.0)*size)),color,size)
            if led[0]>-1:
                cv2.circle(img,(int(x*size),int((y-1/2*4.0)*size)),3*size,led,-1)
    else:
        raise(Exception("Error Drone Type!无人机型号不支持"))

def drone3d(aixs,x,y,z,c,a,led=(-1,-1,-1),acceleration=(0,0,0),g=np.array([0,0,-980]),device="F400"):
    if device=="F400":
        rotate_matrix=iiid_rotate(np.array([acceleration[0],acceleration[1],acceleration[2]]),g)
        wing_force=a-g
        unit_wing_force=wing_force/np.sqrt(wing_force[0]**2+wing_force[1]**2+wing_force[2]**2)
        ring1=np.array(np.dot(rotate_matrix,np.array([21/2*np.cos(np.pi/4+a),21/2*np.sin(np.pi/4+a),0])))
        ring2=np.array(np.dot(rotate_matrix,np.array([21/2*np.cos(3*np.pi/4+a),21/2*np.sin(3*np.pi/4+a),0])))
        ring3=np.array(np.dot(rotate_matrix,np.array([21/2*np.cos(-3*np.pi/4+a),21/2*np.sin(-3*np.pi/4+a),0])))
        ring4=np.array(np.dot(rotate_matrix,np.array([21/2*np.cos(-np.pi/4+a),21/2*np.sin(-np.pi/4+a),0])))
        aixs.append([(x+ring1[0][0],y+ring1[0][1],z+ring1[0][2]),c,(14.9-21/4*2**0.5),1,(unit_wing_force[0],unit_wing_force[1],unit_wing_force[2]),'ring'])
        aixs.append([(x+ring2[0][0],y+ring2[0][1],z+ring2[0][2]),c,(14.9-21/4*2**0.5),1,(unit_wing_force[0],unit_wing_force[1],unit_wing_force[2]),'ring'])
        aixs.append([(x+ring3[0][0],y+ring3[0][1],z+ring3[0][2]),c,(14.9-21/4*2**0.5),1,(unit_wing_force[0],unit_wing_force[1],unit_wing_force[2]),'ring'])
        aixs.append([(x+ring4[0][0],y+ring4[0][1],z+ring4[0][2]),c,(14.9-21/4*2**0.5),1,(unit_wing_force[0],unit_wing_force[1],unit_wing_force[2]),'ring'])
        aixs.append([(x+ring1[0][0],y+ring1[0][1],z+ring1[0][2]),(x+ring3[0][0],y+ring3[0][1],z+ring3[0][2]),c,1,8,'line'])
        aixs.append([(x+ring2[0][0],y+ring2[0][1],z+ring2[0][2]),(x+ring4[0][0],y+ring4[0][1],z+ring4[0][2]),c,1,8,'line'])
        if led[0]>-1:
            aixs.append([(x,y,z),led,5,-1,'sphere'])
        else:
            aixs.append([(x,y,z),c,1,-1,'sphere'])
    elif device=="F600":
        rotate_matrix=iiid_rotate(np.array([acceleration[0],acceleration[1],acceleration[2]]),g)
        wing_force=a-g
        unit_wing_force=wing_force/np.sqrt(wing_force[0]**2+wing_force[1]**2+wing_force[2]**2)
        ring1=np.array(np.dot(rotate_matrix,np.array([12.6/2*np.cos(np.pi/4+a),12.6/2*np.sin(np.pi/4+a),0])))
        ring2=np.array(np.dot(rotate_matrix,np.array([12.6/2*np.cos(3*np.pi/4+a),12.6/2*np.sin(3*np.pi/4+a),0])))
        ring3=np.array(np.dot(rotate_matrix,np.array([12.6/2*np.cos(-3*np.pi/4+a),12.6/2*np.sin(-3*np.pi/4+a),0])))
        ring4=np.array(np.dot(rotate_matrix,np.array([12.6/2*np.cos(-np.pi/4+a),12.6/2*np.sin(-np.pi/4+a),0])))
        aixs.append([(x+ring1[0][0],y+ring1[0][1],z+ring1[0][2]),c,(17.5/2-12.6/4*2**0.5),1,(unit_wing_force[0],unit_wing_force[1],unit_wing_force[2]),'ring'])
        aixs.append([(x+ring2[0][0],y+ring2[0][1],z+ring2[0][2]),c,(17.5/2-12.6/4*2**0.5),1,(unit_wing_force[0],unit_wing_force[1],unit_wing_force[2]),'ring'])
        aixs.append([(x+ring3[0][0],y+ring3[0][1],z+ring3[0][2]),c,(17.5/2-12.6/4*2**0.5),1,(unit_wing_force[0],unit_wing_force[1],unit_wing_force[2]),'ring'])
        aixs.append([(x+ring4[0][0],y+ring4[0][1],z+ring4[0][2]),c,(17.5/2-12.6/4*2**0.5),1,(unit_wing_force[0],unit_wing_force[1],unit_wing_force[2]),'ring'])
        aixs.append([(x+ring1[0][0],y+ring1[0][1],z+ring1[0][2]),(x+ring3[0][0],y+ring3[0][1],z+ring3[0][2]),c,1,8,'line'])
        aixs.append([(x+ring2[0][0],y+ring2[0][1],z+ring2[0][2]),(x+ring4[0][0],y+ring4[0][1],z+ring4[0][2]),c,1,8,'line'])
        if led[0]>-1:
            aixs.append([(x,y,z),led,6.7/2,-1,'sphere'])
        else:
            aixs.append([(x,y,z),c,1,-1,'sphere'])
    else:
        raise(Exception("Error Drone Type!无人机型号不支持"))


'''def color(n):
    n=n*180/7
    x=255
    if int((n%765)/255)==0:
        return(255-n%255,n%255,x)
    if int((n%765)/255)==1:
        return(n%255,x,255-n%255)
    if int((n%765)/255)==2:
        return(x,255-n%255,n%255)'''

def getGui(field,size):
    size=int(size)
    img=np.zeros((600*size,1200*size,3),np.uint8)
    cv2.rectangle(img,(0,0),(600*size,600*size),(255,255,255),size)
    for x in range(12):
        for y in range(12):
            if x==11 and y!=11:
                cv2.rectangle(img,(570*size,(580-y*50)*size),(580*size,(580-(y*50+50))*size),(63+128*((x+y)%2),63+128*((x+y)%2),63+128*((x+y)%2)),-1)
            elif x!=11 and y==11:
                cv2.rectangle(img,((x*50+20)*size,30*size),((x*50+70)*size,20*size),(63+128*((x+y)%2),63+128*((x+y)%2),63+128*((x+y)%2)),-1)
            elif x==11 and y==11:
                cv2.rectangle(img,(570*size,30*size),(580*size,20*size),(63+128*((x+y)%2),63+128*((x+y)%2),63+128*((x+y)%2)),-1)
            else:
                cv2.rectangle(img,((x*50+20)*size,(580-y*50)*size),((x*50+70)*size,(580-(y*50+50))*size),(63+128*((x+y)%2),63+128*((x+y)%2),63+128*((x+y)%2)),-1)
    cv2.rectangle(img,(600*size,0),(1200*size,270*size),(255,255,255),size)
    cv2.rectangle(img,(600*size,270*size),(1200*size,540*size),(255,255,255),size)
    for x in range(0,18):
        cv2.line(img,(600*size,(x*10+20)*size),(620*size,(x*10+20)*size),(255,255,255),size)
        cv2.line(img,(600*size,(x*10+290)*size),(620*size,(x*10+290)*size),(255,255,255),size)
        if x%5==0:
            cv2.line(img,(600*size,(x*10+20)*size),(640*size,(x*10+20)*size),(255,255,255),size)
            cv2.line(img,(600*size,(x*10+290)*size),(640*size,(x*10+290)*size),(255,255,255),size)
    for a in range(7):
        if a<4:
            for x in range(150):
                cv2.line(img,((600+a*150+x)*size,540*size),((600+a*150+x)*size,570*size),color(a,(x-75)/75*125),size)
        else:
            for x in range(150):
                cv2.line(img,((600+(a-4)*150+x)*size,570*size),((600+(a-4)*150+x)*size,600*size),color(a,(x-75)/75*125),size)
    for x in range(4):
        cv2.rectangle(img,((600+x*150)*size,540*size),((750+x*150)*size,570*size),(255,255,255),size)
        cv2.rectangle(img,((600+x*150)*size,570*size),((750+x*150)*size,600*size),(255,255,255),size)
    cv2.rectangle(img,(1120*size,570*size),(1200*size,600*size),(255,255,255),size)
    if field==4:
        cv2.rectangle(img,(20*size,580*size),(380*size,220*size),(255,255,255),size)
        cv2.rectangle(img,(1000*size,0),(1000*size,540*size),(255,255,255),size)
    font=cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(img,'front',(600*size,260*size), font, size,(255,255,255),size)
    cv2.putText(img,'right',(600*size,530*size), font, size,(255,255,255),size)
    return img

def show(data,t0,music,field=6,device="F400",show=True,save="",FPS=200,max_fps=200,ThreeD=False,imshow=[120,-15],d=(600,450),track=[],skin=1,size=0,ssaa=1):
    size=int(size)
    ssaa=int(ssaa)
    if size==0:
        if len(save)>0:
            size=1
        else:
            screenWidth, screenHeight = pyautogui.size()
            while screenHeight>600*size/ssaa and screenWidth>1200*size/ssaa:
                size+=1
            size-=1
            while (600*size)%ssaa!=0:
                size-=1
    font=cv2.FONT_HERSHEY_SIMPLEX
    t0=int(t0+0.5)+3*max_fps
    if len(save)>0 and not ThreeD:  # save 2D video
        show=False
        video = cv2.VideoWriter(save+"_process.mp4", cv2.VideoWriter_fourcc('M', 'P', '4', 'V'), FPS,(int(1200*size/ssaa),int(600*size/ssaa)))
    if len(save)>0 and ThreeD:      # save 3D video
        if len(track)==0:
            video = cv2.VideoWriter(save+"_process.mp4", cv2.VideoWriter_fourcc('M', 'P', '4', 'V'), FPS,(1280,720))
        else:
            video = cv2.VideoWriter(save+"_process.mp4", cv2.VideoWriter_fourcc('M', 'P', '4', 'V'), FPS,(3840,1920))
    if (show and not ThreeD) or len(save)>0:
        # 生成gui.png   2D 背景图
        img=getGui(field,size)
        cv2.imwrite('gui.png',img)
        #生成可视化界面↑
    if ThreeD:
        if field==6:
            center=(280,280,165)#三维渲染旋转中心
        if field==4:
            center=(180,180,165)#三维渲染旋转中心
        lines=[]#三维渲染的线
        if field==6:
            lines.append([(-20,-20,0),(580,-20,0),(0,0,255),1,8,'line'])
            lines.append([(-20,-20,0),(-20,580,0),(0,255,0),1,8,'line'])
            lines.append([(-20,-20,0),(-20,-20,300),(255,0,0),1,8,'line'])
            lines.append([(-20,-20,0),(580,-20,0),(0,0,255),1,8,'line'])
            lines.append([(-20,-20,0),(-20,580,0),(0,255,0),1,8,'line'])
            lines.append([(-20,-20,0),(-20,-20,300),(255,0,0),1,8,'line'])
            lines.append([(0,0,0),(560,0,0),(255,255,255),1,8,'line'])
            lines.append([(0,0,0),(0,560,0),(255,255,255),1,8,'line'])
            lines.append([(0,560,0),(560,560,0),(255,255,255),1,8,'line'])
            lines.append([(560,0,0),(560,560,0),(255,255,255),1,8,'line'])
        if field==4:
            lines.append([(-20,-20,0),(380,-20,0),(0,0,255),1,8,'line'])
            lines.append([(-20,-20,0),(-20,380,0),(0,255,0),1,8,'line'])
            lines.append([(-20,-20,0),(-20,-20,300),(255,0,0),1,8,'line'])
            lines.append([(-20,-20,0),(380,-20,0),(0,0,255),1,8,'line'])
            lines.append([(-20,-20,0),(-20,380,0),(0,255,0),1,8,'line'])
            lines.append([(-20,-20,0),(-20,-20,300),(255,0,0),1,8,'line'])
            lines.append([(0,0,0),(360,0,0),(255,255,255),1,8,'line'])
            lines.append([(0,0,0),(0,360,0),(255,255,255),1,8,'line'])
            lines.append([(0,360,0),(360,360,0),(255,255,255),1,8,'line'])
            lines.append([(360,0,0),(360,360,0),(255,255,255),1,8,'line'])
        for x in range(1,57):
            if field==4 and x>36:
                break
            if x%10==5:
                lines.append([(x*10,-20,0),(x*10,20,40),(255,255,0),1,8,'line'])
                lines.append([(-20,x*10,0),(20,x*10,40),(255,0,255),1,8,'line'])
            elif x%10==0:
                lines.append([(x*10,-20,0),(x*10,30,50),(255,255,0),1,8,'line'])
                lines.append([(-20,x*10,0),(30,x*10,50),(255,0,255),1,8,'line'])
            else:
                lines.append([(x*10,-20,0),(x*10,10,30),(255,255,0),1,8,'line'])
                lines.append([(-20,x*10,0),(10,x*10,30),(255,0,255),1,8,'line'])
        for x in range(8,26):
            if x%10==5:
                lines.append([(-20,-20,x*10),(20,20,x*10),(0,255,255),1,8,'line'])
            elif x%10==0:
                lines.append([(-20,-20,x*10),(30,30,x*10),(0,255,255),1,8,'line'])
            else:
                lines.append([(-20,-20,x*10),(10,10,x*10),(0,255,255),1,8,'line'])
        i=imshow[0]
    if (show and len(save)==0) or (ThreeD and len(save)==0):
        # 添加音乐并播放
        if len(music)>1:
            for root, dirs, files in os.walk(music[0]):
                for file in files:
                    if os.path.splitext(file)[0]==music[1]:
                        music_name=(os.path.join(root , file))
            pygame.mixer.init()
            pygame.mixer.music.load(music_name)
            pygame.mixer.music.play(start=0.0)
        elif len(music)==1:
            pygame.mixer.init()
            pygame.mixer.music.load(music[0])
            pygame.mixer.music.play(start=0.0)
    time_read=time.time()
    k=0
    K=0
    #print('时间\t距离\t距离程度\t错误无人机')
    time_FPS=time.time()
    f=0     #记录帧数
    if (show and len(save)>0):
        # 如果保存视频，就加载渲染视频的进度条
        pbar = tqdm.tqdm(total=t0)
        pbar.set_description('Video Rendering')
    k_previous = k
    while k < t0:
        if (show or len(save)>0) and not ThreeD:    # 2D
            img2=cv2.imread('gui.png')
        aixs=[]
        if not ThreeD:                              # 2D
            t=0
            for a in range(len(data)):
                if len(data[a])>k:
                    t=max(t,data[a][k][0]/1000)
                    x=data[a][k][1]
                    y=data[a][k][2]
                    z=data[a][k][3]
                    angle=data[a][k][4]
                    led=data[a][k][5]
                else:
                    t=max(t,data[a][-1][0]/1000)
                    x=data[a][-1][1]
                    y=data[a][-1][2]
                    z=data[a][-1][3]
                    angle=data[a][-1][4]
                    led=data[a][-1][5]
                '''cv2.circle(img2,(x,560-y),15,color(a),-1)
                cv2.rectangle(img2,(560+x-15,250-z+5),(560+x+15,250-z-5),color(a),-1)
                cv2.rectangle(img2,(560+y-15,500-z+5),(560+y+15,500-z-5),color(a),-1)'''
                if (show or len(save)>0) and not ThreeD:
                    if a<4:
                        cv2.putText(img2,str(a+1)+' ('+str(int(x*1+0.5))+','+str(int(y*1+0.5))+','+str(int(z*1+0.5))+')',((600+a*150)*size,560*size), font, 0.5*size,(255,255,255),size)
                    else:
                        #在img2上画出无人机的位置并显示坐标
                        cv2.putText(img2,str(a+1)+' ('+str(int(x*1+0.5))+','+str(int(y*1+0.5))+','+str(int(z*1+0.5))+')',(a*150*size,590*size), font, 0.5*size,(255,255,255),size)
                aixs.append((x,y,z,angle,led,a))
        if (show or len(save)>0) and not ThreeD:
            Xs=sorted(aixs,key=lambda x:x[0])
            Ys=sorted(aixs,key=lambda x:x[1],reverse=True)
            Zs=sorted(aixs,key=lambda x:x[2])
            #根据距离远近渲染
            for X in Xs:
                draw_drone(img2,620+X[1],540-X[2],color(X[5],(X[0]-280)/280*125),led=X[4],skin=skin,device=device,size=size)
                #cv2.rectangle(img2,(int(560+X[1]-15),int(500-X[2]+5)),(int(560+X[1]+15),int(500-X[2]-5)),color(X[3],(X[0]-280)/280*125),-1)
            for Y in Ys:
                draw_drone(img2,620+Y[0],270-Y[2],color(Y[5],(280-Y[1])/280*125),led=Y[4],skin=skin,device=device,size=size)
                #cv2.rectangle(img2,(int(560+Y[0]-15),int(250-Y[2]+5)),(int(560+Y[0]+15),int(250-Y[2]-5)),color(Y[3],(280-Y[1])/280*125),-1)
            for Z in Zs:
                draw_drone(img2,20+Z[0],580-Z[1],color(Z[5],(Z[2]-125)/125*125),a=Z[3]/180*np.pi,led=Z[4],up=True,skin=skin,device=device,size=size)
                #cv2.circle(img2,(Z[0],560-Z[1]),15,color(Z[3],(Z[2]-125)/125*125),-1)
        #print(Xs)
        #print(aixs)
        if not ThreeD:
            for m in range(len(aixs)):
                for n in range(m+1,len(aixs)):#计算距离
                    distance=((aixs[m][0]-aixs[n][0])**2+(aixs[m][1]-aixs[n][1])**2)**0.5
                    if device=="F400":
                        if distance<51:
                            #print(t,distance,int(distance/20),m+1,n+1)#距离太近就输出错误
                            warnings.warn('In '+str(int(t))+'s,distance between d'+str(m+1)+' and d'+str(n+1)+' is less than '+str((int(distance/17)+1)*17)+'cm.在'+str(int(t))+'秒，无人机'+str(m+1)+'和无人机'+str(n+1)+'之间的距离小于'+str((int(distance/17)+1)*17)+'厘米。',Warning,2)
                            if show or len(save)>0:
                                cv2.circle(img2,(int((20+aixs[m][0])*size),int((580-aixs[m][1])*size)),20*size,(0,0,255),3*size)
                                cv2.circle(img2,(int((620+aixs[m][0])*size),int((270-aixs[m][2])*size)),20*size,(0,0,255),3*size)
                                cv2.circle(img2,(int((620+aixs[m][1])*size),int((540-aixs[m][2])*size)),20*size,(0,0,255),3*size)
                                cv2.circle(img2,(int((20+aixs[n][0])*size),int((580-aixs[n][1])*size)),20*size,(0,0,255),3*size)
                                cv2.circle(img2,(int((620+aixs[n][0])*size),int((270-aixs[n][2])*size)),20*size,(0,0,255),3*size)
                                cv2.circle(img2,(int((620+aixs[n][1])*size),int((540-aixs[n][2])*size)),20*size,(0,0,255),3*size)#错误红点标记
                    elif device=="F600":
                        if distance<33:
                            #print(t,distance,int(distance/20),m+1,n+1)#距离太近就输出错误
                            warnings.warn('In '+str(int(t))+'s,distance between d'+str(m+1)+' and d'+str(n+1)+' is less than '+str((int(distance/11)+1)*11)+'cm.在'+str(int(t))+'秒，无人机'+str(m+1)+'和无人机'+str(n+1)+'之间的距离小于'+str((int(distance/11)+1)*11)+'厘米。',Warning,2)
                            if show or len(save)>0:
                                cv2.circle(img2,(int((20+aixs[m][0])*size),int((580-aixs[m][1])*size)),12*size,(0,0,255),2*size)
                                cv2.circle(img2,(int((620+aixs[m][0])*size),int((270-aixs[m][2])*size)),12*size,(0,0,255),2*size)
                                cv2.circle(img2,(int((620+aixs[m][1])*size),int((540-aixs[m][2])*size)),12*size,(0,0,255),2*size)
                                cv2.circle(img2,(int((20+aixs[n][0])*size),int((580-aixs[n][1])*size)),12*size,(0,0,255),2*size)
                                cv2.circle(img2,(int((620+aixs[n][0])*size),int((270-aixs[n][2])*size)),12*size,(0,0,255),2*size)
                                cv2.circle(img2,(int((620+aixs[n][1])*size),int((540-aixs[n][2])*size)),12*size,(0,0,255),2*size)#错误红点标记
        if (show or len(save)>0) and not ThreeD:
            cv2.putText(img2,str(int(t*1000)/1000),(1050*size,590*size),font,0.5*size,(255,255,255),size)#在img2上显示时间
        time_fps=time.time()
        if len(save)==0 and show or (ThreeD and len(save)==0):
            k=int((time_fps-time_read)*max_fps)
        if show and not ThreeD:
            f+=1
            if f==1:
                time_fps=time.time()
                try:
                    fps=str(int(10/(time_fps-time_FPS)+0.5)/10)
                    fs=int(float(fps)/10+0.5)*10
                except:
                    fps=str(float(max_fps))
                    fs=max_fps
                if fs==0:
                    fs=10
            elif f%fs==0:
                fps=str(int(fs*10/(time_fps-time_FPS)+0.5)/10)
                time_FPS=time_fps
        if len(save)>0:
            fps=str(int(FPS*10+0.5)/10)
        if (show or len(save)>0) and not ThreeD:
            cv2.putText(img2,'fps:'+fps,(1120*size,590*size),font,0.5*size,(255,255,255),size)
        if show and not ThreeD:
            #cv2.destroyAllWindows()
            #cv2.namedWindow('img')
            #cv2.createTrackbar('time','img',int(t),int(t0),nothing)
            img2=cv2.resize(img2,(int(img2.shape[1]/ssaa),int(img2.shape[0]/ssaa)))
            cv2.imshow('img',img2)
            key = cv2.waitKey(1) & 0xff
            #Esc键退出
            if key == 27:
                break
            elif key==32:#空格暂停
                if len(music)>0:
                    pygame.mixer.music.stop()
                cv2.waitKey(0)
                time_read=time.time()-k/max_fps
                if len(music)>0:
                    pygame.mixer.music.play(start=k/max_fps)
            elif key==ord('q'):#后退
                k-=max_fps
                #time_read+=0.5
                if time_read>time_fps:
                    time_read=time_fps
                if k<0:
                    k=0
                if len(music)>0:
                    pygame.mixer.music.stop()
                cv2.waitKey(0)
                time_read=time.time()-k/max_fps
                if len(music)>0:
                    pygame.mixer.music.play(start=k/max_fps)
            elif key==ord('e'):#快进
                #time_read-=0.5
                k+=max_fps
                if len(music)>0:
                    pygame.mixer.music.stop()
                cv2.waitKey(0)
                time_read=time.time()-k/max_fps
                if len(music)>0:
                    pygame.mixer.music.play(start=k/max_fps)
            #time_read-=t-cv2.getTrackbarPos('time','img')
        #print('\r'+str(t)+'/'+str((t0-300)/100)+'  ',end='')
        
        if ThreeD:
            texts=[]#显示的文字
            t=0
            for a in range(len(data)):
                if len(data[a])>k:
                    t=max(t,data[a][k][0]/1000)
                    x=data[a][k][1]
                    y=data[a][k][2]
                    z=data[a][k][3]
                    angle=data[a][k][4]
                    led=data[a][k][5]
                    acceleration=data[a][k][6]
                else:
                    t=max(t,data[a][-1][0]/1000)
                    x=data[a][-1][1]
                    y=data[a][-1][2]
                    z=data[a][-1][3]
                    angle=data[a][-1][4]
                    led=data[a][-1][5]
                    acceleration=data[a][-1][6]
                c=color(a)
                #aixs.append([(x,y,z),c,5,1,'ring'])
                #drone.append([x,y,z,c])
                drone3d(aixs,x,y,z,color(a,127),angle/180*np.pi,led,acceleration,device=device)
                drone3d(aixs,x,y,0,color(a,-127),angle/180*np.pi,device=device)
                texts.append([str(a+1)+'('+str(int(x+0.5))+','+str(int(y+0.5))+','+str(int(z+0.5))+')',(0,140+30*a),0.5,c,1,'text'])
            texts.append(['T+'+str(int(t*1000)/1000),(0,80),0.5,(255,255,255),1,'text'])
            errors=[]#圈出错误的飞机
            for m in range(0,len(aixs),14):
                for n in range(m+14,len(aixs),14):#计算距离
                    distance=((aixs[m][0][0]-aixs[n][0][0]+aixs[m+2][0][0]-aixs[n+2][0][0])**2+(aixs[m][0][1]-aixs[n][0][1]+aixs[m+2][0][1]-aixs[n+2][0][1])**2)**0.5/2
                    if device=="F400":
                        if distance<51:
                            warnings.warn('In '+str(int(t))+'s,distance between d'+str(int(m/12+1))+' and d'+str(int(n/12+1))+' is less than '+str((int(distance/17)+1)*17)+'cm.在'+str(int(t))+'秒，无人机'+str(int(m/12+1))+'和无人机'+str(int(n/12+1))+'之间的距离小于'+str((int(distance/17)+1)*17)+'厘米。',Warning,2)
                            #print(t,distance,int(distance/20),m+1,n+1)#距离太近就输出错误
                            if len(track)==0:
                                errors.append([((aixs[m][0][0]+aixs[m+2][0][0])/2,(aixs[m][0][1]+aixs[m+2][0][1])/2,aixs[m][0][2]),(0,0,255),10,1,'sphere'])#错误红圈标记
                                errors.append([((aixs[n][0][0]+aixs[n+2][0][0])/2,(aixs[n][0][1]+aixs[n+2][0][1])/2,aixs[n][0][2]),(0,0,255),10,1,'sphere'])
                            else:
                                errors.append([((aixs[m][0][0]+aixs[m+2][0][0])/2,(aixs[m][0][1]+aixs[m+2][0][1])/2,aixs[m][0][2]),(0,0,255),10,1,'ring'])#错误红圈标记
                                errors.append([((aixs[n][0][0]+aixs[n+2][0][0])/2,(aixs[n][0][1]+aixs[n+2][0][1])/2,aixs[n][0][2]),(0,0,255),10,1,'ring'])
                    elif device=="F600":
                        if distance<33:
                            warnings.warn('In '+str(int(t))+'s,distance between d'+str(int(m/12+1))+' and d'+str(int(n/12+1))+' is less than '+str((int(distance/11)+1)*11)+'cm.在'+str(int(t))+'秒，无人机'+str(int(m/12+1))+'和无人机'+str(int(n/12+1))+'之间的距离小于'+str((int(distance/11)+1)*11)+'厘米。',Warning,2)
                            #print(t,distance,int(distance/20),m+1,n+1)#距离太近就输出错误
                            if len(track)==0:
                                errors.append([((aixs[m][0][0]+aixs[m+2][0][0])/2,(aixs[m][0][1]+aixs[m+2][0][1])/2,aixs[m][0][2]),(0,0,255),6,1,'sphere'])#错误红圈标记
                                errors.append([((aixs[n][0][0]+aixs[n+2][0][0])/2,(aixs[n][0][1]+aixs[n+2][0][1])/2,aixs[n][0][2]),(0,0,255),6,1,'sphere'])
                            else:
                                errors.append([((aixs[m][0][0]+aixs[m+2][0][0])/2,(aixs[m][0][1]+aixs[m+2][0][1])/2,aixs[m][0][2]),(0,0,255),6,1,'ring'])#错误红圈标记
                                errors.append([((aixs[n][0][0]+aixs[n+2][0][0])/2,(aixs[n][0][1]+aixs[n+2][0][1])/2,aixs[n][0][2]),(0,0,255),6,1,'ring'])
            img=IIID.show(aixs+lines+errors+texts,center,1280,720,[imshow[0],imshow[1],1,0,0],d)
            f+=1
            if f==1:
                time_fps=time.time()
                try:
                    fps=str(int(10/(time_fps-time_FPS)+0.5)/10)
                    fs=int(float(fps)/10+0.5)*10
                except:
                    fps=str(float(max_fps))
                    fs=max_fps
                if fs==0:
                    fs=10
            elif f%fs==0:
                fps=str(int(fs*10/(time_fps-time_FPS)+0.5)/10)
                time_FPS=time_fps
            if len(save)>0:
                fps=str(int(FPS*10+0.5)/10)
            texts.append(['FPS:'+fps,(0,110),0.5,(255,255,255),1,'text'])
            if len(track)==1:
                if len(data[track[0]])>k:
                    x=data[track[0]][k][1]
                    y=data[track[0]][k][2]
                    z=data[track[0]][k][3]
                else:
                    x=data[track[0]][-1][1]
                    y=data[track[0]][-1][2]
                    z=data[track[0]][-1][3]
                center=(x,y,z+5)
            if len(track)==3:
                center=track
            if len(track)==0:
                img=IIID.show(aixs+lines+errors+texts,center,1280,720,[imshow[0],imshow[1],1,0,0],d)
            else:
                img=IIID2.show(aixs+lines+errors,center,3840,1920)
            if len(save)==0:
                cv2.imshow('img',img)
                key = cv2.waitKey(1) & 0xff
                #Esc键退出
                if key == 27:
                    break
                elif key==32:#长按空格键暂停，暂停后可以按wasd旋转，按esc退出暂停
                    if len(music)>0:
                        pygame.mixer.music.stop()
                    imshow[0],imshow[1]=IIID.show(aixs+lines+errors+texts,center,1280,720,[imshow[0],imshow[1],1],d)
                    i=imshow[0]-int(k/max_fps*36+0.5)
                    time_read=time.time()-k/max_fps
                    if len(music)>0:
                        pygame.mixer.music.play(start=k/max_fps)
                elif key==ord('q'):#后退
                    k-=max_fps
                    #time_read+=0.5
                    if time_read>time_fps:
                        time_read=time_fps
                    if k<0:
                        k=0
                    if len(music)>0:
                        pygame.mixer.music.stop()
                    cv2.waitKey(0)
                    time_read=time.time()-k/max_fps
                    if len(music)>0:
                        pygame.mixer.music.play(start=k/max_fps)
                elif key==ord('e'):#快进
                    k+=max_fps
                    if len(music)>0:
                        pygame.mixer.music.stop()
                    cv2.waitKey(0)
                    time_read=time.time()-k/max_fps
                    if len(music)>0:
                        pygame.mixer.music.play(start=k/max_fps)
            
        if not show and len(save)==0 and not ThreeD:
            k+=1
        if len(save)>0:
            if ThreeD:
                video.write(img)
            else:
                img2=cv2.resize(img2,(int(img2.shape[1]/ssaa),int(img2.shape[0]/ssaa)))
                video.write(img2)
            K+=max_fps/FPS
            k=int(K+0.5)
        if (show and len(save)>0):  # 加载进度条
            # k 是进度条的当前进度
            # t0 是进度条的总进度
            pbar.update(k - k_previous)
            k_previous = k
    if (show and len(save)==0) or (ThreeD and len(save)==0):
        cv2.destroyAllWindows()
        if len(music)>1 or (len(music)==1 and music[0].split('.')[-1] in ['mp3','wav']):
            pygame.mixer.music.stop()
    timer=time.time()-time_read
    print('平均帧率：'+str(int(10*f/timer+0.5)/10))
    print('飞行总时间：'+str(int((time.time()-time_read)*1000+0.5)/1000)+'秒')
    if len(save)>0:
        print('视频保存中')
        video.release()#储存视频
        if len(music)>1:
            print('音频添加中')
            for root, dirs, files in os.walk(music[0]):
                for file in files:
                    if os.path.splitext(file)[0]==music[1]:
                        music_name=(os.path.join(root , file))
            if os.path.exists(save+'.mp4'):
                os.remove(save+'.mp4')
            video_add_audio(save+"_process.mp4",music_name,save+'.mp4')
        elif len(music)==1:
            print('音频添加中')
            if os.path.exists(save+'.mp4'):
                os.remove(save+'.mp4')
            video_add_audio(save+"_process.mp4",music[0],save+'.mp4')
        else:
            print('No music!')
            shutil.copy(save+"_process.mp4",save+'.mp4')
        os.remove(save+'_process.mp4')
        print(save+".mp4保存成功")