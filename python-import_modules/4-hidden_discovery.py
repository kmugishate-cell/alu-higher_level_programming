#!/usr/bin/python3
if __name__ == "__main__":
    names = [name for name in dir(__import__("hidden_4"))
             if not name.startswith("__")]
    for name in sorted(names):
        print(name)
