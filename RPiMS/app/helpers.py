def normalize_config_text(text: str):
    normalized = []

    for line in text.splitlines():
        # remove comments
        line = line.split("#", 1)[0]

        # remove whitespace from start and end of file
        line = line.strip()

        # ignore empty lines
        if not line:
            continue

        normalized.append(line)

    # return sorted
    return sorted(normalized)


def file_differs_config(path: str, new_data: str) -> bool:
    # normalize text data
    new_norm = normalize_config_text(new_data)

    try:
        with open(path, "r") as f:
            current_data = f.read()
    except FileNotFoundError:
        return True  # file not exist → the data from the file differ

    # normalize data from file
    current_norm = normalize_config_text(current_data)

    #print("CURRENT:", repr(current_norm))
    #print("NEW    :", repr(new_norm))

    # comparison of lists
    return current_norm != new_norm
