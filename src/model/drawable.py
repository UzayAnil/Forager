

class GameDrawable(object):
    """Super class for everything that we might draw"""
    def __init__(self, **kwargs):
        super(GameDrawable, self).__init__(**kwargs)
        self._picture = None

    def set_sprite(self, image):
        self._picture = image

    def get_sprite(self):
        return self._picture