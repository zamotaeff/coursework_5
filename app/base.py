from app.unit import BaseUnit


class BaseSingleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Arena(metaclass=BaseSingleton):
    STAMINA_PER_ROUND = 1
    player = None
    enemy = None
    game_is_running = False
    battle_result = None

    def start_game(self, player: BaseUnit, enemy: BaseUnit) -> None:
        self.player = player
        self.enemy = enemy
        self.game_is_running = True

    def _check_players_hp(self):

        if self.player.hp > 0 and self.enemy.hp > 0:
            return None # Продолжаем битву

        elif self.player.hp <= 0 and self.enemy.hp > 0:
            self.battle_result = 'Lose'

        elif self.player.hp > 0 and self.enemy.hp <= 0:
            self.battle_result = 'Win'

        elif self.player.hp <= 0 and self.enemy.hp <= 0:
            self.battle_result = 'Tie'

        return self._end_game()

    def _stamina_regeneration(self):

        if self.player.stamina + (self.STAMINA_PER_ROUND * self.player.unit_class.stamina) >= self.player.unit_class.max_stamina:
            self.player.stamina = self.player.unit_class.max_stamina
        else:
            self.player.stamina += (self.STAMINA_PER_ROUND * self.player.unit_class.stamina)

        if self.enemy.stamina + (self.STAMINA_PER_ROUND * self.enemy.unit_class.stamina) >= self.enemy.unit_class.max_stamina:
            self.enemy.stamina = self.enemy.unit_class.max_stamina
        else:
            self.enemy.stamina += (self.STAMINA_PER_ROUND * self.enemy.unit_class.stamina)

    def next_turn(self):
        result = self._check_players_hp()
        if result:
            return result

        self._stamina_regeneration()

        return self.enemy.hit(self.player)

    def _end_game(self) -> str:
        self._instances = {}
        self.game_is_running = False
        return self.battle_result

    def player_hit(self) -> str:
        result = self._check_players_hp()
        if result:
            return result

        result_by_player = self.player.hit(self.enemy)
        result_by_enemy = self.next_turn()
        return f"{result_by_player} {result_by_enemy}"

    def player_use_skill(self) -> str:
        result = self._check_players_hp()
        if result:
            return result

        result_by_player = self.player.use_skill(self.enemy)
        result_by_enemy = self.next_turn()
        return f"{result_by_player} {result_by_enemy}"
