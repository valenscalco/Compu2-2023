import os
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", required=True, help="Archivo a procesar")
    args = parser.parse_args()

    file_name = args.file

    with open(file_name) as file:
        lines = file.readlines()
        file.close

    rpipe = []
    wpipe = []
    r0, w0 = os.pipe()
    for i in range(len(lines)):
        r, w = os.pipe()
        rpipe.append(r)
        wpipe.append(w)

    for j in range(len(lines)):
        pid = os.fork()
        if pid == 0:
            pipe = os.fdopen(rpipe[j])
            while True:
                leido = pipe.readline()
                if (len(leido) != 0):
                    leido = str(leido)[:-1]
                    leido_split = leido.split("-")[1]
                    investedText = leido_split[::-1]
                    returnText = leido_split[0]+"-" + investedText+"\n"
                    os.write(w0, returnText.encode("utf-8"))
                    pipe.close()
                    os._exit(0)

    for i in range(len(lines)):
        texto = str(i)+"-"+lines[i]+"\n"
        os.write(wpipe[i], texto.encode("utf-8"))

    for i in range(len(lines)):
        os.wait()
    leido = os.read(r0, 1000)
    leido = leido.decode()
    leido_split = leido.split("\n")
    invert_list = []

    for text in leido_split:
        if (len(text) != 0):
            text = text.split("-")
            invert_list.append(text[1])

    for sentence in invert_list:
        print(sentence)


if __name__ == '__main__':
    main()
