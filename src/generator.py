import random
import json
import copy


def load_profiles(filename):
    with open(filename, "r", encoding="utf-8") as file:
        profiles = json.load(file)

    validate_profiles(profiles)
    return profiles


def weighted_pick(entries):
    names = [entry["name"] for entry in entries]
    weights = [entry["weight"] for entry in entries]
    return random.choices(names, weights=weights, k=1)[0]


def generate_name(profile):
    first = weighted_pick(profile["first_names"])
    last = weighted_pick(profile["last_names"])
    return f"{first} {last}"


def get_profile_by_name(profiles, profile_name):
    for profile in profiles:
        if profile["name"] == profile_name:
            return profile
    raise ValueError(f"No profile named {profile_name!r} was found.")


def pick_profile(profiles):
    names = [p["name"] for p in profiles]
    weights = [p["weight"] for p in profiles]

    chosen_name = random.choices(names, weights=weights, k=1)[0]

    for p in profiles:
        if p["name"] == chosen_name:
            return p


def generate_multiple_from_profiles(profiles, n):
    names = []
    for _ in range(n):
        profile = pick_profile(profiles)
        names.append(generate_name(profile["data"]))
    return "\n".join(names)


def generate_multiple_from_one_profile(profiles, n):
    profile = pick_profile(profiles)

    names = []
    for _ in range(n):
        names.append(generate_name(profile["data"]))

    return "\n".join(names)


def generate_batch(profiles, n, mode="mixed", profile_name=None):
    if mode == "mixed":
        return generate_multiple_from_profiles(profiles, n)

    elif mode == "locked":
        return generate_multiple_from_one_profile(profiles, n)

    elif mode == "specific":
        if profile_name is None:
            raise ValueError("profile_name is required when mode='specific'.")

        profile = get_profile_by_name(profiles, profile_name)

        names = []
        for _ in range(n):
            names.append(generate_name(profile["data"]))

        return "\n".join(names)

    else:
        raise ValueError("mode must be 'mixed', 'locked', or 'specific'.")


def make_custom_mix(profiles, weights_by_name):
    custom_profiles = copy.deepcopy(profiles)

    for profile in custom_profiles:
        if profile["name"] in weights_by_name:
            profile["weight"] = weights_by_name[profile["name"]]
        else:
            profile["weight"] = 0

    return custom_profiles

def validate_name_entry(entry, profile_name, list_name):
    if not isinstance(entry, dict):
        raise ValueError(f"Invalid entry in {profile_name} / {list_name}: entry must be a dictionary.")

    if "name" not in entry:
        raise ValueError(f"Invalid entry in {profile_name} / {list_name}: missing 'name'.")

    if "weight" not in entry:
        raise ValueError(f"Invalid entry {entry.get('name')!r} in {profile_name} / {list_name}: missing 'weight'.")

    if not isinstance(entry["name"], str):
        raise ValueError(f"Invalid entry in {profile_name} / {list_name}: name must be a string.")

    if entry["name"].strip() == "":
        raise ValueError(f"Invalid entry in {profile_name} / {list_name}: name cannot be blank.")

    if not isinstance(entry["weight"], (int, float)):
        raise ValueError(f"Invalid entry {entry['name']!r} in {profile_name} / {list_name}: weight must be a number.")

    if entry["weight"] <= 0:
        raise ValueError(f"Invalid entry {entry['name']!r} in {profile_name} / {list_name}: weight must be positive.")

def validate_name_list(entries, profile_name, list_name):
    if not isinstance(entries, list):
        raise ValueError(f"{profile_name} / {list_name} must be a list.")

    if len(entries) == 0:
        raise ValueError(f"{profile_name} / {list_name} cannot be empty.")

    seen_names = set()

    for entry in entries:
        validate_name_entry(entry, profile_name, list_name)

        normalized_name = entry["name"].strip().lower()

        if normalized_name in seen_names:
            raise ValueError(f"Duplicate name {entry['name']!r} found in {profile_name} / {list_name}.")

        seen_names.add(normalized_name)

def validate_profiles(profiles):
    if not isinstance(profiles, list):
        raise ValueError("Profiles must be a list.")

    if len(profiles) == 0:
        raise ValueError("Profiles cannot be empty.")

    seen_profile_names = set()

    for profile in profiles:
        if not isinstance(profile, dict):
            raise ValueError("Each profile must be a dictionary.")

        if "name" not in profile:
            raise ValueError("Profile missing 'name'.")

        if not isinstance(profile["name"], str):
            raise ValueError("Profile name must be a string.")

        if profile["name"].strip() == "":
            raise ValueError("Profile name cannot be blank.")

        normalized_profile_name = profile["name"].strip().lower()

        if normalized_profile_name in seen_profile_names:
            raise ValueError(f"Duplicate profile name {profile['name']!r}.")

        seen_profile_names.add(normalized_profile_name)

        if "weight" not in profile:
            raise ValueError(f"Profile {profile['name']!r} missing 'weight'.")

        if not isinstance(profile["weight"], (int, float)):
            raise ValueError(f"Profile {profile['name']!r} weight must be a number.")

        if profile["weight"] <= 0:
            raise ValueError(f"Profile {profile['name']!r} weight must be positive.")

        if "data" not in profile:
            raise ValueError(f"Profile {profile['name']!r} missing 'data'.")

        if not isinstance(profile["data"], dict):
            raise ValueError(f"Profile {profile['name']!r} data must be a dictionary.")

        data = profile["data"]

        if "first_names" not in data:
            raise ValueError(f"Profile {profile['name']!r} missing 'first_names'.")

        if "last_names" not in data:
            raise ValueError(f"Profile {profile['name']!r} missing 'last_names'.")

        validate_name_list(data["first_names"], profile["name"], "first_names")
        validate_name_list(data["last_names"], profile["name"], "last_names")