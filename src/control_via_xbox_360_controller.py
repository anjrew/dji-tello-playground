import argparse
import logging

from control_via_controller import main

args = argparse.ArgumentParser()
args.add_argument(
    "--controller",
    default="xbox360",
    choices=["xbox360", "xboxone"],
    help="Specify the controller type (default: xbox360)",
)

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

CADENCE_SECS = 0.1


if __name__ == "__main__":
    main("xbox360", cadence_secs=CADENCE_SECS, log_level="INFO")
