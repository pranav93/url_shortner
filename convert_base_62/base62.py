from app.config import ALPHANUM


class Base62(object):
    alphanum = ALPHANUM

    def encode(self, url_id):
        """Encode a number in Base 62
        :param url_id: url_id to be converted
        :return: converted url_id
        """
        if url_id == 0:
            return self.alphanum[0]
        arr = []
        base = len(self.alphanum)
        while url_id:
            rem = url_id % base
            url_id /= base
            arr.append(self.alphanum[rem])
        arr.reverse()
        return ''.join(arr)

    def decode(self, url_hash):
        """Decode a Base 62 encoded string into the number
        :param url_hash: url_hash to be converted
        :return: converted url_hash
        """
        base = len(self.alphanum)
        str_len = len(url_hash)
        num = 0

        idx = 0
        for char in url_hash:
            power = (str_len - (idx + 1))
            num += self.alphanum.index(char) * (base ** power)
            idx += 1

        return num