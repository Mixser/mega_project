import string


class Encipher(object):
    def __init__(self, key, alphabet=string.printable):
        self._key = key
        self._alphabet = alphabet

    def _encrypt_char(self, ch, i):
        raise NotImplementedError

    def _decrypt_char(self, ch, i):
        raise NotImplementedError

    def encode(self, msg):
        cipher = ''
        for i, ch in enumerate(msg):

            if ch not in self._alphabet:
                raise ValueError("Message has a character not a from of alphabet.")

            cipher += self._encrypt_char(ch, i)

        return cipher

    def decode(self, cipher):
        msg = ''
        for i, ch in enumerate(cipher):
            msg += self._decrypt_char(ch, i)

        return msg


class CaesarCipher(Encipher):
    def _encrypt_char(self, ch, i):
        encrypted_char_index = (self._alphabet.find(ch) + self._key) % len(self._alphabet)
        return self._alphabet[encrypted_char_index]

    def _decrypt_char(self, ch, i):
        decrypted_char_index = (self._alphabet.find(ch) - self._key) % len(self._alphabet)
        return self._alphabet[decrypted_char_index]


class VigenereCipher(Encipher):
    def _encrypt_char(self, ch, i):
        index = (self._alphabet.index(ch) + self._alphabet.index(self._key[i % len(self._key)])) % len(self._alphabet)
        return self._alphabet[index]

    def _decrypt_char(self, ch, i):
        index = (self._alphabet.index(ch) - self._alphabet.index(self._key[i % len(self._key)])) % len(self._alphabet)
        return self._alphabet[index]


class VernamCipher(Encipher):
    def _encrypt_char(self, ch, i):
        index = (self._alphabet.index(ch) ^ self._alphabet.index(self._key[i])) % len(self._alphabet)
        return self._alphabet[index]

    def _decrypt_char(self, ch, i):
        index = (self._alphabet.index(ch) ^ self._alphabet.index(self._key[i])) % len(self._alphabet)
        return self._alphabet[index]

    def encode(self, msg):
        if len(msg) != len(self._key):
            raise ValueError('Message must be same length as key.')

        return super(VernamCipher, self).encode(msg)

    def decode(self, cipher):
        if len(cipher) != len(self._key):
            raise ValueError('Message must be same length as key.')
        return super(VernamCipher, self).decode(cipher)


def test_cipher(msg, gen):
    cipher = gen.encode(msg)
    decoded_message = gen.decode(cipher)

    print repr("%s => %s => %s" % (msg, cipher, decoded_message))

    assert msg == decoded_message

if __name__ == '__main__':
    caesar = CaesarCipher(key=3)
    vigenere = VigenereCipher(key='lemon')
    vernam = VernamCipher(key='abcdebfdsasd')

    message = 'Hello, World'

    test_cipher(message, caesar)
    test_cipher(message, vigenere)
    test_cipher(message, vernam)






