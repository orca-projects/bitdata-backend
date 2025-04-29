import random
import string


class StateUtil:
    @staticmethod
    def get_sate():
        return "".join(random.choices(string.ascii_letters + string.digits, k=16))
