"""Weber State University - CS 1400 (Adamic): Programming I -- Midterm Project

Python implementation of the classic game Pong.

This implementation:
@author: J. Adamic (template) and Michael Reid (function)
@weber W#: 01251998
@date: 3/2/2024
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

# pylint: disable=global-statement
# Put any other global variables you may need here (optional).

# Flag to keep initialization state
game_initialized = False
PADDLE_VELOCITY = 5
velocity = {'x': 2, 'y': 2}
player_scores = {"player1": 0, "player2": 0}


# Define any helper functions here (optional).
def wall_hit():
    """
    The wall_hit function checks to see if the ball has hit a wall.
    If it has, then it returns True and adds one point to the appropriate player's score.
    Otherwise, it returns False.

    :return: True if wall hit, False if not collision occurred
    """
    x = int(ball[0])
    wall_collision = False

    # add the this to make the conditional easier to read
    right_wall_collision = WINDOW_WIDTH - (BALL_WIDTH / 2)

    if x < 0:
        wall_collision = True
        player_scores['player2'] += 1

    elif x > right_wall_collision:
        wall_collision = True
        player_scores['player1'] += 1

    return wall_collision


def init_positions():
    """
    Initializes the default positions of the player paddles and ball.
    """
    global player1, player2, ball

    # player1's paddle is on the left side of the board and centered vertically
    player1 = [0, WINDOW_HEIGHT / 2 - PADDLE_HEIGHT / 2]

    # player2's paddle is on the right side of the board brought in 50px so tha it is not off the
    # screen and centered vertically
    player2 = [WINDOW_WIDTH - 50, WINDOW_HEIGHT / 2 - PADDLE_HEIGHT / 2]

    # center the ball in the middle of the board
    ball = [(WINDOW_WIDTH/2) - (BALL_WIDTH/2), (WINDOW_HEIGHT/2) - (BALL_WIDTH/2)]


def change_y_velocity(y):
    """
    The function changes the velocity of the ball by flipping the y velocity,
    which reverses its direction.

    It then adds this new velocity to the current position of the ball to get a new position.

    :param y: current ball-y coordinate
    :return: new ball-y position
    """
    velocity['y'] = -velocity['y']
    y += velocity['y']
    return y


def paddle_hit():
    """
    The paddle_hit function is used to determine if the ball has collided with either paddle.
    If it has, then the velocity of the ball will change in both x and y directions.

    The function also checks for a collision on each side of the paddle,
    so that when a player hits the top or bottom of their paddle,
    they can still hit it back towards their opponent.

    Lastly it updates the balls coordinates
    """
    # several variable created for both ease of use and to make the logic below more readable
    x = ball[0]
    y = ball[1]
    paddle1_x = player1[0]
    paddle1_y = player1[1]

    paddle2_x = player2[0]
    paddle2_y = player2[1]

    # Create a few pygame rectangles. Using built in pygame function
    # makes finding collisions easier.
    ball_rect = pygame.Rect((x, y), (BALL_WIDTH, BALL_HEIGHT))
    paddle1_rect = pygame.Rect((paddle1_x, paddle1_y), (BALL_WIDTH, PADDLE_HEIGHT))
    paddle2_rect = pygame.Rect((paddle2_x, paddle2_y), (BALL_WIDTH, PADDLE_HEIGHT))

    # Check to see if the ball has collided with player1's paddle also make sure the ball is
    # moving to the right since player2's paddle is on the right side of the board.
    if pygame.Rect.colliderect(ball_rect, paddle1_rect) and velocity['x'] < 0:
        # this checks to see if the players paddle has been hit on the right side.
        # 10 is to give some leeway
        if abs(ball_rect.left - paddle1_rect.right) < 10:
            velocity['x'] = -velocity['x']
            x += velocity['x']

        # this checks to see if the players paddle has been hit on the top of the paddle.
        # We also need to make sure the ball is heading down toward the paddle
        # 10 is to give some leeway
        elif abs(ball_rect.bottom - paddle1_rect.top) < 10 and  velocity['y'] > 0:
            y = change_y_velocity(velocity['y'])

        # this checks to see if the players paddle has been hit on from the bottom of the paddle.
        # We also need to make sure the ball is heading up toward the paddle
        # 10 is to give some leeway
        elif abs(ball_rect.top - paddle1_rect.bottom) < 10 and  velocity['y'] < 0:
            y = change_y_velocity(velocity['y'])

    # Check to see if the ball has collided with player2's paddle also make sure the ball is
    # moving to the left since player1's paddle is on the left side of the board.
    if pygame.Rect.colliderect(ball_rect, paddle2_rect) and velocity['x'] > 0:
        # this checks to see if the players paddle has been hit on the left side.
        # 10 is to give some leeway
        if abs(ball_rect.right - paddle2_rect.left) < 10:
            velocity['x'] = -velocity['x']
            x += velocity['x']

        # this checks to see if the players paddle has been hit on from the top of the paddle.
        # We also need to make sure the ball is heading down toward the paddle
        # 10 is to give some leeway
        elif abs(ball_rect.bottom - paddle2_rect.top) < 10 and  velocity['y'] > 0:
            y = change_y_velocity(velocity['y'])

        # this checks to see if the players paddle has been hit on from the bottom of the paddle.
        # We also need to make sure the ball is heading up toward the paddle
        # 10 is to give some leeway
        elif abs(ball_rect.top - paddle2_rect.bottom) < 10 and  velocity['y'] < 0:
            y = change_y_velocity(velocity['y'])

    # update the current ball coordinates
    ball[0] = x
    ball[1] = y



def update_ball_position():
    # store values in more
    """
    The update_ball_position function updates the ball's position by adding the velocity to it.
    If the ball hits a the top or bottom of the display, its y-velocity is reversed.
    """

    # get the x,y corrdinates for the ball. adding velocity at this point smooths out the movement
    x = ball[0] + velocity['x']
    y = ball[1] + velocity['y']

    # if the y point with height of the ball hits the bottom of the display
    # "bounce" it back into play
    if y + BALL_HEIGHT > WINDOW_HEIGHT:
        x -= 1
        y -= 1
        velocity['y'] = -velocity['y']

    # if the y point with height of the ball hits the top of the display
    # "bounce" it back into play
    elif y < 0:
        x += 1
        y += 1
        velocity['y'] = -velocity['y']

    # set the current ball coordinates
    ball[0] = x
    ball[1] = y

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
    - If the user presses ESC, quit the game.
    - If the user presses W or S, update the player1 position.
    - If the user presses the UP or DOWN arrow keys, update the player2 position.
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

    # send the paddle up but don't let it go off the screen
    if user_inputs[USER1_UP] and player1[1] > 0:
        player1[1] -= PADDLE_VELOCITY

    # send the paddle down but don't let it go off the screen
    if user_inputs[USER1_DOWN] and player1[1] < WINDOW_HEIGHT - PADDLE_HEIGHT:
        player1[1] += PADDLE_VELOCITY

    # send the paddle up but don't let it go off the screen
    if user_inputs[USER2_UP] and player2[1] > 0:
        player2[1] -= PADDLE_VELOCITY
    # send the paddle down but don't let it go off the screen

    if user_inputs[USER2_DOWN] and player2[1] < WINDOW_HEIGHT - PADDLE_HEIGHT:
        player2[1] += PADDLE_VELOCITY


def update():
    """
    The update function is responsible for updating the game state.

    - It updates the ball and paddle positions
    - It also checks if there are any collisions between paddles or walls.

    """
    global game_initialized

    # if this is the start of the app. Initialize the ball and paddles to the start position
    # and set the flag so the program doesn't run the init code again
    if game_initialized is False:
        init_positions()
        game_initialized = True

    # move the ball to the next pixel on the screen
    update_ball_position()

    # check to see if a wall is hit and adjust the score as needed
    if wall_hit():
        init_positions()

    # check to see if a paddle has been hit and "bounce" it back into play if it has
    paddle_hit()



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
        _paddle2 = (player2['x'], player2['y'], PADDLE_WIDTH, PADDLE_HEIGHT)
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
