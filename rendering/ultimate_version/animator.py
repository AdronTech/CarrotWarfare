from timing import now
from game import player, carrot, sprout
from rendering.constants import IMAGE_RESOURCE


class EntityAnimator:
    # loops if duration == 0
    def __init__(self, entity, current_animation="state_stand", frame_duration=125):

        self.entity = entity
        self.state = current_animation
        self.frame_duration = frame_duration
        self.start = now()

        if issubclass(type(entity), player.Player):
            self.name = "player"
        elif issubclass(type(entity), carrot.Carrot):
            self.name = "carrot"
        elif issubclass(type(entity), sprout.Sprout):
            self.name = "sprout"

        self.priority = 0
        if current_animation == "state_idle":
            self.priority = 1
        elif current_animation == "state_walk":
            self.priority = 2
        elif current_animation == "state_attack":
            self.priority = 3
        elif current_animation == "state_die":
            self.priority = 4

    def get_frame(self, looking_left: bool):

        if looking_left:
            dir = "left"
        else:
            dir = "right"

        index = int((now() - self.start) / self.frame_duration)
        if index > 3 or self.state == "state_stand":
            return None
        frame = IMAGE_RESOURCE["entities"][self.name + str(self.entity.alliance)][self.state][dir]["frame" + str(index)]
        return frame

    def set_animation(self, current_animation="state_stand", frame_duration=125):

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
            self.priority = priority
            self.state = current_animation
            self.frame_duration = frame_duration
            self.start = now()
