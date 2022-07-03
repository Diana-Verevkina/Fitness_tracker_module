from dataclasses import dataclass, asdict
from typing import Dict, Type


@dataclass()
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    MESSAGE = ("Тип тренировки: {}; Длительность: {:.3f}; "
               "Дистанция: {:.3f}; Ср. скорость: {:.3f}; "
               "Потрачено ккал: {:.3f}")
    def get_message(self) -> str:
        return self.MESSAGE.format(*asdict(self).values())


class Training:
    """Базовый класс тренировки."""

    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    MINUTES: int = 60
    # Количество действий, длительность тренировки, вес спортсмена

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight


    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError()

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(type(self).__name__, self.duration,
                              self.get_distance(), self.get_mean_speed(),
                              self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""

    COEFF_MEAN_SPEED: int = 18
    COEFF_SPEED: int = 20

    def get_spent_calories(self) -> float:
        return ((self.COEFF_MEAN_SPEED * self.get_mean_speed()
                - self.COEFF_SPEED) * self.weight /
                self.M_IN_KM * self.duration * self.MINUTES)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    COEFF_WEIGHT_1: float = 0.035
    COEFF_WEIGHT_2: float = 0.029
    COEFF_SPEED: int = 2

    def __init__(self, action: int,
                 duration: float,
                 weight: float,
                 height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        return ((self.COEFF_WEIGHT_1 * self.weight
                + (self.get_mean_speed() ** self.COEFF_SPEED // self.height)
                * self.COEFF_WEIGHT_2 * self.weight)
                * self.duration * self.MINUTES)


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: float = 1.38
    COEFF_SPEED: float = 1.1
    COEFF_WEIGHT: int = 2

    def __init__(self, action: int, duration: float,
                 weight: float, length_pool: float,
                 count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_distance(self) -> float:
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        return (self.length_pool
            * self.count_pool / self.M_IN_KM
            / self.duration)

    def get_spent_calories(self) -> float:
        return (self.get_mean_speed() + self.COEFF_SPEED)\
            * self.COEFF_WEIGHT * self.weight


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    types_of_training: Dict[str, Type[Training]] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }

    if workout_type in types_of_training:
        return types_of_training[workout_type](*data)

    print('training not found')
    #не поняла, как вызвать аварийный возврат с исключением.
    #пробовала try - exept и raise


def main(training: Training) -> None:
    """Главная функция."""
    print(training.show_training_info().get_message())


if __name__ == '__main__':
    packages = {
        'SWM': [720, 1, 80, 25, 40],
        'RUN': [15000, 1, 75],
        'WLK': [9000, 1, 75, 180]
    }

    for workout_type, data in packages.items():
        main(read_package(workout_type, data))