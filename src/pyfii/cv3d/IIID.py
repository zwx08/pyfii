from typing import Any, List, Tuple
import cv2
from cv2.typing import MatLike, Scalar
import numpy as np
from .transfer import *
from .typing import Vec3, Degree, Radian


def eye_vector(a: Degree, b: Degree) -> Tuple[float, float, float]:
    return (
        np.cos(np.radians(abs(a))) * np.cos(np.radians(abs(b))),
        np.sin(np.radians(abs(a))) * np.cos(np.radians(abs(b))),
        np.sin(np.radians(abs(b))),
    )


def eye_axis(a: Degree, b: Degree, d0: float) -> Tuple[float, float, float]:
    return (
        -np.cos(np.radians(abs(a))) * np.cos(np.radians(abs(b))) * d0,
        -np.sin(np.radians(abs(a))) * np.cos(np.radians(abs(b))) * d0,
        -np.sin(np.radians(abs(b))) * d0,
    )


def abs_3d_vector(v: Vec3) -> float:
    """取得三维向量的模长

    Args:
        v (Vec3): 三维向量

    Returns:
        float: 三维向量的模长
    """
    assert len(v) == 3
    return np.linalg.norm(v)


def dot_3d_v1_v2(v1: Vec3, v2: Vec3) -> float:
    """两个三维向量的点乘

    Args:
        v1 (Vec3): 三维向量
        v2 (Vec3): 三维向量

    Returns:
        float: 点乘（内积）
    """
    assert len(v1) == 3 and len(v2) == 3
    return np.dot(v1, v2)


def iiid2iid(
    point: Vec3,
    x: float,
    y: float,
    a: Degree,
    b: Degree,
    center: Vec3 = (0, 0, 0),
    d: Vec2 = (1, 0),
) -> Tuple[float, float, float]:
    """三维坐标点投影在二维平面的位置(三维坐标点,二维平面原点xy,观察者面朝角度ab,观察者观察的中心位置)

    Args:
        point (Vec3): 三维坐标点
        x (float): 二维平面原点x
        y (float): 二维平面原点y
        a (Degree): 观察者面朝角度a
        b (Degree): 观察者面朝角度b
        center (Vec3, optional): 观察者观察的中心位置. Defaults to (0, 0, 0).
        d (Vec2, optional): _description_. Defaults to (1, 0).

    Returns:
        Tuple[ float, float, float ]: 第一二个输出为显示的xy坐标,第三个输出为点与观察者的相对距离(用于确定渲染的先后顺序,远先近后)
    """
    a = np.radians(a)
    b = np.radians(b)
    point = rotate3d(
        (point[0] - center[0], point[1] - center[1], point[2] - center[2]), -a, -b
    )
    if d[1] == 0:
        return (
            x - point[1] * d[0],
            y - point[2] * d[0],
            point[0],
        )  # 第一二个输出为显示的xy坐标,第三个输出为点与观察者的相对距离(用于确定渲染的先后顺序,远先近后)
    elif point[0] + d[0] == 0:
        return 0, 0, 0
    else:
        return (
            x - point[1] * d[1] / (point[0] + d[0]),
            y - point[2] * d[1] / (point[0] + d[0]),
            point[0] + d[0],
        )  # 第一二个输出为显示的xy坐标,第三个输出为点与观察者的相对距离(用于确定渲染的先后顺序,远先近后)


def sphere(
    img: MatLike,
    point: Vec3,
    x: float,
    y: float,
    a: Degree,
    b: Degree,
    color: Scalar,
    r: int = 1,
    center: Vec3 = (0, 0, 0),
    thickness: int = -1,
    d: Vec2 = (1, 0),
):
    """在图像上显示球体（点）(img,球心坐标,二维平面原点xy,观察者面朝角度ab,颜色,半径,观察者观察的中心位置)

    Args:
        img (MatLike): 图像
        point (Vec3): 球心坐标
        x (float): 二维平面原点x
        y (float): 二维平面原点y
        a (Degree): 观察者面朝角度a
        b (Degree): 观察者面朝角度b
        color (Scalar): 颜色
        r (int, optional): 半径. Defaults to 1.
        center (Vec3, optional): 观察者观察的中心位置. Defaults to (0, 0, 0).
        thickness (int, optional): 绘制的线宽，默认实心. Defaults to -1.
        d (Vec2, optional): _description_. Defaults to (1, 0).
    """
    x1, y1, z = iiid2iid(point, x, y, a, b, center, d)
    if d[1] == 0:
        cv2.circle(img, (int(x1), int(y1)), r, color, thickness)
    else:
        if z > 0:
            cv2.circle(img, (int(x1), int(y1)), int(r * d[1] / z + 1), color, thickness)


