from timing import now
from game import player, carrot, sprout
from rendering.constants import IMAGE_RESOURCE


class EntityAnimator:
    # loops if duration == 0
    def __init__(self, entity, current_animation="state_stand", frame_duration=125, duration=500):

        self.state = current_animation
        self.duration = duration
        self.done = False
        self.loop = duration == 0
        self.frame_duration = frame_duration
        self.start = now()

        if issubclass(type(entity), player.Player):
            self.name = "player" + str(entity.alliance)
            self.player = entity
        elif issubclass(type(entity), carrot.Carrot):
            self.name = "carrot" + str(entity.alliance)
        elif issubclass(type(entity), sprout.Sprout):
            self.name = "sprout" + str(entity.alliance)

        if current_animation == "state_plant" and self.player:
            self.state = "state_stand"
            self.player.hard_lock = IMAGE_RESOURCE["entities"]["player_generic"]["planting_locks"]["hard"]
            self.player.soft_lock = IMAGE_RESOURCE["entities"]["player_generic"]["planting_locks"]["soft"]
            return

        self.priority = 0
        if current_animation == "state_idle":
            self.priority = 1
        elif current_animation == "state_walk":
            self.priority = 2
        elif current_animation == "state_attack":
            self.priority = 3
        elif current_animation == "state_die":
            self.priority = 4

        if self.player:
            self.player.hard_lock = IMAGE_RESOURCE["entities"][self.name][current_animation]["hard_lock"]
            self.player.soft_lock = IMAGE_RESOURCE["entities"][self.name][current_animation]["soft_lock"]

    def get_frame(self, looking_left: bool):
        if (not self.loop) and (now() - self.start > self.duration):
            return None

        if self.state == "state_stand":
            return IMAGE_RESOURCE["entities"][self.name][self.state]["frame0"]

        if looking_left:
            dir = "left"
        else:
            dir = "right"

        index = int((now() - self.start) / self.frame_duration) % 4
        frame = IMAGE_RESOURCE["entities"][self.name][self.state][dir]["frame" + str(index)]
        return frame

    def set_animation(self, current_animation="state_stand", frame_duration=125, duration=500):

        if current_animation == "state_plant" and self.player:
            self.state = "state_stand"
            self.player.hard_lock = IMAGE_RESOURCE["entities"]["player_generic"]["planting_locks"]["hard"]
            self.player.soft_lock = IMAGE_RESOURCE["entities"]["player_generic"]["planting_locks"]["soft"]
            return

        priority = 0
        if current_animation == "state_idle":
            priority = 1
        elif current_animation == "state_walk":
            priority = 2
        elif current_animation == "state_attack":
            priority = 3
        elif current_animation == "state_die":
            priority = 4

        if priority > self.priority:
            if self.player:
                self.player.hard_lock = IMAGE_RESOURCE["entities"][self.name][current_animation]["hard_lock"]
                self.player.soft_lock = IMAGE_RESOURCE["entities"][self.name][current_animation]["soft_lock"]
            self.priority = priority
            self.state = current_animation
            self.duration = duration
            self.done = False
            self.loop = duration == 0
            self.frame_duration = frame_duration
            self.start = now()
