# Orginal Game Link: https://github.com/techwithtim/Flappy-Bird
# Programmer: Trevon Fullwood
def flappy():
    import pygame
    import random
    import statistics

    # Initialize Pygame
    pygame.init()

    # Screen dimensions
    WIDTH, HEIGHT = 500, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Jumping Square")

    # Colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    BLUE = (0, 100, 255)
    GREEN = (0, 200, 0)
    RED = (255, 0, 0)

    # Game variables
    gravity = 0.5
    jump_strength = -10
    pipe_speed = 3
    gap_size = 150
    score = 0
    high_scores = []

    # Fonts
    font = pygame.font.SysFont(None, 36)

    # Load scores from file
    try:
        with open("scores.txt", "r") as f:
            high_scores = [int(x.strip()) for x in f.readlines()]
    except:
        high_scores = []


    # Player class
    class Player:
        def __init__(self):
            self.x = 50
            self.y = HEIGHT // 2
            self.width = 30
            self.height = 30
            self.velocity = 0

        def draw(self):
            pygame.draw.rect(screen, BLUE, (self.x, self.y, self.width, self.height))

        def jump(self):
            self.velocity = jump_strength

        def move(self):
            self.velocity += gravity
            self.y += self.velocity


    # Pipe class
    class Pipe:
        def __init__(self, x):
            self.x = x
            self.width = 50
            self.top = random.randint(50, HEIGHT - gap_size - 50)
            self.bottom = self.top + gap_size

        def move(self):
            self.x -= pipe_speed

        def draw(self):
            pygame.draw.rect(screen, GREEN, (self.x, 0, self.width, self.top))
            pygame.draw.rect(screen, GREEN, (self.x, self.bottom, self.width, HEIGHT))

        def collide(self, player):
            if player.x + player.width > self.x and player.x < self.x + self.width:
                if player.y < self.top or player.y + player.height > self.bottom:
                    return True
            return False


    # Game loop
    def game_loop():
        global score
        run = True
        clock = pygame.time.Clock()
        player = Player()
        pipes = [Pipe(300), Pipe(500), Pipe(700)]
        score = 0

        while run:
            clock.tick(30)
            screen.fill(WHITE)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        player.jump()

            player.move()
            player.draw()

            # Pipes
            rem = []
            add_pipe = False
            for pipe in pipes:
                pipe.move()
                pipe.draw()
                if pipe.collide(player):
                    run = False
                if pipe.x + pipe.width < 0:
                    rem.append(pipe)
                    add_pipe = True

            if add_pipe:
                pipes.append(Pipe(WIDTH))
                score += 1

            for r in rem:
                pipes.remove(r)

            if player.y > HEIGHT or player.y < 0:
                run = False

            text = font.render("Score: " + str(score), True, BLACK)
            screen.blit(text, (10, 10))

            pygame.display.update()

        high_scores.append(score)
        if len(high_scores) > 5:
            high_scores.pop(0)
        with open("scores.txt", "w") as f:
            for s in high_scores:
                f.write(str(s) + "\n")

        screen.fill(WHITE)
        try:
            mean_score = statistics.mean(high_scores)
            max_score = max(high_scores)
            min_score = min(high_scores)
            lines = [
                f"Game Over! Your score: {score}",
                f"Mean: {mean_score:.2f}, Max: {max_score}, Min: {min_score}",
                "Press any key to exit."
            ]
            for i, line in enumerate(lines):
                text = font.render(line, True, RED)
                screen.blit(text, (50, 200 + i * 40))
        except Exception as e:
            text = font.render(f"Error showing stats: {e}", True, RED)
            screen.blit(text, (50, 250))

        pygame.display.update()
        wait = True
        while wait:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                    wait = False


    # Play again loop
    while True:
        game_loop()

        screen.fill(BLACK)
        font = pygame.font.SysFont(None, 30)
        text = font.render("Press any key to play again or ESC to quit.", True, RED)
        screen.blit(text, (50, 300))
        pygame.display.update()

        wait = True
        while wait:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        quit()
                    else:
                        wait = False

