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
    in_entity = False
    entity = ""

    print("\n============Response body============")

    for c in body:
        if c == "<":
            in_tag = True
        elif c == ">":
            in_tag = False
        elif not in_tag:
            if c == "&":
                in_entity = True
                entity = "&"
            elif in_entity:
                entity += c
                if c == ";":
                    if entity == "&lt;":
                        print("<", end="")
                    elif entity == "&gt;":
                        print(">", end="")
                    else:
                        print(entity, end="")
                    in_entity = False
                    entity = ""
            else:
                print(c, end="")


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        # Interactive mode - 계속 URL 입력 받기
        while True:
            url_input = input("\nEnter URL (or 'quit' to exit): ")
            if url_input.lower() in ["quit", "exit", "q"]:
                break
            try:
                load(URL(url_input))
            except Exception as e:
                print(f"Error: {e}")
    else:
        # Single URL mode
        load(URL(sys.argv[1]))
