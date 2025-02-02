import random
import string


class StateHelper:
    @staticmethod
    def get_sate():
        return "".join(random.choices(string.ascii_letters + string.digits, k=16))
