import json

def json_to_dictionary(path):
    with open(path, "r") as f:
        dictionary = json.loads(f.read())
    return dictionary

def main() -> bool:
    print(json_to_dictionary("turing.json")["Delta"])
    return True

if __name__ == "__main__":
    main()