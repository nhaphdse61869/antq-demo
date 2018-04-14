from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from ui.figure import SingleLineChart


class GraphWP(QWidget):

    def __init__(self):
        super().__init__()
        # Main layout
        self.main_layout = QVBoxLayout()

        # Sub layout
        self.tab_chart_layout = QVBoxLayout()
        self.top_layout = QHBoxLayout()

        # Statistic chart tabs layout
        self.chart_tabs = QTabWidget()
        self.chart1_tab = QWidget()
        self.chart2_tab = QWidget()
        self.chart3_tab = QWidget()
        self.best_length_chart = SingleLineChart(title="Best Length")
        self.mean_length_chart = SingleLineChart(title="Mean Length")
        self.st_deviation_chart = SingleLineChart(title="Standard Deviation")

        self.chart_tabs.addTab(self.chart1_tab, "Best Length")
        self.chart_tabs.addTab(self.chart2_tab, "Mean Length")
        self.chart_tabs.addTab(self.chart3_tab, "Standard Deviation")

        self.chart1_tab.layout = QVBoxLayout()
        self.chart1_tab.setLayout(self.chart1_tab.layout)
        self.chart1_tab.layout.addWidget(self.best_length_chart)

        self.chart2_tab.layout = QVBoxLayout()
        self.chart2_tab.setLayout(self.chart2_tab.layout)
        self.chart2_tab.layout.addWidget(self.mean_length_chart)

        self.chart3_tab.layout = QVBoxLayout()
        self.chart3_tab.setLayout(self.chart3_tab.layout)
        self.chart3_tab.layout.addWidget(self.st_deviation_chart)

        self.tab_chart_layout.addWidget(self.chart_tabs)

        # Top layout
        # Algorithm parameter tabs
        self.algorithm_tabs = QTabWidget()
        self.aco_tab = ACOTab()
        self.sa_tab = SimAnnealTab()
        self.antq_tab = AntQTab()
        self.algorithm_tabs.addTab(self.antq_tab, "Ant-Q")
        self.algorithm_tabs.addTab(self.aco_tab, "ACO")
        self.algorithm_tabs.addTab(self.sa_tab, "Simulated Annealing")

        self.left_top_layout = QVBoxLayout()
        # Function buttons
        self.button_layout = QHBoxLayout()
        self.apply_button = QPushButton("Apply")
        self.run_button = QPushButton("Run")
        self.generate_button = QPushButton("Generate")

        self.left_button_layout = QFormLayout()
        self.left_button_layout.addWidget(self.apply_button)
        self.left_button_layout.addWidget(self.run_button)
        self.right_button_layout = QFormLayout()
        self.right_button_layout.addWidget(self.generate_button)

        self.button_layout.setStretch(10, 10)
        self.button_layout.addLayout(self.left_button_layout)
        self.button_layout.addLayout(self.right_button_layout)

        # Current parameter
        self.param_container = QGroupBox("Current Parameter")
        self.param_layout = QFormLayout()
        self.param_container.setLayout(self.param_layout)

        self.left_top_layout.addLayout(self.button_layout)
        self.left_top_layout.addWidget(self.param_container)

        self.top_layout.addWidget(self.algorithm_tabs)
        self.top_layout.addLayout(self.left_top_layout)

        # Add to main layout
        self.main_layout.addLayout(self.top_layout)
        self.main_layout.addLayout(self.tab_chart_layout)
        self.setLayout(self.main_layout)

