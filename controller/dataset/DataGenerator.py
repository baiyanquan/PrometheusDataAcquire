import random

class DataGenerator:


    def __init__(self):
        pass

    @staticmethod
    def generate_random_data(min, max, num):
        list = []
        for i in range(num):
            list.append(random.uniform(min, max))

        return list
