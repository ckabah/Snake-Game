import pygame
from pygame.locals import *
import time
import random
from settings import *


class Apple:
    def __init__(self, parent_surface) -> None:
        """
        Init Apple class.

        Parameters
        ----------
        parent_surface : pygame Surface
            The whole screen of SnakeGame class
        
        """
        self.parent_surface = parent_surface
        self.image = pygame.image.load('resources/apple.png')  # load apple image in png.

        # Initial position (x, y) of apple.
        self.x = random.randint(0, WINDOW_SIZE_X//MOVE_SIZE - 5)*MOVE_SIZE
        self.y = random.randint(0, WINDOW_SIZE_Y//MOVE_SIZE - 5)*MOVE_SIZE

    def move(self):
        """To change apple position in main surface."""
        self.x = random.randint(0, (WINDOW_SIZE_X//MOVE_SIZE - 5))*MOVE_SIZE
        self.y = random.randint(0, (WINDOW_SIZE_Y//MOVE_SIZE - 5))*MOVE_SIZE
        
    def draw(self):
        """To put apple in main screen"""
        self.parent_surface.blit(self.image, (self.x, self.y))


class Snake:
    def __init__(self, parent_surface, length) -> None:
        """
        initialise Snake class.

        Parameters
        ----------
        parent_surface: pygame Surface
            The whole screen of SnakeGame class
        length: int
            initial length of snake.
        """
        self.length = length
        self.parent_surface = parent_surface

        # Load different directions of snake head image.
        self.head_right = pygame.image.load('resources/head_right.png')
        self.head_left = pygame.image.load('resources/head_left.png')
        self.head_up = pygame.image.load('resources/head_up.png')
        self.head_down = pygame.image.load('resources/head_down.png')

        # Load body image of snake.

        self.block = pygame.image.load('resources/body.png').convert()

        # Finally load queue image of snake.
        self.queue = pygame.image.load('resources/queue.png')

        # initial lists of snake positions.
        self.x = [START_X]*length
        self.y = [START_Y]*length

        # Initial direction of snake.
        self.direction = 'right'
        # Find last positions of value in list.
        self.last_x = self.x[len(self.x)//2]
        self.last_y = self.x[len(self.x)//2]

    def increase_length(self, value):
        """
        To increase snake length by value pass in parameter.

        Parameters
        ----------
        value: int
            This value must be > 0, it's used to increase snake length.

        """
        self.length += int(value)
        # Just append some number in list x and y to increase their length.
        # I use -1 here, but we can use 0. That's not the best solution, but it works for this small game.
        for i in range(value):
            self.x.append(-1)
            self.y.append(-1)
        
    def draw(self):
        """To put apple in main screen"""
        self.parent_surface.fill(BACKGROUND_COLOR)

        # append head
        
        if self.direction == 'up':
            self.parent_surface.blit(self.head_up, (self.x[0], self.y[0]))
        elif self.direction == 'down':
            self.parent_surface.blit(self.head_down, (self.x[0], self.y[0]))
        elif self.direction == 'right':
            self.parent_surface.blit(self.head_right, (self.x[0], self.y[0]))
        else:
            self.parent_surface.blit(self.head_left, (self.x[0], self.y[0]))

        # append body
        if self.length > 2:
            for i in range(1, self.length-1):
                self.parent_surface.blit(self.block, (self.x[i], self.y[i]))

        # append queue
        self.parent_surface.blit(self.queue, (self.x[-1], self.y[-1]))

    def walk(self):
        """To move the snake in screen."""
        for i in range(self.length - 1, 0, -1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]
        if self.direction == 'up':
            self.y[0] -= MOVE_SIZE
        if self.direction == 'down':
            self.y[0] += MOVE_SIZE
        if self.direction == 'right':
            self.x[0] += MOVE_SIZE
        if self.direction == 'left':
            self.x[0] -= MOVE_SIZE

        # After each move, we call draw method to reload snake in screen.
        self.draw()

    def move_left(self):
        """ Change direction to right"""
        if self.direction != 'right':
            self.direction = 'left'

    def move_right(self):
        """ Change direction to left"""
        if self.direction != 'left':
            self.direction = 'right'

    def move_up(self):
        """ Change direction to down"""
        if self.direction != 'down':
            self.direction = 'up'

    def move_down(self):
        """ Change direction to up"""
        if self.direction != 'up':
            self.direction = 'down'


def is_collision(x1, y1, x2, y2):
    """Check collision of two points"""
    if (x1 >= x2) and (x1 < x2 + SIZE):
        if (y1 >= y2) and (y1 < y2 + SIZE):
            return True
    return False


class SnakeGame:
    def __init__(self) -> None:
        """
        Initialise SnakeGame class. It initialises pygame, create a new surface whit  (WINDOW_SIZE_X, WINDOW_SIZE_Y).
        Create new instance of Apple and Snake and load them in game  surface through their draw method.
        Initialise score, best_core and pause attributes.
        """
        pygame.init()
        self.surface = pygame.display.set_mode((WINDOW_SIZE_X, WINDOW_SIZE_Y))
        pygame.mixer.init()
        self.surface.fill(BACKGROUND_COLOR)
        self.snake = Snake(self.surface, 2)
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()
        self.score: int = 0
        self.best_score: int = 0
        self.pause: bool = False
        self.start_time = ...

        # Find best core BEST_SCORE_PATH file.
        with open(BEST_SCORE_PATH, 'r') as f:
            self.best_score = int(f.read())

    @staticmethod
    def play_sound(sound_name: str):
        """
        Play a given Sound.

        Parameters
        ----------
        sound_name: str
            It's the sound file name
        """
        sound = pygame.mixer.Sound(f'resources/{sound_name}')
        pygame.mixer.Sound.play(sound)

    @staticmethod
    def font(font_size: int = FONT_SIZE):
        """Return a pygame font."""
        return pygame.font.SysFont('arial', font_size)

    def display_position(self):
        """ Display Snake position in game surface. """
        position = self.font().render(f'x: {self.snake.x[0]}, y: {self.snake.y[0]}', True, PRIMARY_COLOR)
        self.surface.blit(position, (600, 10))

    def display_time(self):
        """ Display time in game surface."""
        timer = self.font().render(f'Time: {time.time() - self.start_time}', True, PRIMARY_COLOR)
        self.surface.blit(timer, (200, 10))

    def display_score(self):
        """ Display time in game surface."""
        score = self.font().render(f'Best score: {self.best_score}  Score: {self.score}', True, PRIMARY_COLOR)
        self.surface.blit(score, (800, 10))

    def game_over(self):
        """
        The Game over Screen, it's displays message when game over conditions satisfied.
        """
        self.surface.fill(BACKGROUND_COLOR)
        line1 = self.font(FONT_MEDIUM).render(
            f'Game Over !!! Your Score: {self.score}  Best score: {self.best_score}', True, PRIMARY_COLOR
        )
        text_rect1 = line1.get_rect(center=(WINDOW_SIZE_X/2, WINDOW_SIZE_Y/2))
        self.surface.blit(line1, text_rect1)
        line2 = self.font(FONT_MEDIUM).render(
            'To play again press < Enter >  Or < Escape > to exit', True,  SECOND_COLOR
        )
        text_rect2 = line2.get_rect(center=(WINDOW_SIZE_X/2, WINDOW_SIZE_Y/2+50))
        self.surface.blit(line2, text_rect2)

        # Update best score
        if self.score > self.best_score:
            with open(BEST_SCORE_PATH, 'w') as f:
                f.write(str(self.score))
        pygame.display.flip()

    def play(self):
        """Play game method, it's allow user to play game by calling all functional method"""
        self.snake.walk()
        self.apple.draw()
        self.display_score()
        self.display_position()
        self.display_time()
        pygame.display.flip()

        # snake colliding with apple
        if is_collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            self.play_sound('eat.mp3')
            # If the snake is too close of surface limit : increase snake length by 2 else increase by 1.
            if ((self.apple.x <= SIZE or self.apple.x >= WINDOW_SIZE_X - SIZE) or
                    (self.apple.y <= SIZE or self.apple.y >= WINDOW_SIZE_Y - SIZE)):
                self.snake.increase_length(2)
                self.score += 2
            else:
                self.snake.increase_length(1)
                self.score += 1
            self.apple.move()

        # snake colliding with itself
        for i in range(3, self.snake.length):
            if is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                self.play_sound('crash-sound.mp3')
                raise "Game over"

        # Surface limit
        if ((0 > self.snake.x[0] or self.snake.x[0] > WINDOW_SIZE_X) or
                (0 > self.snake.y[0] or self.snake.y[0] > WINDOW_SIZE_Y)):
            self.play_sound('crash-sound.mp3')
            with open(BEST_SCORE_PATH, 'r') as f:
                self.best_score = int(f.read())
            raise "Game over"

    def restart(self):
        """ Restart game by resetting snake, apple and score"""
        self.snake = Snake(self.surface, 2)
        self.apple = Apple(self.surface)
        self.score = 0
        self.start_time = time.time()

    def run(self):
        """Make the snake walk as long as no collision or Quit event"""
        running = True
        self.start_time = time.time()
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                if event.type == KEYDOWN:
                    if event.key == K_RETURN:
                        self.pause = False
                    if event.key == K_UP:
                        self.snake.move_up()
                    if event.key == K_DOWN:
                        self.snake.move_down()
                    if event.key == K_RIGHT:
                        self.snake.move_right()
                    if event.key == K_LEFT:
                        self.snake.move_left()
                    if event.key == K_ESCAPE:
                        running = False
            try:
                if not self.pause:
                    self.play()
            except Exception as e:
                self.game_over()
                self.pause = True
                self.restart()
            time.sleep(0.05)
    