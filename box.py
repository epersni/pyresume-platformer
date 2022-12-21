from sprite import Sprite

class Box(Sprite):
    def __init__(self, startx, starty):
        super().__init__("graphics/boxAlt.png", startx, starty)

    @staticmethod
    def get_size():
        box = Box(0, 0)
        rect = box.image.get_rect()
        return [rect.width, rect.height]

