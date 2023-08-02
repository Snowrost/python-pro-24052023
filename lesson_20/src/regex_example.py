import re


def main():
    test_tex = """Напишіть мені будь-ласка на email supervanyok@gmail.com, я буду чекати вашої відповіді"""
    print("Email: ", repr(parse_email(test_tex)))
    print("Is phone valid: ", is_phone_numer_valid("+447501071088"))
    print("Is phone valid: ", is_phone_numer_valid("+380508609143"))
    print("Is email valid: ", is_email_valid("name@gmail.com"))


def parse_email(text: str) -> str:
    pattern = r"""\w+@.+\.\w{2,4}"""
    matches = re.findall(pattern, text)
    return matches.pop()


def is_phone_numer_valid(phone_number: str) -> bool:
    pattern = r"^(\+44)\d{10}"
    return re.fullmatch(pattern, phone_number) is not None


def is_email_valid(email: str) -> str:
    pattern = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    return re.fullmatch(pattern, email) is not None


if __name__ == "__main__":
    main()
