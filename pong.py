#!/usr/bin/python3

"""Weber State University - CS 1400 (Adamic): Programming I -- Midterm Project
Python implementation of the classic game Pong.

This is a template for the implementation of the game Pong. You should
implement the game logic in this file.
"""
# pylint: disable=no-member
# import math # You may want to use math functions in your implementation.
# Remove if unused.
import sys

import pygame

# Global constants. You shouldn't need to change these.
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
PADDLE_WIDTH = 20
PADDLE_HEIGHT = 100
BALL_WIDTH = 20
BALL_HEIGHT = 20
USER1_UP = pygame.K_w       # W key
USER1_DOWN = pygame.K_s     # S key
USER2_UP = pygame.K_UP      # Up arrow key
USER2_DOWN = pygame.K_DOWN  # Down arrow key
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)

# Define the game objects
ball = {'x': (WINDOW_WIDTH/2) - (BALL_WIDTH/2),
        'y': (WINDOW_HEIGHT/2) - (BALL_WIDTH/2)}
player1 = {'x': 50, 'y': (WINDOW_HEIGHT/2) - (PADDLE_HEIGHT/2), 'score': 0}
player2 = {'x': WINDOW_WIDTH - 50,
           'y': (WINDOW_HEIGHT/2) - (PADDLE_HEIGHT/2), 'score': 0}


# pylint: disable=global-statement
# Put any other global variables you may need here (optional).
BOARD_CENTER = ((WINDOW_WIDTH/2) - (BALL_WIDTH/2),
                (WINDOW_HEIGHT/2) - (BALL_WIDTH/2))

BALL_VELOCITY_X = 2
BALL_VELOCITY_Y = .7
PADDLE_VELOCITY = 4

# Define any helper functions here (optional).


# pylint: enable=invalid-name
# Required Functions.

def move_ball():
    """
    The move_ball function is responsible for moving the ball
    around the screen.
    It takes into account collisions with paddles and walls,
    as well as changing the velocity of the ball when it
    collides with a paddle or wall.

    :return: A dictionary with the current ball coordinates
    """
    global BALL_VELOCITY_X, BALL_VELOCITY_Y

    # Bouncing Algorithm when the Ball hit the edge of the canvas
    x = ball['x'] + BALL_VELOCITY_X
    y = ball['y'] + BALL_VELOCITY_Y
    collision_wall = False

    if x < 0:
        player2['score'] += 1
        BALL_VELOCITY_X = -BALL_VELOCITY_X
        x = x + BALL_VELOCITY_X
        collision_wall = True

    elif x > WINDOW_WIDTH - BALL_WIDTH / 2:
        player1['score'] += 1
        BALL_VELOCITY_X = -BALL_VELOCITY_X
        x = x + BALL_VELOCITY_X
        collision_wall = True

    elif (x + BALL_WIDTH >= player2['x'] and
          y <= (player2['y'] + PADDLE_HEIGHT) >= player2['y']):
        x += 1
        y += 1
        BALL_VELOCITY_X = -BALL_VELOCITY_X

    elif (x <= (player1['x'] + PADDLE_WIDTH) and
          y <= (player1['y'] + PADDLE_HEIGHT) >= player1['y']):
        x += 1
        y += 1
        BALL_VELOCITY_X = -BALL_VELOCITY_X

    if y + BALL_HEIGHT > WINDOW_HEIGHT:
        x -= 1
        y -= 1
        BALL_VELOCITY_Y = -BALL_VELOCITY_Y

    elif y < 0:
        x += 1
        y += 1
        BALL_VELOCITY_Y = -BALL_VELOCITY_Y

    if collision_wall is True:
        ball['x'], ball['y'] = BOARD_CENTER
    # set the current ball coordinates
    else:
        ball['x'] = x
        ball['y'] = y


def get_scores():
    """Return the current scores of player1 and player2 as a tuple.
    """
    return (player1['score'], player2['score'])


def process_input():
    """Process the user input to update the game objects and state.

    If the user presses ESC, quit the game.
    If the user presses W or S, update the player1 position.
    If the user presses the UP or DOWN arrow keys, update the player2 position.
    """
    # Check for user input to close the game window. DO NOT MODIFY THIS LOOP.
    for event in pygame.event.get():
        if (
            event.type == pygame.QUIT or
            (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE)
        ):
            pygame.quit()
            sys.exit()

    # Get a dictionary of all user inputs.
    user_inputs = pygame.key.get_pressed()

    # Use the dictionary of user inputs, to update the player positions.
    # UPDATE THE CODE BELOW TO MOVE THE PLAYERS BASED ON USER INPUTS.
    # HERE IS AN EXAMPLE ON HOW TO ACCESS THE USER INPUTS.
    if user_inputs[USER1_UP]:
        if player1['y'] > 0:
            player1['y'] -= PADDLE_VELOCITY

    if user_inputs[USER1_DOWN]:
        if player1['y'] < WINDOW_HEIGHT - PADDLE_HEIGHT:
            player1['y'] += PADDLE_VELOCITY

    if user_inputs[USER2_UP]:
        if player2['y'] > 0:
            player2['y'] -= PADDLE_VELOCITY

    if user_inputs[USER2_DOWN]:
        if player2['y'] < WINDOW_HEIGHT - PADDLE_HEIGHT:
            player2['y'] += PADDLE_VELOCITY


