from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QPushButton, QWidget


class StateWidget(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        style1 = "background-color: yellow"
        style2 = "background-color: black"

        # animation doesn't work for strings but provides an appropriate delay
        animation = QtCore.QPropertyAnimation(self, 'styleSheet')
        animation.setDuration(150)

        state1 = QtCore.QState()
        state2 = QtCore.QState()
        state1.assignProperty(self, 'styleSheet', style1)
        state2.assignProperty(self, 'styleSheet', style2)
        #              change a state after an animation has played
        #                               v
        state1.addTransition(state1.propertiesAssigned, state2)
        state2.addTransition(state2.propertiesAssigned, state1)

        self.machine = QtCore.QStateMachine()
        self.machine.addDefaultAnimation(animation)
        self.machine.addState(state1)
        self.machine.addState(state2)
        self.machine.setInitialState(state1)
        self.machine.start()