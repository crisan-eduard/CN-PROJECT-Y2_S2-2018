def create_text_file(filename):
    try:
        target_file = open(filename + ".txt", "w")
        target_file.close()
    except:
        print("Error creating file" + filename + ".txt")
        exit(1)


def append_line_to_file(line, filename):
    try:
        target_file = open(filename, "a")
        target_file.write(line + '\n')
        target_file.close()
    except:
        print("Error appending to file" + filename + ".txt")
        exit(1)


def read_delete_line(file):
    try:

        source_file = open(file, "r")
        # readlock.acquire()
        line = source_file.readline()
        # print(line)
        try:

            lines = source_file.readlines()
            # printlock.acquire()
            target_file = open(file, "w")
            # for line in lines:
            target_file.writelines(lines)
            # printlock.release()
            target_file.close()
        except:
            print("Error writing file")
            exit(1)

        try:
            target_file_2 = open(file, "a")
            target_file_2.write(line)
            target_file_2.close()
        except:
            print("error re-writing in file")
            exit(1)
        # readlock.release()
        source_file.close()
        return line
    except:
        print("error opening file")
        exit(1)


def file_contains_line(filename, findline):
    try:
        source_file = open(filename, "r")
        lines = source_file.readlines()
        for line in lines:
            if line == findline:
                source_file.close()
                return True
        source_file.close()
        return False
    except:
        print("Error opening file to find line" + filename)
        exit(1)


def empty_file(filename):
    try:
        target_file = open(filename, "w")
        target_file.write("")
        target_file.close()
    except:
        print("Error emptying file" + '\n')
        exit(1)