# Simple Web Browser

A basic web browser implementation in Python that fetches and displays web pages.

This project is based on https://browser.engineering and implements the exercises and examples from the book to practice building a browser from scratch.

## Features

- HTTP and HTTPS support
- File scheme support (file://) for local files and directories
- Custom URL parsing
- HTTP/1.1 requests with headers
- HTML tag stripping for text display

## Usage

```bash
python main.py <url>
```

Example:
```bash
python main.py http://example.com
python main.py https://www.google.com
python main.py file:///C:/Users/eun/Desktop/test.txt
```

## Project Structure

- `main.py` - Entry point and HTML rendering logic
- `url.py` - URL class for handling HTTP/HTTPS requests

## Implementation Details

- Uses Python sockets for network connections
- SSL/TLS support for HTTPS
- HTTP/1.1 protocol with Host, Connection, and User-Agent headers
- Parses response bodies using either `Transfer-Encoding: chunked` or `Content-Length`
- Keeps TCP connections for reuse when possible (simple keep-alive pool)
- Simple text renderer that strips HTML tags

## Current Limitation

- If an HTTP response has neither `Transfer-Encoding: chunked` nor `Content-Length`, the client raises an error.
