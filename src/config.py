import yaml


class Config:
    def __init__(self, location: str):
        self.location = location
        self.data = self._load(location)

    @staticmethod
    def _load(location):
        with open(location) as file:
            return yaml.load(file, Loader=yaml.Loader)
