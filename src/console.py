import sys
import os

def parse_command(line):
    parts = []
    word = []
    quotes = False

    for i in line:
        if i == '"':
            quotes = not quotes

        elif i == " " and quotes == False:
            if word:
                value = "".join(word)
                parts.append(env_var(value))
                word = []

        else:
            word.append(i)

    if check_error(quotes):
        return []

    if word:
        value = "".join(word)
        parts.append(env_var(value))

    return parts

def env_var(word):
    if word and word[0] == "$":
        name = word[1:]

        if name == "HOME":
            return os.path.expanduser("~")
        
        return os.environ.get(name, "")

    return word

def check_error(quotes):
    if quotes:
        print("Quotes error")
        return True
    return False

def cmd(command, args):
    print(command, *args)


def run(vfs_name):
    commands = {
        "ls": cmd,
        "cd": cmd
    }
    while True:
        line = input(f"{vfs_name}>")
        parts = parse_command(line)

        if not parts:
            continue

        command = parts[0]
        args = parts[1:]

        if command == "exit":
            break

        if command in commands:
            commands[command](command, args)

        else:
            print("Wrong command")
        

def main():
    if len(sys.argv) != 2:
        print("console.py <VFS name>")
        return 1

    vfs_name = sys.argv[1]

    return run(vfs_name)

if __name__ == "__main__":
    main()