def update():
    """Update the positions of the game objects for the next frame.

    ! UPDATE THIS DOCSTRING BASED ON YOUR IMPLEMENTATION.

    YOU SHOULD IMPLEMENT THE FOLLOWING FUNCTIONALITY:
        - Update the ball position based on velocity/direction.
        - Boundary Detection: Check if the ball passes the left or right wall.
        - Ball Collisions: Check if the ball collides with the top/bottom walls
            or the paddles. Update the ball position/velocity accordingly.
        - Paddle Collisions: Check if the paddles collide with the top/bottom.
            Stop the paddle movement if a collision is detected.
    """
    move_ball()


def render():
    """Draw the game objects to the window based on their current position.

    DO NOT MODIFY ANYTHING IN THIS FUNCTION.
    """
    # pylint: disable=unsubscriptable-object
    window.fill(COLOR_BLACK)

    # Draw a line down the middle of the window.
    pygame.draw.line(window, COLOR_WHITE, (400, 0), (400, 600), 4)

    # Get the current ball position and dimensions, then draw the ball.
    if isinstance(ball, dict):
        _ball = (ball['x'], ball['y'], BALL_WIDTH, BALL_HEIGHT)
    elif isinstance(ball, (tuple, list)):
        _ball = (ball[0], ball[1], BALL_WIDTH, BALL_HEIGHT)
    else:
        raise TypeError("ball must be either a list, tuple, or dictionary.")
    pygame.draw.rect(window, COLOR_WHITE, pygame.Rect(*_ball))

    # Get the current paddle positions and dimensions.
    if isinstance(player1, dict) and isinstance(player2, dict):
        _paddle1 = (player1['x'], player1['y'], PADDLE_WIDTH, PADDLE_HEIGHT)
        _paddle2 = (player2['x'], player2['y'], PADDLE_WIDTH, PADDLE_HEIGHT)
    # elif (isinstance(player1, (tuple, list)) and
    #       isinstance(player2, (tuple, list))):
    #     _paddle1 = (player1[0], player1[1], PADDLE_WIDTH,
    #                 PADDLE_HEIGHT)  # type: ignore
    #     _paddle2 = (player2[0], player2[1], PADDLE_WIDTH,
    #                 PADDLE_HEIGHT)  # type: ignore
    else:
        raise TypeError("player1 and player2 must be either both lists, "
                        "both tuples, or both dictionaries.")

    # Draw the paddles
    pygame.draw.rect(window, COLOR_WHITE, pygame.Rect(*_paddle1))
    pygame.draw.rect(window, COLOR_WHITE, pygame.Rect(*_paddle2))

    # Draw the scores for each player
    font = pygame.font.Font(None, 74)
    scores = get_scores()
    score1 = font.render(str(scores[0]), True, COLOR_WHITE)
    score2 = font.render(str(scores[1]), True, COLOR_WHITE)
    score1_pos = (WINDOW_WIDTH / 4 - score1.get_width() / 2, 30)
    score2_pos = (3 * WINDOW_WIDTH / 4 - score2.get_width() / 2, 30)
    window.blit(score1, score1_pos)
    window.blit(score2, score2_pos)

    # Flip the display (update the screen)
    pygame.display.flip()


def run():
    """Start the game loop.

    - Collect player input (and update TENTATIVE paddle positions).
    - Updates all game objects positions for final render...
        Move ball position based on its velocity.
        Check if ball passes the left or right wall
            Update player scores accordingly and reset the ball position.
        Check for ball collision with walls or paddles.
            Update ball velocity accordingly.
        Check paddle collision with top and bottom walls.
            Stop paddle movement if a collision is detected.
    - Render the game objects to the window.

    DO NOT MODIFY ANYTHING IN THIS FUNCTION.
    """
    while True:
        # DO NOT MODIFY THIS LOOP.
        process_input()
        update()
        render()

        # Limit the game to update consistently 60 times per second
        clock.tick(60)


# Initialize the game
pygame.init()
pygame.display.set_caption("Pong")
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()

run()
