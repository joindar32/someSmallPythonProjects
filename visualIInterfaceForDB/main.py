import psycopg2
import sys

from PyQt5.QtWidgets import (QApplication, QWidget,
                             QTabWidget, QAbstractScrollArea,
                             QVBoxLayout, QHBoxLayout,
                             QTableWidget, QGroupBox,
                             QTableWidgetItem, QPushButton, QMessageBox)


class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()

        self._connect_to_db()

        self.setWindowTitle("Schedule")

        self.vbox = QVBoxLayout(self)

        self.tabs = QTabWidget(self)
        self.vbox.addWidget(self.tabs)

        self._create_schedule_tab()
        self._create_subject_tab()
        self._create_teacher_tab()

    def _connect_to_db(self):
        self.conn = psycopg2.connect(database="schedule",
                                     user="postgres",
                                     password="jametime2",
                                     host="localhost",
                                     port="5432")

        self.cursor = self.conn.cursor()

    def _create_schedule_tab(self):
        self.schedule_tab = QWidget()
        self.tabs.addTab(self.schedule_tab, "Расписание")

        self.monday_gbox = QGroupBox("Monday")
        self.tuesday_gbox = QGroupBox("Tuesday")
        self.wednesday_gbox = QGroupBox("Wednesday")
        self.thursday_gbox = QGroupBox("Thursday")
        self.friday_gbox = QGroupBox("Friday")
        self.friday_gbox = QGroupBox("Friday")

        self.svbox = QVBoxLayout()
        self.shbox1 = QHBoxLayout()
        self.shbox2 = QHBoxLayout()

        self.svbox.addLayout(self.shbox1)
        self.svbox.addLayout(self.shbox2)

        self.shbox1.addWidget(self.monday_gbox)
        self.shbox1.addWidget(self.tuesday_gbox)
        self.shbox1.addWidget(self.wednesday_gbox)
        self.shbox1.addWidget(self.thursday_gbox)
        self.shbox1.addWidget(self.friday_gbox)

        self._create_monday_table()
        self._create_tuesday_table()
        self._create_wednesday_table()
        self._create_thursday_table()
        self._create_friday_table()

        self.update_schedule_button = QPushButton("Update")
        self.shbox2.addWidget(self.update_schedule_button)
        self.update_schedule_button.clicked.connect(self._update_schedule)

        self.schedule_tab.setLayout(self.svbox)

    def _create_subject_tab(self):
        self.subject_tab = QWidget()
        self.tabs.addTab(self.subject_tab, "Предмет")
        self.subject_gbox = QGroupBox("Subject")

        self.svbox = QVBoxLayout()
        self.shbox1 = QHBoxLayout()
        self.shbox2 = QHBoxLayout()

        self.svbox.addLayout(self.shbox1)
        self.svbox.addLayout(self.shbox2)

        self.shbox1.addWidget(self.subject_gbox)
        self._create_subject_table()

        self.update_subject_button = QPushButton("Update")
        self.shbox2.addWidget(self.update_subject_button)
        self.update_subject_button.clicked.connect(self._update_subject)

        self.subject_tab.setLayout(self.svbox)

    def _create_teacher_tab(self):
        self.teacher_tab = QWidget()
        self.tabs.addTab(self.teacher_tab, "Преподаватель")
        self.teacher_gbox = QGroupBox("Teacher")

        self.svbox = QVBoxLayout()
        self.shbox1 = QHBoxLayout()
        self.shbox2 = QHBoxLayout()

        self.svbox.addLayout(self.shbox1)
        self.svbox.addLayout(self.shbox2)

        self.shbox1.addWidget(self.teacher_gbox)
        self._create_teacher_table()

        self.update_teacher_button = QPushButton("Update")
        self.shbox2.addWidget(self.update_teacher_button)
        self.update_teacher_button.clicked.connect(self._update_teacher)
        self.teacher_tab.setLayout(self.svbox)

    def _create_teacher_table(self):
        self.teacher_table = QTableWidget()
        self.teacher_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        self.teacher_table.setColumnCount(5)
        self.teacher_table.setHorizontalHeaderLabels(
            ["teacher_id", "Фамилия и инициалы", "Предмет", "Изменение", "Удаление"])

        self.mvbox = QVBoxLayout()
        self.mvbox.addWidget(self.teacher_table)
        self.teacher_gbox.setLayout(self.mvbox)

        self._update_teacher_table()

    def _update_teacher_table(self):
        self.cursor.execute('''select teacher.teacher_id, teacher.full_name, subject.name
         from teacher
         inner join subject
         on subject.id = teacher.subject''')
        records = list(self.cursor.fetchall())

        self.teacher_table.setRowCount(len(records) + 1)
        for i, r in enumerate(records):
            r = list(r)

            joinButton = QPushButton("Join")
            deleteButton = QPushButton("Delete")

            self.teacher_table.setItem(i, 0,
                                       QTableWidgetItem(str(r[0])))
            self.teacher_table.setItem(i, 1,
                                       QTableWidgetItem(str(r[1])))
            self.teacher_table.setItem(i, 2,
                                       QTableWidgetItem(str(r[2])))
            self.teacher_table.setCellWidget(i, 3, joinButton)

            joinButton.clicked.connect(lambda ch, num=i: self._change_teacher(num, r[0]))
            print(r)
            self.teacher_table.setCellWidget(i, 4, deleteButton)
            deleteButton.clicked.connect(lambda ch, num=r[0]: self._delete_teacher(num))

            self.teacher_table.resizeRowsToContents()

    def _change_teacher(self, rowNum, id):
        row = list()
        print(rowNum, id)

        for i in range(self.friday_table.columnCount()):
            try:
                row.append(self.friday_table.item(rowNum, i).text())
            except:
                row.append(None)
        try:
            print()
            query = "UPDATE public.teacher SET full_name = %s, subject =%s WHERE teacher_id =%s;"

            values = (row[1], row[2], id)
            print(row[1], row[2], id)

            self.cursor.execute(query, values)
        except:
            QMessageBox.about(self, "Error", "Enter all fields")

    def _delete_teacher(self, id):
        print(1)
        try:
            query = "delete from public.teacher where teacher_id = %s;"

            values = (id,)
            print(id)

            self.cursor.execute(query, values)

            self.conn.commit()
        except Exception as e:
            QMessageBox.about(self, "Error", f"An error occurred: {str(e)}")

    def _create_subject_table(self):
        self.subject_table = QTableWidget()
        self.subject_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        self.subject_table.setColumnCount(4)
        self.subject_table.setHorizontalHeaderLabels(["id", "Предмет", "Изменение", "Удаление"])

        self.mvbox = QVBoxLayout()
        self.mvbox.addWidget(self.subject_table)
        self.subject_gbox.setLayout(self.mvbox)

        self._update_subject_table()

    def _update_subject_table(self):
        self.cursor.execute('''select * from subject''')
        records = list(self.cursor.fetchall())

        self.subject_table.setRowCount(len(records) + 1)
        for i, r in enumerate(records):
            r = list(r)

            joinButton = QPushButton("Join")
            deleteButton = QPushButton("Join")

            self.subject_table.setItem(i, 0,
                                       QTableWidgetItem(str(r[0])))
            self.subject_table.setItem(i, 1,
                                       QTableWidgetItem(str(r[1])))
            self.subject_table.setCellWidget(i, 2, joinButton)
            self.subject_table.setCellWidget(i, 3, deleteButton)

            joinButton.clicked.connect(lambda ch, num=i: self._change_day_from_table(num))

            self.subject_table.resizeRowsToContents()

    def _create_monday_table(self):
        self.monday_table = QTableWidget()
        self.monday_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        self.monday_table.setColumnCount(7)
        self.monday_table.setHorizontalHeaderLabels(["id", "Subject", "Week", "Time", "Room", "Изменение", "Удаление"])

        self._update_monday_table()

        self.mvbox = QVBoxLayout()
        self.mvbox.addWidget(self.monday_table)
        self.monday_gbox.setLayout(self.mvbox)

    def _create_tuesday_table(self):
        self.tuesday_table = QTableWidget()
        self.tuesday_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        self.tuesday_table.setColumnCount(7)
        self.tuesday_table.setHorizontalHeaderLabels(["id", "Subject", "Week", "Time", "Room", "Изменение", "Удаление"])

        self._update_tuesday_table()

        self.mvbox = QVBoxLayout()
        self.mvbox.addWidget(self.tuesday_table)
        self.tuesday_gbox.setLayout(self.mvbox)

    def _create_wednesday_table(self):
        self.wednesday_table = QTableWidget()
        self.wednesday_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        self.wednesday_table.setColumnCount(7)
        self.wednesday_table.setHorizontalHeaderLabels(
            ["id", "Subject", "Week", "Time", "Room", "Изменение", "Удаление"])

        self._update_wednesday_table()

        self.mvbox = QVBoxLayout()
        self.mvbox.addWidget(self.wednesday_table)
        self.wednesday_gbox.setLayout(self.mvbox)

    def _create_thursday_table(self):
        self.thursday_table = QTableWidget()
        self.thursday_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        self.thursday_table.setColumnCount(7)
        self.thursday_table.setHorizontalHeaderLabels(
            ["id", "Subject", "Week", "Time", "Room", "Изменение", "Удаление"])

        self._update_thursday_table()

        self.mvbox = QVBoxLayout()
        self.mvbox.addWidget(self.thursday_table)
        self.thursday_gbox.setLayout(self.mvbox)

    def _create_friday_table(self):
        self.friday_table = QTableWidget()
        self.friday_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        self.friday_table.setColumnCount(7)
        self.friday_table.setHorizontalHeaderLabels(["id", "Subject", "Week", "Time", "Room", "Изменение", "Удаление"])

        self._update_friday_table()

        self.mvbox = QVBoxLayout()
        self.mvbox.addWidget(self.friday_table)
        self.friday_gbox.setLayout(self.mvbox)

    def _update_monday_table(self):
        self.cursor.execute('''select  oop.id_lesson,subject.name, oop.week, oop.start_time, oop.room_numb
                    from (SELECT * FROM public.timetable WHERE day='Понедельник') AS oop
                    inner  join subject
                    on subject.id = oop.subject ORDER BY week, oop.start_time''')
        records = list(self.cursor.fetchall())
        print(records)

        self.monday_table.setRowCount(len(records) + 1)

        for i, r in enumerate(records):
            r = list(r)
            print(i, r)
            joinButton = QPushButton("Join")
            deleteButton = QPushButton("Delete")

            self.monday_table.setItem(i, 0,
                                      QTableWidgetItem(str(r[0])))
            self.monday_table.setItem(i, 1,
                                      QTableWidgetItem(str(r[1])))
            self.monday_table.setItem(i, 2,
                                      QTableWidgetItem(str(r[2])))
            self.monday_table.setItem(i, 3,
                                      QTableWidgetItem(str(r[3])))
            self.monday_table.setItem(i, 4,
                                      QTableWidgetItem(str(r[4])))
            self.monday_table.setCellWidget(i, 5, joinButton)
            self.monday_table.setCellWidget(i, 6, deleteButton)

            joinButton.clicked.connect(lambda ch, num=i, id=r[0]: self._change_day_from_table(num, id, 'Понедельник'))
            deleteButton.clicked.connect(lambda ch, num=r[0]: self._delete_day_from_table(num, ))

            self.monday_table.resizeRowsToContents()

    def _update_tuesday_table(self):
        self.cursor.execute('''select  oop.id_lesson,subject.name, oop.week, oop.start_time, oop.room_numb
                    from (SELECT * FROM public.timetable WHERE day='Вторник') AS oop
                    inner  join subject
                    on subject.id = oop.subject ORDER BY week, oop.start_time''')
        records = list(self.cursor.fetchall())

        self.tuesday_table.setRowCount(len(records) + 1)

        for i, r in enumerate(records):
            r = list(r)
            joinButton = QPushButton("Join")
            deleteButton = QPushButton("Delete")

            self.tuesday_table.setItem(i, 0,
                                       QTableWidgetItem(str(r[0])))
            self.tuesday_table.setItem(i, 1,
                                       QTableWidgetItem(str(r[1])))
            self.tuesday_table.setItem(i, 2,
                                       QTableWidgetItem(str(r[2])))
            self.tuesday_table.setItem(i, 3,
                                       QTableWidgetItem(str(r[3])))
            self.tuesday_table.setItem(i, 4,
                                       QTableWidgetItem(str(r[4])))
            self.tuesday_table.setCellWidget(i, 5, joinButton)
            self.tuesday_table.setCellWidget(i, 6, deleteButton)

            joinButton.clicked.connect(lambda ch, num=i, id=r[0]: self._change_day_from_table(num, id, 'Вторник'))
            deleteButton.clicked.connect(lambda ch, num=r[0]: self._delete_day_from_table(num, ))

            self.tuesday_table.resizeRowsToContents()

    def _update_wednesday_table(self):
        self.cursor.execute('''select  oop.id_lesson,subject.name, oop.week, oop.start_time, oop.room_numb
                    from (SELECT * FROM public.timetable WHERE day='Среда') AS oop
                    inner  join subject
                    on subject.id = oop.subject ORDER BY week, oop.start_time''')
        records = list(self.cursor.fetchall())

        self.wednesday_table.setRowCount(len(records) + 1)

        for i, r in enumerate(records):
            r = list(r)
            joinButton = QPushButton("Join")
            deleteButton = QPushButton("Delete")

            self.wednesday_table.setItem(i, 0,
                                         QTableWidgetItem(str(r[0])))
            self.wednesday_table.setItem(i, 1,
                                         QTableWidgetItem(str(r[1])))
            self.wednesday_table.setItem(i, 2,
                                         QTableWidgetItem(str(r[2])))
            self.wednesday_table.setItem(i, 3,
                                         QTableWidgetItem(str(r[3])))
            self.wednesday_table.setItem(i, 4,
                                         QTableWidgetItem(str(r[4])))
            self.wednesday_table.setCellWidget(i, 5, joinButton)
            self.wednesday_table.setCellWidget(i, 6, deleteButton)

            joinButton.clicked.connect(lambda ch, num=i, id=r[0]: self._change_day_from_table(num, id, 'Среда'))
            deleteButton.clicked.connect(lambda ch, num=r[0]: self._delete_day_from_table(num, ))

            self.wednesday_table.resizeRowsToContents()

    def _update_thursday_table(self):
        self.cursor.execute('''select  oop.id_lesson,subject.name, oop.week, oop.start_time, oop.room_numb
                    from (SELECT * FROM public.timetable WHERE day='Четверг') AS oop
                    inner  join subject
                    on subject.id = oop.subject ORDER BY week, oop.start_time''')
        records = list(self.cursor.fetchall())

        self.thursday_table.setRowCount(len(records) + 1)

        for i, r in enumerate(records):
            r = list(r)
            joinButton = QPushButton("Join")
            deleteButton = QPushButton("Delete")

            self.thursday_table.setItem(i, 0,
                                        QTableWidgetItem(str(r[0])))
            self.thursday_table.setItem(i, 1,
                                        QTableWidgetItem(str(r[1])))
            self.thursday_table.setItem(i, 2,
                                        QTableWidgetItem(str(r[2])))
            self.thursday_table.setItem(i, 3,
                                        QTableWidgetItem(str(r[3])))
            self.thursday_table.setItem(i, 4,
                                        QTableWidgetItem(str(r[4])))
            self.thursday_table.setCellWidget(i, 5, joinButton)
            self.thursday_table.setCellWidget(i, 6, deleteButton)

            joinButton.clicked.connect(lambda ch, num=i, id=r[0]: self._change_day_from_table(num, id, 'Четверг'))
            deleteButton.clicked.connect(lambda ch, num=r[0]: self._delete_day_from_table(num, ))

            self.thursday_table.resizeRowsToContents()

    def _update_friday_table(self):
        self.cursor.execute('''select  oop.id_lesson,subject.name, oop.week, oop.start_time, oop.room_numb
                    from (SELECT * FROM public.timetable WHERE day='Пятница') AS oop
                    inner  join subject
                    on subject.id = oop.subject ORDER BY week, oop.start_time''')
        records = list(self.cursor.fetchall())

        self.friday_table.setRowCount(len(records) + 1)

        for i, r in enumerate(records):
            r = list(r)
            print(i, r)
            joinButton = QPushButton("Join")
            deleteButton = QPushButton("Delete")

            self.friday_table.setItem(i, 0,
                                      QTableWidgetItem(str(r[0])))
            self.friday_table.setItem(i, 1,
                                      QTableWidgetItem(str(r[1])))
            self.friday_table.setItem(i, 2,
                                      QTableWidgetItem(str(r[2])))
            self.friday_table.setItem(i, 3,
                                      QTableWidgetItem(str(r[3])))
            self.friday_table.setItem(i, 4,
                                      QTableWidgetItem(str(r[4])))
            self.friday_table.setCellWidget(i, 5, joinButton)
            self.friday_table.setCellWidget(i, 6, deleteButton)

            joinButton.clicked.connect(lambda ch, num=i, id=r[0]: self._change_day_from_table(num, id, 'Пятница'))
            deleteButton.clicked.connect(lambda ch, num=r[0]: self._delete_day_from_table(num, ))

            self.friday_table.resizeRowsToContents()

    def _change_day_from_table(self, rowNum, id, day):
        row = list()
        print(rowNum, id, day)
        if day == 'Пятница':
            for i in range(self.friday_table.columnCount()):
                try:
                    row.append(self.friday_table.item(rowNum, i).text())
                except:
                    row.append(None)
        if day == 'Понедельник':
            for i in range(self.monday_table.columnCount()):
                try:
                    row.append(self.monday_table.item(rowNum, i).text())
                except:
                    row.append(None)
        if day == 'Вторник':
            for i in range(self.tuesday_table.columnCount()):
                try:
                    row.append(self.tuesday_table.item(rowNum, i).text())
                except:
                    row.append(None)
        if day == 'Среда':
            for i in range(self.wednesday_table.columnCount()):
                try:
                    row.append(self.wednesday_table.item(rowNum, i).text())
                except:
                    row.append(None)
        if day == 'Четверг':
            for i in range(self.thursday_table.columnCount()):
                try:
                    row.append(self.thursday_table.item(rowNum, i).text())
                except:
                    row.append(None)

        try:
            query = "UPDATE public.timetable SET week = %s, start_time =%s, room_numb = %s WHERE id_lesson =%s;"

            values = (row[2], row[3], row[4], id)
            print(row[2], row[3], row[4], id)

            self.cursor.execute(query, values)

            self.conn.commit()
        except Exception as e:
            QMessageBox.about(self, "Error", f"An error occurred: {str(e)}")

    def _delete_day_from_table(self, id):
        print('Delete')
        try:
            query = "delete from timetable where id_lesson = %s;"

            values = (id,)
            print(id)

            self.cursor.execute(query, values)

            self.conn.commit()
        except Exception as e:
            QMessageBox.about(self, "Error", f"An error occurred: {str(e)}")

    def _update_schedule(self):
        self._update_monday_table()
        self._update_tuesday_table()
        self._update_wednesday_table()
        self._update_thursday_table()
        self._update_friday_table()

    def _update_subject(self):
        self._update_subject_table()

    def _update_teacher(self):
        self._update_teacher_table()


app = QApplication(sys.argv)
win = MainWindow()
win.show()
sys.exit(app.exec_())
