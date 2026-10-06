import sys
import os
import argparse
import configparser
import json

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

def default_vfs():
    return {
        "name": "root",
        "type": "directory",
        "children": []
    }


def load_vfs(path):
    if not path:
        return default_vfs()

    try:
        with open(path, "r", encoding="utf-8") as file:
            return json.load(file)
    except (OSError, json.JSONDecodeError):
        print("VFS load error")
        return None

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

            if not parts:
                print("Startup script error")
                return False

            result = do_comm(parts, commands)

            if result == "error":
                print("Startup script error")
                return False

            if result == "exit":
                return True

    return True       

def valid_node(node):
    if not isinstance(node, dict) or not isinstance(node.get("name"), str):
        return False

    if node.get("type") == "file":
        return isinstance(node.get("content"), str)

    if node.get("type") == "directory":
        children = node.get("children")

        if not isinstance(children, list):
            return False

        return all(valid_node(child) for child in children)

    return False

def load_vfs(path):
    if not path:
        return default_vfs()

    try:
        with open(path, "r", encoding="utf-8") as file:
            vfs = json.load(file)
    except (OSError, json.JSONDecodeError):
        print("VFS load error")
        return None

    if not valid_node(vfs):
        print("VFS format error")
        return None

    return vfs

def main():
    args = parse_args()

    config = read_config(args.config)
    config_vfs, config_startup = get_config_values(config)

    vfs_path, startup = priority(
        args,
        config_vfs,
        config_startup
    )

    vfs = load_vfs(vfs_path)

    if vfs is None:
        return 1

    if vfs_path:
        vfs_name = os.path.basename(vfs_path)
    else:
        vfs_name = "default-vfs"

    print("Параметры запуска:")
    print(f"VFS: {vfs_path or 'default'}")
    print(f"Стартовый скрипт: {startup}")
    print(f"Конфигурационный файл: {args.config}")

    if startup:
        run_startup(startup, vfs_name)

    return run(vfs_name)

if __name__ == "__main__":
    main()