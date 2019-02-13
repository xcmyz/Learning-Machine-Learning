import sys
import json
import widget
import preprocessing
import desion_tree

if __name__ == "__main__":

    # app = widget.QtWidgets.QApplication(sys.argv)
    # window = widget.mywindow()
    # window.show()
    # sys.exit(app.exec_())

    # str_1 = input()
    # list_symptom = [str_1]
    # file_tree = "./tree/decision_tree.json"
    # tree_test = desion_tree.Decision_Tree(ifload=True, file_name=file_tree)
    # preprocessing.test(list_symptom, tree_test)

    # with open("./data/9939jbks.json", "r", encoding="utf-8") as file_ks:
    #     ks = json.load(file_ks)

    # str_2 = input()
    # for ele in ks:
    #     if ele["病名"] == str_2:
    #         print(ele["挂号科室"])
    #         break

    app = widget.QtWidgets.QApplication(sys.argv)
    window = widget.mywindow()
    window.show()
    sys.exit(app.exec_())
