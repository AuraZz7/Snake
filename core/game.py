from core.prepare import *
from core.utils import *
import random


class Snake(pg.sprite.Sprite):
    """
    Snake class containing all logic for the snake to move,
    grow in size and die.
    """
    def __init__(self):
        super().__init__()
        # Creating the body
        failed_creation = True
        while failed_creation:
            # Generating random coordinates for the head
            x = random.randrange(0, SCREEN_WIDTH, TILE_SIZE)
            y = random.randrange(0, SCREEN_HEIGHT, TILE_SIZE)
            # Resetting failed_creation each iteration
            failed_creation = False
            # Generating a random direction to start facing, and generate the body
            # behind the head, facing this direction.
            self.facing = random.choice(("left", "right", "up", "down"))
            self.body = [[x + i * TILE_SIZE, y] if self.facing == "left" else [x-i*TILE_SIZE, y] if self.facing == "right"
                         else [x, y+i*TILE_SIZE] if self.facing == "up" else [x, y-i*TILE_SIZE] for i in range(3)]
            self.rect = pg.Rect(self.body[0][0], self.body[0][1], TILE_SIZE, TILE_SIZE)

            # Multiple checks to ensure the body generates in a valid position.
            # It should not generate outside the map, or facing the wall.
            if self.body[0][0] == 0 and self.facing == "left"\
                    or self.body[0][0]+TILE_SIZE == SCREEN_WIDTH and self.facing == "right"\
                    or self.body[0][1] == 0 and self.facing == "up" \
                    or self.body[0][1]+TILE_SIZE == SCREEN_HEIGHT and self.facing == "down":
                failed_creation = True
            for part in self.body:
                if not (0 <= part[0] <= SCREEN_WIDTH-TILE_SIZE and 0 <= part[1] <= SCREEN_HEIGHT-TILE_SIZE):
                    failed_creation = True

        # Setting difficulty variable from the prepare.py value
        self.difficulty = difficulty

        # Variables to track the snake's state
        self.speed_counter = 0
        self.score = 0
        self.right = self.left = self.up = self.down = False

    def update(self):
        # Calling all methods to update the snake
        self.rect = pg.Rect(self.body[0][0], self.body[0][1], TILE_SIZE, TILE_SIZE)

        self.check_eating()
        self.move()
        self.update_empty_tiles()
        self.check_game_over()

    def move(self):
        """
        Moves the snake by one tile whenever the outermost if statement is True
        Also controls the speed of the movement dependent on fps and difficulty
        """
        # Increment speed counter to control speed of movement
        self.speed_counter += 1
        # If statement to control the speed of the snake's movement
        if (self.speed_counter % (fps // self.difficulty)) == 0 and self.speed_counter != 0:
            # Checking if the snake has started moving / game has begun
            if self.right or self.left or self.up or self.down:
                # Inserting a body piece at the head of the snake and removing the last body piece
                # Gives the effect of movement
                if self.right:
                    self.facing = "right"
                    self.body.insert(0, [self.body[0][0] + TILE_SIZE, self.body[0][1]])
                if self.left:
                    self.facing = "left"
                    self.body.insert(0, [self.body[0][0] - TILE_SIZE, self.body[0][1]])
                if self.down:
                    self.facing = "down"
                    self.body.insert(0, [self.body[0][0], self.body[0][1] + TILE_SIZE])
                if self.up:
                    self.facing = "up"
                    self.body.insert(0, [self.body[0][0], self.body[0][1] - TILE_SIZE])
                # Removing last body piece
                self.body.pop(-1)

    def check_eating(self):
        """
        Checks if the snake is eating an apple and grows the snake
        and generates a new apple if so.
        """
        collision = pg.sprite.spritecollide(self, game.apple_group, True)
        if collision:
            # Grow body and create new apple
            game.apple_group.add(Apple())
            self.grow()
            self.score += 1

    def grow(self):
        """
        Grows the snake body by adding a piece to the end of the snake.
        Depending on the direction, this piece will be added in a different place.
        """
        # Check if the x of the last 2 pieces are equal
        if self.body[-1][0] == self.body[-2][0]:
            # Check if last piece is below 2nd last piece
            if self.body[-1][1] > self.body[-2][1]:
                self.body.append([self.body[-1][0], self.body[-1][1] + TILE_SIZE])
            # Check if last piece is above 2nd last piece
            if self.body[-1][1] < self.body[-2][1]:
                self.body.append([self.body[-1][0], self.body[-1][1] - TILE_SIZE])
        # Check if the y of the last 2 pieces are equal
        if self.body[-1][1] == self.body[-2][1]:
            # Check if last piece is to the right of 2nd last piece
            if self.body[-1][0] > self.body[-2][0]:
                self.body.append([self.body[-1][0] + TILE_SIZE, self.body[-1][1]])
            # Check if last piece is to the left of 2nd last piece
            if self.body[-1][0] < self.body[-2][0]:
                self.body.append([self.body[-1][0] - TILE_SIZE, self.body[-1][1]])

    def check_game_over(self):
        """
        Checking if the snake has collided with any walls or itself, and ending
        the game if it has.
        """
        # Checking for wall collision
        if self.rect.top < 0 or self.rect.bottom > SCREEN_HEIGHT or self.rect.left < 0 or self.rect.right > SCREEN_WIDTH:
            game.game_over = True

        # Checking for body collision
        for part in self.body[1:]:
            if part == self.body[0]:
                game.game_over = True

    def update_empty_tiles(self):
        """
        NOT WORKING CURRENTLY.

        Updates the list of empty_tiles so that apples cannot generate within the snake's body
        """
        for i, (pos) in reversed(list(enumerate(empty_tiles))):
            for part in self.body:
                if pos == tuple(part):
                    pass

    def draw(self):
        """
        Draw the snake as well as red eyes at it's head
        """
        for i, part in enumerate(self.body):
            border_x, border_y = part[0]+(border-1), part[1]+(border-1)
            border_w = border_h = TILE_SIZE-2*(border-1)
            x, y = part[0]+border, part[1]+border
            w = h = TILE_SIZE-2*border
            pg.draw.rect(screen, "black", (border_x, border_y, border_w, border_h))
            pg.draw.rect(screen, "green", (x, y, w, h))
            # Drawing eyes
            for j in range(1, 3):
                if i == 0 and (self.facing in ("left", "right")):
                    pg.draw.circle(screen, "red", (part[0]+TILE_SIZE*(0.25 if self.facing == "left" else 0.75), part[1]+j*TILE_SIZE//3), 3)
                elif i == 0 and (self.facing in ("up", "down")):
                    pg.draw.circle(screen, "red", (part[0]+j*TILE_SIZE//3, part[1]+TILE_SIZE*(0.75 if self.facing == "down" else 0.25)), 3)


class Apple(pg.sprite.Sprite):
    def __init__(self):
        """
        Apple class to randomly generate an apple and draw it
        """
        # Randomly generates a position in the list of available positions
        super().__init__()
        index = random.randint(0, len(empty_tiles)-1)
        self.rect = pg.Rect((empty_tiles[index]), (TILE_SIZE, TILE_SIZE))

    def draw(self):
        """
        Draw the apple to the screen
        """
        border_x, border_y = self.rect.x+(border-1), self.rect.y+(border-1)
        border_w, border_h = self.rect.w-2*(border-1), self.rect.h-2*(border-1)
        x, y = self.rect.x+border, self.rect.y+border
        w, h = self.rect.w-2*border, self.rect.h-2*border
        pg.draw.rect(screen, "black", (border_x, border_y, border_w, border_h))
        pg.draw.rect(screen, "red", (x, y, w, h))


class Game(object):
    """
    Game class to control all game logic including updates, drawing and events
    """
    def __init__(self):
        """
        Initialise the snake, apple and any attributes.
        """
        self.game_over = False

        # Creating instances of the snake and apple
        self.snake = Snake()
        self.apple_group = pg.sprite.Group()
        self.apple_group.add(Apple())

    def update(self):
        """
        Updates any onscreen elements
        """
        global empty_tiles
        # Reset the empty tiles list to all available
        # tiles at the start of each frame
        empty_tiles = [(x, y) for x in range(0, SCREEN_WIDTH, TILE_SIZE)
                       for y in range(0, SCREEN_HEIGHT, TILE_SIZE)]

        # Only update the snake's position if the game is not over
        if not self.game_over:
            self.snake.update()

    def draw(self):
        """
        Draws all onscreen elements including the background, the snake
        and the apples. Also draws any text such as scores or game over text
        """
        # Fill the screen
        screen.fill("beige")
        # Draw the snake and apples
        self.snake.draw()
        for apple in self.apple_group:
            apple.draw()

        # Display the score in the top left if the game is not over
        if not self.game_over:
            score = get_font(36).render(f"Score: {self.snake.score}", True, "black")
            screen.blit(score, (0, 0))

        # If the game is over, draw relevant text to the user
        else:
            game_over_txt = get_font(48).render("Game over!", True, "red")
            screen.blit(game_over_txt, (SCREEN_WIDTH // 2 - game_over_txt.get_width() // 2,
                                        SCREEN_HEIGHT // 2 - game_over_txt.get_height()))
            score_txt = get_font(40).render(f"Score: {self.snake.score}", True, "black")
            screen.blit(score_txt, (SCREEN_WIDTH // 2 - score_txt.get_width() // 2,
                                    SCREEN_HEIGHT // 2 + game_over_txt.get_height() // 3))
            play_again_txt = get_font(40).render("Press space to play again", True, "black")
            screen.blit(play_again_txt, (SCREEN_WIDTH // 2 - play_again_txt.get_width() // 2,
                                         SCREEN_HEIGHT // 2 + play_again_txt.get_height()*2))

    def handle_events(self):
        for e in pg.event.get():
            if e.type == pg.KEYDOWN:
                if not self.game_over:
                    # Changing the snake direction depending on user input if the game is not over
                    if e.key in (pg.K_RIGHT, pg.K_d) and self.snake.facing != "left":
                        self.snake.right = True
                        self.snake.left = self.snake.down = self.snake.up = False
                    if e.key in (pg.K_LEFT, pg.K_a) and self.snake.facing != "right":
                        self.snake.left = True
                        self.snake.right = self.snake.down = self.snake.up = False
                    if e.key in (pg.K_DOWN, pg.K_s) and self.snake.facing != "up":
                        self.snake.down = True
                        self.snake.right = self.snake.left = self.snake.up = False
                    if e.key in (pg.K_UP, pg.K_w) and self.snake.facing != "down":
                        self.snake.up = True
                        self.snake.right = self.snake.left = self.snake.down = False
                else:
                    # If game is over then SPACE can be used to reset the game
                    if e.key == pg.K_SPACE:
                        self.__init__()


# Create an instance of the game
game = Game()
