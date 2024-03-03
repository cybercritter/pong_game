"""Weber State University - CS 1400 (Adamic): Programming I -- Midterm Project
Python implementation of the classic game Pong.

This is a template for the implementation of the game Pong. You should
implement the game logic in this file.
"""
# pylint: disable=no-member disable=invalid-sequence-index
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

# pylint: disable=invalid-name
# Define the game objects
ball = [0, 0]
player1 = [0, 0]
player2 = [0, 0]

# Define any helper functions here (optional).
"""
This module contains additional helper functions for the pong program.
"""

def wall_hit(ball_pos, scores, ball_velo, window_width, ball_width):
    """
    The wall_hit function checks to see if the ball has hit either wall.
    If it has, then the function returns True and updates the score of whichever player scored.
    Otherwise, it returns False.

    :param ball: Get the x and y coordinates of the ball
    :param scores: Keep track of the score for each player
    :param ball_velo: Change the velocity of the ball
    :param window_width: Determine the width of the window
    :param ball_width: Determine the width of the ball
    :return: collision found
    """
    x = int(ball_pos[0])
    velocity_x = ball_velo[0]
    wall_collision = False
    right_wall_collision = window_width - (ball_width / 2)

    if ball_pos[0] < 0:
        wall_collision = True
        velocity_x = -velocity_x
        x = x + velocity_x
        scores['player2'] += 1

    elif x > right_wall_collision:
        wall_collision = True
        velocity_x = -velocity_x
        x = x + velocity_x
        scores['player1'] += 1

    return wall_collision


def init_positions(window_height, window_width, ball_width, paddle_height):
    """
    The init function initializes the game by setting up the left and right paddles, as well as
    the ball.

    :param window_height: Set the height of the window,
    :param window_width: Set the width of the window
    :param ball_width: Determine the width of the ball
    :param paddle_height: Set the height of the paddle
    :param half_paddle_width: Determine the position of the paddle
    :return:
    - left paddle position (x and y),
    - right paddle position (x and y)
    - ball position (x and y).

    """

    left_paddle = [ball_width + 1,
                   window_height / 2 - paddle_height / 2]

    right_paddle = [window_width - (ball_width - 1),
                    (window_height / 2) - (paddle_height / 2)]

    ball_pos = [(window_width/2) - (ball_width/2) + 1,
                (window_height/2) - (ball_width/2)]

    return (left_paddle, right_paddle, ball_pos)


def paddle_hit(ball_pos,
               ball_width,
               ball_height,
               ball_velo,
               player1_pos,
               player2_pos,
               paddle_height,
               paddle_width):
    """
    The paddle_hit function is used to check if the ball has collided with either of the paddles.
    If it has, then it will reverse the direction of travel for that axis and move
    in that direction.


    :param ball: Determine the position of the ball
    :param ball_velo: Change the velocity of the ball
    :param player1: Check if the ball collides with the paddle
    :param player2: Check if the ball collides with player2's paddle
    :param paddle_height: Determine the height of the paddle
    :param paddle_width: Define the width of the paddle
    :param ball_width: Determine if the ball is within a certain range of the paddle
    :return: The new ball position and velocity
    """

    velocity_x = ball_velo[0]
    velocity_y = ball_velo[1]
    x = ball_pos[0]
    y = ball_pos[1]
    paddle1_x = player1_pos[0]
    paddle1_y = player1_pos[1]

    paddle2_x = player2_pos[0]
    paddle2_y = player2_pos[1]

    ball_rect = pygame.Rect((x, y), (ball_width, ball_height))
    paddle1_rect = pygame.Rect((paddle1_x, paddle1_y), (paddle_width, paddle_height))
    paddle2_rect = pygame.Rect((paddle2_x, paddle2_y), (paddle_width, paddle_height))

    # player 1 is paddle_left
    if pygame.Rect.colliderect(ball_rect, paddle1_rect):
        velocity_x = -velocity_x
        x += velocity_x

    # player2 is paddle_right
    if pygame.Rect.colliderect(ball_rect, paddle2_rect):
        velocity_x = -velocity_x
        x += velocity_x

    return ([int(x), int(y)], [velocity_x, velocity_y])


