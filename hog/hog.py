"""CS 61A Presents The Game of Hog."""

from dice import four_sided, six_sided, make_test_dice
from ucb import main, trace, log_current_line, interact

GOAL_SCORE = 100  # The goal of Hog is to score 100 points.

######################
# Phase 1: Simulator #
######################

def roll_dice(num_rolls, dice=six_sided):
    """Simulate rolling the DICE exactly NUM_ROLLS>0 times. Return the sum of
    the outcomes unless any of the outcomes is 1. In that case, return the
    number of 1's rolled (capped at 11 - NUM_ROLLS).
    """
    # These assert statements ensure that num_rolls is a positive integer.
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls > 0, 'Must roll at least once.'
    # BEGIN PROBLEM 1
    assert num_rolls <= 10
    rolls, sum_out, ones = 0, 0, 0

    while rolls < num_rolls:
        rolls += 1
        outcome = dice()
        if outcome == 1:
            ones += 1
        else:
            sum_out = sum_out + outcome
    if ones:
        return min(11 - num_rolls, ones)
    else:
        return sum_out
    # END PROBLEM 1


def free_bacon(opponent_score):
    """Return the points scored from rolling 0 dice (Free Bacon)."""
    # BEGIN PROBLEM 2
    assert (opponent_score) <= 99
    if opponent_score == 0:
        return 1
    elif opponent_score < 10:
        return opponent_score + 1
    else:
        return max(opponent_score % 10, opponent_score // 10) + 1
    # END PROBLEM 2


# def prime_determinator(n):
def is_prime(x):
    "checks if a number is prime"
    if x >= 2:
        for y in range(2, x):
            if not (x % y):
                return False
    else:
        return False
    return True

def hogtimus_prime(int):
    "implements Hogtimus prime rule if players score is prime"
    if is_prime(int):
        while int<100:
            int = int + 1
            if is_prime(int):
                return int


def take_turn(num_rolls, opponent_score, dice=six_sided):
    """Simulate a turn rolling NUM_ROLLS dice, which may be 0 (Free Bacon).
    Return the points scored for the turn by the current player. Also
    implements the Hogtimus Prime rule.

    num_rolls:       The number of dice rolls that will be made.
    opponent_score:  The total score of the opponent.
    dice:            A function of no args that returns an integer outcome.
    """
    # Leave these assert statements here; they help check for errors.
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls >= 0, 'Cannot roll a negative number of dice in take_turn.'
    assert num_rolls <= 10, 'Cannot roll more than 10 dice.'
    assert opponent_score < 100, 'The game should be over.'
    # BEGIN PROBLEM 2
    if num_rolls== 0:
        if is_prime(free_bacon(opponent_score)):
            return hogtimus_prime(free_bacon(opponent_score))
        else:
            return free_bacon(opponent_score)
    else:
        sum = roll_dice(num_rolls, dice)
        if is_prime(sum):
            return hogtimus_prime(sum)
        else:
            return sum
    # END PROBLEM 2


def select_dice(score, opponent_score):
    """Select six-sided dice unless the sum of SCORE and OPPONENT_SCORE is a
    multiple of 7, in which case select four-sided dice (Hog Wild).
    """
    # BEGIN PROBLEM 3
    if score % 7 == 0 and opponent_score % 7 == 0:
        return four_sided
    elif ((score + opponent_score) % 7 == 0):
        return four_sided
    else:
        return six_sided
    # END PROBLEM 3

def is_swap(score0, score1):
    """Returns whether one of the scores is double the other.
    """
    # BEGIN PROBLEM 4
    if score1 - score0 == score0:
        return True
    elif score0 - score1 == score1:
        return True
    else:
        return False
    # END PROBLEM 4

def other(player):
    """Return the other player, for a player PLAYER numbered 0 or 1.

    >>> other(0)
    1
    >>> other(1)
    0
    """
    return 1 - player


def play(strategy0, strategy1, score0=0, score1=0, goal=GOAL_SCORE):
    """Simulate a game and return the final scores of both players, with
    Player 0's score first, and Player 1's score second.

    A strategy is a function that takes two total scores as arguments
    (the current player's score, and the opponent's score), and returns a
    number of dice that the current player will roll this turn.

    strategy0:  The strategy function for Player 0, who plays first
    strategy1:  The strategy function for Player 1, who plays second
    score0   :  The starting score for Player 0
    score1   :  The starting score for Player 1
    """
    player = 0  # Which player is about to take a turn, 0 (first) or 1 (second)
    # BEGIN PROBLEM 5
    assert score0 < 100, 'The game should be over.'
    assert score1 < 100, 'The game should be over.'
    while score0 < goal and score1 < goal:
        if player==0:
            score = score0
            opponent_score = score1
            strategy = strategy0
            num_rolls = strategy(score,opponent_score)
        else:
            score = score1
            opponent_score=score0
            strategy=strategy1
            num_rolls= strategy(score,opponent_score)
        scoreTemp = take_turn(num_rolls, opponent_score, select_dice(score0, score1))
        score = score + scoreTemp
        if is_swap(score,opponent_score):
            score, opponent_score= opponent_score, score
        player= other(player)
        if player==1:
            score0=score
            score1= opponent_score
        elif player==0:
            score1=score
            score0= opponent_score
    # END PROBLEM 5
    return score0, score1


#######################
# Phase 2: Strategies #
#######################

def always_roll(n):
    """Return a strategy that always rolls N dice.

    A strategy is a function that takes two total scores as arguments
    (the current player's score, and the opponent's score), and returns a
    number of dice that the current player will roll this turn.

    >>> strategy = always_roll(5)
    >>> strategy(0, 0)
    5
    >>> strategy(99, 99)
    5
    """
    def strategy(score, opponent_score):
        return n
    return strategy


def check_strategy_roll(score, opponent_score, num_rolls):
    """Raises an error with a helpful message if NUM_ROLLS is an invalid
    strategy output. All strategy outputs must be integers from -1 to 10.

    >>> check_strategy_roll(10, 20, num_rolls=100)
    Traceback (most recent call last):
     ...
    AssertionError: strategy(10, 20) returned 100 (invalid number of rolls)

    >>> check_strategy_roll(20, 10, num_rolls=0.1)
    Traceback (most recent call last):
     ...
    AssertionError: strategy(20, 10) returned 0.1 (not an integer)

    >>> check_strategy_roll(0, 0, num_rolls=None)
    Traceback (most recent call last):
     ...
    AssertionError: strategy(0, 0) returned None (not an integer)
    """
    msg = 'strategy({}, {}) returned {}'.format(
        score, opponent_score, num_rolls)
    assert type(num_rolls) == int, msg + ' (not an integer)'
    assert 0 <= num_rolls <= 10, msg + ' (invalid number of rolls)'


def check_strategy(strategy, goal=GOAL_SCORE):
    """Checks the strategy with all valid inputs and verifies that the
    strategy returns a valid input. Use `check_strategy_roll` to raise
    an error with a helpful message if the strategy returns an invalid
    output.

    >>> def fail_15_20(score, opponent_score):
    ...     if score != 15 or opponent_score != 20:
    ...         return 5
    ...
    >>> check_strategy(fail_15_20)
    Traceback (most recent call last):
     ...
    AssertionError: strategy(15, 20) returned None (not an integer)
    >>> def fail_102_115(score, opponent_score):
    ...     if score == 102 and opponent_score == 115:
    ...         return 100
    ...     return 5
    ...
    >>> check_strategy(fail_102_115)
    >>> fail_102_115 == check_strategy(fail_102_115, 120)
    Traceback (most recent call last):
     ...
    AssertionError: strategy(102, 115) returned 100 (invalid number of rolls)
    """
    # BEGIN PROBLEM 6
    assert goal <= 100
    score, num_rolls = 0,0
    while score < goal or score < 100:
        opponent_score = 0
        while opponent_score < 100:
            check_strategy_roll(score, opponent_score, num_rolls)
            num_rolls = strategy(score, opponent_score)
            opponent_score +=1
        score += 1
    return None
    # END PROBLEM 6
# Experiments

def make_averaged(fn, num_samples=1000):
    """Return a function that returns the average_value of FN when called.

    To implement this function, you will have to use *args syntax, a new Python
    feature introduced in this project.  See the project description.

    >>> dice = make_test_dice(3, 1, 5, 6)
    >>> averaged_dice = make_averaged(dice, 1000)
    >>> averaged_dice()
    3.75
    """
    # BEGIN PROBLEM 7
    def average(*args) :
        total, bekfast = 0, 0
        while bekfast < num_samples :
            total += fn(*args)
            bekfast += 1
        return total/num_samples
    return average
    # END PROBLEM 7

def max_scoring_num_rolls(dice=six_sided, num_samples=1000):
    """Return the number of dice (1 to 10) that gives the highest average turn
    score by calling roll_dice with the provided DICE over NUM_SAMPLES times.
    Assume that the dice always return positive outcomes.

    >>> dice = make_test_dice(3)
    >>> max_scoring_num_rolls(dice)
    10
    """
    # BEGIN PROBLEM 8
    num_roll, max_roll, max_num = 1, 0, 0

    avg = make_averaged(roll_dice,num_samples)
    while num_roll < 11:
        temp = avg(num_roll, dice)
        if temp > max_num:
            max_roll = num_roll
            max_num = temp
        num_roll += 1

    return max_roll
    # END PROBLEM 8

def winner(strategy0, strategy1):
    """Return 0 if strategy0 wins against strategy1, and 1 otherwise."""
    score0, score1 = play(strategy0, strategy1)
    if score0 > score1:
        return 0
    else:
        return 1


def average_win_rate(strategy, baseline=always_roll(4)):
    """Return the average win rate of STRATEGY against BASELINE. Averages the
    winrate when starting the game as player 0 and as player 1.
    """
    win_rate_as_player_0 = 1 - make_averaged(winner)(strategy, baseline)
    win_rate_as_player_1 = make_averaged(winner)(baseline, strategy)

    return (win_rate_as_player_0 + win_rate_as_player_1) / 2


def run_experiments():
    """Run a series of strategy experiments and report results."""
    if True:  # Change to False when done finding max_scoring_num_rolls
        six_sided_max = max_scoring_num_rolls(six_sided)
        print('Max scoring num rolls for six-sided dice:', six_sided_max)
        four_sided_max = max_scoring_num_rolls(four_sided)
        print('Max scoring num rolls for four-sided dice:', four_sided_max)

    if False:  # Change to True to test always_roll(8)
        print('always_roll(8) win rate:', average_win_rate(always_roll(8)))

    if False:  # Change to True to test bacon_strategy
        print('bacon_strategy win rate:', average_win_rate(bacon_strategy))

    if False:  # Change to True to test swap_strategy
        print('swap_strategy win rate:', average_win_rate(swap_strategy))

    "*** You may add additional experiments as you wish ***"


# Strategies

def bacon_strategy(score, opponent_score, margin=8, num_rolls=4):
    """This strategy rolls 0 dice if that gives at least MARGIN points,
    and rolls NUM_ROLLS otherwise.
    """
    # BEGIN PROBLEM 9
    if take_turn(0 , opponent_score ) >= margin:
        return 0
    else:
        return num_rolls
    # END PROBLEM 9
check_strategy(bacon_strategy)


def swap_strategy(score, opponent_score, margin=8, num_rolls=4):
    """This strategy rolls 0 dice when it triggers a beneficial swap. It also
    rolls 0 dice if it gives at least MARGIN points. Otherwise, it rolls
    NUM_ROLLS.
    """
    # BEGIN PROBLEM 10
    bekfast = free_bacon(opponent_score)
    if is_prime(bekfast):
        bekfast = hogtimus_prime(bekfast)
    temp_score = score + bekfast
    if bacon_strategy(score, opponent_score, margin, num_rolls) == 0:
        if opponent_score * 2 != temp_score:
            return 0
    if temp_score * 2 == opponent_score:
        return 0
    return num_rolls
    # END PROBLEM 10
check_strategy(swap_strategy)

def final_strategy(score, opponent_score):
    """Write a brief description of your final strategy.

For our final strategy we applied the bacon strategy if our score was larger
than 88 and we only needed a few points to win the game. We choose 5 as our
margin and 3 as the alternative number of dice rolled as that gave us the best
results. For our final strategy we also applied the swap strategy if our score
was at least 9 higher than the opponent score or our score was above 80 in order
to limit the number of points the opponent could get to catch up as a 4-sided
dice on average will return fewer points than a six-sided dice."""


    # BEGIN PROBLEM 11
    if score > 88:
        return bacon_strategy(score, opponent_score, 5, 3)
    elif (score - opponent_score) > 9 or score >= 80:
        return swap_strategy(score, opponent_score, 8, 5)
    return swap_strategy(score, opponent_score, 11, 5)
    # END PROBLEM 11
check_strategy(final_strategy)


##########################
# Command Line Interface #
##########################

# NOTE: Functions in this section do not need to be changed. They use features
# of Python not yet covered in the course.

@main
def run(*args):
    """Read in the command-line argument and calls corresponding functions.

    This function uses Python syntax/techniques not yet covered in this course.
    """
    import argparse
    parser = argparse.ArgumentParser(description="Play Hog")
    parser.add_argument('--run_experiments', '-r', action='store_true',
                        help='Runs strategy experiments')

    args = parser.parse_args()

    if args.run_experiments:
        run_experiments()
