import argparse
import sys
import MarkdownLog as ml
import Dashboard as ds
import DatabaseConnector as db
from pathlib import Path
# my markdown: "/home/richard/Documents/Obsidian/Personal/03-Areas/Exercise.md"

def _getDefaultDb() -> Path:
    """
    Finds the user's 'Documents' folder across different operating systems, and returns the 'gym.sqlite' file path.
    """
    if sys.platform == "win32":
        # Windows: Documents folder is usually directly under the user profile
        import ctypes
        from ctypes import wintypes
        CSIDL_PERSONAL = 5       # My Documents
        SHGFP_TYPE_CURRENT = 0   # Get current, not default value
        buf = ctypes.create_unicode_buffer(wintypes.MAX_PATH)
        ctypes.windll.shell32.SHGetFolderPathW(None, CSIDL_PERSONAL, None, SHGFP_TYPE_CURRENT, buf)
        return Path(buf.value) / "gym.sqlite"
    elif sys.platform == "darwin":
        # macOS: Documents is under the user's home directory
        return Path.home() / "Documents" / "gym.sqlite"
    else:
        # Linux/Unix: Documents is usually under the user's home directory
        # This is a common XDG Base Directory specification, but not universally guaranteed.
        # For simplicity, we'll assume it's directly under home for now.
        return Path.home() / "Documents" / "gym.sqlite"


def parse_markdown(input_file:Path, database_path:Path, verbose:bool):
    print(f"Parsing '{input_file}' into '{database_path}'...")
    if verbose:
        print(" (Verbose output enabled)")
    myMD = ml.MarkdownLog(str(input_file))
    myDays = myMD.days
    myWriter = db.DatabaseWriter(str(database_path))
    for d in myDays:
        myWriter.writeDayClass(d)

def serve_dashboard(database_path:Path, host:str, port:int, debug:bool):
    print(f"Starting web app from '{database_path}' on {host}:{port}...")
    if debug:
        print(" (Debug mode enabled)")
    ds.run_dashboard(str(database_path), host, port, debug)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A tool to manage workout data.")

    # Create subparsers for distinct commands
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Parser for the 'parse' command
    parse_parser = subparsers.add_parser("parse", help="Parse a markdown file into the database.")
    parse_parser.add_argument("input", type=Path, help="Path to the markdown input file.")
    parse_parser.add_argument("-d", "--database", type=Path, default=_getDefaultDb(), help=f"Path to the SQLite database file. (default: {_getDefaultDb()})")
    parse_parser.add_argument("-v", "--verbose", action="store_true", help="Enable progress updates during parsing. (default: False)")

    # Parser for the 'serve' command
    serve_parser = subparsers.add_parser("serve", help="Render a web app to display statistics.")
    serve_parser.add_argument("-d", "--database", type=Path, default=_getDefaultDb(), help=f"Path to the SQLite database file. (default: {_getDefaultDb()})")
    serve_parser.add_argument("--host", default="127.0.0.1", help="Host address to bind the web server to. (default: 127.0.0.1)")
    serve_parser.add_argument("--port", type=int, default=8000, help="Port number to listen on. (default: 8000)")
    serve_parser.add_argument("--debug", action="store_true", help="Enable debug mode for the web app.")


    args = parser.parse_args()

    if args.command == "parse":
        parse_markdown(args.input, args.database, args.verbose)
    elif args.command == "serve":
        serve_dashboard(args.database, args.host, args.port, args.debug)
    else:
        parser.print_help()