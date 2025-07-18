import argparse
from pathlib import Path

from pylift.classes.day import Day
from pylift.classes.exercise_type import ExerciseType
import pylift.dashboard as ds
from pylift.input.markdown import read_markdown
from pylift.utils.dir import get_data_dir

# my markdown: "/home/richard/Documents/Obsidian/Personal/03-Areas/Exercise.md"


def parse_markdown(input_file: Path, database_path: Path, *, verbose: bool) -> None:
    print(f"Parsing '{input_file}' into '{database_path}'...")
    if verbose:
        print(" (Verbose output enabled)")
    my_days = read_markdown(input_file)
    exercises = ExerciseType.read(database_path / "exercises.json")
    for d in my_days:
        Day.save(d, exercises, database_path)


def serve_dashboard(database_path: Path, host: str, port: str, *, debug: bool) -> None:
    print(f"Starting web app from '{database_path}' on {host}:{port}...")
    if debug:
        print(" (Debug mode enabled)")
    ds.run_dashboard(database_path, host, port, debug=debug)


def main() -> None:
    parser = argparse.ArgumentParser(description="A tool to manage workout data.")

    # Create subparsers for distinct commands
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Parser for the 'parse' command
    parse_parser = subparsers.add_parser("parse", help="Parse a markdown file into the database.")
    parse_parser.add_argument("input", type=Path, help="Path to the markdown input file.")
    parse_parser.add_argument(
        "-d",
        "--database",
        type=Path,
        default=get_data_dir(),
        help=f"Path to the SQLite database file. (default: {get_data_dir()})",
    )
    parse_parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Enable progress updates during parsing. (default: False)",
    )

    # Parser for the 'serve' command
    serve_parser = subparsers.add_parser("serve", help="Render a web app to display statistics.")
    serve_parser.add_argument(
        "-d",
        "--database",
        type=Path,
        default=get_data_dir(),
        help=f"Path to the SQLite database file. (default: {get_data_dir()})",
    )
    serve_parser.add_argument(
        "--host",
        default="127.0.0.1",
        help="Host address to bind the web server to. (default: 127.0.0.1)",
    )
    serve_parser.add_argument(
        "--port", type=str, default=8000, help="Port number to listen on. (default: 8000)",
    )
    serve_parser.add_argument(
        "--debug", action="store_true", help="Enable debug mode for the web app.",
    )

    args = parser.parse_args()

    if args.command == "parse":
        parse_markdown(args.input, args.database, verbose=args.verbose)
    elif args.command == "serve":
        serve_dashboard(args.database, args.host, args.port, debug=args.debug)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
