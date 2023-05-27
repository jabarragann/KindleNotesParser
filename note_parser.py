from typing import List
import pandas as pd
from pathlib import Path
import argparse


class NotesParser:
    def __init__(self):
        self.data_dict = dict(author=[], meta=[], quote=[])

    def is_correctly_formatted(self, entry: List[str]):
        if len(entry) != 5:
            return False
        elif not "===" in entry[-1]:
            return False
        elif not entry[2] == "\n":
            return False
        return True

    def parse_entry(self, entry: List[str]):
        if not self.is_correctly_formatted(entry):
            print(entry)
            raise Exception("Wrong format")
        self.data_dict["author"].append(entry[0].strip())
        self.data_dict["meta"].append(entry[1].strip())
        self.data_dict["quote"].append(entry[3])

    def parse_notes(self, file):
        dst_path = file.parent / f"parsed_{file.name}.csv"
        with open(file, "r", encoding="utf-8") as f:
            lines = f.readlines()
            try:
                for i in range((len(lines)) // 5):
                    new_entry = lines[0 + i * 5 : 5 + i * 5]
                    self.parse_entry(new_entry)
            except Exception as e:
                print(e)

        df = pd.DataFrame(self.data_dict)
        df.to_csv(dst_path, index=False, encoding="utf-8")


if __name__ == "__main__":
    arg = argparse.ArgumentParser(prog="Kindle notes parser")
    arg.add_argument(
        "--input_path", action="store", type=str, required=True, help="path to 'My Clippings.txt'"
    )
    arguments = arg.parse_args()

    file = Path(arguments.input_path)
    if not file.exists():
        print("given file does not exists")

    parser = NotesParser()
    parser.parse_notes(file)
