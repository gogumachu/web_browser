from url import URL


def load(url):

    body = url.request()

    if url.scheme == "file":
        print("File content:")
        print(body)
    else:
        show(body)


def show(body):
    in_tag = False
    for c in body:
        if c == "<":
            in_tag = True
        elif c == ">":
            in_tag = False
        elif not in_tag:
            print(c, end="")


if __name__ == "__main__":
    import sys

    load(URL(sys.argv[1]))
