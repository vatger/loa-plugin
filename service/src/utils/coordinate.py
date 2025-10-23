def coord_to_decimal(coord: str) -> float:
    negative = coord.startswith("-")
    coord = coord.lstrip("+-")

    if len(coord) == 6:  # ddmmss
        deg = int(coord[:2])
        min_ = int(coord[2:4])
        sec = int(coord[4:6])
    elif len(coord) == 7:  # dddmmss
        deg = int(coord[:3])
        min_ = int(coord[3:5])
        sec = int(coord[5:7])
    else:
        raise ValueError(f"Unexpected coordinate length: {coord}")

    dec = deg + min_ / 60 + sec / 3600
    return -dec if negative else dec
