import re


def convert(input_file_path: str, output_file_path: str) -> None:
    """
    :param input_file_path: csv input file
    :param output_file_path: csv output file
    :return:
    """
    group = r"^(.*),(.*),(.*),(.*),(.*),(.*),(.*),(.*),(.*)$"

    group = re.compile(group)

    email = r"@[!#$%&'*+-/=?^_`{|}~\w]*\.\w*(\.\w*)?"

    email = re.compile(email)

    with open(input_file_path, "r") as inputf, open(output_file_path, "w") as outputf:
        new_text = []
        text = inputf.readlines()
        #text = re.sub(email, "@ing.unlpam.edu.ar", text)
        #print(text)
        for line in text:
            format_line = group.match(line)
            new_text.append("{},{},{},{},{},{},{},{}\n".format(
                format_line.group(1),
                format_line.group(3),
                format_line.group(2),
                email.sub("@ing.unlpam.edu.ar",format_line.group(4)),
                format_line.group(6),
                format_line.group(7),
                format_line.group(8),
                format_line.group(9)
            ))
        print(new_text)
        outputf.writelines(new_text)





if __name__ == '__main__':
    convert("MOCK_DATA.csv", "MOCK_DATA_RESULT.csv")