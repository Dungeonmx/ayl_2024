import json
import xml.etree.ElementTree as et
import sys
import os

def main() -> int:
    signal = 0
    state = False
    steps_enable = False
    if len(sys.argv) > 4:
        print("Error, demasiados argumentos!")
        signal = 1
    elif len(sys.argv) < 3:
        print("Error, faltan argumentos!")
    else:
        # match sys.argv[len(sys.argv) - 1]:
        #     case "-s":
        #         steps_enable = True
        #     case "--steps":
        #         steps_enable = True
        #     case "-ns":
        #         steps_enable = False
        #     case "--nonsteps":
        #         steps_enable = False
        #     case _:
        #         print("Error: argumento invalido!")
        #         signal = 1


        if len(sys.argv) == 3:
            state = turing_machine(sys.argv[1], sys.argv[2])
            print(f"Resutaldo : {state}")
        else:
            state = turing_machine(sys.argv[1], sys.argv[2], int(sys.argv[3]))
            print(f"Resutaldo : {state}")
    

    return signal

def xml_to_dictionary(path: str) -> dict:
    automaton = {
        "Q": [],
        "Sigma": [],
        "Gamma": [],
        "Delta": {},
        "B": "#",
        "q0": "",
        "F": ""
    }

    with open(path, "r") as f:
        root = et.fromstring(f.read())

        # agregar las funciones
        for states in root.iter("state"):
            automaton["Q"].append(states.get("name"))

            if states.find("initial") is not None:
                automaton["q0"] = states.get("name")

            if states.find("final") is not None:
                automaton["F"] = states.get("name")

        for transitions in root.iter("transition"):
            instruction = {}
            for instructions in transitions:
                match instructions.tag:
                    case "from":
                        instruction["from"] = automaton["Q"][int(instructions.text)]
                    case "to":
                        instruction["to"] = automaton["Q"][int(instructions.text)]
                    case "read":
                        if instructions.text is None:
                            instruction["read"] = "#"
                        else:
                            instruction["read"] = instructions.text

                        if not(instructions.text in automaton["Gamma"]):
                            automaton["Gamma"].append(instruction["read"])
                    case "write":
                        if instructions.text is None:
                            instruction["write"] = "#"
                        else:
                            instruction["write"] = instructions.text

                        if not(instructions.text in automaton["Gamma"]):
                            automaton["Gamma"].append(instruction["write"])
                    case "move":
                        instruction["move"] = instructions.text.lower()

            # verifico si existe, porque no se pueden crear dos keys anidadas al mismo timepo
            if not (instruction["from"] in automaton["Delta"].keys()):
                automaton["Delta"][instruction["from"]] = {}

            automaton["Delta"][instruction["from"]][instruction["read"]] = {
                "q": instruction["to"],
                "e": instruction["write"],
                "m": instruction["move"]
            }

        automaton["Sigma"] = automaton["Gamma"].copy()
        #se hace una copia porque o sino cuando elimino a # se elimina de Gamma
        #tambien
        if "#" in automaton["Sigma"]:
            automaton["Sigma"].remove("#")

    return automaton

def json_to_dictionary(path: str) -> dict:
    with open(path, "r") as f:
        dictionary = json.loads(f.read())
    return dictionary

def turing_machine(path: str, string: str, numb: int = 4, steps_enable: bool = False) -> bool:
    automaton = {}
    state = False
    list_string = []
    pos = 0
    step = 0

    if os.path.splitext(path)[1] == ".json":
        automaton = json_to_dictionary(path)
    elif os.path.splitext(path)[1] == ".jff":
        automaton = xml_to_dictionary(path)
    else:
        print("Error: la archivo no coinside con un formato valido")

    for i in range(numb):
        list_string.append(automaton["B"])

    for i in string:
        list_string.append(i)

    for i in range(numb):
        list_string.append(automaton["B"])

    while list_string[pos] == automaton["B"]:
        pos += 1

    p = automaton["q0"]
    e = ""
    fp = automaton["F"]

    if fp == "":
        steps_enable = True

    print(f"Comienzo")
    print_step(list_string, p, pos)
    
    while p != fp and (list_string[pos] in automaton["Delta"][p].keys()):
        e = list_string[pos]
        list_string[pos] = automaton["Delta"][p][e]["e"]
        match automaton["Delta"][p][e]["m"]:
            case "r":
                pos += 1
            case "l":
                pos -= 1
            case "s":
                pass
        p = automaton["Delta"][p][e]["q"]

        step += 1
        print(f"Paso {step}")
        print_step(list_string, p, pos)

        if steps_enable:
            inp = input()
            if inp == "q":
                p = fp


    if p != fp:
        state = False
    else:
        state = True

    return state

def print_step(string: list, ap: str, pos: str):
    text = ""
    pos_text = ""
    p = 0
    print(f"proceso actual: {ap}\n")
    for i in string:
        if p == pos:
            pos_text += "^"
        else:
            pos_text += " "
        text += i
        p += 1

    print(text)
    print(pos_text)
    print("\n")


if __name__ == "__main__":
    main()
