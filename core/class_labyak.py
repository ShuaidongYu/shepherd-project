import logging

"""
LabYak class
"""
class LabYak:
    """
    The LabYak objects which contains the info of many yaks

    Args:
        name (str):  the name of the yak.
        age (float): the age of the yak.

    Attributes:
        name (str):                    the name of a yak, instance attribute
        age (float):                   the age of a yak, instance attribute
        milk_production (float):       the milk production of a yak, instance attribute
        wool_production (int):         the wool production of a yak, instance attribute
        age_last_shaved (float):       the last-shaved age of a yak
        num_of_yaks (int):             the number of yaks created from this class, class attribute
    """

    num_of_yaks = 0

    def __init__(self, name, age):
        # Make sure the initial age is valid
        assert age < 10.0 and age > 0, "Invalid age! The initial age must be between 0 and 10!"
        self.name = name
        self._age = age # update in _final_age method
        self.milk_production = 0.0
        self.wool_production = 0
        self.age_last_shaved = None
        LabYak.num_of_yaks += 1

    @property
    def age(self):
        return self._age

    @age.setter
    def age(self, value):
        raise AttributeError("Yak age is read-only")

    def __repr__(self) -> str:
        return "LabYak({}, {})".format(self.name, self.age)

    def __str__(self) -> str:
        return "A LabYak whose name is {} and age is {}".format(self.name, self.age)

    def _milk_production(self, days) -> None:
        """The computation of milk production for a labyak.
        Each day a LabYak produces 50-D*0.03 liters of milk (D = age in days).
        """
        # Make sure the initial age is valid
        assert self.age < 10.0, "A LabYak dies the day it turns 10!"
        milk = 0.0
        age_in_days = self.age * 100
        for _ in range(days):
            if age_in_days < 10*100: # When the LabYak is alive
                milk += 50-age_in_days*0.03
                age_in_days += 1
            else: # the labyak dies
                break
        # assign the value to the labyak object
        self.milk_production = milk

    def _wool_production(self, days) -> None:
        """The computation of wool production and last-saved age for a labyak.
        At most every 8+D*0.01 days you can again shave a LabYak (D = age in days).
        """
        # Make sure the initial age is valid
        assert self.age < 10.0, "A LabYak dies the day it turns 10!"
        day = 0
        wool = 0
        age_in_days = self.age * 100
        for _ in range(days):
            if age_in_days < 10*100: # When the LabYak is alive
                if day == 0 and age_in_days >= 1*100: # at day 0 when the yak is at least 1 year old
                    wool += 1
                    age_last_shaved = age_in_days # update the age after shaving
                elif day > (8+ age_in_days*0.01) and age_in_days >= 1*100: # at day 8+D*0.01 when the yak is at least 1 year old
                    wool += 1
                    age_last_shaved = age_in_days # update the age after shaving
                    day = 0 # date resets to 0 after shaving
                elif age_in_days < 1*100:
                    age_last_shaved = None
                    age_in_days += 1
                    continue
                day += 1
                age_in_days += 1
            else: # the labyak dies
                break
        # assign the values to the labyak object
        self.wool_production = wool
        self.age_last_shaved = age_last_shaved/100 if age_last_shaved else None

    def _final_age(self, days) -> None:
        """
        Set the age in years of a yak after the given days.
        """
        final_age = (self._age*100+days)/100
        if final_age < 10.0:
            # set the age of the labyak
            self._age = final_age
        else:
            logging.warning("The age of {0} turns 10.0 and a LabYak dies at 10!".format(self.name))
            self._age = 10.0

    def yak_production(self, days) -> tuple:
        """
        Compute the production of milk, wool and the age after the given days.

        Args:
            days (int): elapsed days

        Returns:
            a tuple of (milk, wool, age_last_shaved, age) after the elapsed days
        """
        if days < 1 or not isinstance(days, int):
            raise ValueError("Days should start with 1 and could not be a float number.")
        self._milk_production(days)
        self._wool_production(days)
        self._final_age(days)
        return self.milk_production, self.wool_production, self.age_last_shaved, self.age