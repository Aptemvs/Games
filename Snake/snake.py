import pygame
import random


class SnakeGame:
    def launch_game(self):
        score = 0
        fps = pygame.time.Clock()

        fruit = Fruit()
        snake = Snake()
        scene = Scene(fruit, snake)

        pygame.init()

        while True:
            click = self.get_click()

            if click:
                self.process_click(click, snake)

            snake.move()

            snake.get_bigger()

            if snake.position == fruit.position:
                score += 10
                fruit.spawn_fruit()
            else:
                snake.body.pop()

            scene.draw_scene()

            self.check_borders(snake)

            pygame.display.update()
            fps.tick(snake.speed)

    def get_click(self):
        event = pygame.event.get(pygame.KEYDOWN)
        if not event:
            return None
        return event[0].__getattribute__("key")

    def process_click(self, click, snake):
        if click == pygame.K_UP and snake.direction != "DOWN":
            snake.direction = "UP"

        elif click == pygame.K_DOWN and snake.direction != "UP":
            snake.direction = "DOWN"

        elif click == pygame.K_LEFT and snake.direction != "RIGHT":
            snake.direction = "LEFT"

        elif click == pygame.K_RIGHT and snake.direction != "LEFT":
            snake.direction = "RIGHT"

    def check_borders(self, snake):
        if snake.position[0] < 0 or snake.position[0] > GameSettings.display_width \
                or snake.position[1] < 0 or snake.position[1] > GameSettings.display_height:
            self.end_game()

        for block in snake.body[1:]:
            if snake.position[0] == block[0] and snake.position[1] == block[1]:
                self.end_game()

    def end_game(self):
        pygame.quit()
        quit()


class Color:
    BLACK = (0, 0, 0)
    GREEN = (0, 255, 0)
    RED = (220, 50, 80)
    WHITE = (255, 255, 255)


class GameSettings(SnakeGame):
    display_width = 800
    display_height = 400
    pygame.display.set_caption('Snake')


class Snake(SnakeGame):
    def __init__(self):
        self.block = 10
        self.speed = 15
        self.direction = "RIGHT"
        self.position = [100, 50]
        self.body = [
            [100, 50],
            [90, 50],
            [80, 50],
            [70, 50]
        ]

    def move(self):
        if self.direction == "UP":
            self.position[1] -= 10
        if self.direction == "DOWN":
            self.position[1] += 10
        if self.direction == "LEFT":
            self.position[0] -= 10
        if self.direction == "RIGHT":
            self.position[0] += 10

    def get_bigger(self):
        self.body.insert(0, list(self.position))


class Fruit(SnakeGame):
    def __init__(self):
        self.position = None
        self.spawn_fruit()

    def spawn_fruit(self):
        self.position = [random.randrange(1, (GameSettings.display_width // 10)) * 10,
                         random.randrange(1, (GameSettings.display_height // 10)) * 10]


class Scene(SnakeGame):
    def __init__(self, fruit: Fruit, snake: Snake):
        self.display = pygame.display
        self.window = pygame.display.set_mode((GameSettings.display_width, GameSettings.display_height))
        self.fruit = fruit
        self.snake = snake

    def draw_scene(self):
        self.draw_background()
        self.draw_fruit()
        self.draw_snake()
        pygame.display.update()

    def draw_background(self):
        self.window.fill(Color.BLACK)

    def draw_fruit(self):
        pygame.draw.rect(self.window, Color.RED, pygame.Rect(self.fruit.position[0], self.fruit.position[1], 10, 10))

    def draw_snake(self):
        for block in self.snake.body:
            pygame.draw.rect(self.window, Color.GREEN, pygame.Rect(block[0], block[1], 10, 10))


if __name__ == '__main__':
    SnakeGame().launch_game()
