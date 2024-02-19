import tkinter as tk
from tkinter import messagebox
import random

# Initialize variables
rounds = 1
player_scores = {'Player 1': 0, 'Player 2': 0}
round_winner = None

# Create a tkinter window
root = tk.Tk()
root.title('Dice Poker Game')


# Function to roll the dice
def roll_dice():
    dice_values = [random.randint(1, 6) for _ in range(5)]  # Roll 5 dice
    return dice_values


# Function to determine the hand value
def get_hand_value(dice_values):
    return sum(dice_values)


# Function to play a round
def play_round():
    global rounds, player_scores, round_winner

    # Roll dice for players
    player1_dice = roll_dice()
    player2_dice = roll_dice()

    # Determine the hand value for each player
    player1_value = get_hand_value(player1_dice)
    player2_value = get_hand_value(player2_dice)

    # Compare hand values to find the winner
    if player1_value > player2_value:
        player_scores['Player 1'] += 1
        round_winner = 'Player 1'
    elif player2_value > player1_value:
        player_scores['Player 2'] += 1
        round_winner = 'Player 2'
    else:
        round_winner = 'Draw'

    # Update round and display results
    rounds += 1
    messagebox.showinfo('Round Results',
                        f"Round {rounds - 1} Winner: {round_winner}\nPlayer 1 Score: {player_scores['Player 1']}\nPlayer 2 Score: {player_scores['Player 2']}")


# Create tkinter buttons
btn_roll = tk.Button(root, text='Roll Dice', command=play_round)
btn_roll.pack()

# Run the tkinter main loop
root.mainloop()
