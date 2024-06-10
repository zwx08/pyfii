from typing import Any, List
import cv2
from cv2.typing import MatLike, Scalar
import numpy as np
from .transfer import *
from .typing import Vec2, Vec3, Degree, Radian


def polar3d(point3d: Vec3, center: Vec3 = (0, 0, 0)) -> Tuple[Degree, Degree, float]:
    """将三维空间直角坐标系坐标转化为极坐标

    Args:
        point3d (Vec3): 三维坐标点
        center (Vec3, optional): 坐标系原点. Defaults to (0, 0, 0).

    Returns:
        Tuple[Degree, Degree, float]: 方向角, 仰角, 距离
    """
    r, a, b = xyz2rab(
        point3d[0] - center[0], point3d[1] - center[1], point3d[2] - center[2]
    )
    return np.degrees(a), np.degrees(b), r


def polylines(
    img: MatLike,
    points3d: Vec3,
    center: Vec3,
    color: Scalar,
    isclosed: bool = True,
    thickness: int = 1,
):
    """在图像上绘制折线

    Args:
        img (MatLike): 图像
        points3d (Vec3): 折线端点
        center (Vec3): 坐标系原点
        color (Scalar): 颜色
        isclosed (bool, optional): 是否为封闭图形. Defaults to True.
        thickness (int, optional): 粗细. Defaults to 1.
    """
    polar_points3d = []
    for p in points3d:
        polar_points3d.append((polar3d(p, center)))
    points3d = polar_points3d
    dots = []
    for p in points3d:
        dots.append(
            [
                (-p[0] + 180) % 360 / 360 * img.shape[1],
                (-p[1] + 90) / 180 * img.shape[0],
            ]
        )
    if isclosed:
        for d in range(len(dots)):
            if abs(dots[d - 1][0] - dots[d][0]) > img.shape[1] / 2:
                if dots[d - 1][0] - dots[d][0] > 0:
                    cv2.line(
                        img,
                        (int(dots[d - 1][0] - img.shape[1]), int(dots[d - 1][1])),
                        (int(dots[d][0]), int(dots[d][1])),
                        color,
                        thickness,
                    )
                    cv2.line(
                        img,
                        (int(dots[d - 1][0]), int(dots[d - 1][1])),
                        (int(dots[d][0] + img.shape[1]), int(dots[d][1])),
                        color,
                        thickness,
                    )
                else:
                    cv2.line(
                        img,
                        (int(dots[d - 1][0] + img.shape[1]), int(dots[d - 1][1])),
                        (int(dots[d][0]), int(dots[d][1])),
                        color,
                        thickness,
                    )
                    cv2.line(
                        img,
                        (int(dots[d - 1][0]), int(dots[d - 1][1])),
                        (int(dots[d][0] - img.shape[1]), int(dots[d][1])),
                        color,
                        thickness,
                    )
            else:
                cv2.line(
                    img,
                    (int(dots[d - 1][0]), int(dots[d - 1][1])),
                    (int(dots[d][0]), int(dots[d][1])),
                    color,
                    thickness,
                )
    else:
        for d in range(1, len(dots)):
            if abs(dots[d - 1][0] - dots[d][0]) > img.shape[1] / 2:
                if dots[d - 1][0] - dots[d][0] > 0:
                    cv2.line(
                        img,
                        (int(dots[d - 1][0] - img.shape[1]), int(dots[d - 1][1])),
                        (int(dots[d][0]), int(dots[d][1])),
                        color,
                        thickness,
                    )
                    cv2.line(
                        img,
                        (int(dots[d - 1][0]), int(dots[d - 1][1])),
                        (int(dots[d][0] + img.shape[1]), int(dots[d][1])),
                        color,
                        thickness,
                    )
                else:
                    cv2.line(
                        img,
                        (int(dots[d - 1][0] + img.shape[1]), int(dots[d - 1][1])),
                        (int(dots[d][0]), int(dots[d][1])),
                        color,
                        thickness,
                    )
                    cv2.line(
                        img,
                        (int(dots[d - 1][0]), int(dots[d - 1][1])),
                        (int(dots[d][0] - img.shape[1]), int(dots[d][1])),
                        color,
                        thickness,
                    )
            else:
                cv2.line(
                    img,
                    (int(dots[d - 1][0]), int(dots[d - 1][1])),
                    (int(dots[d][0]), int(dots[d][1])),
                    color,
                    thickness,
                )


def line(
    img: MatLike, p1: Vec3, p2: Vec3, color, thickness=1, center: Vec3 = (0, 0, 0)
):  # 在img上显示线段(img,端点1坐标,端点2坐标,颜色,粗细,观察者位置,直线类型)
    a1, b1, _ = polar3d(p1, center)
    a2, b2, _ = polar3d(p2, center)
    dis = ((a1 - a2) ** 2 + (b1 - b2) ** 2) ** 0.5
    plts = []
    m = int(dis / 8 + 1)
    for n in range(m + 1):
        plts.append(
            (
                p1[0] + n * (p2[0] - p1[0]) / m,
                p1[1] + n * (p2[1] - p1[1]) / m,
                p1[2] + n * (p2[2] - p1[2]) / m,
            )
        )
    polylines(img, plts, center, color, False, thickness)


def ring(img, aixs, color, r, center=(0, 0, 0), n=1):
    a1, b1, r1 = polar3d(aixs, center)
    plts = []
    if r1 == 0:
        cv2.line(
            img,
            (0, int(img.shape[0] / 2)),
            (img.shape[1], int(img.shape[0] / 2)),
            color,
            n,
        )
    else:
        m = int(r / r1 * 180 + 1)
        if m < 12:
            m = 12
        elif m > 360:
            m = 360
        for l in range(m):
            l = l / m * 2 * np.pi
            plts.append((aixs[0] + r * np.cos(l), aixs[1] + r * np.sin(l), aixs[2]))
        polylines(img, plts, center, color, True, n)


def distance(aixs, center=(0, 0, 0)):  # 计算距离
    if aixs[-1] == "text":
        return -10000
    elif aixs[-1] == "line":
        return polar3d(
            (
                (aixs[0][0] + aixs[1][0]) / 2,
                (aixs[0][1] + aixs[1][1]) / 2,
                (aixs[0][2] + aixs[1][2]) / 2,
            ),
            center,
        )[2]
    elif aixs[-1] == "sphere":
        return polar3d(aixs[0], center)[2]
    elif aixs[-1] == "ring":
        return polar3d(aixs[0], center)[2]


def show(
    objects3d: List[Any], center: Vec3 = (0, 0, 0), x: int = 3840, y: int = 1920
):  # 显示(aixs：记录所有需要显示的点线面的列表,观察者位置,显示的视图大小)
    objects3d = sorted(
        objects3d, key=lambda u: distance(u, center), reverse=True
    )  # 计算渲染顺序
    img = np.zeros((y, x, 3), np.uint8)
    for obj3d in objects3d:
        if obj3d[-1] == "line":
            line(img, obj3d[0], obj3d[1], obj3d[2], obj3d[3], center, obj3d[4])
        elif obj3d[-1] == "ring":
            ring(img, obj3d[0], obj3d[1], obj3d[2], center, obj3d[3])
    return img
