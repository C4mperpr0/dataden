with open("merp01_small.svg", 'w+') as newfile:
    with open("merp01.svg") as file:
        text = file.read()
        text = text.replace('\n', '')
        x = None
        while text != x:
            x = text
            text = text.replace('  ', '')
        newfile.write(text)

with open("merp02_small.svg", 'w+') as newfile:
    with open("merp02.svg") as file:
        text = file.read()
        text = text.replace('\n', '')
        x = None
        while text != x:
            x = text
            text = text.replace('  ', '')
        newfile.write(text)
