import json
import os
import shutil
import subprocess
import time

from PySide6.QtCore import (
	Property, QDate, QDir, QPropertyAnimation, QSize, Qt, Slot
)
from PySide6.QtGui import (
	QAction, QIcon, QPainter, QPixmap
)
from PySide6.QtWidgets import (
	QAbstractButton, QApplication, QButtonGroup, QComboBox, QDateTimeEdit, QDoubleSpinBox, QFileDialog, QFrame,
	QGraphicsDropShadowEffect, QGridLayout, QHBoxLayout, QLabel, QLineEdit, QMainWindow, QPushButton, QSizePolicy,
	QSpinBox, QStyle, QTreeWidget, QTreeWidgetItem, QVBoxLayout, QWidget
)
from mailmerge import MailMerge


APP_TITLE = "Kuna's Inventory & Stock Manager"
APP_VERSION = "v1.0.0"
APP_FOLDER = "Inventory & Stock Manager"


def app_path(filename, directory="resource", write_file=False, root_folder=False):
	if root_folder:
		base_path = os.path.join(os.path.join(os.path.expanduser("~"), APP_FOLDER), directory)
	else:
		base_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), directory)
	if not os.path.exists(base_path):
		os.makedirs(base_path)
	abs_path = os.path.join(base_path, filename).replace("\\", "/")
	if os.path.isfile(abs_path) or write_file:
		return abs_path
	elif ".png" in filename:
		return os.path.join(base_path, "default.png").replace("\\", "/")
	else:
		return None


def name_to_pix(text):
	item = text.lower().replace(" ", "") + ".png"
	return app_path(item)


class Storage:
	def __init__(self):
		self._file = "data.json"

	@property
	def data(self):
		# if app_path(filename=self._file, directory="stored", root_folder=True):
		# 	fd = open(app_path(filename=self._file, directory="stored"), "r")
		if file := app_path(filename=self._file, directory="stored", root_folder=True):
			fd = open(file, "r")
			data = json.loads(fd.read())
			fd.close()
		else:
			data = {"delivery": {}, "product": {}, "client": {}, "supplier": {}}
		return data

	@data.setter
	def data(self, data):
		tmp = self.data
		for item in data:
			tmp[item] = data[item]
		fd = open(app_path(filename=self._file, directory="stored", write_file=True, root_folder=True), "w")
		json_object = json.dumps(tmp, indent=4)
		fd.write(json_object)
		fd.close()


# -------------------------------------------------------------------------------------------------------------------- #
def stylesheet():
	return f"""
	/*----- All Widgets -----*/
	*, *::pane {{
		border: 0px; 
		border-image: none; 
		border-style: none; 
		outline: 0; 
		padding: 0px; 
		margin: 0px;
		selection-color: rgb(30, 144, 255); 
		selection-background-color: transparent;
	}}

	/*----- QAbstractButton -----*/
	QAbstractButton[prop_type="0"] {{
		color: rgb(30, 144, 255);
		background: rgb(179, 179, 179);
	}}
	QAbstractButton[prop_type="0"]:disabled {{
		color: rgba(30, 144, 255, 0.2);
		background: rgba(179, 179, 179, 0.2);
	}}
	QAbstractButton[prop_type="1"] {{
		font-size: 14px;
		font-weight: 500;
		margin: 8px;
	}}
	QAbstractButton[prop_type="1"]:checked {{
		border-bottom: 2px solid rgb(0, 139, 204);
		color: rgb(0, 139, 204);
	}}
	QAbstractButton[prop_type="1"]:!checked {{
		border-bottom: 2px solid transparent;
		color: rgb(89, 89, 89);
	}}
	QAbstractButton[prop_type="2"] {{
		color: rgb(242, 242, 242);
		background: rgb(0, 139, 204);
		border: none;
		border-radius: 6px;
		font-size: 13px;
		font-weight: 500;
		height: 13px;
		padding-top: 8px;
		padding-bottom: 8px;
		min-width: 8em;
	}}
	QAbstractButton[prop_type="2"]:disabled {{
		background: rgba(0, 139, 204, 0.3);
	}}
	QAbstractButton[prop_type="2"]:hover {{
		background: rgb(0, 105, 153);
	}}
	QAbstractButton[prop_type="2"]:pressed {{
		background: rgb(0, 70, 102);
	}}
	QAbstractButton[prop_type="3"] {{
		color: rgb(242, 242, 242);
		background: rgb(0, 128, 0);
		border: none;
		border-radius: 6px;
		font-size: 13px;
		font-weight: 500;
		height: 13px;
		padding-right: 8px; 
		padding-left: 8px;
		padding-top: 4px;
		padding-bottom: 4px;
	}}
	QAbstractButton[prop_type="3"]:disabled {{
		background: rgba(0, 128, 0, 0.3);
	}}
	QAbstractButton[prop_type="3"]:hover {{
		background: rgb(0, 102, 0);
	}}
	QAbstractButton[prop_type="3"]:pressed {{
		background: rgb(0, 77, 0);
	}}
	QAbstractButton[prop_type="4"] {{
		color: rgb(242, 242, 242);
		background: rgb(172, 32, 22);
		border: none;
		border-radius: 6px;
		font-size: 13px;
		font-weight: 500;
		height: 13px;
		padding-right: 8px; 
		padding-left: 8px;
		padding-top: 4px;
		padding-bottom: 4px;
	}}
	QAbstractButton[prop_type="4"]:disabled {{
		background: rgba(172, 32, 22, 0.3);
	}}
	QAbstractButton[prop_type="4"]:hover {{
		background: rgb(149, 28, 19);
	}}
	QAbstractButton[prop_type="4"]:pressed {{
		background: rgb(126, 24, 16);
	}}
	QAbstractButton[prop_type="5"] {{
		color: rgb(172, 32, 22);
		background: rgb(0, 128, 0);
	}}
	QAbstractButton[prop_type="5"]:disabled {{
		color: rgba(172, 32, 22, 0.3);
		background: rgba(0, 128, 0, 0.3);
	}}
	QAbstractButton[prop_type="6"] {{
		background: rgb(172, 32, 22);
		color: rgb(0, 128, 0);
	}}
	QAbstractButton[prop_type="6"]:disabled {{
		background: rgba(172, 32, 22, 0.3);
		color: rgba(0, 128, 0, 0.3);
	}}

	/*----- QAbstractScrollArea -----*/
	QAbstractScrollArea::corner {{
		background: transparent;
	}}

	/*----- QAbstractSpinBox -----*/
	QAbstractSpinBox {{
		background: rgb(255, 255, 240);
		border: 1px solid transparent;
		border-radius: 6px;
		color: rgb(128, 128, 128);
		font-size: 13px;
		font-weight: 552;
		padding: 4px;
	}}
	QAbstractSpinBox:disabled {{
		color: rgba(255, 255, 240, 0.3);
	}}
	QAbstractSpinBox::down-arrow {{
		image: url({name_to_pix("down")});
		width: 16px;
	}}
	QAbstractSpinBox::down-button, QAbstractSpinBox::up-button {{
		border: none;
		background: rgb(0, 139, 204);
		width: 16px;
	}}
	QAbstractSpinBox::down-button {{
		border-bottom-right-radius: 6px;
	}}
	QAbstractSpinBox::down-button:disabled, QAbstractSpinBox::up-button:disabled {{
		background: rgba(0, 139, 204, 0.3);
	}}
	QAbstractSpinBox::down-button:hover, QAbstractSpinBox::up-button:hover {{
		background: rgb(0, 105, 153);
	}}
	QAbstractSpinBox::down-button:pressed, QAbstractSpinBox::up-button:pressed {{
		background: rgb(0, 70, 102);
	}}
	QAbstractSpinBox::up-arrow {{
		image: url({name_to_pix("up")});
		width: 16px;
	}}
	QAbstractSpinBox::up-button {{
		border-top-right-radius: 6px;
	}}

	/*----- QComboBox -----*/
	QComboBox {{
		background: rgb(255, 255, 240);
		border: 1px solid transparent;
		border-radius: 6px;
		color: rgb(128, 128, 128);
		font-size: 13px;
		font-weight: 552;
		padding: 4px;
		selection-background-color: rgb(0, 105, 153);
		selection-color: rgb(242, 242, 242);
	}}
	QComboBox:disabled {{
		color: rgba(255, 255, 240, 0.3);		
	}}
	QComboBox::down-arrow {{
		image: url({name_to_pix("down")});
		width: 16px;
	}}
	QComboBox::drop-down, QDateTimeEdit::drop-down {{
		border: none;
		border-bottom-right-radius: 6px;
		border-top-right-radius: 6px;
		background: rgb(0, 139, 204);
		width: 16px;
	}}
	QComboBox::drop-down:disabled, QDateTimeEdit::drop-down:disabled {{
		background: rgba(0, 139, 204, 0.3);
	}}
	QComboBox::drop-down:hover, QDateTimeEdit::drop-down:hover {{
		background: rgb(0, 105, 153);
	}}
	QComboBox::drop-down:pressed, QDateTimeEdit::drop-down:pressed {{
		background: rgb(0, 70, 102);
	}}
	QComboBox QAbstractItemView {{
		background-color: rgb(242, 242, 242);
		color: rgb(51, 51, 51);
		border: 1px solid transparent;
		outline: 0;
	}}

	/*----- QHeaderView -----*/
	QHeaderView {{
		background: transparent;
	}}
	QHeaderView::down-arrow {{
		subcontrol-origin:padding;
		subcontrol-position: center right;
		width: 16px;
		image: url({name_to_pix("sortdownlight")})
	}}
	QHeaderView::up-arrow {{
		subcontrol-origin:padding;
		subcontrol-position: center right;
		width: 16px;
		image: url({name_to_pix("sortuplight")})
	}}
	QHeaderView::section {{
		background: transparent;
		color: rgb(179, 179, 179);
		font-size: 13px;
		font-weight: 552;
		outline: none;
		padding-bottom: 2px;
		padding-left: 4px;
		padding-right: 4px;
		padding-top: 2px;
	}}
	QHeaderView::section:first {{
		border-top-left-radius: 6px;
	}}
	QHeaderView::section:last {{
		border-top-right-radius: 6px;
	}}

	/*----- QLabel -----*/
	QLabel[prop_type="0"] {{
		background: transparent;
		color: rgb(137, 137, 137);
		font-size: 14px;
		font-weight: 500;
	}}
	QLabel[prop_type="0"]:disabled {{
		background: transparent;
		color: rgba(137, 137, 137, 0.3);
		font-size: 14px;
		font-weight: 500;
	}}
	QLabel[prop_type="1"] {{
		background: transparent;
		color: rgb(137, 137, 137);
		font-size: 13px;
	}}
	QLabel[prop_type="1"]:disabled {{
		background: transparent;
		color: rgba(137, 137, 137, 0.3);
		font-size: 13px;
	}}
	QLabel[prop_type="2"] {{
		background: transparent;
		color: rgb(179, 179, 179);
		font-size: 14px;
		font-weight: 500;
	}}
	QLabel[prop_type="2"]:disabled {{
		background: transparent;
		color: rgba(179, 179, 179, 0.3);
		font-size: 14px;
		font-weight: 500;
	}}
	QLabel[prop_type="3"] {{
		background: transparent;
		color: rgb(137, 137, 137);
		font-size: 15px;
		font-weight: 500;
	}}
	QLabel[prop_type="3"]:disabled {{
		background: transparent;
		color: rgba(137, 137, 137, 0.3);
		font-size: 15px;
		font-weight: 500;
	}}
	QLabel[prop_type="4"] {{
		background: transparent;
		color: rgb(179, 179, 179);
		font-size: 12px;
		font-weight: 500;
	}}
	QLabel[prop_type="4"]:disabled {{
		background: transparent;
		color: rgba(179, 179, 179, 0.3);
		font-size: 12px;
		font-weight: 500;
	}}

	/*----- QLineEdit -----*/
	QLineEdit[prop_type="0"] {{
		background: rgb(255, 255, 240);
		border: 1px solid transparent;
		border-radius: 6px;
		color: rgb(128, 128, 128);
		font-size: 13px;
		font-weight: 552;
		padding: 4px;
	}}
	QLineEdit[prop_type="0"]:disabled {{
		background: rgba(255, 255, 240, 0.3);
		color: rgba(128, 128, 128, 0.3);
	}}
	QLineEdit[prop_type="1"] {{
		background: rgb(240, 247, 255);
		border: 1px solid transparent;
		border-radius: 6px;
		color: rgb(128, 128, 128);
		font-size: 13px;
		font-weight: 552;
		padding: 4px;
	}}

	/*----- QMainWindow -----*/
	QMainWindow {{
		background: rgb(230, 230, 230);
	}}

	/*----- QScrollBar -----*/
	QScrollBar {{
		background: rgb(204, 204, 204);
		border-radius: 6px;
	}}
	QScrollBar:disabled {{
		background: rgba(204, 204, 204, 0.3);
	}}
	QScrollBar:horizontal {{
		height: 12px;
	}}
	QScrollBar:vertical {{
		width: 12px;
	}}
	QScrollBar::handle {{
		background: rgb(179, 179, 179);
		border-radius: 4px;
	}}
	QScrollBar::handle:disabled {{
		background: rgba(179, 179, 179, 0.3);
	}}
	QScrollBar::handle:horizontal {{
		height: 8px;
		min-width: 8px;
		margin: 2px;
	}}
	QScrollBar::handle:vertical {{
		min-height: 8px;
		width: 8px;
		margin: 2px;
	}}
	QScrollBar::add-line, QScrollBar::add-page, QScrollBar::handle:disabled, QScrollBar::sub-line, 
	QScrollBar::sub-page {{
		background: transparent;
	}}
	QScrollBar::add-line:vertical, QScrollBar::add-page:vertical, QScrollBar::sub-line:vertical, 
	QScrollBar::sub-page:vertical {{
		height: 0px;
	}}
	QScrollBar::add-line:horizontal, QScrollBar::add-page:horizontal, QScrollBar::sub-line:horizontal, 
	QScrollBar::sub-page:horizontal {{
		width: 0px;
	}}

	/*----- QTreeView -----*/
	QTreeView {{
		alternate-background-color: transparent;
		background: rgb(242, 242, 242);
		border: 1px solid transparent;
		border-radius: 6px;
		color: rgb(51, 51, 51);
		font-size: 13px;
		padding: 2px;
	}}
	QTreeView::item {{
		border-top: 1px solid rgb(232, 232, 232);
		padding-top: 4px;
		padding-bottom: 4px;
	}}
	QTreeView::item:disabled {{
		color: rgba(51, 51, 51, 0.3);
	}}
	QTreeView::item:hover {{
		background: rgb(242, 242, 242);
		color: rgb(0, 105, 153);
	}}
	QTreeView::item:selected {{
		background: rgb(0, 105, 153);
		color: rgb(242, 242, 242);
	}}
	QTreeView::item:selected:disabled {{
		background: rgba(0, 105, 153, 0.3);
		color: rgb(242, 242, 242);
	}}
	QTreeView::item:selected:last {{
		margin-right: 2px;
	}}

	/*----- QToolBar -----*/
	QToolBar * {{
		margin: 0px; padding: 0px;
	}}

	/*----- Custom Widgets -----*/
	#CustomContainer[prop_type="0"] {{
		background: qlineargradient(
		spread:pad, x1: 0, y1: 0, x2: 0, y2: 1,
		stop:0 rgb(237, 237, 237),
		stop:1 rgb(212, 212, 212));
		border-radius: 8px;
	}}
	#CustomContainer[prop_type="0"] {{
		background: qlineargradient(
			spread:pad, x1: 0, y1: 0, x2: 0, y2: 1, stop:0 rgb(237, 237, 237), stop:1 rgb(212, 212, 212)
		);
		border-radius: 8px;
	}}
	#CustomContainer[prop_type="1"] {{
		background: qlineargradient(
			spread:pad, x1: 0, y1: 0, x2: 0, y2: 1, stop:0 rgb(212, 212, 212), stop:1 rgb(186, 186, 186)
		);
		border-radius: 8px;
	}}
	#CustomBackground {{
		background: rgb(242, 242, 242);
		border: 1px solid transparent;
		border-radius: 6px;
	}}
	#CustomToggle {{
		padding: 4px;
	}}
	"""


