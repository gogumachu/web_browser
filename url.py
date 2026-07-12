import os
import socket
import ssl
from urllib import response


class URL:
    # 지속적인 connections 을 저장한다.
    connections = {}

    def __init__(self, url: str):
        # split 된 결과가 차례로 scheme, url 에 할당된다.
        self.scheme, url = url.split("://", 1)
        assert self.scheme in ["http", "https", "file"]

        if self.scheme == "file":
            self.path = url
            return

        if "/" not in url:
            url = url + "/"
        self.host, url = url.split("/", 1)
        self.path = "/" + url
        self.port = self.get_basic_port(self.scheme)
        self.request_headers = ""
        if ":" in self.host:
            self.host, port = self.host.split(":", 1)
            self.port = int(port)

    def get_basic_port(self, scheme):
        if scheme == "https":
            return 443
        elif scheme == "http":
            return 80

    def request(self):
        if self.scheme == "file":
            return self.request_file()

        key = (self.host, self.port)
        if key in URL.connections:
            print(f"[DEBUG] Reusing existing connection to {self.host}:{self.port}")
            s = URL.connections[key]
        else:
            print(f"[DEBUG] Creating new connection to {self.host}:{self.port}")
            s = socket.socket(
                family=socket.AF_INET, type=socket.SOCK_STREAM, proto=socket.IPPROTO_TCP
            )
            s.connect((self.host, self.port))
            # 소켓 연결 후 wrapping 해야 한다. TCP 소켓 위에서 SSL 이 수행되기 때문이다.
            if self.scheme == "https":
                ctx = ssl.create_default_context()
                s = ctx.wrap_socket(s, server_hostname=self.host)

        # 요청
        request = "GET {} HTTP/1.1\r\n".format(self.path)
        self.add_request_header("Host", self.host)
        self.add_request_header("Connection", "keep-alive")
        self.add_request_header(
            "User-Agent",
            "Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/604.1.38 (KHTML, like Gecko) Chrome/49.0.2623 Safari/604.1.38 CoherentGT/2.0",
        )
        request += self.request_headers
        # 반드시 한번 더 개행을 넣어야 한다.
        request += "\r\n"
        # print("request is: ", request)
        s.send(request.encode("utf8"))

        # 응답
        response = s.makefile("rb")
        statusline = response.readline().decode("utf8")
        version, status, explanation = statusline.split(" ", 2)

        response_headers = {}
        while True:
            line = response.readline().decode("utf8")
            if line == "\r\n":
                break
            header, value = line.split(":", 1)
            # 헤더는 대소문자 구분을 하지 않으므로 소문자로 변환한다.
            response_headers[header.casefold()] = value.strip()

        print("header is: ", response_headers)
        # assert "transfer-encoding" in response_headers
        # assert "content-encoding" not in response_headers

        # Content-length bytes 만큼 읽는다.
        assert (
            "content-length" in response_headers
        ), "Content-Length header required for keep-alive"

        content_length = int(response_headers["content-length"])
        body = response.read(content_length).decode("utf8")
        print("body is: ", body)
        # 소켓을 닫지 않고 재사용을 위해 연결 풀에 유지
        URL.connections[key] = s
        return body

    def add_request_header(self, header, value):
        self.request_headers += "{}: {}\r\n".format(header, value)

    def request_file(self):
        file_path = self.path

        if os.path.isdir(file_path):
            files = os.listdir(file_path)
            return "Directory listing for {}:\n".format(file_path) + "\n".join(files)
        else:
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
