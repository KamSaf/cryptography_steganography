from typing import Iterable
import numpy as np
from PIL import Image


def bits_provider(message) -> Iterable[int]:
    """
    """
    for char in message:
        bit_repr = str(format(ord(char), 'b'))
        if len(bit_repr) <= 8:
            bit_repr = str(format(ord(char), 'b')).rjust(8, '0')
            for bit in bit_repr:
                yield int(bit)


def chars_provider(pixel_red_values) -> Iterable[str]:
    """
    """
    b_str = ''
    for i, pixel_red_value in enumerate(pixel_red_values):
        if i != 0 and i % 8 == 0:
            if int(b_str, 2) == 0:
                break
            char = chr(int(b_str, 2))
            b_str = ''
            yield char
        b_str += str(format(pixel_red_value, 'b'))[-1]


def clear_low_order_bits(pixels) -> None:
    """
    """
    for row in range(pixels.shape[0]):
        for col in range(pixels.shape[1]):
            pixels[row, col, 0] &= ~1  # &= ~1 means that all common bits of the value and ~1 are assigned


def create_image(message, input_file, output_file) -> None:
    """
    """
    input_img = Image.open(input_file)
    pixels = np.array(input_img)
    input_img.close()
    clear_low_order_bits(pixels)
    if len(message) * 8 > pixels.shape[1]:
        raise Exception('Message is too long to save in given file')
    for i, bit in enumerate(bits_provider(message)):
        pass
        row = i // pixels.shape[1]
        col = i % pixels.shape[1]
        pixels[row, col][0] |= bit  # |= means sum of the bits first and second value
    img = Image.fromarray(pixels)
    img.save(output_file)
    img.close()


def decode_image(input_file: str) -> str:
    """
    """
    img = Image.open(input_file)
    result = ''.join(chars_provider(img.getdata(band=0)))  # band=0 means only red color is returned from getdata()
    img.close()
    return result
