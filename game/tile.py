class Tile:
    def __init__(self):
        self.entities = []

    def register(self, entity):
        self.entities.append(entity)

    def unregister(self, entity):
        if entity in self.entities:
            self.entities.remove(entity)
