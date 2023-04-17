from dataclasses import dataclass, asdict
from typing import Dict, Type


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    message = ('Тип тренировки: {}; '
               'Длительность: {:.3f} ч.; '
               'Дистанция: {:.3f} км; '
               'Ср. скорость: {:.3f} км/ч; '
               'Потрачено ккал: {:.3f}.')

    def get_message(self) -> str:
        return self.message.format(*asdict(self).values())


class Training:
    """Базовый класс тренировки."""
    M_IN_KM: int = 1000
    LEN_STEP: float = 0.65
    MIN_IN_HOURS: int = 60

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
        raise NotImplementedError('Method isnt defined')

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79
    CALORIES_MEAN_SPEED_MULTIPLIER: int = 18
    """Тренировка: бег."""
    def __init__(self, action: int, duration: float, weight: float) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_spent_calories(self) -> float:
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER * self.get_mean_speed()
                 + self.CALORIES_MEAN_SPEED_SHIFT) * self.weight
                / self.M_IN_KM * self.duration * self.MIN_IN_HOURS)


class SportsWalking(Training):
    FIRST_COEFFICIENT: float = 0.035
    SECOND_COEFFICIENT: float = 0.029
    KMH_TO_MS: float = 0.278
    SM_TO_M: int = 100
    """Тренировка: спортивная ходьба."""
    def __init__(self, action: int, duration: float,
                 weight: float, height: float) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight
        self.height = height

    def get_spent_calories(self) -> float:
        return ((self.FIRST_COEFFICIENT * self.weight
                 + ((self.get_mean_speed() * self.KMH_TO_MS)**2
                    / (self.height / self.SM_TO_M))
                 * self.SECOND_COEFFICIENT * self.weight)
                * self.duration * self.MIN_IN_HOURS)


class Swimming(Training):
    SWIMMING_COEFFICIENT: float = 1.1
    LEN_STEP: float = 1.38
    CONST: int = 2
    """Тренировка: плавание."""
    def __init__(self, action: int, duration: float, weight: float,
                 length_pool: float, count_pool: int) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_distance(self) -> float:
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        return ((self.get_mean_speed() + self.SWIMMING_COEFFICIENT)
                * self.CONST * self.weight * self.duration)


def read_package(workout_type: str,
                 data: list[int]) -> Dict[str, Type[Training]]:
    """Прочитать данные полученные от датчиков."""
    dict_for_training = {'SWM': Swimming,
                         'RUN': Running,
                         'WLK': SportsWalking}
    if workout_type in dict_for_training:
        return dict_for_training[workout_type](*data)
    raise Exception(f'There is no such training as {workout_type}')


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
