from dataclasses import dataclass, asdict, fields
from typing import Dict, Type


@dataclass()
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    MESSAGE = ("Тип тренировки: {training_type}; "
               "Длительность: {duration:.3f} ч.; "
               "Дистанция: {distance:.3f} км; "
               "Ср. скорость: {speed:.3f} км/ч; "
               "Потрачено ккал: {calories:.3f}.")

    def get_message(self) -> str:
        return self.MESSAGE.format(**asdict(self))

@dataclass()
class Training:
    """Базовый класс тренировки."""

    action: int
    duration: float
    weight: float
    LEN_STEP = 0.65
    M_IN_KM = 1000
    MINUTES = 60

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError(f"Вызван метод из "
                                  f"родительского класса "
                                  f"{type(self).__name__}")

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(type(self).__name__, self.duration,
                           self.get_distance(), self.get_mean_speed(),
                           self.get_spent_calories())


@dataclass()
class Running(Training):
    """Тренировка: бег."""

    COEFF_MEAN_SPEED = 18
    COEFF_SPEED = 20

    def get_spent_calories(self) -> float:
        return ((self.COEFF_MEAN_SPEED * self.get_mean_speed()
                - self.COEFF_SPEED) * self.weight
                / self.M_IN_KM * self.duration * self.MINUTES)

@dataclass()
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    action: int
    duration: float
    weight: float
    height: float
    COEFF_WEIGHT_1 = 0.035
    COEFF_WEIGHT_2 = 0.029
    SPEED_EXHIBITOR = 2

    def get_spent_calories(self) -> float:
        return ((self.COEFF_WEIGHT_1 * self.weight
                + (self.get_mean_speed()
                   ** self.SPEED_EXHIBITOR // self.height)
                * self.COEFF_WEIGHT_2 * self.weight)
                * self.duration * self.MINUTES)


@dataclass()
class Swimming(Training):
    """Тренировка: плавание."""

    action: int
    duration: float
    weight: float
    length_pool: float
    count_pool: int
    LEN_STEP = 1.38
    COEFF_SPEED = 1.1
    COEFF_WEIGHT = 2

    def get_distance(self) -> float:
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        return (self.length_pool
                * self.count_pool / self.M_IN_KM
                / self.duration)

    def get_spent_calories(self) -> float:
        return ((self.get_mean_speed() + self.COEFF_SPEED)
                * self.COEFF_WEIGHT * self.weight)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    types_of_training: Dict[str, Type[Training]] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }

    if workout_type not in types_of_training:
        raise ValueError(f"Значение {workout_type} не найдено в словаре")

    elif len(data) != len(fields(types_of_training[workout_type])):
        raise TypeError(f"Количество передаваемых аргументов не совпадает "
                        f"с количеством агрументов класса")

    return types_of_training[workout_type](*data)


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