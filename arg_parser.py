import argparse


class InputArgParser:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-l",
        "--headless",
        dest="headless",
        help="Headless Mode",
        default=False,
        type=bool,
    )
    parser.add_argument(
        "-d",
        "--debug",
        dest="debug",
        help="Debug Mode",
        default=False,
        type=bool,
    )

    args = parser.parse_args()

    @classmethod
    def is_headless(cls):
        return cls.args.headless

    @classmethod
    def is_debug(cls):
        return cls.args.debug
