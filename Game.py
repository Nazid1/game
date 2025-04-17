# Full updated Snakes and Ladders game with leaderboard average wins displayed before game launch

import turtle
import random
import os

def show_leaderboard_summary():
    try:
        with open("leaderboard.csv", "r") as file:
            lines = file.readlines()
            if not lines:
                print("\n📊 No leaderboard data yet.\n")
                return

            total_wins = 0
            print("\n📊 Leaderboard Summary")
            print("--------------------------")
            print("Current players:")

            for line in lines:
                name, wins = line.strip().split(",")
                print(f"- {name}: {wins} wins")
                total_wins += int(wins)

            avg = total_wins / len(lines)
            print(f"\n🏆 Average Wins Across Players: {avg:.2f}")
            print("--------------------------\n")

    except FileNotFoundError:
        print("\n⚠️ Leaderboard file not found. It will be created when the game is played.\n")


def update_leaderboard(winner_name):
    filename = "leaderboard.csv"
    scores = {}

    if os.path.exists(filename):
        with open(filename, "r") as file:
            for line in file:
                name, wins = line.strip().split(",")
                scores[name] = int(wins)

    if winner_name in scores:
        scores[winner_name] += 1
    else:
        scores[winner_name] = 1

    with open(filename, "w") as file:
        for name, wins in scores.items():
            file.write(f"{name},{wins}\n")


def snake_and_the_ladder():
    """
    Initializes and runs the Snakes and Ladders game using turtle graphics.
    This is a two-player game with a GUI-based board and interactive dice rolls.
    """

    show_leaderboard_summary()

    screen = turtle.Screen()
    screen.setup(800, 800)
    screen.title("Snakes and Ladders")
    screen.bgpic("snakes-and-ladders.png")  # Assumes you have a board image

    p1_name = screen.textinput("Player 1", "Enter Player 1 name:")
    p2_name = screen.textinput("Player 2", "Enter Player 2 name:")

    dice_writer = turtle.Turtle()
    dice_writer.hideturtle()
    dice_writer.penup()
    dice_writer.goto(-350, 300)

    scoreboard = turtle.Turtle()
    scoreboard.hideturtle()
    scoreboard.penup()
    scoreboard.goto(200, 300)

    def update_scoreboard(p1_pos, p2_pos):
        scoreboard.clear()
        scoreboard.write(f"{p1_name}: {p1_pos}     {p2_name}: {p2_pos}", font=("Arial", 16, "bold"))

    def movePlayer(player, position):
        if position < 1:
            position = 1
        yPos = (position - 1) // 10
        xPos = (position - 1) % 10
        y = -170 + yPos * 37
        if yPos % 2 == 0:
            x = -170 + xPos * 38
        else:
            x = 170 - xPos * 38
        player.goto(x, y)

    def create_player(color):
        player = turtle.Turtle()
        player.shape("circle")
        player.color(color)
        player.penup()
        player.speed(5)
        return player

    player1 = create_player("#810081")
    player2 = create_player("blue")

    player1_pos = 1
    player2_pos = 1
    movePlayer(player1, player1_pos)
    movePlayer(player2, player2_pos)

    def roll_dice():
        dice = random.randint(1, 6)
        print(f"Dice roll: {dice}")
        return dice

    def handle_snakes_and_ladders(position):
        original = position
        # Ladders
        ladders = {5: 35, 8: 13, 11: 52, 21: 41, 59: 83, 72: 91, 85: 96}
        snakes = {36: 22, 63: 41, 68: 48, 84: 66, 93: 86}
        if position in ladders:
            print(f"Ladder! Climbing from {position} to {ladders[position]}\n")
            position = ladders[position]
        elif position in snakes:
            print(f"Snake! Sliding from {position} to {snakes[position]}\n")
            position = snakes[position]
        if position != original:
            print(f"New Position: {position}")
        return position

    turn = 1
    game_over = False

    while not game_over:
        if turn == 1:
            input(f"{p1_name}'s turn. Press Enter to roll the dice...\n")
            dice = roll_dice()
            dice_writer.clear()
            dice_writer.write(f"{p1_name} rolled: {dice}", font=("Arial", 16, "normal"))

            player1_pos += dice
            if player1_pos > 100:
                player1_pos = 100 - (player1_pos - 100)
            player1_pos = handle_snakes_and_ladders(player1_pos)
            movePlayer(player1, player1_pos)
            update_scoreboard(player1_pos, player2_pos)

            if player1_pos == 100:
                print(f"🎉 {p1_name} wins! 🎉")
                dice_writer.goto(-100, 0)
                dice_writer.write(f"{p1_name} Wins!", font=("Arial", 24, "bold"))
                update_leaderboard(p1_name)
                again = screen.textinput("Game Over", f"{p1_name} Wins!\nDo you want to play again? (yes/no)").lower()
                if again == "yes":
                    screen.clear()
                    snake_and_the_ladder()
                    return
                else:
                    screen.bye()
                    break
            else:
                turn = 2

        elif turn == 2:
            input(f"{p2_name}'s turn. Press Enter to roll the dice...\n")
            dice = roll_dice()
            dice_writer.clear()
            dice_writer.write(f"{p2_name} rolled: {dice}", font=("Arial", 16, "normal"))

            player2_pos += dice
            if player2_pos > 100:
                player2_pos = 100 - (player2_pos - 100)
            player2_pos = handle_snakes_and_ladders(player2_pos)
            movePlayer(player2, player2_pos)
            update_scoreboard(player1_pos, player2_pos)

            if player2_pos == 100:
                print(f"🎉 {p2_name} wins! 🎉")
                dice_writer.goto(-100, 0)
                dice_writer.write(f"{p2_name} Wins!", font=("Arial", 24, "bold"))
                update_leaderboard(p2_name)
                again = screen.textinput("Game Over", f"{p2_name} Wins!\nDo you want to play again? (yes/no)").lower()
                if again == "yes":
                    screen.clear()
                    snake_and_the_ladder()
                    return
                else:
                    screen.bye()
                    break
            else:
                turn = 1

    turtle.done()
    return player1_pos, player2_pos

show_leaderboard_summary()  # <--- Show leaderboard summary before game starts

# Start the game
snake_and_the_ladder()