def update_ball_position(ball_pos, ball_velo, window_height, ball_height):
    # Bouncing Algorithm when the Ball hit the edge of the canvas
    """
    The update_ball_position function takes in the ball's current position, its width and height,
    its velocity (velocity_x and velocity_y), the window's width and height, as well as the ball's
    height. It then updates the ball position based on its current x-coordinate (x) and y-coordinate
    (y). If it hits a wall or ceiling of canvas, it will bounce off by reversing its direction. The
    ball is also updated to move at a constant speed.

    :param ball_pos: Store the current position of the ball
    :param ball_width: Set the width of the ball
    :param ball_velo: Set the velocity of the ball
    :param window_width: Set the width of the window
    :param window_height: Determine the height of the window
    :param ball_height: Determine the height of the ball
    :return: A list of two elements, the first element is a list of x and y coordinates
    """
    velocity_x = ball_velo[0]
    velocity_y = ball_velo[1]
    x = ball_pos[0] + velocity_x
    y = ball_pos[1] + velocity_y

    if y + ball_height > window_height:
        x -= 1
        y -= 1
        velocity_y = -velocity_y

    elif y < 0:
        x += 1
        y += 1
        velocity_y = -velocity_y

    # set the current ball coordinates
    return ([int(x), int(y)], [velocity_x, velocity_y])


# pylint: disable=global-statement
# Put any other global variables you may need here (optional).
PADDLE_VELOCITY = 5
HALF_PAD_HEIGHT = 50
HALF_PAD_WIDTH = 10
ball_velocity = [2, 2]
player_scores = {"player1": 0, "player2": 0}

# Flag to keep initialization state
game_initialized = False

# pylint: enable=invalid-name
# Required Functions.
def get_scores():
    """
    The get_scores function returns the scores of both players as a tuple.

    The first element in the tuple is player 1's score, and the second element is player 2's score.

    :return: A tuple of the scores for both players
    """
    return (player_scores['player1'], player_scores['player2'])


def process_input():
    """
    The process_input function is used to update the game objects and state.
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

    if user_inputs[USER1_UP] and player1[1] > 0:
        player1[1] -= PADDLE_VELOCITY

    if user_inputs[USER1_DOWN] and player1[1] < WINDOW_HEIGHT - PADDLE_HEIGHT:
        player1[1] += PADDLE_VELOCITY

    if user_inputs[USER2_UP] and player2[1] > 0:
        player2[1] -= PADDLE_VELOCITY

    if user_inputs[USER2_DOWN] and player2[1] < WINDOW_HEIGHT - PADDLE_HEIGHT:
        player2[1] += PADDLE_VELOCITY


def update():
    """
    The update function is responsible for updating the game state.
    It takes no arguments and returns nothing. It updates the ball and paddle positions

    It also checks if there are any collisions between paddles or walls.

    :return: A tuple of the ball and the velocity
    """
    global player1, player2, ball, game_initialized, ball_velocity

    if game_initialized is False:
        player1, player2, ball = init_positions(WINDOW_HEIGHT,
                                    WINDOW_WIDTH,
                                    BALL_WIDTH,
                                    PADDLE_HEIGHT)
        game_initialized = True

    ball, ball_velocity = update_ball_position(ball,
                                                                ball_velocity,
                                                                WINDOW_HEIGHT,
                                                                BALL_HEIGHT)

    if wall_hit(ball, player_scores, ball_velocity, WINDOW_WIDTH, BALL_WIDTH):
        player1, player2, ball = init_positions(WINDOW_HEIGHT,
                                                        WINDOW_WIDTH,
                                                        BALL_WIDTH,
                                                        PADDLE_HEIGHT)

    ball, ball_velocity =  paddle_hit(ball,
                                                        BALL_WIDTH,
                                                        BALL_HEIGHT,
                                                        ball_velocity,
                                                        player1,
                                                        player2,
                                                        PADDLE_HEIGHT,
                                                        PADDLE_WIDTH
                                                        )



# ------------------------- !Do Not Modify Below Code-------------------------


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
        _paddle2 = (player2['x'], player2['y'], PADDLE_WIDTH, PADDLE_HEIGHT) # type: ignore
    elif (isinstance(player1, (tuple, list)) and isinstance(player2, (tuple, list))):
        _paddle1 = (player1[0], player1[1], PADDLE_WIDTH, PADDLE_HEIGHT)
        _paddle2 = (player2[0], player2[1], PADDLE_WIDTH, PADDLE_HEIGHT)
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