class BaseComboBox(QComboBox):
	def __init__(self, parent=None, compact=False):
		super().__init__(parent)
		if compact:
			self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)

	def clear_all(self):
		self.clear()

	@property
	def variable(self):
		return self.currentData(Qt.ItemDataRole.UserRole)

	@variable.setter
	def variable(self, data):
		self.setCurrentText(data)


class BaseDateEdit(QDateTimeEdit):
	def __init__(self, parent=None):
		super().__init__(parent)
		self.setDisplayFormat("dd MMM yyyy")
		self.setTimeSpec(Qt.TimeSpec.LocalTime)
		self.setCalendarPopup(True)
		self.lineEdit().setReadOnly(True)
		self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)

	def clear_all(self):
		self.setDate(QDate.currentDate())

	@property
	def variable(self):
		return self.dateTime().toSecsSinceEpoch() + 28800

	@variable.setter
	def variable(self, data):
		self.setDate(QDate.fromString(time.strftime("%Y-%m-%d", time.localtime(data)), "yyyy-MM-dd"))


class BaseLabel(QLabel):
	def __init__(self, text, parent=None, prop_type="4", compact=False):
		super().__init__(parent)
		self.setProperty("prop_type", prop_type)
		self.setText(text)
		if compact:
			self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)

	def clear_all(self):
		self.clear()

	@property
	def variable(self):
		return self.text()

	@variable.setter
	def variable(self, data):
		self.setText(data)


class BaseLineEdit(QLineEdit):
	def __init__(self, text, prop_type="0", parent=None, read_only=False, compact=False):
		super().__init__(parent)
		self.setProperty("prop_type", prop_type)
		self.setPlaceholderText(text)
		self.setReadOnly(read_only)
		if compact:
			self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

	def clear_all(self):
		self.clear()

	@property
	def variable(self):
		return self.text()

	@variable.setter
	def variable(self, data):
		self.setText(data)


class BasePushButton(QPushButton):
	def __init__(self, text, checkable=False, prop_type="0", obj_name=None, conn=None, parent=None):
		super().__init__(parent)
		self.setProperty("prop_type", prop_type)
		self.setText(text)
		self.setCheckable(checkable)
		if obj_name:
			self.setObjectName(obj_name)
		if conn:
			self.clicked.connect(conn)

	def clear_all(self):
		self.setText("")

	def update_button(self, text, obj_name):
		self.setText(text)
		self.setObjectName(obj_name)


class BaseSpinBox(QSpinBox):
	def __init__(self, parent=None, min_value=1, max_value=999999):
		super().__init__(parent)
		self.setRange(min_value, max_value)
		self.setAlignment(Qt.AlignmentFlag.AlignCenter)

	def clear_all(self):
		self.setValue(self.minimum() if self.minimum() > 0 else 1)

	@property
	def variable(self):
		return self.value()

	@variable.setter
	def variable(self, data):
		self.setValue(data)


class BaseSpinDoubleBox(QDoubleSpinBox):
	def __init__(self, parent=None, min_value=0.01, max_value=9999.99):
		super().__init__(parent)
		self.setRange(min_value, max_value)
		self.setValue(1.00)
		self.setAlignment(Qt.AlignmentFlag.AlignCenter)

	def clear_all(self):
		self.setValue(self.minimum() if self.minimum() > 0 else 1.00)

	@property
	def variable(self):
		return self.value()

	@variable.setter
	def variable(self, data):
		self.setValue(data)


class BaseTreeWidget(QTreeWidget):
	def __init__(self, parent=None):
		super().__init__(parent)
		self.setAlternatingRowColors(True)
		self.setUniformRowHeights(True)
		self.setRootIsDecorated(False)
		self.setItemsExpandable(False)
		font = self.header().font()
		font.setItalic(True)
		self.header().setFont(font)
		self.header().setDefaultAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
		self.setHeaderHidden(True)
		self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)

	def resize_tree(self):
		for idx in range(self.columnCount()):
			self.resizeColumnToContents(idx)

	def set_headers(self, data):
		self.setColumnCount(len(data))
		self.setHeaderLabels(data)
		self.setHeaderHidden(False)

	def clear_all(self):
		self.clear()


