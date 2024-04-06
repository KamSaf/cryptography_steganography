from typing import Iterable, Any
import numpy as np
from PIL import Image
from numpy._typing import NDArray


def bits_provider(message: str) -> Iterable[int]:
    """
        Generator yelding single bits of the message.

        Parameters:
        --------------------------------------------
        message: str => string message of which bits are yielded

        Returns:
        ---------------------------------------------
        Iterable[int] => single bits of given string
    """
    for char in message:
        bit_repr = str(format(ord(char), 'b'))
        if len(bit_repr) <= 8:
            bit_repr = str(format(ord(char), 'b')).rjust(8, '0')
            for bit in bit_repr:
                yield int(bit)


def chars_provider(pixel_red_values: Any) -> Iterable[str]:
    """
        Generator yielding single chars built from bits retrieved from image pixel data.

        Parameters:
        -----------------------------------------------
        pixel_red_values: Any => list of integer red color values of image pixels

        Returns:
        -----------------------------------------------
        Iterable[str] => single characters build from 8 bits of data

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


def clear_low_order_bits(pixels: NDArray) -> NDArray:
    """
        Function setting all pixels lowest red color value bits to 0.

        Parameters:
        -----------------------------------------------------
        pixels: NDArray => array of image pixels

        Returns:
        -----------------------------------------------------
        NDArray => array of pixels with altered binary values
    """
    for row in range(pixels.shape[0]):
        for col in range(pixels.shape[1]):
            pixels[row, col, 0] &= ~1  # &= ~1 means that all common bits of the value and ~1 are assigned
    return pixels


def create_image(message: str, input_file: str, output_file: str) -> None:
    """
        Function hiding text message into .jpg image file.

        Parameters:
        ---------------------------------------------------
        message: str => text to be hidden in image
        input_file: str => name/path to file in which text is to be hidden
        output_file: str => name/path for a created file with hidden message

    """
    input_img = Image.open(input_file)
    pixels = np.array(input_img)
    input_img.close()
    pixels = clear_low_order_bits(pixels)
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
        Function decoding hidden message from .jpg image file.

        Parameters:
        -----------------------------------------------
        input_file: str => name/path to a file from which message is to be retrieved

        Returns:
        str => retrieved hidden message

    """
    img = Image.open(input_file)
    result = ''.join(chars_provider(img.getdata(band=0)))  # band=0 means only red color is returned from getdata()
    img.close()
    return result


if __name__ == "__main__":
    pass
