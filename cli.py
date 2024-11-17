import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="Shell Emulator")
    parser.add_argument('hostname', help="Name of the computer")
    parser.add_argument('vfs', help="Path to the VFS zip archive")
    parser.add_argument('log', help="Path to the log file")
    parser.add_argument('script', help="Path to the startup script")

    return parser.parse_args()