class BaseToggleButton(QAbstractButton):
	def __init__(self, parent=None, prop_type="0", state=False, conn=None):
		super().__init__(parent)
		self.setProperty("prop_type", prop_type)
		self.setCheckable(True)
		self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
		self._track_size = 6
		self._margin = 2
		self._base_offset = self._track_size + self._margin
		self._end_offset = {True: lambda: self.width() - self._base_offset, False: lambda: self._base_offset}
		self._offset = self._base_offset
		self.setChecked(state)
		if conn:
			self.toggled.connect(conn)

	def enterEvent(self, event):
		self.setCursor(Qt.PointingHandCursor)
		super().enterEvent(event)

	# noinspection PyPropertyAccess
	def mouseReleaseEvent(self, event):
		super().mouseReleaseEvent(event)
		if event.button() == Qt.LeftButton:
			animate = QPropertyAnimation(self, b"offset", self)
			animate.setDuration(150)
			animate.setStartValue(self.offset)
			animate.setEndValue(self._end_offset[self.isChecked()]())
			animate.start()

	@Property(int)
	def offset(self):
		return self._offset

	@offset.setter
	def offset(self, value):
		self._offset = value
		self.update()

	# noinspection PyPropertyAccess
	def paintEvent(self, event):
		painter = QPainter(self)
		painter.setRenderHint(QPainter.Antialiasing, True)
		painter.setPen(Qt.NoPen)
		painter.setBrush(self.palette().buttonText().color() if self.isChecked() else self.palette().button().color())
		painter.setOpacity(0.5)
		painter.drawRoundedRect(
			self._margin,
			self._margin,
			self.width() - 2 * self._margin,
			self.height() - 2 * self._margin,
			self._track_size,
			self._track_size
		)
		painter.setOpacity(1.0)
		painter.drawEllipse(
			self.offset - (self._track_size + self._margin),
			self._base_offset - (self._track_size + self._margin),
			2 * (self._track_size + self._margin),
			2 * (self._track_size + self._margin)
		)

	def resizeEvent(self, event):
		super().resizeEvent(event)
		self.offset = self._end_offset[self.isChecked()]()

	def setChecked(self, checked):
		super().setChecked(checked)
		self.offset = self._end_offset[checked]()

	def sizeHint(self):
		return QSize(4 * self._track_size + 2 * self._margin, 2 * self._track_size + 2 * self._margin)

	def clear_all(self):
		self.setChecked(False)

	@property
	def variable(self):
		return self.isChecked()

	@variable.setter
	def variable(self, data):
		self.setChecked(data)