class AntQTab(QWidget):

    def __init__(self):
        super().__init__()
        # Main Layout
        self.main_layout = QVBoxLayout()

        # Sub layout
        self.top_para_layout = QVBoxLayout()
        self.bottom_para_layout = QHBoxLayout()

        # Top parameter layout
        self.up_top_para_layout = QHBoxLayout()
        self.down_top_para_layout = QHBoxLayout()
        self.title_num_label = QLabel("Number of Agents:")
        self.num_agent_slider = NumAgentSlider()
        self.num_agent_slider.thresh_sld.valueChanged.connect(self.num_agent_slider.changeValue)
        self.num_text = self.num_agent_slider.k_lbl

        self.up_top_para_layout.addWidget(self.title_num_label)
        self.up_top_para_layout.addWidget(self.num_text)
        self.down_top_para_layout.addWidget(self.num_agent_slider.thresh_sld)

        self.top_para_layout.addLayout(self.up_top_para_layout)
        self.top_para_layout.addLayout(self.down_top_para_layout)

        # Bottom parameter layout
        self.left_bottom_para_layout = QGridLayout()
        self.right_bottom_para_layout = QVBoxLayout()

        self.form_container1 = QGroupBox("Weight Relative")
        self.form_layout1 = QFormLayout()
        self.delta_spin = QSpinBox()
        self.delta_spin.setMinimum(0)
        self.delta_spin.setMaximum(101)
        self.delta_spin.setValue(1)
        self.form_layout1.addRow(QLabel("δ:"), self.delta_spin)
        self.beta_spin = QSpinBox()
        self.beta_spin.setMinimum(0)
        self.beta_spin.setMaximum(100)
        self.beta_spin.setValue(2)
        self.form_layout1.addRow(QLabel("β:"), self.beta_spin)
        self.form_container1.setLayout(self.form_layout1)

        self.form_container2 = QGroupBox("Learning Rate")
        self.form_layout2 = QFormLayout()
        self.learning_rate_spin = QSpinBox()
        self.learning_rate_spin.setMinimum(0)
        self.learning_rate_spin.setMaximum(100)
        self.learning_rate_spin.setValue(10)
        self.form_layout2.addRow(QLabel("α:"), self.learning_rate_spin)
        self.form_container2.setLayout(self.form_layout2)

        self.form_container3 = QGroupBox("Discount Factor")
        self.form_layout3 = QFormLayout()
        self.discount_factor_spin = QSpinBox()
        self.discount_factor_spin.setMinimum(0)
        self.discount_factor_spin.setMaximum(100)
        self.discount_factor_spin.setValue(30)
        self.form_layout3.addRow(QLabel("ϒ:"), self.discount_factor_spin)
        self.form_container3.setLayout(self.form_layout3)

        self.form_container4 = QGroupBox("Balance Rate")
        self.form_layout4 = QFormLayout()
        self.balance_rate_spin = QSpinBox()
        self.balance_rate_spin.setMinimum(0)
        self.balance_rate_spin.setMaximum(100)
        self.balance_rate_spin.setValue(90)
        self.form_layout4.addRow(QLabel("BR:"), self.balance_rate_spin)
        self.form_container4.setLayout(self.form_layout4)

        self.form_container5 = QGroupBox("Iteration")
        self.form_layout5 = QFormLayout()
        self.iteration_spin = QSpinBox()
        self.iteration_spin.setMinimum(0)
        self.iteration_spin.setMaximum(1000)
        self.iteration_spin.setValue(200)
        self.form_layout5.addRow(QLabel("Iter:"), self.iteration_spin)
        self.form_container5.setLayout(self.form_layout5)

        self.form_container6 = QGroupBox("Clustering")
        self.form_layout6 = QFormLayout()
        self.k_num_spin = QSpinBox()
        self.k_num_spin.setMinimum(1)
        self.k_num_spin.setValue(1)
        self.k_num_spin.setMaximum(1000)
        self.form_layout6.addRow(QLabel("K nums:"), self.k_num_spin)
        self.form_container6.setLayout(self.form_layout6)

        self.form_container7 = QGroupBox("Delayed Reinforcement")
        self.form_layout7 = QFormLayout()
        self.dr_combobox = QComboBox()
        self.dr_combobox.addItem("Iter")
        self.dr_combobox.addItem("Global")
        self.form_layout7.addRow(QLabel("DR:"), self.dr_combobox)
        self.form_container7.setLayout(self.form_layout7)

        self.left_bottom_para_layout.addWidget(self.form_container1, 0, 0)
        self.left_bottom_para_layout.addWidget(self.form_container4, 0, 1)
        self.left_bottom_para_layout.addWidget(self.form_container3, 1, 0)
        self.left_bottom_para_layout.addWidget(self.form_container2, 1, 1)

        self.right_bottom_para_layout.addWidget(self.form_container5)
        self.right_bottom_para_layout.addWidget(self.form_container6)
        self.right_bottom_para_layout.addWidget(self.form_container7)

        self.bottom_para_layout.addLayout(self.left_bottom_para_layout)
        self.bottom_para_layout.addLayout(self.right_bottom_para_layout)

        # Add to main layout
        self.main_layout.addLayout(self.top_para_layout)
        self.main_layout.addLayout(self.bottom_para_layout)
        self.setLayout(self.main_layout)

