import sys, os

path = os.getcwd() + r'/src'
sys.path.append(path)

import pyfii as pf

d1=pf.Drone(40,40,pf.drone_config_6m)
d1.ip="192.168.51.51"

d1.takeoff(1,80)

d1.inittime(4)
d1.VelXY(200,400)
d1.VelZ(200,400)
d1.move2(520,520,250)
d1.TurnOnAll('#ffff00')
d1.delay(500)
d1.TurnOnAll((0,255,0))
d1.delay(2999)
d1.TurnOnAll([
    '#ffff00','#ffff00','#ffff00','#ffff00',
    '#ffff00','#ffff00','#ffff00','#ffff00',
    '#ffff00','#ffff00','#ffff00','#ffff00'
])
d1.delay(500)
d1.TurnOnAll([
    (255,0,0),(255,0,0),(255,0,0),(255,0,0),
    (255,0,0),(255,0,0),(255,0,0),(255,0,0),
    (255,0,0),(255,0,0),(255,0,0),(255,0,0)
])

d1.inittime(9)
d1.BlinkFastAll(['#ff0000',(255,255,0),'#00ff00'])
'''
相当于
d1.BlinkFastAll([
    '#ff0000',(255,255,0),'#00ff00',
    '#ff0000',(255,255,0),'#00ff00',
    '#ff0000',(255,255,0),'#00ff00',
    '#ff0000',(255,255,0),'#00ff00'
])
'''
d1.land()

d1.end()

name='output/group_flight_6m_1'
F=pf.Fii(name,[d1])
F.save(field=6)

data,t0,music,field,*_=pf.read_fii(name,getfield=True)
pf.show(data,t0,music,field=field,save=name,FPS=25)
pf.show(data,t0,music,field=field,save=name+'_3D',ThreeD=True,imshow=[90,0],d=(600,450),FPS=25)

'''
单机飞行示例，
如果灯光与无人机运动状态相符，
说明无人机性能良好，
且能达到设置的速度加速度。
'''