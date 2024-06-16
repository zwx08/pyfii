from . import drone
def Drone_first(first_coords: tuple,vel: int=200,acc:int=400,drone_config=drone.drone_config_6m):
    X=first_coords[0]
    Y=first_coords[1]
    Z=first_coords[2]
    d=drone.Drone(X,Y,drone_config)
    d.takeoff(1,Z)
    d.inittime(4)
    d.VelXY(vel,acc)
    d.VelZ(vel,acc)
    return d