class TreeItemClient(QTreeWidgetItem):
	def __init__(self, data, parent=None):
		super().__init__(parent)
		self.updateData(data)
		self.setTextAlignment(0, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignRight)
		self.setTextAlignment(1, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
		self.setTextAlignment(2, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignHCenter)
		self.setTextAlignment(3, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignHCenter)
		self.setTextAlignment(4, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignHCenter)

	def updateData(self, data):
		self.setData(0, Qt.ItemDataRole.UserRole, data)
		self.setText(0, f"""{self.treeWidget().invisibleRootItem().childCount()}""")
		self.setText(1, data["name"])
		label1 = QLabel()
		label1.setAlignment(Qt.AlignmentFlag.AlignCenter)
		label1.setPixmap(QPixmap(name_to_pix("yes" if data["custom_sku"] else "no")))
		self.treeWidget().setItemWidget(self, 2, label1)
		label2 = QLabel()
		label2.setAlignment(Qt.AlignmentFlag.AlignCenter)
		label2.setPixmap(QPixmap(name_to_pix("yes" if data["location"]["dual"] else "no")))
		self.treeWidget().setItemWidget(self, 3, label2)
		label3 = QLabel()
		label3.setAlignment(Qt.AlignmentFlag.AlignCenter)
		label3.setPixmap(QPixmap(name_to_pix("yes" if data["show_price"] else "no")))
		self.treeWidget().setItemWidget(self, 4, label3)

	@property
	def recordType(self):
		return "client"


class TreeItemCustomSKU(QTreeWidgetItem):
	def __init__(self, data, parent=None):
		super().__init__(parent)
		self.updateData(data)
		self.setTextAlignment(0, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignRight)
		self.setTextAlignment(1, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
		self.setTextAlignment(2, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignRight)
		self.setTextAlignment(3, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignRight)
		self.setTextAlignment(3, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignHCenter)

	def updateData(self, data):
		self.setData(0, Qt.ItemDataRole.UserRole, data)
		self.setText(0, f"""{self.treeWidget().invisibleRootItem().childCount()}""")
		self.setText(1, data["product_name"])
		self.setText(2, data["product_sku"])
		self.setText(3, data["client_sku"])
		label = QLabel()
		label.setAlignment(Qt.AlignmentFlag.AlignCenter)
		label.setPixmap(QPixmap(name_to_pix("no" if data["locked"] else "yes")))
		self.treeWidget().setItemWidget(self, 4, label)

	@property
	def recordType(self):
		return "client"


class TreeItemDelivery(QTreeWidgetItem):
	def __init__(self, data, parent=None):
		super().__init__(parent)
		self.updateData(data)
		self.setTextAlignment(0, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignRight)
		self.setTextAlignment(1, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignRight)
		self.setTextAlignment(2, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
		self.setTextAlignment(3, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
		self.setTextAlignment(4, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignHCenter)
		self.setTextAlignment(5, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignHCenter)

	def updateData(self, data):
		self.setData(0, Qt.ItemDataRole.UserRole, data)
		self.setText(0, f"""{self.treeWidget().invisibleRootItem().childCount()}""")
		self.setText(1, data["order"])
		self.setText(2, f"""{time.strftime("%d %b %Y", time.gmtime(data["date"]))}""")
		self.setText(3, data["client"]["name"])
		qty = sum(data["details"][i]["location1"] + data["details"][i]["location2"] for i in data["details"])
		self.setText(4, f"""{qty:,}""")
		label = QLabel()
		label.setAlignment(Qt.AlignmentFlag.AlignCenter)
		label.setPixmap(QPixmap(name_to_pix("yes" if data["document"] else "no")))
		self.treeWidget().setItemWidget(self, 5, label)

	@property
	def recordType(self):
		return "delivery"


class TreeItemItems(QTreeWidgetItem):
	def __init__(self, data, parent=None):
		super().__init__(parent)
		self.updateData(data)
		self.setTextAlignment(0, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignRight)
		self.setTextAlignment(1, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
		self.setTextAlignment(2, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignHCenter)
		self.setTextAlignment(3, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignHCenter)
		self.setTextAlignment(4, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignHCenter)
		self.setTextAlignment(5, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignRight)

	def updateData(self, data):
		self.setData(0, Qt.ItemDataRole.UserRole, data)
		self.setText(0, f"""{self.treeWidget().invisibleRootItem().childCount()}""")
		self.setText(1, data["product_name"])
		self.setText(2, data["product_sku"])
		self.setText(3, data["client_sku"])
		self.setText(4, f"""{data["product_price"]:,.2f}""")
		self.setText(5, f"""{data["location1"] + data["location2"]:,}""")

	@property
	def recordType(self):
		return "delivery"


class TreeItemProduct(QTreeWidgetItem):
	def __init__(self, data, parent=None):
		super().__init__(parent)
		self.updateData(data)
		self.setTextAlignment(0, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignRight)
		self.setTextAlignment(1, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
		self.setTextAlignment(2, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignRight)
		self.setTextAlignment(3, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignRight)
		self.setTextAlignment(4, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignRight)
		self.setTextAlignment(5, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignHCenter)

	def updateData(self, data):
		self.setData(0, Qt.ItemDataRole.UserRole, data)
		self.setText(0, f"""{self.treeWidget().invisibleRootItem().childCount()}""")
		self.setText(1, data["name"])
		self.setText(2, data["sku"])
		self.setText(3, f"""{data["price"]:,.2f}""")
		self.setText(4, f"""{sum(data["quantity"][i]["amount"] for i in data["quantity"]):,}""")
		label = QLabel()
		label.setAlignment(Qt.AlignmentFlag.AlignCenter)
		label.setPixmap(QPixmap(name_to_pix("no" if data["discontinued"] else "yes")))
		self.treeWidget().setItemWidget(self, 5, label)

	@property
	def recordType(self):
		return "product"


class TreeItemStock(QTreeWidgetItem):
	def __init__(self, data, parent=None):
		super().__init__(parent)
		self.updateData(data)
		self.setTextAlignment(0, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignRight)
		self.setTextAlignment(1, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignRight)
		self.setTextAlignment(2, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
		self.setTextAlignment(3, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignRight)
		self.setTextAlignment(4, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignHCenter)

	def updateData(self, data):
		self.setData(0, Qt.ItemDataRole.UserRole, data)
		self.setText(0, f"""{self.treeWidget().invisibleRootItem().childCount()}""")
		self.setText(1, f"""{time.strftime("%a, %d %b %Y", time.gmtime(data["date"]))}""")
		self.setText(2, data["source"])
		self.setText(3, f"""{data["amount"]:,}""")
		label = QLabel()
		label.setAlignment(Qt.AlignmentFlag.AlignCenter)
		label.setPixmap(QPixmap(name_to_pix("no" if data["locked"] else "yes")))
		self.treeWidget().setItemWidget(self, 4, label)

	@property
	def recordType(self):
		return "product"


class TreeItemSupplier(QTreeWidgetItem):
	def __init__(self, data, parent=None):
		super().__init__(parent)
		self.updateData(data)
		self.setTextAlignment(0, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignRight)
		self.setTextAlignment(1, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)

	def updateData(self, data):
		self.setData(0, Qt.ItemDataRole.UserRole, data)
		self.setText(0, f"""{self.treeWidget().invisibleRootItem().childCount()}""")
		self.setText(1, data["name"])

	@property
	def recordType(self):
		return "supplier"


class TreeItemTemplate(QTreeWidgetItem):
	def __init__(self, data, parent=None):
		super().__init__(parent)
		self.updateData(data)
		self.setTextAlignment(0, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignRight)
		self.setTextAlignment(1, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
		self.setTextAlignment(2, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)

	def updateData(self, data):
		self.setData(0, Qt.ItemDataRole.UserRole, data)
		self.setText(0, f"""{self.treeWidget().invisibleRootItem().childCount()}""")
		self.setText(1, os.path.basename(data))
		self.setText(2, os.path.dirname(data))

	@property
	def recordType(self):
		return "supplier"


class WidgetBackGround(QFrame):
	def __init__(self, parent=None):
		super().__init__(parent)
		self.setObjectName("CustomBackground")
		self.setLayout(QGridLayout(self))

	def addLayout(self, *args):
		self.layout().addLayout(*args)

	def addWidget(self, *args):
		self.layout().addWidget(*args)


class WidgetContainer(QFrame):
	def __init__(self, parent=None, is_vertical=False, is_expanding=True, prop_type="0"):
		super().__init__(parent)
		self.setObjectName("CustomContainer")
		self.setProperty("prop_type", prop_type)
		self.setSizePolicy(
			QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding if is_expanding else QSizePolicy.Policy.Fixed
		)
		self.setLayout(QVBoxLayout(self) if is_vertical else QHBoxLayout(self))
		self.setGraphicsEffect(QGraphicsDropShadowEffect(
			parent=self,
			offset=0,
			blurRadius=10,
			color=Qt.GlobalColor.black,
			enabled=True
		))

	def addLayout(self, *args):
		self.layout().addLayout(*args)

	def addStretch(self):
		self.layout().addStretch()

	def addWidget(self, *args):
		self.layout().addWidget(*args)


class WidgetFileBrowser(QLineEdit):
	def __init__(self, text, parent=None):
		super().__init__(parent)
		self.setProperty("prop_type", "0")
		self.setContentsMargins(0, 0, 0, 0)
		self.setPlaceholderText(text)
		self.setReadOnly(True)
		action = QAction(self)
		action.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_DirIcon))
		action.setIconText("Browse..")
		action.triggered.connect(self._browse)
		self.addAction(action, QLineEdit.ActionPosition.TrailingPosition)

	def _browse(self):
		filename, _ = QFileDialog.getOpenFileName(self, "Open File..", QDir.homePath(), "*.docx")
		if filename:
			self.setText(filename)

	def clear_all(self):
		self.clear()

	@property
	def variable(self):
		return self.text()

	@variable.setter
	def variable(self, data):
		self.setText(data)


class WidgetLabel(QFrame):
	def __init__(self, title, layout=None, widget=None, parent=None):
		super().__init__(parent)
		_layout = QVBoxLayout(self)
		_layout.setContentsMargins(0, 0, 0, 0)
		_layout.setSpacing(0)
		_layout.addWidget(BaseLabel(text=title, prop_type="4")) if isinstance(title, str) else _layout.addWidget(title)
		_layout.addLayout(layout) if layout else _layout.addWidget(widget)


class WidgetToggle(QFrame):
	def __init__(self, title, widget, parent=None):
		super().__init__(parent)
		self.setObjectName("CustomToggle")
		self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
		_layout = QHBoxLayout(self)
		_layout.setContentsMargins(0, 0, 0, 0)
		if isinstance(title, str):
			_layout.addWidget(widget)
			_layout.addWidget(BaseLabel(text=title, prop_type="3"))
		else:
			_layout.addWidget(BaseLabel(text=title[0], prop_type="3"))
			_layout.addWidget(widget)
			_layout.addWidget(BaseLabel(text=title[1], prop_type="3"))


# MAIN -----------------------------------------------------------------------------------------------------------------
class MainUI(QMainWindow):
	# noinspection PyUnresolvedReferences
	def __init__(self, parent=None):
		super().__init__(parent)
		self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
		self.setWindowTitle(APP_TITLE)
		self.setWindowIcon(QIcon(app_path("icon.ico")))
		self.resize(1280, 720)

		# Set Up Widgets -----------------------------------------------------------------------------------------------
		header_buttons_group = [
			BasePushButton(text="Delivery Order", checkable=True, prop_type="1"),
			BasePushButton(text="Products", checkable=True, prop_type="1"),
			BasePushButton(text="Clients", checkable=True, prop_type="1"),
			BasePushButton(text="Supplier", checkable=True, prop_type="1")
		]
		self._grp = QButtonGroup()
		self._grp.idToggled.connect(self._grp_button_pressed)
		for idx, item in enumerate(header_buttons_group):
			self._grp.addButton(item, idx)

		self._hdr = [
			BasePushButton(text="", prop_type="2", conn=self._hdr_button_pressed),
			BasePushButton(text="", prop_type="2", conn=self._hdr_button_pressed),
			BasePushButton(text="", prop_type="2", conn=self._hdr_button_pressed),
			BasePushButton(text="", prop_type="2", conn=self._hdr_button_pressed),
			BasePushButton(text="", prop_type="2", conn=self._hdr_button_pressed),
			BasePushButton(text="", prop_type="2", conn=self._hdr_button_pressed),
			BasePushButton(text="", prop_type="2", conn=self._hdr_button_pressed)
		]
		self._pnl = [
			WidgetContainer(is_vertical=True, prop_type="0"),
			WidgetContainer(is_vertical=True, prop_type="0"),
			WidgetContainer(is_expanding=False, prop_type="1")
		]
		self._ctr = [
			WidgetBackGround(),
			WidgetBackGround(),
			WidgetBackGround(),
			WidgetBackGround(),
			WidgetBackGround(),
			WidgetBackGround(),
			WidgetBackGround(),
			WidgetBackGround()
		]
		self._wgt = [
			[
				BaseComboBox(),
				BaseComboBox(),
				BaseDateEdit(),
				BaseLineEdit(text="DO Number..", prop_type="1", read_only=True, compact=True),
			],
			[
				BaseComboBox(),
				BaseLineEdit(text="Available Stock..", prop_type="1", read_only=True, compact=True),
				BaseLineEdit(text="Price..", prop_type="1", read_only=True, compact=True),
				BaseLabel(text="", compact=True),
				BaseSpinBox(min_value=0),
				BaseLabel(text="", compact=True),
				BaseSpinBox(min_value=0)
			],
			[
				BaseLineEdit(text="Product Name.."),
				BaseLineEdit(text="SKU Number.."),
				BaseSpinDoubleBox(),
				BaseToggleButton(prop_type="5"),
			],
			[
				BaseComboBox(),
				BaseSpinBox(min_value=-999999),
				BaseDateEdit(),
				BasePushButton(text="", prop_type="3", conn=self._pnl_button_pressed),
				BasePushButton(text="", prop_type="4", conn=self._pnl_button_pressed)
			],
			[
				BaseLineEdit(text="Enter Client Name.."),
				BaseLineEdit(text="Enter Address Line #1.."),
				BaseLineEdit(text="Enter Address Line #2.."),
				BaseLineEdit(text="Enter Postcode..", compact=True),
				BaseLineEdit(text="Enter City.."),
				BaseLineEdit(text="Enter State.."),
				BaseToggleButton(),
				BaseLineEdit(text="Enter Location Label #1.."),
				BaseLineEdit(text="Enter Location Label #2.."),
				BaseToggleButton(prop_type="6"),
			],
			[
				BaseComboBox(),
				BaseLineEdit(text="Client SKU..", compact=True)
			],
			[
				BaseLineEdit(text="Enter Supplier Name.."),
				WidgetFileBrowser(text="Delivery Order Template..")
			],
			[
				WidgetFileBrowser(text="Delivery Template.."),
			],
			BasePushButton(text="", prop_type="3", conn=self._pnl_button_pressed),
			BasePushButton(text="Cancel", obj_name="cancel", prop_type="4", conn=self._pnl_button_pressed)
		]

		# Set Up Core Layout  ------------------------------------------------------------------------------------------
		central = QWidget()
		central_layout = QVBoxLayout(central)
		header_layout = QHBoxLayout()
		central_layout.addLayout(header_layout)
		body_layout = QHBoxLayout()
		central_layout.addLayout(body_layout)
		self.setCentralWidget(central)

		for item in header_buttons_group:
			header_layout.addWidget(item)
		header_layout.addStretch()
		header_layout.addWidget(BaseLabel(text=APP_VERSION))

		body_layout.addWidget(self._pnl[0])
		content_layout = QVBoxLayout()
		body_layout.addLayout(content_layout)
		for idx in range(2, len(self._pnl)):
			content_layout.addWidget(self._pnl[idx])
		content_layout.addWidget(self._pnl[1])

		buttons_layout = QHBoxLayout()
		self._pnl[0].addLayout(buttons_layout)
		buttons_layout.addWidget(self._hdr[0])
		buttons_layout.addWidget(self._hdr[1])
		buttons_layout.addWidget(self._hdr[2])
		buttons_layout.addWidget(self._hdr[3])
		buttons_layout.addStretch()
		self.tree1 = BaseTreeWidget()
		self.tree1.itemClicked.connect(self._tree1_item_selected)
		self._pnl[0].addWidget(self.tree1)

		buttons_layout = QHBoxLayout()
		self._pnl[1].addLayout(buttons_layout)
		buttons_layout.addWidget(self._hdr[4])
		buttons_layout.addWidget(self._hdr[5])
		buttons_layout.addWidget(self._hdr[6])
		buttons_layout.addStretch()
		self.tree2 = BaseTreeWidget()
		self.tree2.itemClicked.connect(self._tree2_item_selected)
		self._pnl[1].addWidget(self.tree2)

		container_layout1 = QVBoxLayout()
		for item in self._ctr:
			container_layout1.addWidget(item)
		self._pnl[2].addLayout(container_layout1, 1)
		container_layout2 = QVBoxLayout()
		container_layout2.addWidget(self._wgt[-2])
		container_layout2.addWidget(self._wgt[-1])
		container_layout2.addStretch()
		self._pnl[2].addLayout(container_layout2)

		# Set Up Layout: Delivery Order [Order] ------------------------------------------------------------------------
		self._ctr[0].addWidget(
			WidgetLabel(title="Client:", widget=self._wgt[0][0]), 0, 0, 1, 3, Qt.AlignmentFlag.AlignTop
		)
		self._ctr[0].addWidget(
			WidgetLabel(title="Supplier:", widget=self._wgt[0][1]), 1, 0, 1, 3, Qt.AlignmentFlag.AlignTop
		)
		self._ctr[0].addWidget(
			WidgetLabel(title="Date:", widget=self._wgt[0][2]), 2, 0, 1, 1, Qt.AlignmentFlag.AlignTop
		)
		self._ctr[0].addWidget(
			WidgetLabel(title="DO Number:", widget=self._wgt[0][3]), 2, 1, 1, 1, Qt.AlignmentFlag.AlignTop
		)
		self._wgt[0][1].currentIndexChanged.connect(self._generate_do_number)

		# Set Up Layout: Delivery Order [Item] -------------------------------------------------------------------------
		self._ctr[1].addWidget(
			WidgetLabel(title="Product:", widget=self._wgt[1][0]), 0, 0, 1, 2, Qt.AlignmentFlag.AlignTop
		)
		self._ctr[1].addWidget(
			WidgetLabel(title="Available Stock:", widget=self._wgt[1][1]), 1, 0, 1, 1, Qt.AlignmentFlag.AlignTop
		)
		self._ctr[1].addWidget(
			WidgetLabel(title="Price:", widget=self._wgt[1][2]), 1, 1, 1, 1, Qt.AlignmentFlag.AlignTop
		)
		self._ctr[1].addWidget(
			WidgetLabel(title=self._wgt[1][3], widget=self._wgt[1][4]), 2, 0, 1, 1, Qt.AlignmentFlag.AlignTop
		)
		self._ctr[1].addWidget(
			WidgetLabel(title=self._wgt[1][5], widget=self._wgt[1][6]), 2, 1, 1, 1, Qt.AlignmentFlag.AlignTop
		)
		self._wgt[1][0].currentIndexChanged.connect(self._update_available_stock_and_price)
		# Set Up Layout: Products [Product] ----------------------------------------------------------------------------
		self._ctr[2].addWidget(
			WidgetLabel(title="Product:", widget=self._wgt[2][0]), 0, 0, 1, 3, Qt.AlignmentFlag.AlignTop
		)
		self._ctr[2].addWidget(
			WidgetLabel(title="SKU Number:", widget=self._wgt[2][1]), 1, 0, 1, 1, Qt.AlignmentFlag.AlignTop
		)
		self._ctr[2].addWidget(
			WidgetLabel(title="Price:", widget=self._wgt[2][2]), 1, 1, 1, 1, Qt.AlignmentFlag.AlignTop
		)
		self._ctr[2].addWidget(
			WidgetLabel(
				title="Discontinued:",
				widget=WidgetToggle(title=["No", "Yes"], widget=self._wgt[2][3])), 1, 2, 1, 1, Qt.AlignmentFlag.AlignTop
		)

		# Set Up Layout: Products [Stock] ------------------------------------------------------------------------------
		self._ctr[3].addWidget(
			WidgetLabel(title="Type:", widget=self._wgt[3][0]), 0, 0, 1, 2, Qt.AlignmentFlag.AlignTop
		)
		self._ctr[3].addWidget(
			WidgetLabel(title="Quantity:", widget=self._wgt[3][1]), 0, 2, 1, 1, Qt.AlignmentFlag.AlignTop
		)
		self._ctr[3].addWidget(
			WidgetLabel(title="Date:", widget=self._wgt[3][2]), 1, 0, 1, 1, Qt.AlignmentFlag.AlignTop
		)

		# Set Up Layout: Clients [Client] ------------------------------------------------------------------------------
		self._ctr[4].addWidget(
			WidgetLabel(title="Company Name:", widget=self._wgt[4][0]), 0, 0, 1, 3, Qt.AlignmentFlag.AlignTop
		)
		self._ctr[4].addWidget(
			WidgetLabel(title="Address:", widget=self._wgt[4][1]), 1, 0, 1, 3, Qt.AlignmentFlag.AlignTop
		)
		self._ctr[4].addWidget(self._wgt[4][2], 2, 0, 1, 3, Qt.AlignmentFlag.AlignTop)
		self._ctr[4].addWidget(
			WidgetLabel(title="Postcode:", widget=self._wgt[4][3]), 3, 0, 1, 1, Qt.AlignmentFlag.AlignTop
		)
		self._ctr[4].addWidget(
			WidgetLabel(title="City:", widget=self._wgt[4][4]), 3, 1, 1, 1, Qt.AlignmentFlag.AlignTop
		)
		self._ctr[4].addWidget(
			WidgetLabel(title="State:", widget=self._wgt[4][5]), 3, 2, 1, 1, Qt.AlignmentFlag.AlignTop
		)
		self._ctr[4].addWidget(
			WidgetLabel(
				title="Delivery Location:",
				widget=WidgetToggle(title=["1x", "2x"], widget=self._wgt[4][6])), 4, 0, 1, 1, Qt.AlignmentFlag.AlignTop
		)
		_container1 = QWidget()
		_container1.setEnabled(False)
		_container1_layout = QHBoxLayout(_container1)
		_container1_layout.setContentsMargins(0, 0, 0, 0)
		_container1_layout.addWidget(
			WidgetLabel(title="Location Label #1:", widget=self._wgt[4][7]), Qt.AlignmentFlag.AlignTop
		)
		_container1_layout.addWidget(
			WidgetLabel(title="Location Label #2:", widget=self._wgt[4][8]), Qt.AlignmentFlag.AlignTop
		)
		self._ctr[4].addWidget(_container1, 4, 1, 1, 2)
		_container2 = WidgetLabel(
			title="Show Price in DO:",
			widget=WidgetToggle(title=["No", "Yes"], widget=self._wgt[4][9])
		)
		self._ctr[4].addWidget(_container2, 5, 0, 1, 1)
		self._wgt[4][6].toggled.connect(_container1.setEnabled)
		self._wgt[4][6].toggled.connect(self._wgt[4][9].clear_all)
		self._wgt[4][6].toggled.connect(self._wgt[4][9].setDisabled)
		self._wgt[4][6].toggled.connect(_container2.setDisabled)

		# Set Up Layout: Clients [Client SKU] --------------------------------------------------------------------------
		self._ctr[5].addWidget(
			WidgetLabel(title="Product:", widget=self._wgt[5][0]), 0, 0, 1, 2, Qt.AlignmentFlag.AlignTop
		)
		self._ctr[5].addWidget(
			WidgetLabel(title="SKU Number:", widget=self._wgt[5][1]), 1, 0, 1, 1, Qt.AlignmentFlag.AlignTop
		)

		# Set Up Layout: Supplier [Supplier] ---------------------------------------------------------------------------
		self._ctr[6].addWidget(
			WidgetLabel(title="Supplier Name:", widget=self._wgt[6][0]), 0, 0, 1, 1, Qt.AlignmentFlag.AlignTop
		)
		self._ctr[6].addWidget(
			WidgetLabel(title="MS-Word Templates:", widget=self._wgt[6][1]), 1, 0, 1, 1, Qt.AlignmentFlag.AlignTop
		)

		# Set Up Layout: Supplier [Template] ---------------------------------------------------------------------------
		self._ctr[7].addWidget(
			WidgetLabel(title="MS-Word Template:", widget=self._wgt[7][0]), 0, 0, 1, 1, Qt.AlignmentFlag.AlignTop
		)

		self._data = Storage().data
		self._reset_view()
		self.show()

	def _generate_do_number(self):
		spr = self._wgt[0][1].variable
		if spr:
			if self._wgt[-2].text() == "Add":
				idx = sum(1 for i in self._data["delivery"] if self._data["delivery"][i]["supplier"] == spr)
				self._wgt[0][3].variable = f"""{1 + idx:08}"""
			else:
				if self.tree1.selectedItems():
					data = self.tree1.selectedItems()[0].data(0, Qt.ItemDataRole.UserRole)
					if data["supplier"]["index"] != spr:
						idx = sum(1 for i in self._data["delivery"] if self._data["delivery"][i]["supplier"] == spr)
						self._wgt[0][3].variable = f"""{1 + idx:08}"""
					else:
						self._wgt[0][3].variable = data["order"]

	def _update_available_stock_and_price(self):
		idx = self._wgt[1][0].variable
		if self.tree1.selectedItems() and idx:
			data = self.tree1.selectedItems()[0].data(0, Qt.ItemDataRole.UserRole)["product"][idx]
			self._wgt[1][1].variable = f"""{data["quantity"]:,}"""
			self._wgt[1][2].variable = f"""{data["price"]:,.2f}"""

	def _reset_view(self):
		for item in self._hdr:
			item.setText("")
			item.setEnabled(False)
			item.setVisible(False)
		for item in self._ctr:
			item.setVisible(False)
		self._pnl[2].setVisible(False)

	@Slot(int)
	def _grp_button_pressed(self, index):
		if index == self._grp.checkedId():
			self._reset_view()
			match index:
				case 0:  # Delivery Order
					self.tree1.set_headers(["No", "DO Number", "Date", "Client", "Total", "Generated", ""])
					self.tree2.set_headers(["No", "Product", "Product SKU", "Client SKU", "Price", "Quantity", ""])
					buttons = [
						["New Order", "new_delivery", 0],
						["Edit Order", "edit_delivery", 1],
						["Generate Order", "generate_delivery", 2],
						["Open in MS-Word", "open_document", 3],
						["Add Item", "new_item", 4],
						["Edit Item", "edit_item", 5]
					]
				case 1:  # Products
					self.tree1.set_headers(["No", "Product", "SKU", "Price", "Quantity", "In Distribution", ""])
					self.tree2.set_headers(["No", "Date", "Source", "Quantity", "Editable", ""])
					buttons = [
						["New Product", "new_product", 0],
						["Edit Product", "edit_product", 1],
						["Add Stock", "new_stock", 4],
						["Edit Stock", "edit_stock", 5]
					]
				case 2:  # Clients
					self.tree1.set_headers(["No", "Name", "Custom SKU", "Dual Locations", "Price in DO", ""])
					self.tree2.set_headers(["No", "Product", "Product SKU", "Client SKU", "In Distribution", ""])
					buttons = [
						["New Client", "new_client", 0],
						["Edit Client", "edit_client", 1],
						["Add Client SKU", "new_client_sku", 4],
						["Edit Client SKU", "edit_client_sku", 5]
					]
				case _:  # Supplier
					self.tree1.set_headers(["No", "Name", ""])
					self.tree2.set_headers(["No", "Template", "File Location", ""])
					buttons = [
						["New Supplier", "new_supplier", 0],
						["Edit Supplier", "edit_supplier", 1],
						["Replace Template", "replace_template", 5],
						["Open in MS-Word", "open_template", 6]
					]
			for button in buttons:
				self._hdr[button[2]].setText(button[0])
				self._hdr[button[2]].setObjectName(button[1])
				self._hdr[button[2]].setVisible(True)
			self._hdr[0].setEnabled(True)
			self._pnl[0].setDisabled(False)
			self._pnl[1].setDisabled(False)
			self._tree1_item_refresh(index)

	def _hdr_button_pressed(self):
		disable_main = True
		disable_content = True
		curr_ctr = -1
		self._pnl[2].setVisible(False)
		match self.sender().objectName():
			case "new_delivery":
				self._wgt[-2].update_button("Add", "add_delivery")
				curr_ctr = 0
				for item in self._wgt[curr_ctr]:
					item.clear_all()
				for k, v in sorted(self._data["client"].items(), key=lambda x: x[1]["name"]):
					self._wgt[curr_ctr][0].addItem(v["name"], userData=k)
				self._wgt[0][1].blockSignals(True)
				for k, v in sorted(self._data["supplier"].items(), key=lambda x: x[1]["name"]):
					self._wgt[curr_ctr][1].addItem(v["name"], userData=k)
				self._wgt[0][1].blockSignals(False)
				self._generate_do_number()
			case "edit_delivery":
				if self.tree1.selectedItems():
					self._wgt[-2].update_button("Update", "update_delivery")
					curr_ctr = 0
					for item in self._wgt[curr_ctr]:
						item.clear_all()
					for k, v in sorted(self._data["client"].items(), key=lambda x: x[1]["name"]):
						self._wgt[curr_ctr][0].addItem(v["name"], userData=k)
					self._wgt[0][1].blockSignals(True)
					for k, v in sorted(self._data["supplier"].items(), key=lambda x: x[1]["name"]):
						self._wgt[curr_ctr][1].addItem(v["name"], userData=k)
					self._wgt[0][1].blockSignals(False)
					data = self.tree1.selectedItems()[0].data(0, Qt.ItemDataRole.UserRole)
					self._wgt[curr_ctr][0].variable = data["client"]["name"]
					self._wgt[0][1].blockSignals(True)
					self._wgt[curr_ctr][1].variable = data["supplier"]["name"]
					self._wgt[0][1].blockSignals(False)
					self._wgt[curr_ctr][2].variable = data["date"]
					# self._wgt[curr_ctr][3].variable = data["order"]
					self._generate_do_number()
				else:
					disable_main = False
					disable_content = False
			case "new_item":
				if self.tree1.selectedItems():
					self._wgt[-2].update_button("Add", "add_item")
					curr_ctr = 1
					for item in self._wgt[curr_ctr]:
						item.clear_all()
					data = self.tree1.selectedItems()[0].data(0, Qt.ItemDataRole.UserRole)
					used = [data["details"][i]["product"] for i in data["details"]]
					for k, v in sorted(data["product"].items(), key=lambda x: x[1]["name"]):
						if k not in used:
							self._wgt[curr_ctr][0].addItem(v["name"], userData=k)
					# self._wgt[curr_ctr][3].variable =
					if data["client"]["location"]["dual"]:
						self._wgt[curr_ctr][3].variable = f"""{data["client"]["location"]["label1"]} Quantity:"""
						self._wgt[curr_ctr][5].variable = f"""{data["client"]["location"]["label2"]} Quantity:"""
						self._wgt[curr_ctr][5].setVisible(True)
						self._wgt[curr_ctr][6].setVisible(True)
					else:
						self._wgt[curr_ctr][3].variable = "Quantity:"
						self._wgt[curr_ctr][5].variable = ""
						self._wgt[curr_ctr][5].setVisible(False)
						self._wgt[curr_ctr][6].setVisible(False)
				else:
					disable_main = False
					disable_content = False
			case "edit_item":
				if self.tree1.selectedItems() and self.tree2.selectedItems():
					self._wgt[-2].update_button("Update", "update_item")
					curr_ctr = 1
					for item in self._wgt[curr_ctr]:
						item.clear_all()
					data = self.tree1.selectedItems()[0].data(0, Qt.ItemDataRole.UserRole)
					for k, v in sorted(self._data["product"].items(), key=lambda x: x[1]["name"]):
						if not v["discontinued"]:
							self._wgt[curr_ctr][0].addItem(v["name"], userData=k)
					if data["client"]["location"]["dual"]:
						self._wgt[curr_ctr][3].variable = f"""{data["client"]["location"]["label1"]} Quantity:"""
						self._wgt[curr_ctr][5].variable = f"""{data["client"]["location"]["label2"]} Quantity:"""
						self._wgt[curr_ctr][5].setVisible(True)
						self._wgt[curr_ctr][6].setVisible(True)
					else:
						self._wgt[curr_ctr][3].variable = "Quantity:"
						self._wgt[curr_ctr][5].variable = ""
						self._wgt[curr_ctr][5].setVisible(False)
						self._wgt[curr_ctr][6].setVisible(False)
					data = self.tree2.selectedItems()[0].data(0, Qt.ItemDataRole.UserRole)
					self._wgt[curr_ctr][0].variable = data["product_name"]
					self._wgt[curr_ctr][4].variable = data["location1"]
					self._wgt[curr_ctr][6].variable = data["location2"]
				else:
					disable_main = False
					disable_content = False
			case "new_product":
				self._wgt[-2].update_button("Add", "add_product")
				curr_ctr = 2
				for item in self._wgt[curr_ctr]:
					item.clear_all()
			case "edit_product":
				if self.tree1.selectedItems():
					self._wgt[-2].update_button("Update", "update_product")
					curr_ctr = 2
					for item in self._wgt[curr_ctr]:
						item.clear_all()
					data = self.tree1.selectedItems()[0].data(0, Qt.ItemDataRole.UserRole)
					self._wgt[curr_ctr][0].variable = data["name"]
					self._wgt[curr_ctr][1].variable = data["sku"]
					self._wgt[curr_ctr][2].variable = data["price"]
					self._wgt[curr_ctr][3].variable = data["discontinued"]
				else:
					disable_main = False
					disable_content = False
			case "new_stock":
				if self.tree1.selectedItems():
					self._wgt[-2].update_button("Add", "add_stock")
					curr_ctr = 3
					for item in self._wgt[curr_ctr]:
						item.clear_all()
					for item in ("New Shipment", "Stock Adjustment"):
						self._wgt[curr_ctr][0].addItem(item, userData=item)
				else:
					disable_main = False
					disable_content = False
			case "edit_stock":
				if self.tree1.selectedItems() and self.tree2.selectedItems():
					self._wgt[-2].update_button("Save", "save_stock")
					curr_ctr = 3
					for item in self._wgt[curr_ctr]:
						item.clear_all()
					for item in ("New Shipment", "Stock Adjustment"):
						self._wgt[curr_ctr][0].addItem(item, userData=item)
					data = self.tree2.selectedItems()[0].data(0, Qt.ItemDataRole.UserRole)
					self._wgt[curr_ctr][0].variable = data["source"]
					self._wgt[curr_ctr][1].variable = data["amount"]
					self._wgt[curr_ctr][2].variable = data["date"]
				else:
					disable_main = False
					disable_content = False
			case "new_client":
				self._wgt[-2].update_button("Add", "add_client")
				curr_ctr = 4
				for item in self._wgt[curr_ctr]:
					item.clear_all()
			case "edit_client":
				if self.tree1.selectedItems():
					self._wgt[-2].update_button("Update", "update_client")
					curr_ctr = 4
					for item in self._wgt[curr_ctr]:
						item.clear_all()
					data = self.tree1.selectedItems()[0].data(0, Qt.ItemDataRole.UserRole)
					self._wgt[curr_ctr][0].variable = data["name"]
					self._wgt[curr_ctr][1].variable = data["address1"]
					self._wgt[curr_ctr][2].variable = data["address2"]
					self._wgt[curr_ctr][3].variable = data["postcode"]
					self._wgt[curr_ctr][4].variable = data["city"]
					self._wgt[curr_ctr][5].variable = data["state"]
					self._wgt[curr_ctr][6].variable = data["location"]["dual"]
					self._wgt[curr_ctr][7].variable = data["location"]["label1"]
					self._wgt[curr_ctr][8].variable = data["location"]["label2"]
					self._wgt[curr_ctr][9].variable = data["show_price"]
				else:
					disable_main = False
					disable_content = False
			case "new_client_sku":
				if self.tree1.selectedItems():
					self._wgt[-2].update_button("Add", "add_client_sku")
					curr_ctr = 5
					for item in self._wgt[curr_ctr]:
						item.clear_all()
					data = self.tree1.selectedItems()[0].data(0, Qt.ItemDataRole.UserRole)
					used = [data["custom_sku"][i]["product"] for i in data["custom_sku"]]
					for k, v in sorted(self._data["product"].items(), key=lambda x: x[1]["name"]):
						if not v["discontinued"] and k not in used:
							self._wgt[curr_ctr][0].addItem(v["name"], userData=k)
				else:
					disable_main = False
					disable_content = False
			case "edit_client_sku":
				if self.tree1.selectedItems() and self.tree2.selectedItems():
					self._wgt[-2].update_button("Save", "save_client_sku")
					curr_ctr = 5
					for item in self._wgt[curr_ctr]:
						item.clear_all()
					data = self.tree2.selectedItems()[0].data(0, Qt.ItemDataRole.UserRole)
					self._wgt[curr_ctr][0].addItem(data["product_name"], userData=data["product_index"])
					self._wgt[curr_ctr][1].variable = data["client_sku"]
				else:
					disable_main = False
					disable_content = False
			case "new_supplier":
				self._wgt[-2].update_button("Add", "add_supplier")
				curr_ctr = 6
				for item in self._wgt[curr_ctr]:
					item.clear_all()
				if not self._wgt[curr_ctr][1].parent().isEnabled():
					self._wgt[curr_ctr][1].parent().setEnabled(True)
					self._wgt[curr_ctr][2].setEnabled(True)
			case "edit_supplier":
				if self.tree1.selectedItems():
					self._wgt[-2].update_button("Update", "update_supplier")
					curr_ctr = 6
					for item in self._wgt[curr_ctr]:
						item.clear_all()
					if self._wgt[curr_ctr][1].parent().isEnabled():
						self._wgt[curr_ctr][1].parent().setEnabled(False)
					data = self.tree1.selectedItems()[0].data(0, Qt.ItemDataRole.UserRole)
					self._wgt[curr_ctr][0].variable = data["name"]
					self._wgt[curr_ctr][1].variable = data["template"]
			case "replace_template":
				if self.tree1.selectedItems() and self.tree2.selectedItems():
					self._wgt[-2].update_button("Replace", "replace_template")
					curr_ctr = 7
					for item in self._wgt[curr_ctr]:
						item.clear_all()
					data = self.tree2.selectedItems()[0].data(0, Qt.ItemDataRole.UserRole)
					self._wgt[curr_ctr][0].variable = data
			case "open_template":
				if self.tree1.selectedItems() and self.tree2.selectedItems():
					data = self.tree2.selectedItems()[0].data(0, Qt.ItemDataRole.UserRole)
					subprocess.run(["open", data], check=True)
					disable_main = False
					disable_content = False
			case "generate_delivery":
				if self.tree1.selectedItems():
					data = self.tree1.selectedItems()[0].data(0, Qt.ItemDataRole.UserRole)
					label1 = ""
					label2 = "Quantity"
					if data["client"]["show_price"]:
						label1 = "Price"
					elif data["client"]["location"]["dual"]:
						label1 = f"""Quantity\n{data["client"]["location"]["label1"]}"""
						label2 = f"""Quantity\n{data["client"]["location"]["label2"]}"""
					qty = {}
					for i in data["details"]:
						lk = data["details"][i]
						if data["client"]["show_price"]:
							qty[lk["product"]] = [
								f"""{data["product"][lk["product"]]["price"]:,.2f}""",
								f"""{lk["location1"]:,}"""
							]
						elif data["client"]["location"]["dual"]:
							qty[lk["product"]] = [f"""{lk["location1"]:,}""", f"""{lk["location2"]:,}"""]
						else:
							qty[lk["product"]] = ["", f"""{lk["location1"]:,}"""]
					items = []
					for k, v in sorted(data["product"].items(), key=lambda x: x[1]["name"]):
						if k in qty:
							items.append({
								"count": len(items) + 1,
								"client_sku": v["client_sku"],
								"product_name": v["name"],
								"quantity1": qty[k][0],
								"quantity2": qty[k][1]
							})
					output = {
						"client_name": data["client"]["name"],
						"client_address1": data["client"]["address1"],
						"client_address2": data["client"]["address2"],
						"client_postcode": data["client"]["postcode"],
						"client_city": data["client"]["city"],
						"client_state": data["client"]["state"],
						"do_number": data["order"],
						"do_date": time.strftime("%d %b %Y", time.localtime(data["date"])),
						"label1": label1,
						"label2": label2,
						"items": items
					}

					# Generate Document
					document = app_path(
						filename=f"""{output["do_number"]}.doc""",
						directory=f"""documents/{output["client_name"]}""",
						write_file=True,
						root_folder=True
					)
					template = MailMerge(data["supplier"]["template"])
					template.merge_templates(
						[
							{
								"do_number": output["do_number"],
								"do_date": output["do_date"],
								"client_name": output["client_name"],
								"client_address1": output["client_address1"],
								"client_address2": output["client_address2"],
								"client_postcode": output["client_postcode"],
								"client_city": output["client_city"],
								"client_state": output["client_state"],
								"label1": output["label1"],
								"label2": output["label2"],
								"count": output["items"]
							}
						],
						separator="page_break")
					template.write(document)

					# Update Data
					self._data["delivery"][data["index"]]["document"] = document
					if not self._data["delivery"][data["index"]]["committed"]:
						for i in data["details"]:
							idx = f"""{len(self._data["product"][data["details"][i]["product"]]["quantity"]):04}"""
							self._data["product"][data["details"][i]["product"]]["quantity"][idx] = {
								"index": idx,
								"source": f"""[{output["do_number"]}] {output["client_name"]}""",
								"amount": -(data["details"][i]["location1"] + data["details"][i]["location2"]),
								"date": data["date"],
								"locked": True
							}
						self._data["delivery"][data["index"]]["committed"] = True
					self._tree1_item_refresh(0)
					for idx in range(2, len(self._pnl)):
						self._pnl[idx].setVisible(False)
					disable_main = False
					disable_content = False
			case "open_document":
				if self.tree1.selectedItems():
					data = self.tree1.selectedItems()[0].data(0, Qt.ItemDataRole.UserRole)
					subprocess.run(["open", data["document"]], check=True)
					disable_main = False
					disable_content = False
			case _:
				disable_main = False
				disable_content = False
		self._pnl[0].setDisabled(disable_main)
		self._pnl[1].setDisabled(disable_content)
		for item in self._ctr:
			item.setVisible(False)
		if curr_ctr != -1:
			self._ctr[curr_ctr].setVisible(True)
			self._pnl[2].setVisible(True)

	def _pnl_button_pressed(self):
		reset_views = False
		reset_buttons = True
		sdr = self.sender().objectName()
		match sdr:
			case "add_delivery" | "update_delivery":
				ctr = 0
				clt = self._wgt[ctr][0].variable
				spr = self._wgt[ctr][1].variable
				if sdr == "add_delivery" and clt and spr:
					idx = f"""{len(self._data["delivery"]):04}"""
					self._data["delivery"][idx] = {
						"index": idx,
						"client": clt,
						"supplier": spr,
						"date": self._wgt[ctr][2].variable,
						"order": self._wgt[ctr][3].variable,
						"details": {},
						"document": "",
						"committed": False
					}
					self._tree1_item_refresh(0)
					reset_views = True
				if sdr == "update_delivery" and self.tree1.selectedItems() and clt and spr:
					idx = self.tree1.selectedItems()[0].data(0, Qt.ItemDataRole.UserRole)["index"]
					self._data["delivery"][idx]["client"] = clt
					self._data["delivery"][idx]["supplier"] = spr
					self._data["delivery"][idx]["date"] = self._wgt[ctr][2].variable
					self._data["delivery"][idx]["order"] = self._wgt[ctr][3].variable
					self._tree1_item_refresh(0)
					reset_views = True
			case "add_item" | "update_item":
				ctr = 1
				pdt = self._wgt[ctr][0].variable
				qty = self._wgt[ctr][4].variable
				if sdr == "add_item" and self.tree1.selectedItems() and pdt and qty:
					idx1 = self.tree1.selectedItems()[0].data(0, Qt.ItemDataRole.UserRole)["index"]
					idx2 = f"""{len(self._data["delivery"][idx1]["details"]):04}"""
					self._data["delivery"][idx1]["details"][idx2] = {
						"index": idx2,
						"product": pdt,
						"location1": qty,
						"location2": self._wgt[ctr][6].variable if self._wgt[ctr][6].isVisible() else 0,
					}
					self._tree1_item_refresh(0)
					reset_views = True
				if sdr == "update_item" and self.tree1.selectedItems() and self.tree2.selectedItems() and pdt and qty:
					idx1 = self.tree1.selectedItems()[0].data(0, Qt.ItemDataRole.UserRole)["index"]
					idx2 = self.tree2.selectedItems()[0].data(0, Qt.ItemDataRole.UserRole)["index"]
					self._data["delivery"][idx1]["details"][idx2]["product"] = pdt
					self._data["delivery"][idx1]["details"][idx2]["location1"] = qty
					self._data["delivery"][idx1]["details"][idx2]["location2"] = self._wgt[ctr][6].variable
					self._tree1_item_refresh(0)
					reset_views = True
			case "add_product" | "update_product":
				ctr = 2
				nme = self._wgt[ctr][0].variable
				sku = self._wgt[ctr][1].variable
				prc = self._wgt[ctr][2].variable
				if sdr == "add_product" and nme and sku and prc:
					idx = f"""{len(self._data["product"]):04}"""
					self._data["product"][idx] = {
						"index": idx,
						"name": nme,
						"sku": sku,
						"price": prc,
						"quantity": {},
						"discontinued": self._wgt[ctr][3].variable
					}
					self._tree1_item_refresh(1)
					reset_views = True
				if sdr == "update_product" and self.tree1.selectedItems() and nme and sku and prc:
					idx = self.tree1.selectedItems()[0].data(0, Qt.ItemDataRole.UserRole)["index"]
					self._data["product"][idx]["name"] = nme
					self._data["product"][idx]["sku"] = sku
					self._data["product"][idx]["price"] = prc
					self._data["product"][idx]["discontinued"] = self._wgt[ctr][3].variable
					self._tree1_item_refresh(1)
					reset_views = True
			case "add_stock" | "save_stock":
				ctr = 3
				qty = self._wgt[ctr][1].variable
				ve = (self._wgt[ctr][0].currentIndex() and qty) or (not self._wgt[ctr][0].currentIndex() and qty > 0)
				if sdr == "add_stock" and self.tree1.selectedItems() and ve:
					idx1 = self.tree1.selectedItems()[0].data(0, Qt.ItemDataRole.UserRole)["index"]
					idx2 = f"""{len(self._data["product"][idx1]["quantity"]):04}"""
					self._data["product"][idx1]["quantity"][idx2] = {
						"index": idx2,
						"source": self._wgt[ctr][0].variable,
						"amount": qty,
						"date": self._wgt[ctr][2].variable,
						"locked": False
					}
					self._tree1_item_refresh(1)
					reset_views = True
				if sdr == "save_stock" and self.tree1.selectedItems() and self.tree2.selectedItems() and ve:
					idx1 = self.tree1.selectedItems()[0].data(0, Qt.ItemDataRole.UserRole)["index"]
					idx2 = self.tree2.selectedItems()[0].data(0, Qt.ItemDataRole.UserRole)["index"]
					self._data["product"][idx1]["quantity"][idx2] = {
						"index": idx2,
						"source": self._wgt[ctr][0].variable,
						"amount": qty,
						"date": self._wgt[ctr][2].variable,
						"locked": False
					}
					self._tree1_item_refresh(1)
					reset_views = True
			case "add_client" | "update_client":
				ctr = 4
				dual = self._wgt[ctr][6].variable
				label1 = self._wgt[ctr][7].variable
				label2 = self._wgt[ctr][8].variable
				ve1 = (dual and label1 and label2) or not dual
				ve2 = all(self._wgt[ctr][i].variable for i in range(6))
				if sdr == "add_client" and ve1 and ve2:
					idx = f"""{len(self._data["client"]):04}"""
					self._data["client"][idx] = {
						"index": idx,
						"name": self._wgt[ctr][0].variable,
						"address1": self._wgt[ctr][1].variable,
						"address2": self._wgt[ctr][2].variable,
						"postcode": self._wgt[ctr][3].variable,
						"city": self._wgt[ctr][4].variable,
						"state": self._wgt[ctr][5].variable,
						"custom_sku": {},
						"location": {
							"dual": dual,
							"label1": label1,
							"label2": label2
						},
						"show_price": self._wgt[ctr][9].variable
					}
					self._tree1_item_refresh(2)
					reset_views = True
				if sdr == "update_client" and self.tree1.selectedItems() and ve1 and ve2:
					idx = self.tree1.selectedItems()[0].data(0, Qt.ItemDataRole.UserRole)["index"]
					self._data["client"][idx]["name"] = self._wgt[ctr][0].variable
					self._data["client"][idx]["address1"] = self._wgt[ctr][1].variable
					self._data["client"][idx]["address2"] = self._wgt[ctr][2].variable
					self._data["client"][idx]["postcode"] = self._wgt[ctr][3].variable
					self._data["client"][idx]["city"] = self._wgt[ctr][4].variable
					self._data["client"][idx]["state"] = self._wgt[ctr][5].variable
					self._data["client"][idx]["location"]["dual"] = dual
					self._data["client"][idx]["location"]["label1"] = label1
					self._data["client"][idx]["location"]["label2"] = label2
					self._data["client"][idx]["show_price"] = self._wgt[ctr][9].variable
					self._tree1_item_refresh(2)
					reset_views = True
			case "add_client_sku" | "save_client_sku":
				ctr = 5
				pdt = self._wgt[ctr][0].variable
				sku = self._wgt[ctr][1].variable
				if sdr == "add_client_sku" and self.tree1.selectedItems() and pdt and sku:
					idx1 = self.tree1.selectedItems()[0].data(0, Qt.ItemDataRole.UserRole)["index"]
					idx2 = f"""{len(self._data["client"][idx1]["custom_sku"]):04}"""
					self._data["client"][idx1]["custom_sku"][idx2] = {
						"index": idx2,
						"product": pdt,
						"sku": sku
					}
					self._tree1_item_refresh(2)
					reset_views = True
				if sdr == "save_client_sku" and self.tree1.selectedItems() and self.tree2.selectedItems() and sku:
					idx = self.tree1.selectedItems()[0].data(0, Qt.ItemDataRole.UserRole)["index"]
					data = self.tree2.selectedItems()[0].data(0, Qt.ItemDataRole.UserRole)
					self._data["client"][idx]["custom_sku"][data["index"]]["sku"] = sku
					self._tree1_item_refresh(2)
					reset_views = True
			case "add_supplier" | "update_supplier":
				ctr = 6
				spr = self._wgt[ctr][0].variable
				src = self._wgt[ctr][1].variable
				if sdr == "add_supplier" and spr and src:
					idx = f"""{len(self._data["supplier"]):04}"""
					dst = app_path(filename=f"""{idx}.docx""", directory="templates", write_file=True, root_folder=True)
					shutil.copy(src, dst)
					self._data["supplier"][idx] = {
						"index": idx,
						"name": spr,
						"template": dst
					}
					self._tree1_item_refresh(3)
					reset_views = True
				if sdr == "update_supplier" and self.tree1.selectedItems() and spr:
					idx = self.tree1.selectedItems()[0].data(0, Qt.ItemDataRole.UserRole)["index"]
					self._data["supplier"][idx]["name"] = spr
					self._tree1_item_refresh(3)
					reset_views = True
			case "replace_template":
				ctr = 7
				doc = self._wgt[ctr][0].variable
				if self.tree1.selectedItems() and self.tree2.selectedItems() and doc:
					idx = self.tree1.selectedItems()[0].data(0, Qt.ItemDataRole.UserRole)["index"]
					shutil.copy(doc, self._data["supplier"][idx]["template"])
					self._tree1_item_refresh(3)
					reset_views = True
			case _:
				reset_views = True
				reset_buttons = False
		if reset_views:
			for idx in range(2, len(self._pnl)):
				self._pnl[idx].setVisible(False)
			self._pnl[0].setDisabled(False)
			self._pnl[1].setDisabled(False)
		if reset_buttons:
			for idx in range(1, len(self._hdr)):
				self._hdr[idx].setEnabled(False)

	def _tree1_item_refresh(self, index):
		Storage().data = self._data
		self.tree1.clear()
		self.tree2.clear()
		match index:
			case 0:  # Delivery Order
				for i in sorted(self._data["delivery"], reverse=True):
					data = self._data["delivery"][i].copy()
					data["client"] = self._data["client"][data["client"]].copy()
					data["supplier"] = self._data["supplier"][data["supplier"]].copy()
					data["product"] = {}
					lk = data["client"]["custom_sku"]
					tmp = {lk[j]["product"]: lk[j]["sku"] for j in lk}
					for k, v in tmp.items():
						if not self._data["product"][k]["discontinued"]:
							lk = self._data["product"][k].copy()
							data["product"][k] = {
								"index": k,
								"name": lk["name"],
								"internal_sku": lk["sku"],
								"client_sku": v,
								"price": lk["price"],
								"quantity": sum(lk["quantity"][j]["amount"] for j in lk["quantity"])
							}
					TreeItemDelivery(parent=self.tree1, data=data)
			case 1:  # Products
				for i in sorted(self._data["product"], reverse=True):
					TreeItemProduct(parent=self.tree1, data=self._data["product"][i])
			case 2:  # Clients
				for i in sorted(self._data["client"], reverse=True):
					TreeItemClient(parent=self.tree1, data=self._data["client"][i])
			case _:  # Supplier
				for i in sorted(self._data["supplier"], reverse=True):
					TreeItemSupplier(parent=self.tree1, data=self._data["supplier"][i])
		self.tree1.resize_tree()
		self.tree2.resize_tree()

	def _tree1_item_selected(self):
		if self.tree1.selectedItems():
			self.tree2.clear()
			for item in (self._hdr[1], self._hdr[2], self._hdr[3], self._hdr[4]):
				item.setEnabled(True if item.isVisible() else False)
			for item in (self._hdr[5], self._hdr[6]):
				item.setEnabled(False)
			item = self.tree1.selectedItems()[0]
			idx = item.data(0, Qt.ItemDataRole.UserRole)["index"]
			tmp = {}
			match item.recordType:
				case "delivery":  # Delivery Order
					client_lk = self._data[item.recordType][idx]["client"]
					for i in self._data[item.recordType][idx]["details"]:
						prod_lk = self._data[item.recordType][idx]["details"][i]["product"]
						csku_lk = self._data["client"][client_lk]["custom_sku"]
						qty_lk = self._data["product"][prod_lk]["quantity"]
						tmp[self._data["product"][prod_lk]["name"]] = {
							"index": i,
							"product_name": self._data["product"][prod_lk]["name"],
							"product_index": self._data["product"][prod_lk]["index"],
							"product_sku": self._data["product"][prod_lk]["sku"],
							"product_qty": sum(qty_lk[j]["amount"] for j in qty_lk),
							"product_price": self._data["product"][prod_lk]["price"],
							"client_sku": csku_lk[i]["sku"] if csku_lk and i in csku_lk else "N/A",
							"location1": self._data[item.recordType][idx]["details"][i]["location1"],
							"location2": self._data[item.recordType][idx]["details"][i]["location2"]
						}
					for i in sorted(tmp):
						TreeItemItems(parent=self.tree2, data=tmp[i])
					for i in (self._hdr[1], self._hdr[4]):
						i.setDisabled(True if self._data[item.recordType][idx]["document"] else False)
					self._hdr[2].setDisabled(False if int(item.text(4).replace(",", "")) else True)
					self._hdr[3].setDisabled(False if self._data[item.recordType][idx]["document"] else True)
				case "product":  # Products
					for i in self._data[item.recordType][idx]["quantity"]:
						tmp[f"""{self._data[item.recordType][idx]["quantity"][i]["date"]}_{i}"""] = {
							"index": self._data[item.recordType][idx]["quantity"][i]["index"],
							"date": self._data[item.recordType][idx]["quantity"][i]["date"],
							"source": self._data[item.recordType][idx]["quantity"][i]["source"],
							"amount": self._data[item.recordType][idx]["quantity"][i]["amount"],
							"locked": self._data[item.recordType][idx]["quantity"][i]["locked"]
						}
					for i in sorted(tmp, reverse=True):
						TreeItemStock(parent=self.tree2, data=tmp[i])
					self._hdr[4].setDisabled(self._data[item.recordType][idx]["discontinued"])
				case "client":  # Clients
					for i in self._data[item.recordType][idx]["custom_sku"]:
						prod_lk = self._data[item.recordType][idx]["custom_sku"][i]["product"]
						tmp[self._data["product"][prod_lk]["name"]] = {
							"index": i,
							"product_name": self._data["product"][prod_lk]["name"],
							"product_index": self._data["product"][prod_lk]["index"],
							"product_sku": self._data["product"][prod_lk]["sku"],
							"client_sku": self._data[item.recordType][idx]["custom_sku"][i]["sku"],
							"locked": self._data["product"][prod_lk]["discontinued"]
						}
					for i in sorted(tmp, reverse=True):
						TreeItemCustomSKU(parent=self.tree2, data=tmp[i])
				case _:  # Supplier
					TreeItemTemplate(parent=self.tree2, data=self._data[item.recordType][idx]["template"])
			self.tree2.resize_tree()

	def _tree2_item_selected(self):
		if self.tree1.selectedItems() and self.tree2.selectedItems():
			for item in (self._hdr[5], self._hdr[6]):
				item.setEnabled(True if item.isVisible() else False)
			data = self.tree2.selectedItems()[0].data(0, Qt.ItemDataRole.UserRole)
			if (
					(self.tree1.selectedItems()[0].recordType == "product" and "locked" in data) or
					(self.tree1.selectedItems()[0].recordType == "client" and "locked" in data)
			):
				self._hdr[5].setDisabled(data["locked"])


if __name__ == "__main__":
	app = QApplication()
	app.setWindowIcon(QIcon(app_path("icon.ico")))
	main = MainUI()
	main.setStyleSheet(stylesheet())
	app.exec()
