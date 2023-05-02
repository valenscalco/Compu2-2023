import os
import sys
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", required=True, help="Archivo a procesar")
    args = parser.parse_args()
    file_name = args.file

    # Abro archivo, si no lo encuentra, salta error
    try:
        with open(file_name) as file:
            lines = file.readlines()
            file.close
    except OSError:
        print("No such file or directory: ", file_name)
        sys.exit()

    # Creo pipes y agrego en las listas de read y write respectivamente
    rpipe = []
    wpipe = []
    r0, w0 = os.pipe()
    for i in range(len(lines)):
        r, w = os.pipe()
        rpipe.append(r)
        wpipe.append(w)

    # Creo hijos, separo lineas, doy vuelta las oraciones y las envio
    for j in range(len(lines)):
        pid = os.fork()
        if pid == 0:
            pipe = os.fdopen(rpipe[j])
            while True:
                read = pipe.readline()
                if (len(read) != 0):
                    read = str(read)[:-1]
                    read_split = read.split("-")[1]
                    invert = read_split[::-1]
                    separate_invert = read_split[0] + "-" + invert + "\n"
                    os.write(w0, separate_invert.encode("utf-8"))
                    pipe.close()
                    os._exit(0)

    # Leo, separo y escibo las oraciones en la lista de pipe
    for i in range(len(lines)):
        line_content = str(i) + "-" + lines[i] + "\n"
        os.write(wpipe[i], line_content.encode("utf-8"))

    # Leo, decodifico y divido para que cada linea me quede dentro de la lista como un elemento distinto
    for i in range(len(lines)):
        os.wait()
    read = os.read(r0, 1000)
    read = read.decode()
    read_split = read.split("\n")
    invert_list = []
    for content in read_split:
        if (len(content) != 0):
            content = content.split("-")
            invert_list.append(content[1])
    # Imprimo las oraciones invertidas
    for sentence in invert_list:
        print(sentence)


if __name__ == '__main__':
    main()
