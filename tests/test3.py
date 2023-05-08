import keyboard

x = 0

def printnumber():
    print(x)

keyboard.add_hotkey('g', printnumber)

while True:
    x += 1