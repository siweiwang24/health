"""
Body measurement information.

Copyright 2020. Siwei Wang.
"""
from os import path
from math import log10, sqrt
from json import dump, load
import re
from numpy import inner             # type: ignore
from jsonschema import validate     # type: ignore


def report_bound(value, bounds, labels):
    """Report on bounds of values."""
    assert len(bounds) + \
        1 == len(labels), 'Length mismatch between bounds and labels.'
    for bound, label in zip(bounds, labels):
        if value < bound:
            return label
    return labels[-1]


def report_fat(fat_percent: float, gender: bool):
    """Report the fat percent bounds."""
    bounds = (6, 14, 18, 26) if gender \
        else (14, 21, 25, 32)
    labels = ('Essential Fat', 'Athlete', 'Fitness', 'Average', 'Obese')
    print(f'Category: {report_bound(fat_percent, bounds, labels)}')


class Body:
    """Stores information about user."""

    # Information from JSON.
    info: dict = dict()
    # JSON schema for validation.
    schema: dict = dict()
    # Name of the file.
    filename: str = ''
    # Rounding for display.
    rounding: int = 2
    # Height matching regex.
    height_pattern = re.compile(r'([0-9]+)\'([0-9]|1[01])\"')
    # Non-negative integer matching regex.
    integer_pattern = re.compile(r'[0-9]+')
    # Non-negative float matching regex.
    float_pattern = re.compile(r'(\.[0-9]+)|([0-9]+\.?[0-9]*)')
    # Activity level matching regex.
    activity_pattern = re.compile(r'[0-4]')

    def __init__(self, filename: str):
        """Initialize with JSON filename."""
        if path.splitext(filename)[1] != '.json':
            raise ValueError(f'{filename} is not a JSON file.')
        with open('schema.json', 'r') as template:
            self.schema = load(template)
        self.filename = filename
        if not path.isfile(filename):
            return
        with open(filename, 'r') as user:
            self.info = load(user)
        validate(self.info, self.schema)

    def __del__(self):
        """Write fields to file."""
        validate(self.info, self.schema)
        with open(self.filename, 'w') as user:
            dump(self.info, user, indent=2)

    def clear(self):
        """Clear all user information."""
        self.info.clear()
        print('All user data has been reset.')

    def __require_height(self) -> float:
        """Get user input for height."""
        if 'height' in self.info:
            return self.info['height']
        height = input('\tHeight (ft\'in\"): ')
        match = re.fullmatch(self.height_pattern, height)
        if not match:
            raise ValueError(f'{height} does not match height pattern.')
        feet = int(match.group(1))
        inches = int(match.group(2))
        validated_height: float = 2.54 * (12 * feet + inches)
        self.info.update({'height': validated_height})
        return validated_height

    def __require_weight(self) -> float:
        """Get user input for weight."""
        if 'weight' in self.info:
            return self.info['weight']
        weight = input('\tWeight (lb): ')
        if not re.fullmatch(self.float_pattern, weight):
            raise ValueError(f'{weight} does not match weight pattern.')
        validated_weight = 0.453592 * float(weight)
        self.info.update({'weight': validated_weight})
        return validated_weight

    def __require_gender(self) -> bool:
        """Get user input for gender."""
        if 'gender' in self.info:
            return self.info['gender']
        gender = input('\tGender (m/f): ')
        if gender not in ('m', 'f'):
            raise ValueError(f'{gender} does not match gender pattern.')
        validated_gender: bool = (gender == 'm')
        self.info.update({'gender': validated_gender})
        return validated_gender

    def __require_age(self) -> int:
        """Get user input for age."""
        if 'age' in self.info:
            return self.info['age']
        age = input('\tAge (years): ')
        if not re.fullmatch(self.integer_pattern, age):
            raise ValueError(f'{age} does not match age pattern.')
        validated_age = int(age)
        self.info.update({'age': validated_age})
        return validated_age

    def __require_activity(self) -> int:
        """Get user input for activity level."""
        if 'activity' in self.info:
            return self.info['activity']
        levels = ('Sedentary', 'Light', 'Moderate', 'Very', 'Extra')
        for index, level in enumerate(levels):
            print(f'\t{index}. {level}')
        activity = input('\tActivity level: ')
        if not re.fullmatch(self.activity_pattern, activity):
            raise ValueError(f'{activity} does not match activity pattern.')
        validated_activity = int(activity)
        self.info.update({'activity': validated_activity})
        return validated_activity

    def __require_circumference(self) -> dict:
        """Get user input for circumferences."""
        if 'circumference' in self.info:
            return self.info['circumference']
        neck = input('\tNeck circumference (cm): ')
        waist = input('\tWaist circumference (cm): ')
        hip = input('\tHip circumference (cm): ')
        for circ in (neck, waist, hip):
            if not re.fullmatch(self.integer_pattern, circ):
                raise ValueError(
                    f'{circ} does not match circumference pattern.')
        validated_circumference = {
            'neck': int(neck),
            'waist': int(waist),
            'hip': int(hip)
        }
        self.info.update({'circumference': validated_circumference})
        return validated_circumference

    def __require_skinfold(self) -> dict:
        """Get user input for skinfold measurements."""
        if 'skinfold' in self.info:
            return self.info['skinfold']
        abdominal = input('\tAbdominal skinfold (mm): ')
        suprailiac = input('\tSuprailiac skinfold (mm): ')
        tricep = input('\tTricep skinfold (mm): ')
        thigh = input('\tThigh skinfold (mm): ')
        for fold in (abdominal, suprailiac, tricep, thigh):
            if not re.fullmatch(self.integer_pattern, fold):
                raise ValueError(f'{fold} does not match skinfold pattern.')
        validated_skinfold = {
            'abdominal': int(abdominal),
            'suprailiac': int(suprailiac),
            'tricep': int(tricep),
            'thigh': int(thigh)
        }
        self.info.update({'skinfold': validated_skinfold})
        return validated_skinfold

    def bmi(self):
        """Display information about BMI."""
        height = self.__require_height()
        weight = self.__require_weight()
        bmi = 10000 * weight / (height**2)
        print(f'Body Mass Index: {round(bmi, self.rounding)}')
        bounds = (18.5, 25, 30)
        labels = ('Underweight', 'Normal', 'Overweight', 'Obese')
        print(f'Category: {report_bound(bmi, bounds, labels)}')

    def bai(self):
        """Display information about BAI."""
        height: float = self.__require_height()
        gender = self.__require_gender()
        age = self.__require_age()
        hip: int = self.__require_circumference()['hip']
        bai = 1000 * hip / (height * sqrt(height)) - 18
        print(f'Body Adiposity Index: {round(bai, self.rounding)}')
        if not 20 <= age < 80:
            print(f'Age {age} is out of category bounds.')
            return
        if 20 <= age < 40:
            bounds = (8, 21, 26) if gender else (21, 33, 39)
        elif 40 <= age < 60:
            bounds = (11, 23, 29) if gender else (23, 35, 41)
        else:
            bounds = (13, 25, 31) if gender else (25, 38, 43)
        labels = ('Underweight', 'Normal', 'Overweight', 'Obese')
        print(f'Category: {report_bound(bai, bounds, labels)}')

    def bmr(self):
        """Display information about BMR."""
        print('Method: Mifflin-St Jeor')
        height = self.__require_height()
        weight = self.__require_weight()
        gender = self.__require_gender()
        age = self.__require_age()
        activity = self.__require_activity()
        coefficients = (10, 6.25, -5, 1)
        values = (weight, height, age, 5 if gender else -161)
        base_bmr = inner(coefficients, values)
        print(f'Basal Metabolic Rate: {round(base_bmr, self.rounding)}')
        activity_multipliers = (1.2, 1.375, 1.55, 1.725, 1.9)
        kcal = base_bmr * activity_multipliers[activity]
        print(f'Daily kcal requirement: {round(kcal, self.rounding)}')

    def tape(self):
        """Display information about body fat using tape measurements."""
        print('Method: US Navy')
        height = self.__require_height()
        gender = self.__require_gender()
        circumference = self.__require_circumference()
        neck: float = circumference['neck']
        waist: float = circumference['waist']
        hip: float = circumference['hip']
        coefficients = (1.0324, -0.19077, 0.15456) if gender \
            else (1.29579, -0.35004, 0.221)
        values = (1, log10(waist - neck + (0 if gender else hip)),
                  log10(height))
        fat_percent: float = 495 / inner(coefficients, values) - 450
        print(f'Body Fat Percent: {round(fat_percent, self.rounding)}')
        report_fat(fat_percent, gender)

    def calipers(self):
        """Display information about body fat using caliper measurements."""
        print('Method: Jackson-Pollock 4-site')
        gender = self.__require_gender()
        age = self.__require_age()
        skinfold = self.__require_skinfold()
        skin_sum: int = sum(skinfold.values())
        coefficients = (0.29288, -0.0005, 0.15845, -5.76377) if gender \
            else (0.29669, -0.00043, 0.02963, 1.4072)
        values = (skin_sum, skin_sum**2, age, 1)
        fat_percent = inner(coefficients, values)
        print(f'Body Fat Percent: {round(fat_percent, self.rounding)}')
        report_fat(fat_percent, gender)
