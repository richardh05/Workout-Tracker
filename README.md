# PyLift
**PyLift** is a simple Python tool to help you track and visualize your workouts. It can:

- Parse your workout data from Markdown files
- Save it in a structured database
- Display statistics via a web dashboard

## Installation

### 1. Clone the repository:
```bash
git clone https://github.com/richardh05/pylift.git
cd pylift

### 2. Install dependencies with Poetry
```sh
poetry install
poetry shell
```

## Usage
PyLift provides two main commands: parse and serve.

### 1. Parse a Markdown file
Use this command to read your workout logs from a Markdown file and store them in the database.
```sh
python -m pylift parse /path/to/your/Exercise.md
```

#### Options
- `-d, --database`: Path to the database (default is PyLift’s data directory)
- `-v, --verbose`: Show detailed output during parsing

### 2. Serve the Dashboard
Use this command to view your workout statistics in a web interface.
```sh
python -m pylift serve
```

#### Options
- `-d, --database`: Path to the database (default is PyLift’s data directory)
- `--host`: Host address to bind the server (default `127.0.0.1`)
- `--port`: Port to listen on (default `8000`)
- `--debug`: Enable debug mode

## Example Workflow

1. Record a markdown file with your gym data (docs on the format coming soon)

2. Parse it:
```sh
python -m pylift parse ~/Documents/Obsidian/Personal/03-Areas/Exercise.md -v
```

3. Launch the dashboard:
```sh
python -m pylift serve
```