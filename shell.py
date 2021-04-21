from kernell import run

while True:
    # print("########################################")
    text = input("> ")
    result, error = run(text)
    if error: print(error)
    else: print(result)