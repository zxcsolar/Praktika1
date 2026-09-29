import sys
import os
import argparse
import configparser

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

def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("--vfs")
    parser.add_argument("--startup")
    parser.add_argument("--config")

    return parser.parse_args()

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

def read_config(path):
    if not path:
        return None
    
    if not os.path.exists(path):
        print("Config read error")
        return None
    
    config = configparser.ConfigParser()

    try:
        config.read(path, encoding="utf-8")
    except Exception:
        print("Config read error")
        return None

    return config

def get_config_values(config):
    if config is None:
        return None, None

    if "emulator" not in config:
        print("Config error")
        return None, None

    vfs = config["emulator"].get("vfs")
    startup = config["emulator"].get("startup")

    return vfs, startup

def priority(args, config_vfs, config_startup):
    if args.vfs:
        vfs = args.vfs
    else:
        vfs = config_vfs

    if args.startup:
        startup = args.startup
    else:
        startup = config_startup

    return vfs, startup

def do_comm(parts, commands):
    command = parts[0]
    args = parts[1:]

    if command == "exit":
        return "exit"

    if command in commands:
        commands[command](command, args)
        return "ok"

    print("Wrong command")
    return "error"


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

        result = do_comm(parts, commands)

        if result == "exit":
            break


def run_startup(path, vfs_name):
    commands = {
        "ls": cmd,
        "cd": cmd
    }

    try:
        file = open(path, "r", encoding="utf-8")
    except OSError:
        print("Startup script read error")
        return False

    with file:
        for line in file:
            line = line.strip()

            if not line:
                continue

            print(f"{vfs_name}>{line}")
            parts = parse_command(line)
            result = do_comm(parts, commands)

            if result == "error":
                print("Startup script error")
                return False

            if result == "exit":
                return True

    return True
        

def main():
    args = parse_args()

    config = read_config(args.config)
    config_vfs, config_startup = get_config_values(config)

    vfs, startup = priority(
        args,
        config_vfs,
        config_startup
    )

    print("Параметры запуска:")
    print(f"VFS: {vfs}")
    print(f"Стартовый скрипт: {startup}")
    print(f"Конфигурационный файл: {args.config}")

    if not vfs:
        print("VFS is not specified")
        return 1

    if startup:
        run_startup(startup, vfs)

    return run(vfs)

if __name__ == "__main__":
    main()