import argparse


def get_args():
    parser = argparse.ArgumentParser(description="Run the game with specified bot Docker images.")
    parser.add_argument(
        "--bot1",
        type=str,
        default="jokkess/hackatron-random-bot",
        help="Docker image for Bot 1"
    )
    parser.add_argument(
        "--bot2",
        type=str,
        default="jokkess/hackatron-random-bot",
        help="Docker image for Bot 2"
    )
    parser.add_argument(
        "--auto",
        action="store_true",
        help="Run the game in automatic mode without waiting for keypresses"
    )
    parser.add_argument(
        "--manual1",
        action="store_true",
        help="Run Bot 1 in manual mode"
    )
    parser.add_argument(
        "--manual2",
        action="store_true",
        help="Run Bot 2 in manual mode"
    )
    args = parser.parse_args()
    return args.bot1, args.bot2, args.auto, args.manual1, args.manual2
