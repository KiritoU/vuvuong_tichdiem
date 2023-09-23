import random
import string


class Utils:
    def get_response_data(self, data, success: int, message: str) -> dict:
        return {
            "success": success,
            "message": message,
            "data": data,
        }

    def generate_invation_code(self, code_length: int = 6) -> str:
        letters_and_digits = string.ascii_letters + string.digits

        return "".join(
            random.choice(letters_and_digits) for i in range(code_length)
        ).upper()


utils = Utils()
