from dataclasses import dataclass
from typing import List, Optional
from random import uniform
import marshmallow_dataclass
import marshmallow
import json


@dataclass
class Armors:
    id: int
    name: str
    defence: float
    stamina_per_turn: float


@dataclass
class Weapons:
    id: int
    name: str
    min_damage: float
    max_damage: float
    stamina_per_hit: float

    @property
    def damage(self) -> float:
        return uniform(self.min_damage, self.max_damage)


@dataclass
class EquipmentData:
    armors: list[Armors]
    weapons: list[Weapons]


class Equipment:

    def __init__(self):
        self.equipment = self._get_equipment_data()

    def get_weapon(self, weapon_name) -> Optional[Weapons]:
        for weapon in self.equipment.weapons:
            if weapon.name == weapon_name:
                return weapon
        return None

    def get_armor(self, armor_name) -> Optional[Armors]:
        for armor in self.equipment.armors:
            if armor.name == armor_name:
                return armor
        return None

    def get_weapons_names(self) -> list:
        return [weapon.name for weapon in self.equipment.weapons]

    def get_armors_names(self) -> list:
        return [armor.name for armor in self.equipment.armors]

    @staticmethod
    def _get_equipment_data() -> EquipmentData:
        with open("./data/equipment.json", encoding="utf-8") as equipment_file:
            data = json.load(equipment_file)
            equipment_schema = marshmallow_dataclass.class_schema(EquipmentData)
            try:
                return equipment_schema().load(data)
            except marshmallow.exceptions.ValidationError:
                raise ValueError
