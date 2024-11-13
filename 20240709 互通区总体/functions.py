import math

import ezdxf
import numpy as np
from ezdxf.math import Vec2
from shapely import LineString


def extract_entities(msp, layer_filter):
    """
    提取模型空间中指定图层的多段线、直线和圆弧。
    """
    entities = []
    for entity in msp:
        if entity.dxf.layer == layer_filter:
            if entity.dxftype() == 'LWPOLYLINE':
                points = [(p[0], p[1]) for p in entity.get_points()]
                entities.append(LineString(points))
            elif entity.dxftype() == 'LINE':
                start = (entity.dxf.start.x, entity.dxf.start.y)
                end = (entity.dxf.end.x, entity.dxf.end.y)
                entities.append(LineString([start, end]))
            elif entity.dxftype() == 'ARC':
                center = (entity.dxf.center.x, entity.dxf.center.y)
                radius = entity.dxf.radius
                start_angle = math.radians(entity.dxf.start_angle)
                end_angle = math.radians(entity.dxf.end_angle)
                entities.append(('ARC', center, radius, start_angle, end_angle))
    return entities


def line_circle_intersection(line, circle_center, radius):
    """
    计算直线和圆的交点
    """
    x1, y1, x2, y2 = line
    cx, cy = circle_center
    dx = x2 - x1
    dy = y2 - y1
    a = dx ** 2 + dy ** 2
    b = 2 * (dx * (x1 - cx) + dy * (y1 - cy))
    c = (x1 - cx) ** 2 + (y1 - cy) ** 2 - radius ** 2
    det = b ** 2 - 4 * a * c
    if det < 0:
        return []  # No intersection
    elif det == 0:
        t = -b / (2 * a)
        return [(x1 + t * dx, y1 + t * dy)]
    else:
        t1 = (-b + math.sqrt(det)) / (2 * a)
        t2 = (-b - math.sqrt(det)) / (2 * a)
        return [(x1 + t1 * dx, y1 + t1 * dy), (x1 + t2 * dx, y1 + t2 * dy)]


def is_point_on_arc(point, arc_center, radius, start_angle, end_angle):
    """
    检查点是否在圆弧上
    """
    px, py = point
    cx, cy = arc_center
    angle = math.atan2(py - cy, px - cx)
    if angle < 0:
        angle += 2 * math.pi
    if start_angle < end_angle:
        return start_angle <= angle <= end_angle
    else:
        return angle >= start_angle or angle <= end_angle


def find_intersections(dxf_path, line_start, line_end, layer_filter):
    # 打开DXF文件
    doc = ezdxf.readfile(dxf_path)
    msp = doc.modelspace()

    # 提取指定图层的实体
    entities = extract_entities(msp, layer_filter)

    # 创建shapely的直线对象
    input_line = LineString([line_start, line_end])
    input_line_coords = (line_start[0], line_start[1], line_end[0], line_end[1])

    # 找到交点
    intersections = []
    for entity in entities:
        if isinstance(entity, LineString):
            intersection = entity.intersection(input_line)
            if not intersection.is_empty:
                if intersection.geom_type == 'Point':
                    intersections.append((intersection.x, intersection.y))
                elif intersection.geom_type == 'MultiPoint':
                    for point in intersection.geoms:
                        intersections.append((point.x, point.y))
        elif entity[0] == 'ARC':
            arc_center, radius, start_angle, end_angle = entity[1:]
            points = line_circle_intersection(input_line_coords, arc_center, radius)
            for point in points:
                if is_point_on_arc(point, arc_center, radius, start_angle, end_angle):
                    intersections.append(point)

    return intersections


def get_width(dxf_name, cl, station, is_left, layer):
    cc = Vec2(cl.get_coordinate(station))
    ux = Vec2(cl.get_direction(station))
    uy = ux.rotate(0.5 * np.pi)
    pt = cc + uy * 50 if is_left else cc - uy * 50
    intersections = find_intersections(dxf_name, cc, pt, layer)
    res = []
    for o in intersections:
        if is_left and cl.get_side(o[0], o[1]) == -1:
            res.append(o)
        elif not is_left and cl.get_side(o[0], o[1]) == 1:
            res.append(o)
    if len(res) == 1:
        p0 = Vec2(res[0])
        dist = cc.distance(p0)
        return dist
    elif len(res) == 2:
        p0 = Vec2(res[0])
        p1 = Vec2(res[1])
        dist = max(cc.distance(p0), cc.distance(p1))
        return dist
    return None