def line(
    img: MatLike,
    point1: Vec3,
    point2: Vec3,
    x: float,
    y: float,
    a: Degree,
    b: Degree,
    color: Scalar,
    thickness: int = 1,
    center: Vec3 = (0, 0, 0),
    line_type: int = cv2.LINE_8,
    d: Vec2 = (1, 0),
):
    """在图像上显示线段(img,端点1坐标,端点2坐标,二维平面原点xy,观察者面朝角度ab,颜色,粗细,观察者观察的中心位置,直线类型)

    Args:
        img (MatLike): 图像
        point1 (Vec3): 端点1坐标
        point2 (Vec3): 端点2坐标
        x (float): 二维平面原点x
        y (float): 二维平面原点y
        a (Degree): 观察者面朝角度a
        b (Degree): 观察者面朝角度b
        color (Scalar): 颜色
        thickness (int, optional): 绘制的线宽，默认实心. Defaults to 1.
        center (Vec3, optional): 观察者观察的中心位置. Defaults to (0, 0, 0).
        line_type (int, optional): 线的类型. Defaults to cv2.LINE_8.
        d (Vec2, optional): _description_. Defaults to (1, 0).
    """
    x1, y1, z1 = iiid2iid(point1, x, y, a, b, center, d)
    x2, y2, z2 = iiid2iid(point2, x, y, a, b, center, d)
    if d[1] == 0:
        cv2.line(
            img, (int(x1), int(y1)), (int(x2), int(y2)), color, thickness, line_type
        )
    else:
        if z1 > 0 and z2 > 0:
            cv2.line(
                img, (int(x1), int(y1)), (int(x2), int(y2)), color, thickness, line_type
            )


def ring(
    img: MatLike,
    point: Vec3,
    x: float,
    y: float,
    a: Degree,
    b: Degree,
    color: Scalar,
    r: int,
    center: Vec3 = (0, 0, 0),
    thickness: int = 1,
    d: Vec2 = (1, 0),
    normal_vector: Vec3 = (0, 0, 1),
):
    """在图像上显示圆环

    Args:
        img (MatLike): 图像
        point (Vec3): 圆心坐标
        x (float): 二维平面原点x
        y (float): 二维平面原点y
        a (Degree): 观察者面朝角度a
        b (Degree): 观察者面朝角度b
        color (Scalar): 颜色
        r (int): 半径
        center (Vec3, optional): 观察者观察的中心位置. Defaults to (0, 0, 0).
        thickness (int, optional): 绘制的线宽，默认实心. Defaults to 1.
        d (Vec2, optional): _description_. Defaults to (1, 0).
        normal_vector (Vec3, optional): 圆环平面的法向量. Defaults to (0, 0, 1).
    """
    x1, y1, z = iiid2iid(point, x, y, a, b, center, d)
    if d[1] == 0:
        eye_vec = eye_vector(a, b)
        ratio_ellipse_a_b = abs(
            dot_3d_v1_v2(eye_vec, normal_vector) / abs_3d_vector(normal_vector)
        )
        if int(r * ratio_ellipse_a_b + 0.5) < 1:
            cv2.ellipse(
                img, (int(x1), int(y1)), (int(r + 0.5), 1), 0, 0, 360, color, thickness
            )
        else:
            cv2.ellipse(
                img,
                (int(x1), int(y1)),
                (int(r + 0.5), int(r * ratio_ellipse_a_b + 0.5)),
                0,
                0,
                360,
                color,
                thickness,
            )
    else:
        a = np.radians(a)
        b = np.radians(b)
        point = rotate3d(
            (point[0] - center[0], point[1] - center[1], point[2] - center[2]), -a, -b
        )
        where_eye_is = eye_axis(a, b, d[0])
        eye_vec = (
            point[0] - where_eye_is[0],
            point[1] - where_eye_is[1],
            point[2] - where_eye_is[2],
        )
        ratio_ellipse_a_b = abs(
            dot_3d_v1_v2(eye_vec, normal_vector)
            / abs_3d_vector(normal_vector)
            / abs_3d_vector(eye_vec)
        )
        if z > 0:
            if int(r * d[1] / z * ratio_ellipse_a_b + 0.5) < 1:
                cv2.ellipse(
                    img,
                    (int(x1), int(y1)),
                    (int(r * d[1] / z + 0.5), 1),
                    0,
                    0,
                    360,
                    color,
                    thickness,
                )
            else:
                cv2.ellipse(
                    img,
                    (int(x1), int(y1)),
                    (
                        int(r * d[1] / z + 0.5),
                        int(r * d[1] / z * ratio_ellipse_a_b + 0.5),
                    ),
                    0,
                    0,
                    360,
                    color,
                    thickness,
                )


