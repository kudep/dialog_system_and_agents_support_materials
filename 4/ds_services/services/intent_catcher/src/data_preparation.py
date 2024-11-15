import pathlib
import json
import pandas as pd
from tqdm import tqdm
import xeger
import hashlib


def generate_set_of_phrases(template, num=100):
    return set([xeger.Xeger().xeger(template) for _ in range(num)])


def generate_optimized_set_of_phrases(template, num=100):
    intent_set = set()
    continue_flag = True
    while continue_flag:
        intent_num = len(intent_set)
        intent_set |= generate_set_of_phrases(template, num)
        continue_flag = len(intent_set) > intent_num
    return intent_set


def get_file_hash(file_path: pathlib.Path) -> str:
    with file_path.open("rb") as f:
        return hashlib.md5(f.read()).hexdigest()


def load_all_intents_and_tags(dataset_dir: pathlib.Path):
    all_intents = []
    all_tags = []
    intent_scopes = {}
    for json_file in dataset_dir.glob("*.json"):
        with json_file.open() as f:
            data = json.load(f)
            for intent in data.get("intents", []):
                intent_scopes[intent["name"]] = json_file.stem
            all_intents.extend(data.get("intents", []))
            all_tags.extend(data.get("tags", []))
    return all_intents, all_tags, intent_scopes


def get_dir_hash(dir_path: pathlib.Path) -> str:
    hasher = hashlib.md5()
    for json_file in sorted(dir_path.glob("*.json")):
        hasher.update(json_file.name.encode())
        with json_file.open("rb") as f:
            hasher.update(f.read())
    return hasher.hexdigest()


def prepare_dataset(dataset_dir: pathlib.Path, phrases_csv_file: pathlib.Path):
    all_intents, _, __ = load_all_intents_and_tags(dataset_dir)

    dfs = []
    for intent in tqdm(all_intents, desc="Processing intents"):
        phrases = set()
        for phrase in intent["phrases"]:
            phrases |= generate_optimized_set_of_phrases(phrase, num=100)
        dfs.append(pd.DataFrame({"intent": intent["name"], "phrase": list(phrases)}))

    df = pd.concat(dfs)
    df.drop_duplicates(subset=["intent", "phrase"], inplace=True)
    df.to_csv(phrases_csv_file, index=False)

    print(f"Dataset saved to {phrases_csv_file}")
    print(f"Total phrases: {len(df)}")
    print("\nDistribution of intents:")
    print(df.groupby("intent").size())


def update_dataset_if_needed(dataset_dir: pathlib.Path, phrases_csv_file: pathlib.Path) -> bool:
    dir_hash = get_dir_hash(dataset_dir)
    hash_file = phrases_csv_file.with_suffix(".hash")

    if not phrases_csv_file.exists() or not hash_file.exists():
        prepare_dataset(dataset_dir, phrases_csv_file)
        hash_file.write_text(dir_hash)
        return True

    if hash_file.read_text() != dir_hash:
        prepare_dataset(dataset_dir, phrases_csv_file)
        hash_file.write_text(dir_hash)
        return True

    return False
