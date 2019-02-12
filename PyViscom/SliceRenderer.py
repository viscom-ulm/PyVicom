from PyViscom.Canvas import Canvas
from PyViscom.UniformGridVolume import UniformGridVolume, load_dat
from PyViscom.Solution import uniform_grid_volume_get_linear
import time
import glm


class SliceRenderer(object):
    def __init__(self):
        self.canvas = Canvas(512,512)

    def render(self, val, data):
        start = time.time()
        res = glm.vec2(self.canvas.width, self.canvas.height)
        for y in range(0, self.canvas.height):
            for x in range(0, self.canvas.width):
                screen_coord = glm.vec2(x, y) / glm.vec2(res - 1)
                vol_coord = glm.vec3(screen_coord.x, screen_coord.y, val)
                tmp = vol_coord[0]
                vol_coord[0] = vol_coord[2]
                vol_coord[2] = tmp

                color = uniform_grid_volume_get_linear(data=data.raw_data,
                                                       coord=vol_coord,
                                                       res=data.meta_data['Resolution'],
                                                       data_dim=data.meta_data['ObjectModel'])
                self.canvas.set_pixel(x, y, (color.x, color.y, color.z, color.w))

        end = time.time()
        print("time: " + str(end - start))
        self.canvas.draw()


if __name__ == '__main__':
    renderer = SliceRenderer()
    vol = UniformGridVolume()
    load_dat("../media/uniform/nucleon.dat", vol)
    while True:
        renderer.render(val=0.5, data=vol)
