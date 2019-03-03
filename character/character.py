from . import (
    abilities, alignments, backgrounds, bonds, classes, flaws, ideals, items,
    levels, races
)


class Character(object):

    def __init__(
            self,
            race: races.BaseRace,
            class_: classes.BaseClass,
            ability: abilities.BaseAbility,
            alignment: alignments.BaseAlignment,
            ideal: ideals.BaseIdeal,
            bond: bonds.BaseBond,
            flaw: flaws.BaseFlaw,
            background: backgrounds.BaseBackground,
            inventory: items.BaseItem,
            level: levels.BaseLevel
    ):
        super(Character, self).__init__()
        self.race = race
        self.class_ = class_
        self.ability = ability
        self.alignment = alignment
        self.ideal = ideal
        self.bond = bond
        self.flaw = flaw
        self.background = background
        self.inventory = inventory
        self.level = level
