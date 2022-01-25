import logging

"""
LabYak class
"""
class LabYak:
    """
    A LabYak class that is used to create labyak (yak) objects.

    Args:
        name (str):  the name of the yak.
        age (float): the age of the yak.

    Attributes:
        name (str):                    the name of a yak, instance attribute.
        age (float):                   the age of a yak, instance attribute.
        milk_production (float):       the milk production of a yak, instance attribute.
        wool_production (int):         the wool production of a yak, instance attribute.
        age_last_shaved (float):       the last-shaved age of a yak, instance attribute.
        num_of_yaks (int):             the number of yaks created from this class, class attribute.
        age_of_death (float):          the age of death for a labyak, class attribute.

    Methods:
        yak_production:                the method called by a yak object with a given day T
                                       to generate all the information.
    """

    num_of_yaks = 0
    age_of_death = 10.0

    def __init__(self, name, age):
        # Make sure the initial age is valid
        assert age < LabYak.age_of_death and age > 0, "Invalid age! The initial age must be between 0 and {}!".format(LabYak.age_of_death)
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
        assert self.age < LabYak.age_of_death, "A LabYak dies the day it turns {}!".format(LabYak.age_of_death)
        milk = 0.0
        age_in_days = self.age * 100
        for _ in range(days):
            if age_in_days < LabYak.age_of_death*100:
                # When the yak is alive
                milk += 50-age_in_days*0.03
                age_in_days += 1
            else:
                # the yak dies
                break
        # assign the value to the labyak object
        self.milk_production = milk

    def _wool_production(self, days) -> None:
        """The computation of wool production and last-saved age for a labyak.
        At most every 8+D*0.01 days you can again shave a LabYak (D = age in days).
        """
        # Make sure the initial age is valid
        assert self.age < LabYak.age_of_death, "A LabYak dies the day it turns {}!".format(LabYak.age_of_death)
        day = 0
        wool = 0
        age_in_days = self.age * 100
        for _ in range(days):
            if age_in_days < LabYak.age_of_death*100:
                # When the yak is alive
                if day == 0 and age_in_days >= 1*100:
                    # at day 0 when the yak is at least 1 year old
                    wool += 1
                    age_last_shaved = age_in_days # update the age after shaving
                elif day > (8+ age_in_days*0.01) and age_in_days >= 1*100:
                    # at day 8+D*0.01 when the yak is at least 1 year old
                    wool += 1
                    age_last_shaved = age_in_days # update the age after shaving
                    day = 0 # date resets to 0 after shaving
                elif age_in_days < 1*100:
                    # continue if a yak is less than 1 year old
                    age_last_shaved = None
                    age_in_days += 1
                    continue
                day += 1
                age_in_days += 1
            else:
                # the yak dies
                break
        # assign the values to the labyak object
        self.wool_production = wool
        self.age_last_shaved = age_last_shaved/100 if age_last_shaved else None

    def _final_age(self, days) -> None:
        """
        Set the age in years of a yak after the given days.
        """
        final_age = (self._age*100+days)/100
        if final_age < LabYak.age_of_death:
            # set the age of the labyak
            self._age = final_age
        else:
            logging.warning("The age of {0} turns {1} and a LabYak dies at {2}!".format(self.name, self.age, LabYak.age_of_death))
            self._age = LabYak.age_of_death

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