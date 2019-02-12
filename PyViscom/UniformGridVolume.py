import numpy as np
import glm


class UniformGridVolume(object):
    def __init__(self):
        self.raw_data = None
        self.meta_data = None
        self.meta_data = None


def load_dat(dat_file, vol):
    raw_file = str(dat_file).replace(".dat", ".raw")
    with open(dat_file, "r") as dat:
        meta_data = {}
        for line in dat.readlines():
            if line.strip():
                [key, value] = map(str.strip, line.split(":"))
                if key == "Resolution":
                    [x,y,z] = list(map(int, value.split()))
                    meta_data[key] = glm.vec3(x,y,z)
                elif key == "SliceThickness":
                    [x,y,z] = list(map(float, value.split()))
                    meta_data[key] = glm.vec3(x,y,z)
                elif key == "ObjectModel":
                    if key == "I":
                        meta_data[key] = 1
                    elif key == "RG" or key == "XY":
                        meta_data[key] = 2
                    elif key == "RGB" or key == "XYZ":
                        meta_data[key] = 3
                    elif key == "RGBA" or key == "XYZW":
                        meta_data[key] = 4
                    else:
                        meta_data[key] = 1
                else:
                    meta_data[key] = value.strip()
        raw_data = load_raw(raw_file=raw_file, format=meta_data["Format"])
        vol.meta_data = meta_data
        vol.raw_data = raw_data


def load_raw(raw_file, format):
    with open(raw_file, "rb") as raw:
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
    vol = UniformGridVolume()
    load_dat("../media/uniform/nucleon.dat", vol)
