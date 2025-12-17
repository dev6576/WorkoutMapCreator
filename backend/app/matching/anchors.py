def compute_anchor_bonus(route_endpoints, road_nodes):
    bonus = 0.0
    for p in route_endpoints:
        for r in road_nodes:
            if abs(p[0] - r[0]) < 0.0001:
                bonus += 0.5
    return bonus
