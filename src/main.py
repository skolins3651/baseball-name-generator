from generator import load_profiles, generate_batch


def main():
    profiles = load_profiles("../data/profiles.json")
    print(generate_batch(profiles, 10, mode="mixed"))


if __name__ == "__main__":
    main()