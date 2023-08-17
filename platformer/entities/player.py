from platformer.constants import LEFT_FACING, RIGHT_FACING
from platformer.entities.entity import Entity
from platformer.logger import log


class Player(Entity):
    """Player Sprite"""

    def __init__(self, character_number, center=None):

        if character_number == 1:
            folder = "assets/images/sprites/players/pook0"
            file_prefix = "character_pook0"
        else:
            raise ValueError(f"Unknown character number {character_number}")

        # Set up parent class
        super().__init__(folder, file_prefix)

        if center is not None:
            self._center = center
            self.center_x = center[0]
            self.center_y = center[1]
            log(f"Player center initialized at: ({self.center_x}, {self.center_y})")

        # Track our state
        self.jumping = False
        self.climbing = False
        self.is_on_ladder = False

    def update_animation(self, delta_time: float = 1 / 60):

        # Figure out if we need to flip face left or right
        if self.change_x < 0 and self.facing_direction == RIGHT_FACING:
            self.facing_direction = LEFT_FACING
        elif self.change_x > 0 and self.facing_direction == LEFT_FACING:
            self.facing_direction = RIGHT_FACING

        # Climbing animation
        if self.is_on_ladder:
            self.climbing = True
        if not self.is_on_ladder and self.climbing:
            self.climbing = False
        if self.climbing and abs(self.change_y) > 1:
            self.cur_texture += 1
            if self.cur_texture > 7:
                self.cur_texture = 0
        if self.climbing:
            self.texture = self.climbing_textures[self.cur_texture // 4]
            return

        # Jumping animation
        if self.change_y > 0 and not self.is_on_ladder:
            self.texture = self.jump_texture_pair[self.facing_direction]
            return
        elif self.change_y < 0 and not self.is_on_ladder:
            self.texture = self.fall_texture_pair[self.facing_direction]
            return

        # Idle animation
        if self.change_x == 0:
            self.texture = self.idle_texture_pair[self.facing_direction]
            return

        # Walking animation
        self.cur_texture += 1
        if self.cur_texture > 7:
            self.cur_texture = 0
        self.texture = self.walk_textures[self.cur_texture][self.facing_direction]