def distance(
    obj3d: List[Any],
    x: float,
    y: float,
    A: Degree,
    B: Degree,
    center: Vec3 = (0, 0, 0),
    d: Vec2 = (1, 0),
) -> float:
    """计算距离

    Args:
        obj3d (List[Any]): 三维物体
        x (float): 二维平面原点x
        y (float): 二维平面原点y
        A (Degree): 观察者面朝角度a
        B (Degree): 观察者面朝角度b
        center (Vec3, optional): 观察者观察的中心位置. Defaults to (0, 0, 0).
        d (Vec2, optional): _description_. Defaults to (1, 0).

    Returns:
        float: 距离
    """
    if obj3d[-1] == "text":
        return -10000
    elif obj3d[-1] == "line":
        return iiid2iid(
            (
                (obj3d[0][0] + obj3d[1][0]) / 2,
                (obj3d[0][1] + obj3d[1][1]) / 2,
                (obj3d[0][2] + obj3d[1][2]) / 2,
            ),
            x,
            y,
            A,
            B,
            center,
            d,
        )[2]
    elif obj3d[-1] == "sphere":
        return iiid2iid(obj3d[0], x, y, A, B, center, d)[2]
    elif obj3d[-1] == "ring":
        return iiid2iid(obj3d[0], x, y, A, B, center, d)[2]


def show(
    obj3d_list, center=(0, 0, 0), x=720, y=720, imshow=[-1], d=(1, 0)
):  # 显示(aixs：记录所有需要显示的点线面的列表,观察者观察的中心位置,显示的视图大小,imshow：A,B角度，k,l转动参数，最后一个模式设置（-1为直接展示，0为暂停，1为导出图片),d：(1,0)为正交，比例为1，(200,100)表示观察者距离中心200，距观察者100处比例为1)
    if imshow[-1] == 0:
        A = imshow[0]
        B = imshow[1]
        k = imshow[2]
        l = imshow[3]
    elif imshow[-1] == 1:
        A = imshow[0]
        B = imshow[1]
        k = 1
        l = 0
    else:
        A = 90
        B = 0
        k = 1
        l = 0
    obj3d_list = sorted(
        obj3d_list,
        key=lambda obj3d: distance(obj3d, x, y, A, B, center, d),
        reverse=True,
    )  # 计算渲染顺序
    while True:
        img = np.zeros((y, x, 3), np.uint8)
        for obj3d in obj3d_list:
            if obj3d[-1] == "sphere":
                sphere(
                    img,
                    obj3d[0],
                    x / 2,
                    y / 2,
                    A,
                    B,
                    obj3d[1],
                    obj3d[2],
                    center,
                    obj3d[3],
                    d,
                )
            elif obj3d[-1] == "line":
                line(
                    img,
                    obj3d[0],
                    obj3d[1],
                    x / 2,
                    y / 2,
                    A,
                    B,
                    obj3d[2],
                    obj3d[3],
                    center,
                    obj3d[4],
                    d,
                )
            elif obj3d[-1] == "ring":
                if len(obj3d) == 5:
                    ring(
                        img,
                        obj3d[0],
                        x / 2,
                        y / 2,
                        A,
                        B,
                        obj3d[1],
                        obj3d[2],
                        center,
                        obj3d[3],
                        d,
                    )
                elif len(obj3d) == 6:
                    ring(
                        img,
                        obj3d[0],
                        x / 2,
                        y / 2,
                        A,
                        B,
                        obj3d[1],
                        obj3d[2],
                        center,
                        obj3d[3],
                        d,
                        obj3d[4],
                    )
            elif obj3d[-1] == "text":
                cv2.putText(
                    img,
                    obj3d[0],
                    obj3d[1],
                    cv2.FONT_HERSHEY_SIMPLEX,
                    obj3d[2],
                    obj3d[3],
                    obj3d[4],
                )
        A = (A + 180) % 360 - 180
        cv2.putText(
            img, str(A), (0, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1
        )
        cv2.putText(
            img, str(B), (0, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1
        )
        if not imshow[-1] == 0:
            cv2.imshow("img", img)
        key = cv2.waitKey(1) & 0xFF
        if key == 27:  # esc键退出
            break
        elif key == ord("d"):  # w,a,s,d,左右上下旋转
            A += k
            A = (A + 180) % 360 - 180
            k += 1
            l = 0
        elif key == ord("a"):
            A -= k
            A = (A + 180) % 360 - 180
            k += 1
            l = 0
        elif key == ord("w"):
            B -= k
            if B < -90:
                B = -90
            k += 1
            l = 0
        elif key == ord("s"):
            B += k
            if B > 90:
                B = 90
            k += 1
            l = 0
        else:
            l += 1
            # print(l)
            if l > 49:
                k = 1
                l = 0
        if imshow[-1] == 0:
            break
    if imshow[-1] == 0:
        return img
    elif imshow[-1] == 1:
        return A, B
    else:
        cv2.destroyAllWindows()
