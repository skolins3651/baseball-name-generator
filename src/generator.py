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

def validate_profiles(profiles):
    if not isinstance(profiles, list):
        raise ValueError("Profiles must be a list.")

    for profile in profiles:
        if "name" not in profile:
            raise ValueError("Profile missing 'name'.")

        if "weight" not in profile:
            raise ValueError(f"Profile {profile.get('name')} missing 'weight'.")

        if "data" not in profile:
            raise ValueError(f"Profile {profile.get('name')} missing 'data'.")

        data = profile["data"]

        if "first_names" not in data or "last_names" not in data:
            raise ValueError(f"Profile {profile['name']} missing name lists.")

        if not data["first_names"]:
            raise ValueError(f"Profile {profile['name']} has no first names.")

        if not data["last_names"]:
            raise ValueError(f"Profile {profile['name']} has no last names.")

        for entry in data["first_names"] + data["last_names"]:
            if "name" not in entry or "weight" not in entry:
                raise ValueError(f"Invalid name entry in profile {profile['name']}.")