import aiml
import os
import translator
import widget
import sys


def main():

    # mybot = aiml.Kernel()
    # mybot.learn("std-startup.xml")
    # mybot.respond('load aiml b')

    # app = widget.QtWidgets.QApplication(sys.argv)
    # window = widget.mywindow()
    # window.show()
    # sys.exit(app.exec_())

    # while True:
    #     mes = input(">>> ")
    #     if mes == "q"or mes == "quit":
    #         break
    #     else:
    #         # print(mes)
    #         mes = translator.translator(mes, fromLang = "ch", toLang = "en")
    #         # print("[ ", mes, " ]")
    #         get = mybot.respond(mes)
    #         get = translator.translator(get)
    #         print("bot: ", get)

    app = widget.QtWidgets.QApplication(sys.argv)
    window = widget.mywindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":

    main()
