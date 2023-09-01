"""
Game View
"""
import math
import os

import arcade

from platformer.constants import *
from platformer.entities import Player, Robot, Zombie, Hammy0, Enemy
from platformer.views import View
from platformer.logger import log


class GameView(View):
    def __init__(self):
        """
        Initializer for the game
        """
        super().__init__()

        # Track the current state of what key is pressed
        self.left_pressed_p1 = False
        self.left_pressed_p2 = False
        self.right_pressed_p1 = False
        self.right_pressed_p2 = False
        self.up_pressed_p1 = False
        self.up_pressed_p2 = False
        self.down_pressed_p1 = False
        self.down_pressed_p2 = False
        self.shoot_pressed_p1 = False
        self.shoot_pressed_p2 = False
        self.jump_needs_reset_p1 = False
        self.jump_needs_reset_p2 = False

        # Our TileMap Object
        self.tile_map = None

        # Our Scene Object
        self.scene = None

        # Separate variable that holds the player sprite
        self.player_sprite_p1 = None
        self.player_sprite_p2 = None

        # Our 'physics' engine
        self.physics_engine_p1 = None
        self.physics_engine_p2 = None

        # A Camera that can be used for scrolling the screen
        self.camera = None

        # A Camera that can be used to draw GUI elements
        self.gui_camera = None

        self.end_of_map = 0

        # Keep track of the score
        self.score = 0

        # Shooting mechanics
        self.can_shoot_p1 = False
        self.can_shoot_p2 = False
        self.shoot_timer_p1 = 0
        self.shoot_timer_p2 = 0

        # The selected player
        self.selected_player_p1 = 1
        self.selected_player_p2 = 2

        # Load sounds
        self.collect_coin_sound = arcade.load_sound(":resources:sounds/coin1.wav")
        self.jump_sound = arcade.load_sound(":resources:sounds/jump1.wav")
        self.game_over = arcade.load_sound(":resources:sounds/gameover1.wav")
        self.shoot_sound = arcade.load_sound(":resources:sounds/hurt5.wav")
        self.hit_sound = arcade.load_sound(":resources:sounds/hit5.wav")

    def setup(self):
        """Set up the game here. Call this function to restart the game."""

        super().setup()

        # Track the current state of what key is pressed
        self.left_pressed_p1 = False
        self.left_pressed_p2 = False
        self.right_pressed_p1 = False
        self.right_pressed_p2 = False
        self.up_pressed_p1 = False
        self.up_pressed_p2 = False
        self.down_pressed_p1 = False
        self.down_pressed_p2 = False
        self.shoot_pressed_p1 = False
        self.shoot_pressed_p2 = False
        self.jump_needs_reset_p1 = False
        self.jump_needs_reset_p2 = False

        # Setup the Cameras
        self.camera = arcade.Camera(self.window.width, self.window.height)
        self.gui_camera = arcade.Camera(self.window.width, self.window.height)

        # Map name
        map_name = "assets/tiled_maps/test1.json"
        # map_name = ":resources:tiled_maps/map_with_ladders.json"


        # Layer Specific Options for the Tilemap
        layer_options = {
            LAYER_NAME_PLATFORMS: {
                "use_spatial_hash": True,
            },
            LAYER_NAME_MOVING_PLATFORMS: {
                "use_spatial_hash": True,
            },
            LAYER_NAME_LADDERS: {
                "use_spatial_hash": True,
            },
            LAYER_NAME_COINS: {
                "use_spatial_hash": True,
            },
        }

        # Load in TileMap
        self.tile_map = arcade.load_tilemap(map_name, TILE_SCALING, layer_options)

        # Parse static text from the tilemap
        self.static_text = list()
        for obj in self.tile_map.get_tilemap_layer('Text').tiled_objects:
            new_text = arcade.Text(
                obj.text,
                GLOBAL_SCALE * obj.coordinates[0],
                1600 - (GLOBAL_SCALE * obj.coordinates[1]),
                arcade.color.BLACK,
                obj.font_size,
                font_name=obj.font_family,
            )
            # print(new_text, new_text.x, new_text.y)
            new_text._start_x = new_text.x
            new_text._start_y = new_text.y
            self.static_text.append(new_text)

        # Initiate New Scene with our TileMap, this will automatically add all layers
        # from the map as SpriteLists in the scene in the proper order.
        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        # Keep track of the score
        self.score = 0

        # Shooting mechanics
        self.can_shoot_p1 = False
        self.can_shoot_p2 = False
        self.shoot_timer_p1 = 0
        self.shoot_timer_p2 = 0

        # Set up the player, specifically placing it at these coordinates.
        self.player_sprite_p1 = Player(
            character_number=self.selected_player_p1,
            center=(
                # self.tile_map.tiled_map.tile_size[0] * TILE_SCALING * MAP_WIDTH * PLAYER_START_X,
                # self.tile_map.tiled_map.tile_size[1] * TILE_SCALING * MAP_HEIGHT * PLAYER_START_Y
                300,
                200
            )
        )
        self.player_sprite_p2 = Player(
            character_number=self.selected_player_p2,
            center=(
                # self.tile_map.tiled_map.tile_size[0] * TILE_SCALING * MAP_WIDTH * PLAYER_START_X,
                # self.tile_map.tiled_map.tile_size[1] * TILE_SCALING * MAP_HEIGHT * PLAYER_START_Y
                350,
                200
            )
        )
        self.scene.add_sprite(LAYER_NAME_PLAYER, self.player_sprite_p1)
        self.scene.add_sprite(LAYER_NAME_PLAYER2, self.player_sprite_p2)

        # DEBUG
        # log(f"Window size: {self.window.width}x{self.window.height}")
        # log(f"{self.player_sprite._center=}")
        # log(f"{TILE_SCALING=}")
        # log(f"{PLAYER_START_X=}")
        # log(f"{PLAYER_START_Y=}")
        # log(f"{GRID_PIXEL_SIZE=}")

        # Calculate the right edge of the my_map in pixels
        self.end_of_map = self.tile_map.tiled_map.map_size.width * GRID_PIXEL_SIZE
        # breakpoint()

        # -- Enemies
        enemies_layer = self.tile_map.get_tilemap_layer('Enemies')

        for my_object in enemies_layer.tiled_objects:
            continue
            cartesian = self.tile_map.get_cartesian(
                my_object.coordinates[0], my_object.coordinates[1]
            )
            enemy_type = my_object.class_
            if enemy_type == "robot":
                enemy = Robot()
            elif enemy_type == "zombie":
                enemy = Zombie()
            elif enemy_type == "hammy0":
                enemy = Hammy0()
            else:
                raise Exception(f"Unknown enemy type '{enemy_type}'")
            enemy.center_x = math.floor(
                cartesian[0] * TILE_SCALING * self.tile_map.tile_width
            )
            enemy.center_y = math.floor(
                (cartesian[1] + 1) * (self.tile_map.tile_height * TILE_SCALING)
            )
            if "boundary_left" in my_object.properties:
                enemy.boundary_left = my_object.properties["boundary_left"]
            if "boundary_right" in my_object.properties:
                enemy.boundary_right = my_object.properties["boundary_right"]
            if "change_x" in my_object.properties:
                enemy.change_x = my_object.properties["change_x"]
            self.scene.add_sprite(LAYER_NAME_ENEMIES, enemy)

        # Add bullet spritelist to Scene
        self.scene.add_sprite_list(LAYER_NAME_BULLETS)

        # --- Other stuff
        # Set the background color
        if DEBUG:
            assert self.tile_map.tiled_map.background_color is not None
        if self.tile_map.tiled_map.background_color:
            arcade.set_background_color(self.tile_map.tiled_map.background_color)

        # Create the 'physics engine'
        self.physics_engine_p1 = arcade.PhysicsEnginePlatformer(
            self.player_sprite_p1,
            # platforms=self.scene.name_mapping[LAYER_NAME_MOVING_PLATFORMS],
            walls=self.scene.name_mapping[LAYER_NAME_PLATFORMS],
            gravity_constant=GRAVITY,
            # ladders=self.scene.name_mapping[LAYER_NAME_LADDERS],
            # walls=self.scene.name_mapping[LAYER_NAME_PLATFORMS],
        )

        self.physics_engine_p2 = arcade.PhysicsEnginePlatformer(
            self.player_sprite_p2,
            # platforms=self.scene.name_mapping[LAYER_NAME_MOVING_PLATFORMS],
            walls=self.scene.name_mapping[LAYER_NAME_PLATFORMS],
            gravity_constant=GRAVITY,
            # ladders=self.scene.name_mapping[LAYER_NAME_LADDERS],
            # walls=self.scene.name_mapping[LAYER_NAME_PLATFORMS],
        )

        # DEBUG
        walls = self.scene.name_mapping[LAYER_NAME_PLATFORMS]
        if not all(wall.hit_box for wall in walls) and DEBUG:
            raise ValueError("Not all walls have hit boxes.")

    def on_show_view(self):
        arcade.set_background_color(self.tile_map.background_color)

    def name_mapping(self, name: str):
        return self.scene.name_mapping.get(name, list())

    def on_draw(self):
        """Render the screen."""

        # Clear the screen to the background color
        arcade.start_render()

        # Activate the game camera
        self.camera.use()

        # Draw our Scene
        self.scene.draw()

        # Activate the GUI camera before drawing GUI elements
        self.gui_camera.use()

        # Draw our score on the screen, scrolling it with the viewport
        score_text = f"Score: {self.score}"
        # arcade.draw_text(
        #     score_text,
        #     25,
        #     600,
        #     arcade.csscolor.BLACK,
        #     18,
        # )

        # Draw stationary text defined in the tile map
        camx, camy = self.camera.position
        for text in self.static_text:
            # breakpoint()
            text.x = text._start_x - camx
            text.y = text._start_y - camy
            text.draw()

        # Draw hit boxes.
        # DEBUG
        # for wall in self.wall_list:
        #     wall.draw_hit_box(arcade.color.BLACK, 3)

    def process_keychange(self):
        self.process_keychange_p1()
        self.process_keychange_p2()

    def process_keychange_p1(self):
        """
        Called when we change a key up/down or we move on/off a ladder.
        """
        # Process up/down
        if self.up_pressed_p1 and not self.down_pressed_p1:
            if self.physics_engine_p1.is_on_ladder():
                self.player_sprite_p1.change_y = PLAYER_MOVEMENT_SPEED
            elif (
                self.physics_engine_p1.can_jump(y_distance=10)
                and not self.jump_needs_reset_p1
            ):
                self.player_sprite_p1.change_y = PLAYER_JUMP_SPEED
                self.jump_needs_reset_p1 = True
                arcade.play_sound(self.jump_sound)
        elif self.down_pressed_p1 and not self.up_pressed_p1:
            if self.physics_engine_p1.is_on_ladder():
                self.player_sprite_p1.change_y = -PLAYER_MOVEMENT_SPEED

        # Process up/down when on a ladder and no movement
        if self.physics_engine_p1.is_on_ladder():
            if not self.up_pressed_p1 and not self.down_pressed_p1:
                self.player_sprite_p1.change_y = 0
            elif self.up_pressed_p1 and self.down_pressed_p1:
                self.player_sprite_p1.change_y = 0

        # Process left/right
        if self.right_pressed_p1 and not self.left_pressed_p1:
            self.player_sprite_p1.change_x = PLAYER_MOVEMENT_SPEED
        elif self.left_pressed_p1 and not self.right_pressed_p1:
            self.player_sprite_p1.change_x = -PLAYER_MOVEMENT_SPEED
        else:
            self.player_sprite_p1.change_x = 0

    def process_keychange_p2(self):
        """
        Called when we change a key up/down or we move on/off a ladder.
        """
        # Process up/down
        if self.up_pressed_p2 and not self.down_pressed_p2:
            if self.physics_engine_p2.is_on_ladder():
                self.player_sprite_p2.change_y = PLAYER_MOVEMENT_SPEED
            elif (
                self.physics_engine_p2.can_jump(y_distance=10)
                and not self.jump_needs_reset_p2
            ):
                self.player_sprite_p2.change_y = PLAYER_JUMP_SPEED
                self.jump_needs_reset_p2 = True
                arcade.play_sound(self.jump_sound)
        elif self.down_pressed_p2 and not self.up_pressed_p2:
            if self.physics_engine_p2.is_on_ladder():
                self.player_sprite_p2.change_y = -PLAYER_MOVEMENT_SPEED

        # Process up/down when on a ladder and no movement
        if self.physics_engine_p2.is_on_ladder():
            if not self.up_pressed_p2 and not self.down_pressed_p2:
                self.player_sprite_p2.change_y = 0
            elif self.up_pressed_p2 and self.down_pressed_p2:
                self.player_sprite_p2.change_y = 0

        # Process left/right
        if self.right_pressed_p2 and not self.left_pressed_p2:
            self.player_sprite_p2.change_x = PLAYER_MOVEMENT_SPEED
        elif self.left_pressed_p2 and not self.right_pressed_p2:
            self.player_sprite_p2.change_x = -PLAYER_MOVEMENT_SPEED
        else:
            self.player_sprite_p2.change_x = 0

    def on_key_press(self, key, modifiers):
        self.on_key_press_p1(key, modifiers)
        self.on_key_press_p2(key, modifiers)

    def on_key_press_p1(self, key, modifiers):
        """Called whenever a key is pressed."""

        if key == arcade.key.W:
            self.up_pressed_p1 = True
        elif key == arcade.key.S:
            self.down_pressed_p1 = True
        elif key == arcade.key.A:
            self.left_pressed_p1 = True
        elif key == arcade.key.D:
            self.right_pressed_p1 = True
        elif key == arcade.key.SPACE:
            self.shoot_pressed_p1 = True
        elif key == arcade.key.ESCAPE:
            self.window.show_view(self.window.views["pause"])
        else:
            log(f"p1 unmapped key pressed: {key}")
            return

        self.process_keychange_p1()

    def on_key_press_p2(self, key, modifiers):
        """Called whenever a key is pressed."""

        if key == arcade.key.UP:
            self.up_pressed_p2 = True
        elif key == arcade.key.DOWN:
            self.down_pressed_p2 = True
        elif key == arcade.key.LEFT:
            self.left_pressed_p2 = True
        elif key == arcade.key.RIGHT:
            self.right_pressed_p2 = True
        elif key == arcade.key.RSHIFT:
            self.shoot_pressed_p2 = True
        else:
            log(f"p2 unmapped key pressed: {key}")
            return

        self.process_keychange_p2()

    def on_key_release(self, key, modifiers):
        self.on_key_release_p1(key, modifiers)
        self.on_key_release_p2(key, modifiers)

    def on_key_release_p1(self, key, modifiers):
        """Called when the user releases a key."""

        if key == arcade.key.W:
            self.up_pressed_p1 = False
            self.jump_needs_reset_p1 = False
        elif key == arcade.key.S:
            self.down_pressed_p1 = False
        elif key == arcade.key.A:
            self.left_pressed_p1 = False
        elif key == arcade.key.D:
            self.right_pressed_p1 = False
        elif key == arcade.key.SPACE:
            self.shoot_pressed_p1 = False
        else:
            log(f"p1 unmapped key released: {key}")
            return

        self.process_keychange_p1()

    def on_key_release_p2(self, key, modifiers):
        """Called when the user releases a key."""

        if key == arcade.key.UP:
            self.up_pressed_p2 = False
            self.jump_needs_reset_p2 = False
        elif key == arcade.key.DOWN:
            self.down_pressed_p2 = False
        elif key == arcade.key.LEFT:
            self.left_pressed_p2 = False
        elif key == arcade.key.RIGHT:
            self.right_pressed_p2 = False
        elif key == arcade.key.RSHIFT:
            self.shoot_pressed_p2 = False
        else:
            log(f"p2 unmapped key released: {key}")
            return

        self.process_keychange_p2()

    def center_camera_to_player(self, speed=0.2):
        if not self.player_sprite_p1.is_dead:
            self.center_camera_to_player_p1(speed)
        elif not self.player_sprite_p2.is_dead:
            self.center_camera_to_player_p2(speed)
        else:
            # TODO
            self.center_camera_to_player_p1(speed)

    def center_camera_to_player_p1(self, speed=0.2):
        screen_center_x = self.player_sprite_p1.center_x - (self.camera.viewport_width / 2)
        screen_center_y = self.player_sprite_p1.center_y - (
            self.camera.viewport_height / 2
        )
        if screen_center_x < 0:
            screen_center_x = 0
        if screen_center_y < 0:
            screen_center_y = 0
        player_centered = screen_center_x, screen_center_y

        self.camera.move_to(player_centered, speed)

    def center_camera_to_player_p2(self, speed=0.2):
        screen_center_x = self.player_sprite_p2.center_x - (self.camera.viewport_width / 2)
        screen_center_y = self.player_sprite_p2.center_y - (
            self.camera.viewport_height / 2
        )
        if screen_center_x < 0:
            screen_center_x = 0
        if screen_center_y < 0:
            screen_center_y = 0
        player_centered = screen_center_x, screen_center_y

        self.camera.move_to(player_centered, speed)

    def on_update(self, delta_time):
        """Movement and game logic"""

        # Move the player with the physics engine
        self.physics_engine_p1.update()
        self.physics_engine_p2.update()

        # Update animations
        if self.physics_engine_p1.can_jump():
            self.player_sprite_p1.can_jump = False
        else:
            self.player_sprite_p1.can_jump = True

        if self.physics_engine_p2.can_jump():
            self.player_sprite_p2.can_jump = False
        else:
            self.player_sprite_p2.can_jump = True

        if self.physics_engine_p1.is_on_ladder() and not self.physics_engine_p1.can_jump():
            self.player_sprite_p1.is_on_ladder = True
        else:
            self.player_sprite_p1.is_on_ladder = False
        self.process_keychange_p1()

        if self.physics_engine_p2.is_on_ladder() and not self.physics_engine_p2.can_jump():
            self.player_sprite_p2.is_on_ladder = True
        else:
            self.player_sprite_p2.is_on_ladder = False
        self.process_keychange_p2()

        if self.can_shoot_p1 and not self.player_sprite_p1.is_dead:
            if self.shoot_pressed_p1:
                # print(self.player_sprite_p1.position)
                arcade.play_sound(self.shoot_sound)
                bullet_p1 = arcade.Sprite(
                    ":resources:images/space_shooter/laserBlue01.png",
                    SPRITE_SCALING_LASER,
                    flipped_horizontally=self.player_sprite_p1.facing_direction == LEFT_FACING,
                )

                if self.player_sprite_p1.facing_direction == RIGHT_FACING:
                    bullet_p1.change_x = BULLET_SPEED
                else:
                    bullet_p1.change_x = -BULLET_SPEED

                bullet_p1.center_x = self.player_sprite_p1.center_x
                bullet_p1.center_y = self.player_sprite_p1.center_y

                self.scene.add_sprite(LAYER_NAME_BULLETS, bullet_p1)

                self.can_shoot_p1 = False
        else:
            self.shoot_timer_p1 += 1
            if self.shoot_timer_p1 == SHOOT_SPEED:
                self.can_shoot_p1 = True
                self.shoot_timer_p1 = 0

        if self.can_shoot_p2 and not self.player_sprite_p2.is_dead:
            if self.shoot_pressed_p2:
                arcade.play_sound(self.shoot_sound)
                bullet_p2 = arcade.Sprite(
                    ":resources:images/space_shooter/laserBlue01.png",
                    SPRITE_SCALING_LASER,
                    flipped_horizontally=self.player_sprite_p2.facing_direction == LEFT_FACING,
                )

                if self.player_sprite_p2.facing_direction == RIGHT_FACING:
                    bullet_p2.change_x = BULLET_SPEED
                else:
                    bullet_p2.change_x = -BULLET_SPEED

                bullet_p2.center_x = self.player_sprite_p2.center_x
                bullet_p2.center_y = self.player_sprite_p2.center_y

                self.scene.add_sprite(LAYER_NAME_BULLETS, bullet_p2)

                self.can_shoot_p2 = False
        else:
            self.shoot_timer_p2 += 1
            if self.shoot_timer_p2 == SHOOT_SPEED:
                self.can_shoot_p2 = True
                self.shoot_timer_p2 = 0

        # Update Animations
        self.scene.update_animation(
            delta_time,
            [
                LAYER_NAME_COINS,
                LAYER_NAME_BACKGROUND,
                LAYER_NAME_PLAYER,
                LAYER_NAME_PLAYER2,
                LAYER_NAME_ENEMIES,
            ],
        )

        # Update moving platforms, enemies, and bullets
        self.scene.update(
            [LAYER_NAME_MOVING_PLATFORMS, LAYER_NAME_ENEMIES, LAYER_NAME_BULLETS]
        )

        # See if the enemy hit a boundary and needs to reverse direction.
        for enemy in self.scene.get_sprite_list(LAYER_NAME_ENEMIES):
            if (
                enemy.boundary_right
                and enemy.right > enemy.boundary_right
                and enemy.change_x > 0
            ):
                enemy.change_x *= -1

            if (
                enemy.boundary_left
                and enemy.left < enemy.boundary_left
                and enemy.change_x < 0
            ):
                enemy.change_x *= -1

        # See if the moving wall hit a boundary and needs to reverse direction.
        for wall in self.scene.get_sprite_list(LAYER_NAME_MOVING_PLATFORMS):

            if (
                wall.boundary_right
                and wall.right > wall.boundary_right
                and wall.change_x > 0
            ):
                wall.change_x *= -1
            if (
                wall.boundary_left
                and wall.left < wall.boundary_left
                and wall.change_x < 0
            ):
                wall.change_x *= -1
            if wall.boundary_top and wall.top > wall.boundary_top and wall.change_y > 0:
                wall.change_y *= -1
            if (
                wall.boundary_bottom
                and wall.bottom < wall.boundary_bottom
                and wall.change_y < 0
            ):
                wall.change_y *= -1

        player_collision_list_p1 = arcade.check_for_collision_with_lists(
            self.player_sprite_p1,
            [
                self.scene.get_sprite_list(LAYER_NAME_COINS),
                self.scene.get_sprite_list(LAYER_NAME_ENEMIES),
            ],
        )
        player_collision_list_p2 = arcade.check_for_collision_with_lists(
            self.player_sprite_p2,
            [
                self.scene.get_sprite_list(LAYER_NAME_COINS),
                self.scene.get_sprite_list(LAYER_NAME_ENEMIES),
            ],
        )

        for bullet in self.scene.get_sprite_list(LAYER_NAME_BULLETS):
            hit_list = arcade.check_for_collision_with_lists(
                bullet,
                [
                    self.scene.get_sprite_list(LAYER_NAME_ENEMIES),
                    self.scene.get_sprite_list(LAYER_NAME_PLATFORMS),
                    self.scene.get_sprite_list(LAYER_NAME_MOVING_PLATFORMS),
                ],
            )

            if hit_list:
                bullet.remove_from_sprite_lists()

                for collision in hit_list:
                    sprite_list = self.scene.get_sprite_list(LAYER_NAME_ENEMIES)
                    enemies = [sprite for sprite in sprite_list if isinstance(sprite, Enemy)]
                    if enemies:
                        enemy = enemies[0]
                        assert isinstance(enemy, Enemy), f"{enemy=} is not an Enemy"

                        # The collision was with an enemy
                        enemy.health -= BULLET_DAMAGE

                        if enemy.health <= 0:
                            enemy.kill()
                            self.score += 100
                            log(f'Enemy killed: {enemy}')
                            collision.remove_from_sprite_lists()

                        # Hit sound
                        arcade.play_sound(self.hit_sound)

                return

            if (bullet.right < 0) or (
                bullet.left
                > (self.tile_map.width * self.tile_map.tile_width) * TILE_SCALING
            ):
                bullet.remove_from_sprite_lists()

        # Loop through each coin we hit (if any) and remove it
        for collision in player_collision_list_p1:

            if self.scene.get_sprite_list(LAYER_NAME_ENEMIES) in collision.sprite_lists:
                # player dies
                # arcade.play_sound(self.game_over)
                self.player_sprite_p1.hit_enemy = True
                self.player_sprite_p1.kill()
            else:
                # Figure out how many points this coin is worth
                if "Points" not in collision.properties:
                    print("Warning, collected a coin without a Points property.")
                else:
                    points = int(collision.properties["Points"])
                    self.score += points

                # Remove the coin
                collision.remove_from_sprite_lists()
                arcade.play_sound(self.collect_coin_sound)

        for collision in player_collision_list_p2:

            if self.scene.get_sprite_list(LAYER_NAME_ENEMIES) in collision.sprite_lists:
                # arcade.play_sound(self.game_over)
                self.player_sprite_p2.hit_enemy = True
                self.player_sprite_p2.kill()
            else:
                # Figure out how many points this coin is worth
                if "Points" not in collision.properties:
                    print("Warning, collected a coin without a Points property.")
                else:
                    points = int(collision.properties["Points"])
                    self.score += points

                # Remove the coin
                collision.remove_from_sprite_lists()
                arcade.play_sound(self.collect_coin_sound)


        if self.player_sprite_p1.is_dead and self.player_sprite_p2.is_dead:
            arcade.play_sound(self.game_over)
            self.window.show_view(self.window.views["game_over"])
            return

        # Position the camera
        self.center_camera_to_player()
