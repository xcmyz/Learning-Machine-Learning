import aiml
import os
import translator


def main():
    mybot = aiml.Kernel()
    mybot.learn("std-startup.xml")
    mybot.respond('load aiml b')

    print("\n-----------------------------------------\n")
    while True:
        mes = input(">>> ")
        if mes == "q"or mes == "quit":
            break
        else:
            # print(mes)
            mes = translator.translator(mes, fromLang="ch", toLang="en")
            # print("[ ", mes, " ]")
            get = mybot.respond(mes)
            get = translator.translator(get)
            print("bot: ", get)


if __name__ == "__main__":
    main()
