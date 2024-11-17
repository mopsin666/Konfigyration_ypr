import sys
from cli import parse_args
from shell import Shell

def main():
    args = parse_args()
    shell = Shell(args.vfs, args.log, args.script)
    shell.run()

if __name__ == "__main__":
    main()
