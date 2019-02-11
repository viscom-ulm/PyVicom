import numpy as np
from pyrr import Vector3 as vec3


def load_dat(dat_file):
    raw_file = str(dat_file).replace(".dat", ".raw")
    try:
        dat = open(dat_file, "r")
    except IOError as ioe:
        print(ioe)

    meta_data = {}
    for line in dat.readlines():
        if line.strip():
            [key, value] = map(str.strip, line.split(":"))
            if key == "Resolution":
                meta_data[key] = vec3(list(map(float, value.split())))
            elif key == "SliceThickness":
                meta_data[key] = vec3(list(map(float, value.split())))
            else:
                meta_data[key] = value.strip()
    dat.close()
    raw_data = load_raw(raw_file=raw_file, format=meta_data["Format"])
    return meta_data, raw_data


def load_raw(raw_file, format):
    try:
        raw = open(raw_file, "rb")
    except IOError as ioe:
        print(ioe)
    raw_data = raw.read()
    raw.close()

    if format == "UCHAR":
        raw_data = np.frombuffer(raw_data, dtype=np.uint8) / 255.0
    if format == "USHORT":
        raw_data = np.frombuffer(raw_data, dtype=np.uint16) / 65535.0
    if format == "USHORT_12":
        raw_data = np.frombuffer(raw_data, dtype=np.uint16) / 4095.0  # TODO check if np.uint16 works here
    if format == "UINT":
        raw_data = np.frombuffer(raw_data, dtype=np.uint32) / 4294967295.0
    return raw_data


if __name__ == '__main__':
    load_dat("../media/uniform/nucleon.dat")