class ACOTab(QWidget):

    def __init__(self):
        super().__init__()
        # Main layout
        self.main_layout = QVBoxLayout()

        # Sub layout
        self.top_layout = QVBoxLayout()
        self.bottom_layout = QHBoxLayout()

        # Top parameter layout
        self.up_top_layout = QHBoxLayout()
        self.down_top_layout = QHBoxLayout()

        self.title_num_label = QLabel("Number of Agents:")
        self.num_agent_slider = NumAgentSlider()
        self.num_agent_slider.thresh_sld.valueChanged.connect(self.num_agent_slider.changeValue)
        self.num_text = self.num_agent_slider.k_lbl
        self.up_top_layout.addWidget(self.title_num_label)
        self.up_top_layout.addWidget(self.num_text)
        self.down_top_layout.addWidget(self.num_agent_slider.thresh_sld)

        self.top_layout.addLayout(self.up_top_layout)
        self.top_layout.addLayout(self.down_top_layout)

        # Bottom parameter layout
        self.left_bottom_layout = QVBoxLayout()
        self.right_bottom_layout = QVBoxLayout()

        self.form_container1 = QGroupBox("Weight Relative")
        self.form_layout1 = QFormLayout()
        self.delta_spin = QSpinBox()
        self.delta_spin.setMinimum(0)
        self.delta_spin.setMaximum(101)
        self.delta_spin.setValue(1)
        self.form_layout1.addRow(QLabel("δ:"), self.delta_spin)
        self.beta_spin = QSpinBox()
        self.beta_spin.setMinimum(0)
        self.beta_spin.setMaximum(100)
        self.beta_spin.setValue(2)
        self.form_layout1.addRow(QLabel("β:"), self.beta_spin)
        self.form_container1.setLayout(self.form_layout1)

        self.form_container2 = QGroupBox("Learning Rate")
        self.form_layout2 = QFormLayout()
        self.learning_rate_spin = QSpinBox()
        self.learning_rate_spin.setMinimum(0)
        self.learning_rate_spin.setMaximum(100)
        self.learning_rate_spin.setValue(10)
        self.form_layout2.addRow(QLabel("α:"), self.learning_rate_spin)
        self.form_container2.setLayout(self.form_layout2)

        self.form_container3 = QGroupBox("Discount Factor")
        self.form_layout3 = QFormLayout()
        self.discount_factor_spin = QSpinBox()
        self.discount_factor_spin.setMinimum(0)
        self.discount_factor_spin.setMaximum(100)
        self.discount_factor_spin.setValue(30)
        self.form_layout3.addRow(QLabel("ϒ:"), self.discount_factor_spin)
        self.form_container3.setLayout(self.form_layout3)

        self.form_container4 = QGroupBox("Balance Rate")
        self.form_layout4 = QFormLayout()
        self.balance_rate_spin = QSpinBox()
        self.balance_rate_spin.setMinimum(0)
        self.balance_rate_spin.setMaximum(100)
        self.balance_rate_spin.setValue(90)
        self.form_layout4.addRow(QLabel("BR:"), self.balance_rate_spin)
        self.form_container4.setLayout(self.form_layout4)

        self.form_container5 = QGroupBox("Iteration")
        self.form_layout5 = QFormLayout()
        self.iteration_spin = QSpinBox()
        self.iteration_spin.setMinimum(0)
        self.iteration_spin.setMaximum(1000)
        self.iteration_spin.setValue(200)
        self.form_layout5.addRow(QLabel("Iter:"), self.iteration_spin)
        self.form_container5.setLayout(self.form_layout5)

        self.bottom_layout.addLayout(self.left_bottom_layout)
        self.bottom_layout.addLayout(self.right_bottom_layout)
        self.left_bottom_layout.addWidget(self.form_container1)
        self.left_bottom_layout.addWidget(self.form_container2)
        self.left_bottom_layout.addWidget(self.form_container3)
        self.right_bottom_layout.addWidget(self.form_container4)
        self.right_bottom_layout.addWidget(self.form_container5)

        # Add to main layout
        self.main_layout.addLayout(self.top_layout)
        self.main_layout.addLayout(self.bottom_layout)
        self.setLayout(self.main_layout)

