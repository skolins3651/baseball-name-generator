import argparse
from pathlib import Path

from generator import load_profiles, generate_batch, make_custom_mix


# ensures less fragile pathing
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "profiles.json"


def parse_mix(mix_items):
    weights_by_name = {}

    for item in mix_items:
        try:
            name, weight_text = item.split("=", 1)
            weight = float(weight_text)
        except ValueError:
            raise ValueError(f"Invalid mix item {item!r}. Use format Name=Weight.")

        weights_by_name[name] = weight

    return weights_by_name


# creates a CLI interface for the generator, allowing users to specify generation parameters
def main():
    parser = argparse.ArgumentParser(
        description="Generate random baseball prospect names."
    )

    parser.add_argument(
        "--count",
        type=int,
        default=10,
        help="Number of names to generate."
    )

    parser.add_argument(
        "--mode",
        choices=["mixed", "locked", "specific"],
        default="mixed",
        help="How profiles are used during generation."
    )

    parser.add_argument(
        "--profile",
        help="Profile name to use when mode is 'specific'."
    )

    parser.add_argument(
        "--mix",
        nargs="*",
        default=None,
        help="Custom profile mix, e.g. American=20 Dominican=80."
    )

    args = parser.parse_args()

    profiles = load_profiles(DATA_PATH)

    if args.mix is not None:
        custom_weights = parse_mix(args.mix)
        profiles = make_custom_mix(profiles, custom_weights)

    result = generate_batch(
        profiles,
        args.count,
        mode=args.mode,
        profile_name=args.profile
    )

    print(result)


if __name__ == "__main__":
    main()