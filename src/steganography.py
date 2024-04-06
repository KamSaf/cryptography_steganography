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
        row = i // pixels.shape[1]
        col = i % pixels.shape[1]
        pixels[row, col][0] |= bit  # |= means sum of the bits first and second value
    img = Image.fromarray(pixels)
    img.save(output_file)
    img.close()


def chars_provider(pixel_red_values) -> Iterable[str]:
    ascii_value = 0
    for i, pixel_red_value in enumerate(pixel_red_values):
        ascii_value_bit_position = 7 - i % 8
        if pixel_red_value & 1:
            ascii_value |= 1 << ascii_value_bit_position
        if ascii_value_bit_position == 0:
            char: str = chr(ascii_value)
            if not char.isprintable() and char != '\n':
                return

            yield char

            ascii_value = 0


def decode_image(input_file: str) -> str:
    """
    """
    img = Image.open(input_file)
    result = ''.join(chars_provider(img.getdata(band=0)))  # band=0 means only red color is returned from getdata()
    img.close()
    return result


# message = """Unless you have a strong reason and know what you're doing, you should use bitwise operators only for controlling bits. Its too easy to get it wrong otherwise. In most cases, youll want to pass integers as arguments to the bitwise operators."""

message = 'there'

create_image(message=message, input_file='file.png', output_file='file.png')

print(decode_image('file.png'))
