# Static Site Generator

A lightweight static site generator built in Python that turns Markdown content into a polished HTML website. It walks a content directory, converts Markdown into HTML, applies a shared template, and copies static assets into a generated output folder.

## Overview

This project is designed for simple, fast static publishing. Instead of relying on a heavy framework, it uses a small set of Python modules to:

- read Markdown files from a content tree
- convert Markdown into HTML nodes
- inject content into a reusable HTML template
- copy static files such as CSS and images into the output directory

The generated site is written to the docs folder, making it easy to publish or preview locally.

## Features

- Recursive generation of pages from nested content folders
- Markdown-to-HTML conversion with support for:
  - headings
  - bold and italic text
  - inline code
  - links and images
- Automatic page title extraction from the first top-level heading
- Template-based rendering for consistent page structure
- Static asset copying from the static directory
- Simple test suite for parser and rendering behavior

## Project Structure

- content/: source Markdown content for the website
- static/: CSS, images, and other files copied to the output
- src/: Python implementation and tests
  - main.py: build orchestration and file generation
  - mdextractor.py: Markdown parsing and title extraction
  - htmlnode.py, leafnode.py, parentnode.py, blocknode.py, textnode.py: node-based HTML rendering system
- template.html: shared page template
- docs/: generated website output

## Getting Started

### Prerequisites

- Python 3.8+

### Install and Build

From the project root, run:

```bash
python3 -m unittest discover -s src
bash build.sh
```

This will:

1. run the unit tests
2. rebuild the generated site under the docs directory

### Preview the Site

Open the generated files in your browser, for example:

```bash
xdg-open docs/index.html
```

## Usage

The generator reads Markdown files from the content directory and writes HTML pages to docs. Each Markdown file becomes an HTML page with the same folder structure.

If you want to use a custom base path for links and assets (for example when hosting from a subdirectory), pass it as an argument:

```bash
python3 src/main.py "/my-site/"
```

## Development

The project includes a small test suite that exercises parsing and rendering behavior. To run it:

```bash
python3 -m unittest discover -s src
```

If you want to extend the generator, the most relevant place to start is the parser and renderer logic in the src directory.

## Contributing

Contributions are welcome. If you find a bug or want to add a feature, open an issue or submit a pull request with a clear description of the change.

## License

This project does not currently declare a license.