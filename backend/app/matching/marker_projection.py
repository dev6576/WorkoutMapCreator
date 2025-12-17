def project_point_to_polyline(point, polyline):
    closest = None
    min_dist = float("inf")

    for p in polyline:
        d = abs(point[0] - p[0]) + abs(point[1] - p[1])
        if d < min_dist:
            min_dist = d
            closest = p

    return closest
