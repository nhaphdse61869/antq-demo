from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from UI.ResultFrame import *
from UI.Table import *
from util.logging import LogIO
from figure.chart import *
import sys

class UILog(QWidget):

    def __init__(self):
        super().__init__()
        self.list_selected_log = []
        containerLayout = QHBoxLayout()
        leftConLayout = QVBoxLayout()
        rightConLayout = QVBoxLayout()
        leftConLayout.setSizeConstraint(QLayout.SetFixedSize)
        #leftConLayout.re
        containerLayout.addLayout(leftConLayout)
        containerLayout.addLayout(rightConLayout)
        #leftConLayout.setGeometry(QRect(0, 0, 0, 600))
        topLeftConLayout = QHBoxLayout()
        self.botLeftConlayout = QHBoxLayout()
        self.chartContainer = QScrollArea()
        leftConLayout.addLayout(topLeftConLayout)
        leftConLayout.addLayout(self.botLeftConlayout)
        self.logListTree = ResultFrame(self)
        self.tableLog = TableLog(self, remove_log_function=self.remove_list_log)
        self.tableLog.setMinimumSize(1000,300)

        formContainer = QGroupBox()
        formContainerLayout = QHBoxLayout()
        addToTableBtn = QPushButton("Add to Table")
        addToTableBtn.setStyleSheet("box-shadow: 0 12px 16px 0 rgba(0,0,0,0.24), 0 17px 50px 0 rgba(0,0,0,0.19);")
        compareBtn = QPushButton("Compare")
        formContainerLayout.addWidget(addToTableBtn)
        formContainerLayout.addWidget(compareBtn)
        formContainer.setLayout(formContainerLayout)

        rightConLayout.addWidget(self.logListTree)
        rightConLayout.addWidget(formContainer)
        topLeftConLayout.addWidget(self.tableLog)
        self.botLeftConlayout.addWidget(self.chartContainer)
        self.setLayout(containerLayout)
        addToTableBtn.clicked.connect(self.selectLog)
        compareBtn.clicked.connect(self.compareLogs)

    def remove_list_log(self, index):
        del self.list_selected_log[index]

    def testCurrentPos(self):
        qm = QMessageBox
        qm.information(self, "", str(self.logListTree.currentKey))

    def selectLog(self):
        log_key = self.logListTree.currentKey
        duplicated = False
        for i in range(len(self.list_selected_log)):
            if self.list_selected_log[i].key == int(log_key):
                duplicated = True
        if duplicated == False:
            log_io = LogIO()
            select_log = log_io.get_log(int(log_key))
            self.tableLog.addTableItem(select_log)
            self.list_selected_log.append(select_log)

    def compareLogs(self):
        #Check number of cluster
        is_same_number_cluster = True
        for i in range(len(self.list_selected_log) - 1):
            for j in range(i + 1, len(self.list_selected_log)):
                if self.list_selected_log[i].parameter["number_of_cluster"] != self.list_selected_log[j].parameter["number_of_cluster"]:
                    is_same_number_cluster = False

        if is_same_number_cluster == False:
            error = QMessageBox()
            error.critical(self, "Not same number cluster", "Error", QMessageBox.Ok)

        #Clear compare chart
        for i in reversed(range(self.botLeftConlayout.count())):
            self.botLeftConlayout.itemAt(i).widget().setParent(None)

        #Check if it is same algorithm
        is_same_algorithm = True
        for i in range(len(self.list_selected_log) - 1):
            for j in range(i + 1, len(self.list_selected_log)):
                if self.list_selected_log[i].algorithm != self.list_selected_log[j].algorithm:
                    is_same_algorithm = False

        if is_same_algorithm:

            algorithm = self.list_selected_log[0].algorithm
            if algorithm == "AntQ" or algorithm == "ACO":
                self.compareChart = MultiLengthChartCanvas(number_of_chart=3, list_chart_name=["Best Length", "Average Length", "Deviation"])
                for i in range(len(self.list_selected_log)):
                    list_iteration = self.list_selected_log[i].result["list_iteration"]
                    list_best_len = self.list_selected_log[i].result["list_best_len"]
                    list_avg = self.list_selected_log[i].result["list_avg"]
                    list_deviation = self.list_selected_log[i].result["list_deviation"]
                    self.compareChart.add_new_line(0, list_iteration, list_best_len)
                    self.compareChart.add_new_line(1, list_iteration, list_avg)
                    self.compareChart.add_new_line(2, list_iteration, list_deviation)
            elif algorithm == "Simulated Annealing":
                self.compareChart = MultiLengthChartCanvas(number_of_chart=1)
                for i in range(len(self.list_selected_log)):
                    list_iteration = self.list_selected_log[i].result["list_iteration"]
                    list_best_len = self.list_selected_log[i].result["list_best_len"]
                    self.compareChart.add_new_line(0, list_iteration, list_best_len)
        else:
            try:
                number_of_dataset = 1
                log_algorithms = []
                logs_algorithm = [0 for x in range(len(self.list_selected_log))]
                logs_algorithm_index = [0 for x in range(len(self.list_selected_log))]
                type_of_algorithm = {}
                logs_dataset = [0 for x in range(len(self.list_selected_log))]

                # Check dataset
                for i in range(1, len(self.list_selected_log)):
                    have_dataset = False
                    for j in range(i):
                        # Checking dataset
                        if self.list_selected_log[j].dataset["distance_matrix"] == self.list_selected_log[i].dataset[
                            "distance_matrix"]:
                            have_dataset = True
                            logs_dataset[i] = logs_dataset[j]

                    # Set dataset
                    if have_dataset == False:
                        number_of_dataset += 1
                        logs_dataset[i] = number_of_dataset - 1

                # Init algorithm
                for i in range(len(self.list_selected_log)):
                    logs_algorithm[i] = self.list_selected_log[i].algorithm + " 1"
                    type_of_algorithm[self.list_selected_log[i].algorithm] = 0

                log_algorithms.append(logs_algorithm[0])
                logs_algorithm_index.append(0)
                type_of_algorithm[logs_algorithm[0]] = 1

                # Check algorithm
                for i in range(1, len(self.list_selected_log)):
                    create_new_algorithm = True
                    current_number = 1
                    # Check each number of this algorithm
                    while create_new_algorithm and current_number <= type_of_algorithm[
                            self.list_selected_log[i].algorithm]:
                        temp_algorithm = self.list_selected_log[i].algorithm + " " + str(current_number)
                        same_dataset = False
                        same_algorithm = False
                        for j in range(i):
                            if temp_algorithm == logs_algorithm[j] and logs_dataset[i] == logs_dataset[j]:
                                same_dataset = True
                                same_algorithm = True
                            elif temp_algorithm == logs_algorithm[j] and logs_dataset[i] != logs_dataset[j]:
                                same_algorithm = True

                        if same_algorithm and same_dataset == False:
                            create_new_algorithm = False
                        else:
                            create_new_algorithm = True

                        if create_new_algorithm == False:
                            logs_algorithm[i] = temp_algorithm
                            logs_algorithm_index[i] = 0
                            for j in range(len(log_algorithms)):
                                if log_algorithms[j] == temp_algorithm:
                                    logs_algorithm_index[i] = j
                        else:
                            current_number += 1

                    if create_new_algorithm:
                        temp_algorithm = self.list_selected_log[i].algorithm + " " + str(current_number)
                        logs_algorithm[i] = temp_algorithm
                        log_algorithms.append(temp_algorithm)
                        type_of_algorithm[self.list_selected_log[i].algorithm] = current_number
                        logs_algorithm_index[i] = len(log_algorithms) - 1

                # Convert to algorithm data
                data_of_algorithm = [[0 for x in range(number_of_dataset)] for y in range(len(log_algorithms))]
                for i in range(len(self.list_selected_log)):
                    data_of_algorithm[logs_algorithm_index[i]][logs_dataset[i]] = self.list_selected_log[i].result["best_length"]

                # Draw graph
                self.compareChart = ColumnChartCanvas()
                self.compareChart.create_bar(number_of_dataset, data_of_algorithm, log_algorithms)
                pass
            except:
                (type, value, traceback) = sys.exc_info()
                sys.excepthook(type, value, traceback)
                pass


        #Add chart to container
        self.botLeftConlayout.addWidget(self.compareChart)
        #self.botLeftConlayout.addWidget(self.chartContainer)



