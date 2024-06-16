from . import drone
def Drone_first(X: int,Y: int,Z: int,vel: int=200,acc:int=400,drone_config=drone.drone_config_6m):
    d=drone.Drone(X,Y,drone_config)
    d.takeoff(1,Z)
    d.inittime(4)
    d.VelXY(vel,acc)
    d.VelZ(vel,acc)
    return d