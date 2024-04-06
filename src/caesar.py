
class CaesarCipher:
    BOUNDS = (65, 126)

    @staticmethod
    def __validate_data(text: str, shift: int | None = None) -> bool:
        """
            Function validating data given by user

            Parameters:
            ---------------------------------------------
            text: str => text
            shift: int => shift parameter in Caesar cipher

        """
        if not isinstance(text, str):
            return False
        if shift and not isinstance(shift, int):
            return False
        return True

    @staticmethod
    def cipher(text: str, shift: int) -> str:
        """
            Function which encrypts given text with a Caesar cipher
            using given shift parameter

            Parameters:
            ---------------------------------------------
            text: str => text to be ciphered
            shift: int => number of places each character is to be shifted

            Returns:
            ---------------------------------------------
            str => ciphered text

        """
        if not CaesarCipher.__validate_data(text=text, shift=shift):
            raise Exception('Invalid data')

        ciphered_text = []
        for char in text:
            if not CaesarCipher.BOUNDS[0] < ord(char) < CaesarCipher.BOUNDS[1]:
                ciphered_text.append(char)
                continue
            char = ord(char) + shift
            if char > CaesarCipher.BOUNDS[1]:
                char = (CaesarCipher.BOUNDS[0] - 1) + (char - CaesarCipher.BOUNDS[1])
            char = chr(char)
            ciphered_text.append(char)
        return ''.join(ciphered_text)

    @staticmethod
    def decipher(text: str, shift: int) -> str:
        """
            Function which decrypts given text encrypted from Caesar cipher
            using given shift parameter

            Parameters:
            ---------------------------------------------
            text: str => text to be deciphered
            shift: int => number of places each character was shifted

            Returns:
            ---------------------------------------------
            str => deciphered text
        """
        if not CaesarCipher.__validate_data(text=text, shift=shift):
            raise Exception('Invalid data')

        deciphered_text = []
        for char in text:
            if not CaesarCipher.BOUNDS[0] < ord(char) < CaesarCipher.BOUNDS[1]:
                deciphered_text.append(char)
                continue
            char = ord(char) - shift
            if char < CaesarCipher.BOUNDS[0]:
                char = CaesarCipher.BOUNDS[1] - (CaesarCipher.BOUNDS[0] - 1 - char)
            char = chr(char)
            deciphered_text.append(char)
        return ''.join(deciphered_text)


if __name__ == "__main__":
    pass
