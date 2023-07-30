import argparse


class InputArgParser:
    
    _parser = argparse.ArgumentParser()
    _parser.add_argument(
        "-l",
        "--headless",
        dest="headless",
        help="Headless Mode",
        default=False,
        type=bool,
    )
    _parser.add_argument(
        "-d",
        "--debug",
        dest="debug",
        help="Debug Mode",
        default=False,
        type=bool,
    )

    _args = _parser.parse_args()

    @classmethod
    def is_headless(cls):
        return cls._args.headless

    @classmethod
    def is_debug(cls):
        return cls._args.debug
