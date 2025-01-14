from PIL import Image, ImageTk

class Card:
    def __init__(self, image_path):
        self.image_path = image_path
        self.image = None

    def load_image(self, size=(100, 100)):
        img = Image.open(self.image_path)
        img.thumbnail(size)
        self.image = ImageTk.PhotoImage(img)
        return self.image
