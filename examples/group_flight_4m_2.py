import sys, os

path = os.getcwd() + r'/src'
sys.path.append(path)

import pyfii as pf

# 三架F600,4m毯
d1=pf.Drone6(0,0,pf.drone_config_4m,"192.168.51.51")
d2=pf.Drone6(0,0,pf.drone_config_4m,"192.168.51.52")
d3=pf.Drone6(0,0,pf.drone_config_4m,"192.168.51.53")

# 无人机列表
ds=[d1,d2,d3]

for d,y in zip(ds,range(60,360,120)):
    # 定义起飞位置
    d.X=20
    d.Y=y
    
    # 起飞
    d.takeoff(1,80)

    # 4秒开始动作
    d.inittime(4)
    # 水平速度200cm/s 加速度400cm/s^2
    d.VelXY(200,400)
    # 竖直速度200cm/s 加速度400cm/s^2
    # 建议竖直速度加速度与水平速度加速度统一
    d.VelZ(200,400)
    # 移动至(340,y,250)
    d.move2(340,y,250)
    # 全部亮黄灯
    d.AllOn('#ffff00')
    # 等待500ms
    # t = v / a = 200cm/s / 400cm/s^2 = 0.5s = 500ms
    d.delay(500)
    # 全部亮绿灯
    d.AllOn((0,255,0))
    # 等待1312ms
    # t = s_匀速 / v = ( s_总 - s_加速 - s_减速 ) / v
    # = ( sqrt ( ( x_1 - x_0 ) ^ 2 + ( y_1 - y_0 ) ^ 2 + ( z_1 - z_0 ) ^ 2 ) - v ^ 2 / a ) / v
    # = ( sqrt ( ( 340cm - 20cm ) ^ 2 + ( y - y ) ^2 + ( 250cm - 80cm ) ^ 2 ) - 200cm/s ^ 2 / 400cm/s^2 ) / 200cm/s
    # = 1.312s = 1312ms
    d.delay(1312)
    # 全部亮黄灯
    d.AllOn('#ffff00')
    # 等待500ms
    # t = v / a = 200cm/s / 400cm/s^2 = 0.5s = 500ms
    d.delay(500)
    # 全部亮红灯
    d.AllOn((255,0,0))

    # 8秒开始动作
    d.inittime(8)
    # 全部熄灭
    d.AllOff()

    # 降落
    d.land()

    # 结束
    d.end()

# 保存
name='output/group_flight_4m_2'
F=pf.Fii(name,ds)
F.save(field=4)

# 读取
data,t0,music,field,*_=pf.read_fii(name,getfield=True)
# 储存二维模拟视频
pf.show(data,t0,music,field=field,save=name,FPS=25)
# 储存三维模拟视频
pf.show(data,t0,music,field=field,save=name+'_3D',ThreeD=True,imshow=[90,0],d=(600,550),FPS=25)

'''
如果在实际飞行中三架无人机保持在一条直线上，
且灯光与无人机运动状态相符，
说明无人机性能良好，
且能达到设置的速度加速度。
'''