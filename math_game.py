"""
math_quiz.py
-------------
A fun Math Quiz game using random numbers, scoring, and stats.

Source Inspiration:
Adapted from: https://stackoverflow.com/questions/28902064/python-maths-quiz-random-number
"""
def math_quiz():

    import random
    import statistics

    class Player:
        """Class to store player name and track scores."""
        def __init__(self, name):
            self.name = name
            self.scores = []

        def record_score(self, score):
            """Record the score (1 or 0) for each question."""
            self.scores.append(score)

        def get_statistics(self):
            """Return a dictionary with descriptive statistics."""
            if not self.scores:
                return {}
            return {
                'total': sum(self.scores),
                'average': statistics.mean(self.scores),
                'min': min(self.scores),
                'max': max(self.scores),
                'range': max(self.scores) - min(self.scores),
                'count': len(self.scores)
            }

    class MathQuizGame:
        """Class to handle quiz logic and gameplay."""
        def __init__(self, player):
            self.player = player
            self.operations = ['+', '-', '*']

        def generate_question(self, question_num):
            """Generate harder questions as game progresses."""
            if question_num < 3:
                max_val = 10
            elif question_num < 6:
                max_val = 20
            else:
                max_val = 50

            op = random.choice(self.operations)
            num1 = random.randint(1, max_val)
            num2 = random.randint(1, max_val)

            if op == '+':
                answer = num1 + num2
            elif op == '-':
                answer = num1 - num2
            elif op == '*':
                answer = num1 * num2
            question = f"What is {num1} {op} {num2}?"
            return question, answer

        def start_quiz(self, num_questions=10):
            """Run the quiz game with dynamic difficulty."""
            print(f"Welcome {self.player.name}! Let's begin the Math Quiz!\n")

            for i in range(num_questions):
                question, correct_answer = self.generate_question(i)
                print(f"Question {i+1}: {question}")
                try:
                    user_input = int(input("Your answer: "))
                    if user_input == correct_answer:
                        print("Correct!\n")
                        self.player.record_score(1)
                    else:
                        print(f"Wrong! The correct answer was {correct_answer}\n")
                        self.player.record_score(0)
                except ValueError:
                    print("Invalid input! Must be an integer. Score: 0 for this question.\n")
                    self.player.record_score(0)

            print(f"\n{self.player.name}, here are your game stats:")
            stats = self.player.get_statistics()
            for key, value in stats.items():
                print(f"{key.capitalize()}: {value}")

    def main():
        """Entry point for the standalone quiz game."""
        name = input("Enter your name: ")
        try:
            num_qs = int(input("How many questions would you like to answer? "))
        except ValueError:
            print("Invalid input. Defaulting to 5 questions.")
            num_qs = 5

        player = Player(name)
        game = MathQuizGame(player)
        game.start_quiz(num_questions=num_qs)

    if __name__ == "__main__":
        main()
math_quiz()