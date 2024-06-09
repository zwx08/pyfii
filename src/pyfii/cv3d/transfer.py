from typing import List, Tuple
import numpy as np

Vec2 = np.ndarray | Tuple[float, float] | List[float, float]

Degree = float  # 角度制浮点数
Radian = float  # 弧度制浮点数


def xy2ra(x: float, y: float) -> Tuple[float, Radian]:
    """二维坐标转化为距离方位

    Args:
        x (float): x坐标
        y (float): y坐标

    Returns:
        Tuple[float, Radian]: 距离, 角度
    """
    r = (x**2 + y**2) ** 0.5
    if y < 0:
        a = -np.arccos(x / r)
    elif y > 0:
        a = np.arccos(x / r)
    else:
        if x >= 0:
            a = 0
        else:
            a = np.pi
    return r, a


def ra2xy(r: float, a: Radian) -> Tuple[float, float]:
    """距离方位转化为二维坐标

    Args:
        r (float): 距离
        a (Radian): 角度

    Returns:
        Tuple[float, float]: xy坐标
    """
    x = r * np.cos(a)
    y = r * np.sin(a)
    return x, y


def xyz2rab(
    x: float, y: float, z: float
) -> Tuple[float, Radian, Radian]:  # 三维坐标转化为距离方位
    """三维坐标转化为距离方位

    Args:
        x (float): x坐标
        y (float): y坐标
        z (float): z坐标

    Returns:
        Tuple[float, Radian, Radian]: 距离, 方向角, 仰角
    """
    r, a = xy2ra(x, y)
    r, b = xy2ra(r, z)
    return r, a, b


def rab2xyz(r: float, a: Radian, b: Radian) -> Tuple[float, float, float]:
    """距离方位转化为三维坐标

    Args:
        r (float): 距离
        a (Radian): 方向角
        b (Radian): 仰角

    Returns:
        Tuple[float, float, float]: xyz坐标
    """
    r, z = ra2xy(r, b)
    x, y = ra2xy(r, a)
    return x, y, z


def rotate(
    point2d: Vec2, angle: Radian
) -> Tuple[float, float]:  # 二维旋转(坐标点,旋转角度)
    """二维旋转(坐标点,旋转角度)

    Args:
        point2d (Vec2): 坐标点
        angle (Radian): 旋转角度

    Returns:
        Tuple[float, float]: xy坐标
    """
    x = point2d[0]
    y = point2d[1]
    r, a = xy2ra(x, y)
    x, y = ra2xy(r, a + angle)
    return (x, y)


def resize(point2d: Vec2, scale: float) -> Tuple[float, float]:
    """二维缩放(坐标点,缩放大小)

    Args:
        point2d (Vec2): 坐标点
        scale (float): 缩放大小

    Returns:
        Tuple[float, float]: xy坐标
    """
    x = point2d[0] * scale
    y = point2d[1] * scale
    return (x, y)


def move(point2d: Vec2, x: float, y: float) -> Tuple[float, float]:
    """二维移动(坐标点,xy方向移动距离)

    Args:
        point2d (Vec2): 坐标点
        x (float): x方向移动距离
        y (float): y方向移动距离

    Returns:
        Tuple[float, float]: xy坐标
    """
    x += point2d[0]
    y += point2d[1]
    return (x, y)


def rotate3d(aixs, a, b):  # 三维旋转(坐标点,旋转角度)
    x = aixs[0]
    y = aixs[1]
    z = aixs[2]
    x, y = rotate((x, y), a)
    x, z = rotate((x, z), b)
    return (x, y, z)


def resize3d(aixs, n):  # 三维缩放(坐标点,缩放大小)
    x = aixs[0] * n
    y = aixs[1] * n
    z = aixs[2] * n
    return (x, y, z)


def move3d(aixs, x, y, z):  # 三维移动(坐标点,xyz方向移动距离)
    x += aixs[0]
    y += aixs[1]
    z += aixs[2]
    return (x, y, z)