class SimAnnealTab(QWidget):

    def __init__(self):
        super().__init__()
        # Main layout
        self.main_layout = QVBoxLayout()

        # Sub layout
        self.top_layout = QGridLayout()
        self.bottom_layout = QVBoxLayout()

        # Top layout
        self.temper_init_spin = QSpinBox()
        self.temper_end_spin = QSpinBox()

        self.top_layout.addWidget(QLabel('T_0'), 0, 0)
        self.top_layout.addWidget(self.temper_init_spin, 0, 1)
        self.top_layout.addWidget(QLabel('T_min'), 0, 2)
        self.top_layout.addWidget(self.temper_end_spin, 0, 3)

        # Bottom layout
        self.form_container1 = QGroupBox()
        self.form_layout1 = QFormLayout()

        self.iteration_spin = QSpinBox()
        self.iteration_spin.setMinimum(0)
        self.iteration_spin.setMaximum(100)
        self.iteration_spin.setValue(1)

        self.beta_spin = QSpinBox()
        self.beta_spin.setMinimum(0)
        self.beta_spin.setMaximum(100)
        self.beta_spin.setValue(2)

        self.form_layout1.addRow(QLabel("Iter:"), self.iteration_spin)
        self.form_layout1.addRow(QLabel("β:"), self.beta_spin)

        self.form_container1.setLayout(self.form_layout1)

        self.bottom_layout.addWidget(self.form_container1)

        # Add to main layout
        self.main_layout.addLayout(self.top_layout)
        self.main_layout.addLayout(self.bottom_layout)
        self.setLayout(self.main_layout)

class NumAgentSlider(QSlider):
    default_k = 0
    filter_count = 0

    def __init__(self):
        super(NumAgentSlider, self).__init__()
        self.num_agent = 0
        self.k = round(self.num_agent * 0.6)

        # Label for the slider
        self.k_lbl = QLabel(str(self.k))

        # Increase the number of filters created
        NumAgentSlider.filter_count += 1

        # Slider for the first OpenCV filter, with min, max, default and step values
        self.thresh_sld = QSlider(Qt.Horizontal, self)
        self.thresh_sld.setMinimum(round(self.num_agent * 0.6))
        self.thresh_sld.setMaximum(self.num_agent)
        self.thresh_sld.setValue(self.k)


    def changeValue(self, value):
        # Function for setting the value of k1
        self.k = value
        self.thresh_sld.setValue(self.k)
        self.k_lbl.setText(str(self.k))

    def changeMax(self, value):
        self.k = round(value*0.6)
        self.thresh_sld.setMinimum(round(value * 0.6))
        self.thresh_sld.setMaximum(value)
        self.thresh_sld.setValue(self.k)