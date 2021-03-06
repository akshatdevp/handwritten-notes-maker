import numpy as np
from .utils import *
import re

empty_chars = [' ', '\n', '\t']

#Draws on an image using provided parameters
#fill - color of ink used on the image
#space_width - width of ' ' character
#character_padding_x - each character is padded along x with this value
#character_padding_y - each character is padded along y with this value
class PageDrawer():
    def __init__(self, fill, space_width, character_padding_x, character_padding_y):
        self.fill = fill
        self.space_width = space_width
        self.character_padding_x = character_padding_x
        self.character_padding_y = character_padding_y

    def text(self, page, top, left, text, font, rotation=0, scale_x=1, scale_y=1):
        for char in text:
            if char == ' ':
                left += self.space_width
            else:
                im, bbox = imageFromText(char, font, self.character_padding_x, self.character_padding_y)
                image = np.array(im)
                image = scale_image(image, scale_x, scale_y)                
                image = rotate_image(image, rotation)
                image = image[:,:,0]
                image = 255 - image
                page = self.image(page, top+bbox[1], left, image, 254)
                left += im.width
        return page

    def image(self, page, top, left, image, searchColor):
        top = int(top)
        left = int(left)
        for r in range(image.shape[0]):
            for c in range(image.shape[1]):
                if r+top < page.shape[0] and c+left < page.shape[1] and image[r][c] <= searchColor:
                    page[r+top][c+left] = self.fill[:3]
        return page

    def textsize(self, text, font):
        front_spaces = 0
        l = len(text)
        while front_spaces < l and text[front_spaces] in empty_chars:
            front_spaces += 1
        if front_spaces == l:
            return (self.space_width*len(text), 1)
        else:
            back_spaces = 0
            while back_spaces > 0 and text[front_spaces] in empty_chars:
                back_spaces -= 1
            sz = imageFromText(text, font)[1][2:4]
            if sz == (0, 0, 0, 0):
                return (self.space_width, 1)
            return ((front_spaces+back_spaces)*self.space_width + sz[0], sz[1])