
class Card():

    def __init__(self, path, row=None, col=None):
        self.path = path
        self.row = row
        self.col = col
        self.coords = (row, col)

    def set_coords(self, coords):
        self.coords = coords

