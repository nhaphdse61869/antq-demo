from ui.log.log_managepanel import *
from ui.log.log_comparetable import *
from util.log import LogIO
from ui.figure import *
import sys

class LogWindow(QWidget):

    def __init__(self):
        super().__init__()
        # Variable
        self.list_selected_log = []

        # Main layout
        main_layout = QHBoxLayout()
        
        # Sub layout
        left_layout = QVBoxLayout()
        right_layout = QVBoxLayout()
        
        # Left layout
        left_layout.setSizeConstraint(QLayout.SetFixedSize)

        left_top_layout = QHBoxLayout()
        self.log_table = CompareLogTable(self, removeLogFunction=self.removeListLog)
        self.log_table.setMinimumSize(1000, 300)
        left_top_layout.addWidget(self.log_table)

        self.left_bottom_layout = QHBoxLayout()
        self.chart_container = QScrollArea()
        self.left_bottom_layout.addWidget(self.chart_container)

        left_layout.addLayout(left_top_layout)
        left_layout.addLayout(self.left_bottom_layout)

        # Right layout
        form_container = QGroupBox()
        form_container_layout = QHBoxLayout()
        self.add_to_table_button = QPushButton("Add to Table")
        self.add_to_table_button.setStyleSheet("box-shadow: 0 12px 16px 0 rgba(0,0,0,0.24), 0 17px 50px 0 rgba(0,0,0,0.19);")
        self.compare_button = QPushButton("Compare")
        form_container_layout.addWidget(self.add_to_table_button)
        form_container_layout.addWidget(self.compare_button)
        form_container.setLayout(form_container_layout)

        self.log_list_tree = LogPanel(self)

        right_layout.addWidget(self.log_list_tree)
        right_layout.addWidget(form_container)

        # Connect widget to function
        self.add_to_table_button.clicked.connect(self.addLogToTable)
        self.compare_button.clicked.connect(self.compareSelectedLogs)

        # Add to main layout
        main_layout.addLayout(left_layout)
        main_layout.addLayout(right_layout)
        self.setLayout(main_layout)

    def removeListLog(self, index):
        del self.list_selected_log[index]

    def addLogToTable(self):
        log_key = self.log_list_tree.currentKey
        duplicated = False
        for i in range(len(self.list_selected_log)):
            if self.list_selected_log[i].key == int(log_key):
                duplicated = True
        if duplicated == False:
            log_io = LogIO()
            select_log = log_io.getLog(int(log_key))
            self.log_table.addLogToTable(select_log)
            self.list_selected_log.append(select_log)

    def compareSelectedLogs(self):
        #Check if there aren't selected logs
        if len(self.list_selected_log) == 0:
            error = QMessageBox()
            error.critical(self,"Error", "Please add log to table first", QMessageBox.Ok)
            return

        #Check number of cluster
        is_same_number_cluster = True
        for i in range(len(self.list_selected_log) - 1):
            for j in range(i + 1, len(self.list_selected_log)):
                if self.list_selected_log[i].parameter["number_of_cluster"] != self.list_selected_log[j].parameter["number_of_cluster"]:
                    is_same_number_cluster = False

        if is_same_number_cluster == False:
            error = QMessageBox()
            error.critical(self, "Error", "Not same number cluster", QMessageBox.Ok)
            return

        #Clear compare chart
        for i in reversed(range(self.left_bottom_layout.count())):
            self.left_bottom_layout.itemAt(i).widget().setParent(None)

        #Check if it is same algorithm
        is_same_algorithm = True
        for i in range(len(self.list_selected_log) - 1):
            for j in range(i + 1, len(self.list_selected_log)):
                if self.list_selected_log[i].algorithm != self.list_selected_log[j].algorithm:
                    is_same_algorithm = False

        if is_same_algorithm:
            #Show legend
            algorithm = self.list_selected_log[0].algorithm
            if algorithm == "AntQ" or algorithm == "ACO":
                self.compare_chart = MultiLineChart(number_of_chart=3, list_chart_name=["Best Length", "Average Length", "Standard Deviation"])
                for i in range(len(self.list_selected_log)):
                    list_iteration = self.list_selected_log[i].result["list_iteration"]
                    list_best_len = self.list_selected_log[i].result["list_best_len"]
                    list_avg = self.list_selected_log[i].result["list_avg"]
                    list_deviation = self.list_selected_log[i].result["list_deviation"]
                    self.compare_chart.addNewLine(0, list_iteration, list_best_len)
                    self.compare_chart.addNewLine(1, list_iteration, list_avg)
                    self.compare_chart.addNewLine(2, list_iteration, list_deviation)
            elif algorithm == "Simulated Annealing":
                self.compare_chart = MultiLineChart(number_of_chart=1)
                for i in range(len(self.list_selected_log)):
                    list_iteration = self.list_selected_log[i].result["list_iteration"]
                    list_best_len = self.list_selected_log[i].result["list_best_len"]
                    self.compare_chart.addNewLine(0, list_iteration, list_best_len)
            #Show legend
            list_legend = []
            for i in range(len(self.list_selected_log)):
                list_legend.append(self.list_selected_log[i].key)
            self.compare_chart.setLegend(list_legend)
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
                    logs_algorithm[i] = self.list_selected_log[i].algorithm + " " + str(1)
                    type_of_algorithm[self.list_selected_log[i].algorithm] = 0

                log_algorithms.append(logs_algorithm[0])
                type_of_algorithm[self.list_selected_log[0].algorithm] = 1

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
                self.compare_chart = ColumnChart()
                self.compare_chart.createColumn(number_of_dataset, data_of_algorithm, log_algorithms)
                pass
            except:
                (type, value, traceback) = sys.exc_info()
                sys.excepthook(type, value, traceback)
                pass

        #Add chart to container
        self.left_bottom_layout.addWidget(self.compare_chart)



