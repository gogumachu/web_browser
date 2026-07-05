import socket
import ssl


class URL:
    def __init__(self, url: str):
        # split 된 결과가 차례로 scheme, url 에 할당된다.
        self.scheme, url = url.split("://", 1)
        assert self.scheme in ["http", "https"]
        if "/" not in url:
            url = url + "/"
        self.host, url = url.split("/", 1)
        self.path = "/" + url
        self.port = self.get_basic_port(self.scheme)
        if ":" in self.host:
            self.host, port = self.host.split(":", 1)
            self.port = int(port)

    def get_basic_port(self, scheme):
        if scheme == "https":
            return 443
        elif scheme == "http":
            return 80

    def request(self):
        # 소켓 생성
        s = socket.socket(
            family=socket.AF_INET, type=socket.SOCK_STREAM, proto=socket.IPPROTO_TCP
        )
        # 소켓 연결
        s.connect((self.host, self.port))
        # 소켓 연결 후 wrapping 해야 한다. TCP 소켓 위에서 SSL 이 수행되기 때문이다.
        if self.scheme == "https":
            ctx = ssl.create_default_context()
            s = ctx.wrap_socket(s, server_hostname=self.host)
        # 요청
        request = "GET {} HTTP/1.0\r\n".format(self.path)
        request += "Host: {}\r\n".format(self.host)
        # 반드시 한번 더 개행을 넣어야 한다.
        request += "\r\n"
        # print("request is: ", request)
        s.send(request.encode("utf8"))

        # 응답
        response = s.makefile("r", encoding="utf8", newline="\r\n")
        statusline = response.readline()
        version, status, explanation = statusline.split(" ", 2)

        response_headers = {}
        while True:
            line = response.readline()
            if line == "\r\n":
                break
            header, value = line.split(":", 1)
            # 헤더는 대소문자 구분을 하지 않으므로 소문자로 변환한다.
            response_headers[header.casefold()] = value.strip()
            assert "transfer-encoding" not in response_headers
            assert "content-encoding" not in response_headers
            # print("header is: ", response_headers)
            # print("\n")
        body = response.read()
        s.close()
        return body
