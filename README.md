# Simple Web Browser

A basic web browser implementation in Python that fetches and displays web pages.

## Features

- HTTP and HTTPS support
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
```

## Project Structure

- `main.py` - Entry point and HTML rendering logic
- `url.py` - URL class for handling HTTP/HTTPS requests

## Implementation Details

- Uses Python sockets for network connections
- SSL/TLS support for HTTPS
- HTTP/1.1 protocol with Host, Connection, and User-Agent headers
- Simple text renderer that strips HTML tags
