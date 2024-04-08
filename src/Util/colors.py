class colors:
    def __init__(self):
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.RED = (255, 45, 0)

        self.flag = False

    def change_dark_mode(self):
        if not self.flag:
            self.BLACK = (0, 0, 0)
            self.WHITE = (70, 70, 70)
            self.flag = True
        else:
            self.BLACK = (0, 0, 0)
            self.WHITE = (255, 255, 255)
            self.flag = False
