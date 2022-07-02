class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self, training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        return f"Тип тренировки: {self.training_type}; " \
               f"Длительность: {format(self.duration, '.3f')} ч.; " \
               f"Дистанция: {format(self.distance, '.3f')} км; " \
               f"Ср. скорость: {format(self.speed, '.3f')} км/ч; " \
               f"Потрачено ккал: {format(self.calories, '.3f')}."


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    # Количество действий, длительность тренировки, вес спортсмена

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight
        pass

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        message = InfoMessage(self.__class__.__name__, self.duration,
                              self.get_distance(), self.get_mean_speed(),
                              self.get_spent_calories())
        return(message)


class Running(Training):
    """Тренировка: бег."""
    def __init__(self, action: int, duration: float, weight: float) -> None:
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        coeff_calorie_1 = 18
        coeff_calorie_2 = 20
        return (coeff_calorie_1 * self.get_mean_speed() - coeff_calorie_2) \
            * self.weight / self.M_IN_KM * self.duration * 60


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    def __init__(self, action: int,
                 duration: float,
                 weight: float,
                 height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        coeff_calorie_3 = 0.035
        coeff_calorie_4 = 0.029
        return (coeff_calorie_3 * self.weight
                + (self.get_mean_speed() ** 2 // self.height)
                * coeff_calorie_4 * self.weight) * \
            self.duration * 60


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38

    def __init__(self, action: int, duration: float,
                 weight: float, length_pool: float,
                 count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_distance(self) -> float:
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        return self.length_pool \
               * self.count_pool / self.M_IN_KM / self.duration

    def get_spent_calories(self) -> float:
        coeff_calorie_5 = 1.1
        coeff_calorie_6 = 2
        return (self.get_mean_speed() + coeff_calorie_5)\
            * coeff_calorie_6 * self.weight


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    types: dict[str, type[Training]] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking}

    if workout_type in types:
        return types[workout_type](*data)
    else:
        print('training not found')


def main(training: Training) -> None:
    """Главная функция."""
    info: InfoMessage = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = {
        'SWM': [720, 1, 80, 25, 40],
        'RUN': [15000, 1, 75],
        'WLK': [9000, 1, 75, 180]
    }

    for workout_type, data in packages.items():
        training = read_package(workout_type, data)
        main(training)