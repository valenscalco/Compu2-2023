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
                leido = pipe.readline()
                if (len(leido) != 0):
                    leido = str(leido)[:-1]
                    leido_split = leido.split("-")[1]
                    investedText = leido_split[::-1]
                    returnText = leido_split[0]+"-" + investedText+"\n"
                    os.write(w0, returnText.encode("utf-8"))
                    pipe.close()
                    os._exit(0)

    # Leo, separo y escibo las oraciones en la lista de pipe
    for i in range(len(lines)):
        line_content = str(i) + "-" + lines[i] + "\n"
        os.write(wpipe[i], line_content.encode("utf-8"))

    # Leo, decodifico y divido para que cada linea me quede dentro de la lista como un elemento distinto
    for i in range(len(lines)):
        os.wait()
    leido = os.read(r0, 1000)
    leido = leido.decode()
    leido_split = leido.split("\n")
    invert_list = []
    for content in leido_split:
        if (len(content) != 0):
            content = content.split("-")
            invert_list.append(content[1])
    # Imprimo las oraciones invertidas
    for sentence in invert_list:
        print(sentence)


if __name__ == '__main__':
    main()
