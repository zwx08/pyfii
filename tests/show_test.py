import sys, os

path = os.getcwd() + r'/src'
sys.path.append(path)

import pyfii as pf

name='output/无人区'
'''data,t0,music,feild=pf.read_fii(name,getfeild=True)
pf.show(data,t0,music,feild=feild,skin=1)
pf.show(data,t0,music,feild=feild,ThreeD=True,imshow=[120,-30],d=(1,0))'''

data,t0,music,feild,device=pf.read_fii(name,getdevice=True,fps=60,ignore_acc=False)
#pf.show(data,t0,music,feild=feild,device=device,save=name+'_ignore_acc',FPS=20,max_fps=60)
#pf.show(data,t0,music,feild=feild,device=device,save=name+'_3D_ignore_acc',ThreeD=True,imshow=[90,3],d=(600,500),FPS=20,max_fps=60)
pf.show(data,t0,music,feild=feild,device=device,save=name,FPS=60,max_fps=60)
pf.show(data,t0,music,feild=feild,device=device,save=name+'_3D',ThreeD=True,imshow=[90,3],d=(600,500),FPS=60,max_fps=60)
#pf.show(data,t0,music,feild=6,save=name+'_3D2',ThreeD=True,imshow=[120,-30],d=(1,0),FPS=60,max_fps=60)
