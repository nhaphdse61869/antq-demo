from PyQt5.QtCore import QThread,pyqtSignal
import util.logging as log

class AddLogThread(QThread):
    load_completed = pyqtSignal(object)

    def __init__(self, selected_list_log, selected_log, parent=None):
        QThread.__init__(parent)
        self.selected_list_log = selected_list_log
        self.selected_log = selected_log

    def run(self):
        #Load from file
        reader = log.LogIO()
        self.selected_log.dataset = reader.get_dataset_by_log_key(self.selected_log.key)
        self.selected_log.result = reader.get_result_by_log_key(self.selected_log.key)


        #Finish load
        self.load_completed.emit(self.selected_log)


class CompareLogThread(QThread):
    compare_completed = pyqtSignal(dict)

    def __init__(self, selected_list_log ,parent=None):
        QThread.__init__(parent)
        self.selected_list_log = selected_list_log

    def run(self):

        self.compare_completed.emit()

