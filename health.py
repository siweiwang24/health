"""
Health Calculator.

Copyright 2020. Siwei Wang.
"""
import re
from body import Body


def get_user_choice(choice_pattern) -> int:
    """Get user input on choice options."""
    raw = input('\nChoose an option: ')
    while not re.fullmatch(choice_pattern, raw):
        print(f'{raw} does not match option pattern.')
        raw = input('Choose an option: ')
    return int(raw)


def main():
    """Run health script."""
    body = Body('user.json')
    options = ('Save and Quit',
               'Reset Data',
               'Body Mass Index',
               'Body Adiposity Index',
               'Basal Metabolic Rate',
               'Fat Percent (Tape Measure)',
               'Fat Percent (Calipers)')
    func = (body.clear, body.bmi, body.bai,
            body.bmr, body.tape, body.calipers)
    choice_pattern = re.compile(f'[0-{len(options) - 1}]')
    for index, option in enumerate(options):
        print(f'{index}. {option}')
    while True:
        choice = get_user_choice(choice_pattern)
        if choice == 0:
            break
        try:
            func[choice - 1]()
        except ValueError as err:
            print(f'Error: {err}')
            continue


if __name__ == '__main__':
    main()
