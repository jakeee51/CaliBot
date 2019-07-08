with open("test.txt", 'r+') as f:
    lines = f.readlines()
    f.seek(0)
    for line in lines:
        line = line.strip('\n')
        if str(line) != "abc":
            print("here")
            f.write(line)
    f.truncate()
