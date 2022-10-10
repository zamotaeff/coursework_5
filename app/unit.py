from __future__ import annotations

from abc import ABC, abstractmethod
from random import randint
from typing import Optional

from app.classes import UnitClass
from app.equipment import Weapons, Armors


class BaseUnit(ABC):
    """
    Базовый класс юнита
    """
    def __init__(self, name: str, unit_class: UnitClass):
        """
        При инициализации класса Unit используем свойства класса UnitClass
        """
        self.name = name
        self.unit_class = unit_class
        self.hp = unit_class.max_health
        self.stamina = unit_class.max_stamina
        self.weapon = None
        self.armor = None
        self._is_skill_used = False

    @property
    def health_points(self) -> float:
        return round(self.hp, 1)

    @property
    def stamina_points(self) -> float:
        return round(self.stamina, 1)

    def equip_weapon(self, weapon: Weapons):
        self.weapon = weapon
        return f"{self.name} экипирован оружием {self.weapon.name}"

    def equip_armor(self, armor: Armors):
        self.armor = armor
        return f"{self.name} экипирован броней {self.armor.name}"

    def _count_damage(self, target: BaseUnit) -> float:
        damage = self.weapon.damage * self.unit_class.attack
        self.stamina -= self.weapon.stamina_per_hit

        if target.stamina >= target.armor.stamina_per_turn:
            target_armor = target.armor.defence * target.unit_class.armor
            target.stamina -= target.armor.stamina_per_turn
            damage -= target_armor

        return target.get_damage(damage)

    def get_damage(self, damage: float) -> Optional[float]:
        if damage > 0:
            self.hp -= damage
            return damage
        return 0

    @abstractmethod
    def hit(self, target: BaseUnit) -> str:
        """
        Этот метод будет переопределен ниже
        """
        pass

    def use_skill(self, target: BaseUnit) -> str:
        """
        Метод использования умения.
        Если умение уже использовано возвращаем строку
        Навык использован
        Если же умение не использовано тогда выполняем функцию
        self.unit_class.skill.use(user=self, target=target)
        и уже эта функция вернем нам строку, которая характеризует выполнение умения
        """
        if self._is_skill_used:
            return 'Навык использован.'

        self._is_skill_used = True
        return self.unit_class.skill.use(user=self, target=target)


class PlayerUnit(BaseUnit):

    def hit(self, target: BaseUnit) -> str:
        """
        Функция удар игрока:
        здесь происходит проверка достаточно ли выносливости для нанесения удара.
        Вызывается функция self._count_damage(target)
        а также возвращается результат в виде строки
        """
        if self.stamina < self.weapon.stamina_per_hit:
            return f"{self.name} попытался использовать {self.weapon.name}, но у него не хватило выносливости."

        damage = self._count_damage(target)
        if damage > 0:
            return f"{self.name} используя {self.weapon.name} пробивает {target.armor.name} " \
                   f"соперника и наносит {damage} урона."

        if damage == 0:
            return f"{self.name} используя {self.weapon.name} наносит удар, " \
                   f"но {target.armor.name} cоперника его останавливает."


class EnemyUnit(BaseUnit):

    def hit(self, target: BaseUnit) -> str:
        """
        Функция удар соперника
        должна содержать логику применения соперником умения
        (он должен делать это автоматически и только 1 раз за бой).
        Например, для этих целей можно использовать функцию randint из библиотеки random.
        Если умение не применено, противник наносит простой удар, где также используется
        функция _count_damage(target)
        """
        if not self._is_skill_used and self.stamina >= self.unit_class.skill.stamina and randint(0, 100) < 50:
            self.use_skill(target)

        stamina_to_hit = self.weapon.stamina_per_hit * self.unit_class.stamina
        if self.stamina < stamina_to_hit:
            return f"{self.name} попытался использовать {self.weapon.name}, но у него не хватило выносливости."

        damage = self._count_damage(target)
        if damage > 0:
            return f"{self.name} используя {self.weapon.name} пробивает {target.armor.name} " \
                   f"и наносит Вам {damage} урона."

        if damage == 0:
            return f"{self.name} используя {self.weapon.name} наносит удар, " \
                   f"но Ваш(а) {target.armor.name} его останавливает."
