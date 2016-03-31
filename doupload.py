import qiniuUpload


def get():
    return input("Drag your images here,or input 'q' to exit:")


def do():
    path = get()
    path = path.rstrip()
    if path == 'q' or path == 'quit' or path == 'exit':
        exit("Bye")
    else:
        qiniuUpload.upload(path)
        do()


do()
