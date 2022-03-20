# Import the arcade library for game commands
import arcade

# Set some constants for sizing
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 800
SCREEN_TITLE = 'Box Game'
SCALING = 0.5
GRAVITY = 1
PLAYER_JUMP_SPEED = 10

class BoxGame(arcade.Window):
    """ Be a box placing boxes
    Player starts on the bottom left
    Player can place boxes at their current position
    Player returns to original position when box is placed
    Player wins the game when the goal is reached"""

    def __init__(self,width,height,title):
        """Initialize game window
        """
        super().__init__(width,height,title)

        # Set up lists for sprites
        self.box_list = arcade.SpriteList()
        self.platform_list = arcade.SpriteList()
        self.all_sprites_list = arcade.SpriteList()

        # Our physics engine
        self.physics_engine = None

        self.setup()

    def setup(self):
        """Prep game for play
        """

        # Check if the goal has been reached
        self.gameWon = False

        # Set background color
        arcade.set_background_color(arcade.color.SPANISH_GRAY)

        # Set up stage
        self.set_stage()

        # Set up player
        self.player = arcade.Sprite("box_sprites/player_box.png",SCALING)
        self.player.left = 10
        self.player.bottom = self.floor.top + 5
        self.all_sprites_list.append(self.player)

        # Create physics engine
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player, gravity_constant=GRAVITY, walls=self.platform_list
        )

    def set_stage(self):
        """Set up the platforms and goal depening on level
        Note: Different levels not yet available"""

        # Set up floor
        self.floor = arcade.Sprite("box_sprites/floor.png",SCALING)
        self.floor.center_y = 0
        self.floor.center_x = SCREEN_WIDTH / 2
        self.platform_list.append(self.floor)
        self.all_sprites_list.append(self.floor)
        
        # Set up goal
        self.goal = arcade.Sprite("box_sprites/goal_flag.png",SCALING)
        self.goal.center_x = SCREEN_WIDTH - 100
        self.goal.bottom = SCREEN_HEIGHT - 250
        self.all_sprites_list.append(self.goal)

        # Set up platform
        self.platform = arcade.Sprite("box_sprites/platform.png",SCALING)
        self.platform.left = SCREEN_WIDTH -200
        self.platform.top = self.goal.bottom
        self.platform_list.append(self.platform)
        self.all_sprites_list.append(self.platform)

    def make_box(self,x,y):
        """Makes a box at the player's current position,
        as long as it's not where the player spawns
        """

        # Make a box
        box = arcade.Sprite("box_sprites/other_box.png",SCALING)
        box.center_x = x
        box.center_y = y

        # Reset player position
        self.player.left = 10
        self.player.bottom = self.floor.top + 5

        # Check if it's in the spawn area
        if box.left > self.player.right:
            self.box_list.append(box)
            self.platform_list.append(box)
            self.all_sprites_list.append(box)

    def on_key_press(self, symbol: int, modifiers: int):
        """Handle key presses
        Left/Right arrowkeys move left and right, respectively
        A/D also move left and right
        Up arrow and W jump
        Down and S place a block and reset player position
        R erases last block placed
        Q closes the game
        """
        # Make sure the game is not over
        if self.gameWon == False:
            # Handle left/right movement
            if symbol == arcade.key.A or symbol == arcade.key.LEFT:
                self.player.change_x = -3

            if symbol == arcade.key.D or symbol == arcade.key.RIGHT:
                self.player.change_x = 3

            # Handle jumping
            if symbol == arcade.key.W or symbol == arcade.key.UP:
                if self.physics_engine.can_jump():
                    self.player.change_y = PLAYER_JUMP_SPEED

            # Handle box making
            if symbol == arcade.key.S or symbol == arcade.key.DOWN:
                if self.player.change_y == 0 and self.player.bottom < SCREEN_HEIGHT:
                    self.make_box(self.player.center_x, self.player.center_y)

            # Undo last block
            if symbol == arcade.key.R:
                if len(self.box_list) > 0:
                    self.all_sprites_list[len(self.all_sprites_list) - 1].remove_from_sprite_lists()
                    # Reset player position
                    self.player.left = 10
                    self.player.bottom = self.floor.top + 5

        # Quit the game
        if symbol == arcade.key.Q:
            arcade.close_window()

        return super().on_key_press(symbol, modifiers)

    def on_key_release(self, symbol: int, modifiers: int):
        """Handle key releases
        Left/Right and A/D stop player horizontal movement
        """

        if symbol == arcade.key.A or symbol == arcade.key.LEFT:
            self.player.change_x = 0
        if symbol == arcade.key.D or symbol == arcade.key.RIGHT:
            self.player.change_x = 0
        
        return super().on_key_release(symbol, modifiers)

    def on_draw(self):
        """Draw the window
        """

        # Clear the screen and start drawing
        arcade.start_render()

        # Draw all sprites
        self.all_sprites_list.draw()

    def on_update(self, delta_time: float):
        """Update positions and statuses of game objects
        """

        self.all_sprites_list.update()
        self.physics_engine.update()

        # Make sure the player doesn't leave the screen
        if self.player.left < 0:
            self.player.left = 0
        if self.player.right > SCREEN_WIDTH:
            self.player.right = SCREEN_WIDTH

        if self.player.collides_with_sprite(self.goal):
            self.gameWon = True
            self.player.change_x = 0
            self.victoryText = arcade.Sprite("box_sprites/victory_text.png",SCALING)
            self.victoryText.center_x = SCREEN_WIDTH / 2
            self.victoryText.center_y = SCREEN_HEIGHT / 2
            self.all_sprites_list.append(self.victoryText)

        return super().on_update(delta_time)

# Main code entry point
if __name__ == "__main__":
    app = BoxGame(SCREEN_WIDTH,SCREEN_HEIGHT,SCREEN_TITLE)
    arcade.run()