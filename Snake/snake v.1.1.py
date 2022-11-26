import pygame
import random


class SnakeGame:
    def launch_game(self):
        score = 0
        fps = pygame.time.Clock()

        snake = Snake()
        fruit = Fruit(snake)
        score = Score()
        scene = Scene(fruit, snake, score)

        pygame.init()

        while True:
            click = self.__get_click()

            if click:
                self.__process_click(click, snake)

            snake.move()

            snake.get_bigger()

            if snake.position == fruit.position:
                score.score += 1
                fruit.spawn_fruit()
            else:
                snake.body.pop()

            scene.draw_scene()

            self.__check_borders(snake)

            pygame.display.update()
            fps.tick(snake.speed)

    def __get_click(self):
        event = pygame.event.get(pygame.KEYDOWN)
        if not event:
            return None
        return event[0].__getattribute__("key")

    def __process_click(self, click, snake):
        if click == pygame.K_UP and snake.direction != "DOWN":
            snake.direction = "UP"

        elif click == pygame.K_DOWN and snake.direction != "UP":
            snake.direction = "DOWN"

        elif click == pygame.K_LEFT and snake.direction != "RIGHT":
            snake.direction = "LEFT"

        elif click == pygame.K_RIGHT and snake.direction != "LEFT":
            snake.direction = "RIGHT"

    def __check_borders(self, snake):
        if snake.position[0] < 0 or snake.position[0] > GameSettings.display_width - 10 \
                or snake.position[1] < 0 or snake.position[1] > GameSettings.display_height - 10:
            self.__restart_game()

        for block in snake.body[1:]:
            if snake.position[0] == block[0] and snake.position[1] == block[1]:
                self.__restart_game()

    def __restart_game(self):
        pygame.quit()
        self.launch_game()

    def __end_game(self):
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
        self.speed = 30
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


class Score:
    score: int = 0


class Fruit(SnakeGame):
    def __init__(self, snake: Snake):
        self.position = None
        self.snake = snake
        self.spawn_fruit()

    def spawn_fruit(self):
        self.position = [random.randrange(1, (GameSettings.display_width // 10)) * 10,
                         random.randrange(1, (GameSettings.display_height // 10)) * 10]
        if self.position in self.snake.body:
            self.spawn_fruit()


class Scene(SnakeGame):
    def __init__(self, fruit: Fruit, snake: Snake, score: Score):
        self.display = pygame.display
        self.window = pygame.display.set_mode((GameSettings.display_width, GameSettings.display_height))
        self.fruit = fruit
        self.snake = snake
        self.score = score

    def draw_scene(self):
        self.draw_background()
        self.draw_fruit()
        self.draw_snake()
        self.draw_score()
        pygame.display.update()

    def draw_background(self):
        self.window.fill(Color.BLACK)

    def draw_fruit(self):
        pygame.draw.rect(self.window, Color.RED, pygame.Rect(self.fruit.position[0], self.fruit.position[1], 10, 10))

    def draw_snake(self):
        for block in self.snake.body:
            pygame.draw.rect(self.window, Color.GREEN, pygame.Rect(block[0], block[1], 10, 10))

    def draw_score(self):
        score_font = pygame.font.SysFont("timesnewroman", 25)
        score_surface = score_font.render('Score: ' + str(self.score.score), True, Color.WHITE)
        score_rect = score_surface.get_rect()
        self.window.blit(score_surface, score_rect)


if __name__ == '__main__':
    SnakeGame().launch_game()
