from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import sys
import matplotlib as mpl
import matplotlib.pyplot as plt

mpl.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import psycopg2 as ps
import numpy as np
from LPVDisplayer import Ui_MainWindow
from MplWidget import MplWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.main_win = QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.main_win)
        self.ui.pushButton.clicked.connect(self.get_params)

    def get_params(self):
        self.ui.widget_matplot.canvas.ax.cla()
        machine = self.ui.comboBox_machine.currentText()
        channel = self.ui.comboBox_channel.currentText()
        operation = self.ui.comboBox_operation.currentText()
        month = self.ui.comboBox_month.currentText()
        if month == 'June':
            month = 6
        elif month == 'July':
            month = 7
        params = [machine, channel, operation, month]
        print(params)
        Sql_Statement = """SELECT lpv FROM PUBLIC."LPV" 
            WHERE machine_id = %s AND channel = %s AND operation = %s  AND EXTRACT(MONTH FROM extration_date) = %s """
        try:
            # connectar á base de dados
            conn = ps.connect(host='127.0.0.1',
                              database='Prototipo Cork V01',
                              port='5432', user='postgres',
                              password='Joanabonita7@')
            print("Connected to Database")
            cur = conn.cursor()
            # operacao para inserir os dados na base de dados
            cur.execute(Sql_Statement, params)
            lpv_records = cur.fetchall()
            cur.close()
        except (Exception, ps.DatabaseError) as error:
            print("Error Selecting Data")
            print(error)
        finally:
            if conn is not None:
                # fecha conexao com base de dados
                conn.close()
                print("Connection to Database Closed")
                print("There are {} rows of data".format(len(lpv_records)))

        self.ui.widget_matplot.canvas.ax.set_title("LPV NUMBERS on Machine {} Channel {} Operation {}".format(machine,
                                                                                                              channel,
                                                                                                              operation))
        self.ui.widget_matplot.canvas.ax.set_ylim([0, 600000])
        self.ui.widget_matplot.canvas.ax.grid()
        self.ui.widget_matplot.canvas.ax.set_xlabel("Number of records")
        self.ui.widget_matplot.canvas.ax.set_ylabel("LPV Numbers")
        self.ui.widget_matplot.canvas.ax.plot(lpv_records,marker='o', markersize= 2, color='green')
        self.ui.widget_matplot.canvas.draw()

    def show(self):
        self.main_win.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec_())
