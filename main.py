from PySide6.QtCore import (
	QTimer, QThread, QDir, Property, QPropertyAnimation, QSize, Slot, QDate, QDateTime, QAbstractTableModel,
	QModelIndex, QObject, QSortFilterProxyModel, Qt, Signal
)
from PySide6.QtWidgets import (
	QApplication, QSplashScreen, QMainWindow, QFileDialog, QAbstractButton, QAbstractItemView, QButtonGroup, QComboBox, QDoubleSpinBox, QFrame, QGraphicsDropShadowEffect,
	QGridLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QStackedWidget, QSizePolicy, QSpinBox, QTableView,
	QTextBrowser, QTreeWidget, QTreeWidgetItem, QVBoxLayout, QWidget, QInputDialog, QDialog, QDialogButtonBox,
	QFormLayout, QDateTimeEdit, QRadioButton, QCheckBox, QSpacerItem
)
from PySide6.QtGui import (
	QPainter, QIcon, QValidator, QPixmap
)

import os
import json
import time


def app_path(filename, directory="resource", write_file=False):
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

	@property
	def data(self):
		if app_path(filename="data", directory="stored"):
			fd = open(app_path(filename="data", directory="stored"), "r")
			data = json.loads(fd.read())
			fd.close()
		else:
			data = {"delivery": {}, "product": {}, "client": {}}
		return data

	@data.setter
	def data(self, data):
		tmp = self.data
		for item in data:
			tmp[item] = data[item]
		fd = open(app_path(filename="data", directory="stored", write_file=True), "w")
		json_object = json.dumps(tmp, indent=4)
		fd.write(json_object)
		fd.close()


# -------------------------------------------------------------------------------------------------------------------- #
APP_TITLE = "Inventory & Stock Manager"
APP_VERSION = "v0.0.1"
APP_SPLASH = app_path("splash.png")
APP_ICON = app_path("icon.ico")


def stylesheet(darkmode=False):
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
		padding-right: 8px; 
		padding-left: 8px;
		padding-top: 4px;
		padding-bottom: 4px;
	}}
	QAbstractButton[prop_type="2"]:disabled {{
		background: rgba(0, 139, 204, 0.15);
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
		background: rgba(0, 128, 0, 0.15);
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
		background: rgba(172, 32, 22, 0.15);
	}}
	QAbstractButton[prop_type="4"]:hover {{
		background: rgb(149, 28, 19);
	}}
	QAbstractButton[prop_type="4"]:pressed {{
		background: rgb(126, 24, 16);
	}}


	/*----- QAbstractScrollArea -----*/
	QAbstractScrollArea::corner {{
		background: transparent;
	}}

	/*----- QAbstractSpinBox -----*/
	QAbstractSpinBox {{
		background: transparent;
		border: 1px solid {"rgba(204, 204, 204, 0.2)" if darkmode else "rgba(30, 144, 255, 0.2)"};
		border-radius: 6px;
		color: {"rgb(204, 204, 204)" if darkmode else "rgb(51, 51, 51)"};
		font-size: 13px;
		font-weight: 552;
		padding-right: 4px;
	}}
	QAbstractSpinBox:disabled {{
		color: {"rgba(204, 204, 204, 0.2)" if darkmode else "rgba(51, 51, 51, 0.2)"};
	}}
	QAbstractSpinBox::down-button, QAbstractSpinBox::up-button {{
		border: none;
		background: {"rgba(204, 204, 204, 0.5)" if darkmode else "rgba(30, 144, 255, 0.5)"};
		width: 16px;
	}}
	QAbstractSpinBox::down-arrow {{
		image: url({name_to_pix("chevrondowndark" if darkmode else "chevrondownlight")});
		width: 16px;
	}}
	QAbstractSpinBox::down-button {{
		border-bottom-right-radius: 6px;
	}}
	QAbstractSpinBox::down-button:disabled, QAbstractSpinBox::up-button:disabled {{
		background: {"rgba(204, 204, 204, 0.2)" if darkmode else "rgba(30, 144, 255, 0.2)"};
	}}
	QAbstractSpinBox::down-button:hover, QAbstractSpinBox::up-button:hover {{
		background: {"rgba(204, 204, 204, 0.8)" if darkmode else "rgba(30, 144, 255, 0.8)"};
	}}
	QAbstractSpinBox::down-button:pressed, QAbstractSpinBox::up-button:pressed {{
		background: {"rgba(204, 204, 204, 1.0)" if darkmode else "rgba(30, 144, 255, 1.0)"};
	}}
	QAbstractSpinBox::up-arrow {{
		image: url({name_to_pix("chevronupdark" if darkmode else "chevronuplight")});
		width: 16px;
	}}
	QAbstractSpinBox::up-button {{
		border-top-right-radius: 6px;
	}}
	QAbstractSpinBox[prop_type="0"] {{
		padding-left: 0px;
	}}
	QAbstractSpinBox[prop_type="1"] {{
		padding-left: 4px;
	}}

	/*----- QComboBox -----*/
	QComboBox {{
		background: transparent;
		border: 1px solid {"rgba(204, 204, 204, 0.2)" if darkmode else "rgba(30, 144, 255, 0.2)"};
		border-radius: 6px;
		color: {"rgb(204, 204, 204)" if darkmode else "rgb(51, 51, 51)"};
		font-size: 13px;
		font-weight: 552;
		padding-left: 8px;
		padding-right: 4px;
		selection-background-color: {"rgba(204, 204, 204, 0.8)" if darkmode else "rgba(30, 144, 255, 0.8)"};
		selection-color: {"rgb(104, 104, 104)" if darkmode else "rgb(51, 51, 51)"};
	}}
	QComboBox:disabled {{
		color: {"rgba(204, 204, 204, 0.2)" if darkmode else "rgba(51, 51, 51, 0.2)"};		
	}}
	QComboBox::down-arrow {{
		image: url({name_to_pix("chevrondowndark" if darkmode else "chevrondownlight")});
		width: 16px;
	}}
	QComboBox::drop-down {{
		border: none;
		border-bottom-right-radius: 6px;
		border-top-right-radius: 6px;
		background: {"rgba(204, 204, 204, 0.5)" if darkmode else "rgba(30, 144, 255, 0.5)"};
		width: 16px;
	}}
	QComboBox::drop-down:disabled {{
		background: {"rgba(204, 204, 204, 0.2)" if darkmode else "rgba(30, 144, 255, 0.2)"};
	}}
	QComboBox::drop-down:hover {{
		background: {"rgba(204, 204, 204, 0.8)" if darkmode else "rgba(30, 144, 255, 0.8)"};
	}}
	QComboBox::drop-down:pressed {{
		background: {"rgba(204, 204, 204, 1.0)" if darkmode else "rgba(30, 144, 255, 1.0)"};
	}}
	QComboBox QAbstractItemView {{
		background: {"rgb(104, 104, 104)" if darkmode else "rgb(242, 242, 242)"};
		border: 1px solid {"rgba(204, 204, 204, 0.2)" if darkmode else "rgba(30, 144, 255, 0.2)"};
		color: {"rgb(166, 166, 166)" if darkmode else "rgb(51, 51, 51)"};
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
		image: url({name_to_pix("sortdowndark" if darkmode else "sortdownlight")})
	}}
	QHeaderView::up-arrow {{
		subcontrol-origin:padding;
		subcontrol-position: center right;
		width: 16px;
		image: url({name_to_pix("sortupdark" if darkmode else "sortuplight")})
	}}
	QHeaderView::section {{
		background: transparent;
		color: {"rgb(77, 77, 77)" if darkmode else "rgb(179, 179, 179)"};
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
		color: {"rgb(176, 176, 176)" if darkmode else "rgb(137, 137, 137)"};
		font-size: 14px;
		font-weight: 500;
	}}
	QLabel[prop_type="1"] {{
		background: transparent;
		color: {"rgb(176, 176, 176)" if darkmode else "rgb(137, 137, 137)"};
		font-size: 13px;
	}}
	QLabel[prop_type="2"] {{
		background: transparent;
		color: {"rgb(204, 204, 204)" if darkmode else "rgb(179, 179, 179)"};
		font-size: 14px;
		font-weight: 500;
	}}
	QLabel[prop_type="3"] {{
		background: transparent;
		color: {"rgb(176, 176, 176)" if darkmode else "rgb(137, 137, 137)"};
		font-size: 15px;
		font-weight: 500;
	}}
	QLabel[prop_type="4"] {{
		background: transparent;
		color: {"rgb(204, 204, 204)" if darkmode else "rgb(179, 179, 179)"};
		font-size: 12px;
		font-weight: 500;
	}}

	/*----- QLineEdit -----*/
	QLineEdit {{
		background: transparent;
		border: 1px solid {"rgba(204, 204, 204, 0.2)" if darkmode else "rgba(30, 144, 255, 0.2)"};
		border-radius: 6px;
		color: {"rgb(166, 166, 166)" if darkmode else "rgb(51, 51, 51)"};
		font-size: 13px;
		font-weight: 552;
		padding: 4px;
	}}

	/*----- QMainWindow -----*/
	QMainWindow {{
		background: {"rgb(45, 45, 45)" if darkmode else "rgb(230, 230, 230)"};
	}}

	/*----- QScrollBar -----*/
	QScrollBar {{
		background: {"rgb(97, 97, 97)" if darkmode else "rgb(204, 204, 204)"};
		border-radius: 6px;
	}}
	QScrollBar:horizontal {{
		height: 12px;
	}}
	QScrollBar:vertical {{
		width: 12px;
	}}
	QScrollBar::handle {{
		background: {"rgb(68, 68, 68)" if darkmode else "rgb(179, 179, 179)"};
		border-radius: 4px;
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

	/*----- QTableView -----*/
	QTableView {{
		background: {"rgb(104, 104, 104)" if darkmode else "rgb(242, 242, 242)"};
		border: 1px solid transparent;
		border-radius: 6px;
		color: {"rgb(204, 204, 204)" if darkmode else "rgb(51, 51, 51)"};
		font-size: 13px;
		padding: 2px;
	}}
	QTableView::item, QTableView::item:alternative {{
		background: transparent;
		border-top: 1px solid {"rgb(102, 102, 102)" if darkmode else "rgb(230, 230, 230)"};
	}}

	/*----- QTextBrowser -----*/
	QTextBrowser {{
		background: transparent;
		border: 1px solid {"rgba(204, 204, 204, 0.2)" if darkmode else "rgba(30, 144, 255, 0.2)"};
		border-radius: 6px;
		color: {"rgb(204, 204, 204)" if darkmode else "rgb(51, 51, 51)"};
		font-size: 13px;
		padding: 2px;
	}}

	/*----- QToolTip -----*/
	QToolTip {{
		color: {"rgb(204, 204, 204)" if darkmode else "rgb(51, 51, 51)"};
		background: {"rgb(38, 38, 79)" if darkmode else "rgb(255, 255, 240)"};
		padding: 2px;
	}}

	/*----- QTreeView -----*/
	QTreeView {{
		alternate-background-color: transparent;
		background: {"rgb(104, 104, 104)" if darkmode else "rgb(242, 242, 242)"};
		border: 1px solid transparent;
		border-radius: 6px;
		color: {"rgb(204, 204, 204)" if darkmode else "rgb(51, 51, 51)"};
		font-size: 13px;
		padding: 2px;
	}}
	QTreeView::branch:closed:has-children {{
		border-image: none;
		image: url({name_to_pix("branchclosedark" if darkmode else "branchcloselight")});
	}}
	QTreeView::branch:open {{
		border-image: none;
		image: url({name_to_pix("branchopendark" if darkmode else "branchopenlight")});
	}}
	QTreeView::item {{
		border-top: 1px solid transparent;
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
	"""


class LabelContainer(QWidget):

	def __init__(self, title, layout=None, widget=None, parent=None):
		super().__init__(parent)
		_layout = QVBoxLayout(self)
		_layout.setContentsMargins(0, 0, 0, 0)
		_layout.setSpacing(0)
		if isinstance(title, str):
			_layout.addWidget(QLabel(title))
		else:
			_layout.addWidget(title)
		if layout:
			_layout.addLayout(layout)
		else:
			_layout.addWidget(widget)


class ComboBox(QComboBox):
	def __init__(self, parent=None, compact=False):
		super().__init__(parent)
		if compact:
			self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
		# else:
		# 	self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)

	def clear_all(self):
		self.clear()


class CheckBox(QCheckBox):
	def __init__(self, text="", parent=None):
		super().__init__(parent)
		self.setText(text)
		self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

	def clear_all(self):
		self.setChecked(False)


class DateEdit(QDateTimeEdit):
	def __init__(self, parent=None):
		super().__init__(parent)
		self.setDisplayFormat("dd MMM yyyy")
		self.setTimeSpec(Qt.TimeSpec.LocalTime)
		self.setCalendarPopup(True)
		self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)

	def clear_all(self):
		self.setDate(QDate.currentDate())


class PushButton(QPushButton):
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


class Label(QLabel):
	def __init__(self, text, parent=None, compact=False):
		super().__init__(parent)
		self.setText(text)
		if compact:
			self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)

	def clear_all(self):
		self.clear()


class LineEdit(QLineEdit):
	def __init__(self, text, parent=None, compact=False):
		super().__init__(parent)
		self.setPlaceholderText(text)
		if compact:
			self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

	def clear_all(self):
		self.clear()


class RadioButton(QRadioButton):
	def __init__(self, text, obj_name=None, conn=None, parent=None):
		super().__init__(parent)
		self.setText(text)
		if obj_name:
			self.setObjectName(obj_name)
		if conn:
			self.toggled.connect(conn)


class SpinBox(QSpinBox):
	def __init__(self, parent=None, min_value=1, max_value=999999):
		super().__init__(parent)
		self.setRange(min_value, max_value)
		self.setAlignment(Qt.AlignmentFlag.AlignCenter)

	def clear_all(self):
		self.setValue(self.minimum() if self.minimum() > 0 else 1)


class TreeWidget(QTreeWidget):
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


class TreeItemProduct(QTreeWidgetItem):
	def __init__(self, data, parent=None):
		super().__init__(parent)
		self.updateData(data)
		self.setTextAlignment(0, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
		self.setTextAlignment(1, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
		self.setTextAlignment(2, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignRight)
		self.setTextAlignment(3, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignRight)
		self.setTextAlignment(4, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignHCenter)

	def updateData(self, data):
		self.setData(0, Qt.ItemDataRole.UserRole, data)
		self.setText(0, data["index"])
		self.setText(1, data["name"])
		self.setText(2, data["sku"])
		self.setText(3, f"""{sum(data["quantity"][i]["amount"] for i in data["quantity"]):,}""")
		self.setText(4, "Yes" if data["discontinued"] else "No")

	@property
	def recordType(self):
		return "product"


class TreeItemStock(QTreeWidgetItem):
	def __init__(self, data, parent=None):
		super().__init__(parent)
		self.updateData(data)
		self.setTextAlignment(0, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignRight)
		self.setTextAlignment(1, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
		self.setTextAlignment(2, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignRight)

	def updateData(self, data):
		self.setData(0, Qt.ItemDataRole.UserRole, data)
		self.setText(0, f"""{time.strftime("%a, %d %b %Y", time.gmtime(data["date"]))}""")
		self.setText(1, data["source"])
		self.setText(2, f"""{data["amount"]:,}""")

	@property
	def recordType(self):
		return "product"


class TreeItemDelivery(QTreeWidgetItem):
	def __init__(self, data, parent=None):
		super().__init__(parent)
		self.updateData(data)
		self.setTextAlignment(0, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignRight)
		self.setTextAlignment(1, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
		self.setTextAlignment(2, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
		self.setTextAlignment(3, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignHCenter)
		self.setTextAlignment(4, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignHCenter)

	def updateData(self, data):

		self.setData(0, Qt.ItemDataRole.UserRole, data)
		self.setText(0, data["order"])
		self.setText(1, f"""{time.strftime("%a, %d %b %Y", time.gmtime(data["date"]))}""")
		self.setText(2, data["client"]["name"])
		self.setText(3, "Yes" if data["client"]["location"]["dual"] else "No")
		self.setText(4, "Yes" if data["details"] else "No")

	@property
	def recordType(self):
		return "delivery"


class TreeItemItems(QTreeWidgetItem):
	def __init__(self, data, parent=None):
		super().__init__(parent)
		self.updateData(data)
		self.setTextAlignment(0, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
		self.setTextAlignment(1, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignHCenter)
		self.setTextAlignment(2, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignHCenter)
		self.setTextAlignment(3, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignRight)

	def updateData(self, data):

		self.setData(0, Qt.ItemDataRole.UserRole, data)
		self.setText(0, data["product_name"])
		self.setText(1, data["product_sku"])
		self.setText(2, data["client_sku"])
		self.setText(3, f"""{data["location1"] + data["location2"]:,}""")

	@property
	def recordType(self):
		return "delivery"


class TreeItemClient(QTreeWidgetItem):
	def __init__(self, data, parent=None):
		super().__init__(parent)
		self.updateData(data)
		self.setTextAlignment(0, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
		self.setTextAlignment(1, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
		self.setTextAlignment(2, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignHCenter)
		self.setTextAlignment(3, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignHCenter)

	def updateData(self, data):

		self.setData(0, Qt.ItemDataRole.UserRole, data)
		self.setText(0, data["index"])
		self.setText(1, data["name"])
		self.setText(2, "Yes" if data["custom_sku"] else "No")
		self.setText(3, "Yes" if data["location"]["dual"] else "No")

	@property
	def recordType(self):
		return "client"


class TreeItemCustomSKU(QTreeWidgetItem):
	def __init__(self, data, parent=None):
		super().__init__(parent)
		self.updateData(data)
		self.setTextAlignment(0, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
		self.setTextAlignment(1, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignRight)
		self.setTextAlignment(2, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignRight)

	def updateData(self, data):

		self.setData(0, Qt.ItemDataRole.UserRole, data)
		self.setText(0, data["product_name"])
		self.setText(1, data["product_sku"])
		self.setText(2, data["client_sku"])

	@property
	def recordType(self):
		return "client"


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


class MainUI(QMainWindow):
	def __init__(self, parent=None):
		super().__init__(parent)
		self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
		self.setWindowTitle(APP_TITLE)
		self.setWindowIcon(QIcon(APP_ICON))
		self.setFixedSize(1280, 720)

		# Set Up Widgets -----------------------------------------------------------------------------------------------
		header_buttons_group = [
			PushButton(text="Delivery Order", checkable=True, prop_type="1"),
			PushButton(text="Products", checkable=True, prop_type="1"),
			PushButton(text="Clients", checkable=True, prop_type="1")
		]
		self._button_group = QButtonGroup()
		self._button_group.idToggled.connect(self._group_button_changed)
		for idx, item in enumerate(header_buttons_group):
			self._button_group.addButton(item, idx)

		self._header_button = [
			PushButton(text="", prop_type="2", conn=self._header_button_pressed),
			PushButton(text="", prop_type="2", conn=self._header_button_pressed),
			PushButton(text="", prop_type="2", conn=self._header_button_pressed),
			PushButton(text="", prop_type="2", conn=self._header_button_pressed),
			PushButton(text="", prop_type="2", conn=self._header_button_pressed)
		]
		self._panels = [
			WidgetContainer(is_vertical=True, prop_type="0"),
			WidgetContainer(is_vertical=True, prop_type="0"),
			WidgetContainer(is_expanding=False, prop_type="1"),
			WidgetContainer(is_expanding=False, prop_type="1"),
			WidgetContainer(is_expanding=False, prop_type="1"),
			WidgetContainer(is_expanding=False, prop_type="1"),
			WidgetContainer(is_expanding=False, prop_type="1"),
			WidgetContainer(is_expanding=False, prop_type="1")
		]

		# Set Up Core Layout  ------------------------------------------------------------------------------------------
		central = QWidget()
		central_layout = QVBoxLayout(central)
		header_layout = QHBoxLayout()
		central_layout.addLayout(header_layout)
		body_layout = QHBoxLayout()
		central_layout.addLayout(body_layout)

		for item in header_buttons_group:
			header_layout.addWidget(item)
		header_layout.addStretch()
		header_layout.addWidget(QLabel(APP_VERSION))

		body_layout.addWidget(self._panels[0])
		content_layout = QVBoxLayout()
		body_layout.addLayout(content_layout)
		for idx in range(2, len(self._panels)):
			content_layout.addWidget(self._panels[idx])
		content_layout.addWidget(self._panels[1])

		buttons_layout = QHBoxLayout()
		self._panels[0].addLayout(buttons_layout)
		buttons_layout.addWidget(self._header_button[0])
		buttons_layout.addWidget(self._header_button[1])
		buttons_layout.addWidget(self._header_button[2])
		buttons_layout.addStretch()
		self.tree_main = TreeWidget()
		self.tree_main.itemClicked.connect(self._tree_main_item_selected)
		self._panels[0].addWidget(self.tree_main)

		buttons_layout = QHBoxLayout()
		self._panels[1].addLayout(buttons_layout)
		buttons_layout.addWidget(self._header_button[3])
		buttons_layout.addWidget(self._header_button[4])
		buttons_layout.addStretch()
		self.tree_content = TreeWidget()
		self.tree_content.itemClicked.connect(self._tree_content_item_selected)
		self._panels[1].addWidget(self.tree_content)

		self._widgets0 = [
			ComboBox(),
			LineEdit(text="DO Number..", compact=True),
			DateEdit(),
			PushButton(text="", prop_type="3", conn=self._panels_button_pressed),
			PushButton(text="", prop_type="4", conn=self._panels_button_pressed)
		]
		delivery_layout1 = WidgetBackGround()
		self._panels[4].addWidget(delivery_layout1, 1)
		delivery_layout1.addWidget(
			LabelContainer(title="Client:", widget=self._widgets0[0]), 0, 0, 1, 2, Qt.AlignmentFlag.AlignTop
		)
		delivery_layout1.addWidget(
			LabelContainer(title="DO Number:", widget=self._widgets0[1]), 0, 2, 1, 1, Qt.AlignmentFlag.AlignTop
		)
		delivery_layout1.addWidget(
			LabelContainer(title="Date:", widget=self._widgets0[2]), 1, 0, 1, 1, Qt.AlignmentFlag.AlignTop
		)
		delivery_layout2 = QVBoxLayout()
		self._panels[4].addLayout(delivery_layout2)
		delivery_layout2.addWidget(self._widgets0[-2])
		delivery_layout2.addWidget(self._widgets0[-1])
		delivery_layout2.addStretch()

		self._widgets1 = [
			ComboBox(),
			Label(text="", compact=True),
			SpinBox(min_value=0),
			Label(text="", compact=True),
			SpinBox(min_value=0),
			PushButton(text="", prop_type="3", conn=self._panels_button_pressed),
			PushButton(text="", prop_type="4", conn=self._panels_button_pressed)
		]
		item_layout1 = WidgetBackGround()
		self._panels[7].addWidget(item_layout1, 1)
		item_layout1.addWidget(
			LabelContainer(title="Product:", widget=self._widgets1[0]), 0, 0, 1, 2, Qt.AlignmentFlag.AlignTop
		)
		item_layout1.addWidget(
			LabelContainer(title=self._widgets1[1], widget=self._widgets1[2]), 1, 0, 1, 1, Qt.AlignmentFlag.AlignTop
		)
		item_layout1.addWidget(
			LabelContainer(title=self._widgets1[3], widget=self._widgets1[4]), 1, 1, 1, 1, Qt.AlignmentFlag.AlignTop
		)
		item_layout2 = QVBoxLayout()
		self._panels[7].addLayout(item_layout2)
		item_layout2.addWidget(self._widgets1[-2])
		item_layout2.addWidget(self._widgets1[-1])
		item_layout2.addStretch()

		self._widgets2 = [
			LineEdit(text="Product Name.."),
			LineEdit(text="SKU Number..", compact=True),
			CheckBox(text="Discontinued"),
			PushButton(text="", prop_type="3", conn=self._panels_button_pressed),
			PushButton(text="", prop_type="4", conn=self._panels_button_pressed)
		]
		product_layout1 = WidgetBackGround()
		self._panels[5].addWidget(product_layout1, 1)
		product_layout1.addWidget(
			LabelContainer(title="Product:", widget=self._widgets2[0]), 0, 0, 1, 3, Qt.AlignmentFlag.AlignTop
		)
		product_layout1.addWidget(
			LabelContainer(title="SKU Number:", widget=self._widgets2[1]), 1, 0, 1, 1, Qt.AlignmentFlag.AlignTop
		)
		product_layout1.addWidget(
			LabelContainer(title=" ", widget=self._widgets2[2]), 1, 1, 1, 1, Qt.AlignmentFlag.AlignTop
		)
		product_layout2 = QVBoxLayout()
		self._panels[5].addLayout(product_layout2)
		product_layout2.addWidget(self._widgets2[-2])
		product_layout2.addWidget(self._widgets2[-1])
		product_layout2.addStretch()

		self._widgets3 = [
			ComboBox(),
			SpinBox(min_value=-999999),
			DateEdit(),
			PushButton(text="", prop_type="3", conn=self._panels_button_pressed),
			PushButton(text="", prop_type="4", conn=self._panels_button_pressed)
		]
		stock_layout1 = WidgetBackGround()
		self._panels[6].addWidget(stock_layout1, 1)
		stock_layout1.addWidget(
			LabelContainer(title="Type:", widget=self._widgets3[0]), 0, 0, 1, 2, Qt.AlignmentFlag.AlignTop
		)
		stock_layout1.addWidget(
			LabelContainer(title="Quantity:", widget=self._widgets3[1]), 0, 2, 1, 1, Qt.AlignmentFlag.AlignTop
		)
		stock_layout1.addWidget(
			LabelContainer(title="Date:", widget=self._widgets3[2]), 1, 0, 1, 1, Qt.AlignmentFlag.AlignTop
		)
		stock_layout2 = QVBoxLayout()
		self._panels[6].addLayout(stock_layout2)
		stock_layout2.addWidget(self._widgets3[-2])
		stock_layout2.addWidget(self._widgets3[-1])
		stock_layout2.addStretch()

		self._widgets4 = [
			LineEdit(text="Client Name.."),
			LineEdit(text="Address Line #1.."),
			LineEdit(text="Address Line #2.."),
			LineEdit(text="Postcode..", compact=True),
			LineEdit(text="City.."),
			LineEdit(text="State.."),
			CheckBox(text="Dual Locations"),
			LineEdit(text="Location #1.."),
			LineEdit(text="Location #2.."),
			PushButton(text="", prop_type="3", conn=self._panels_button_pressed),
			PushButton(text="", prop_type="4", conn=self._panels_button_pressed)
		]
		client_layout1 = WidgetBackGround()
		self._panels[2].addWidget(client_layout1, 1)
		client_layout1.addWidget(
			LabelContainer(title="Company Name:", widget=self._widgets4[0]), 0, 0, 1, 3, Qt.AlignmentFlag.AlignTop
		)
		client_layout1.addWidget(
			LabelContainer(title="Address:", widget=self._widgets4[1]), 1, 0, 1, 3, Qt.AlignmentFlag.AlignTop
		)
		client_layout1.addWidget(self._widgets4[2], 2, 0, 1, 3, Qt.AlignmentFlag.AlignTop)
		client_layout1.addWidget(
			LabelContainer(title="Postcode:", widget=self._widgets4[3]), 3, 0, 1, 1, Qt.AlignmentFlag.AlignTop
		)
		client_layout1.addWidget(
			LabelContainer(title="City:", widget=self._widgets4[4]), 3, 1, 1, 1, Qt.AlignmentFlag.AlignTop
		)
		client_layout1.addWidget(
			LabelContainer(title="State:", widget=self._widgets4[5]), 3, 2, 1, 1, Qt.AlignmentFlag.AlignTop
		)
		client_layout1.addWidget(
			LabelContainer(title="Delivery:", widget=self._widgets4[6]), 4, 0, 1, 1, Qt.AlignmentFlag.AlignTop
		)

		client_layout1a_container = QWidget(self._panels[2])
		client_layout1a_container.setEnabled(False)
		client_layout1a_layout = QHBoxLayout(client_layout1a_container)
		client_layout1a_layout.setContentsMargins(0, 0, 0, 0)
		client_layout1a_layout.addWidget(
			LabelContainer(title="Location #1", widget=self._widgets4[7]), Qt.AlignmentFlag.AlignTop
		)
		client_layout1a_layout.addWidget(
			LabelContainer(title="Location #2", widget=self._widgets4[8]), Qt.AlignmentFlag.AlignTop
		)
		client_layout1.addWidget(client_layout1a_container, 4, 1, 1, 2)
		self._widgets4[6].toggled.connect(client_layout1a_container.setEnabled)
		client_layout2 = QVBoxLayout()
		self._panels[2].addLayout(client_layout2)
		client_layout2.addWidget(self._widgets4[-2])
		client_layout2.addWidget(self._widgets4[-1])
		client_layout2.addStretch()

		self._widgets5 = [
			ComboBox(),
			LineEdit(text="Client SKU..", compact=True),
			PushButton(text="", prop_type="3", conn=self._panels_button_pressed),
			PushButton(text="", prop_type="4", conn=self._panels_button_pressed)
		]
		csku_layout1 = WidgetBackGround()
		self._panels[3].addWidget(csku_layout1, 1)
		csku_layout1.addWidget(
			LabelContainer(title="Product:", widget=self._widgets5[0]), 0, 0, 1, 2, Qt.AlignmentFlag.AlignTop
		)
		csku_layout1.addWidget(
			LabelContainer(title="SKU Number:", widget=self._widgets5[1]), 1, 0, 1, 1, Qt.AlignmentFlag.AlignTop
		)
		csku_layout2 = QVBoxLayout()
		self._panels[3].addLayout(csku_layout2)
		csku_layout2.addWidget(self._widgets5[-2])
		csku_layout2.addWidget(self._widgets5[-1])
		csku_layout2.addStretch()

		self.setCentralWidget(central)
		self._reset_view()
		self._data = Storage().data
		self.show()

	def _reset_view(self):
		for item in self._header_button:
			item.setText("")
			item.setEnabled(False)
			item.setVisible(False)
		for idx in range(2, len(self._panels)):
			self._panels[idx].setVisible(False)

	@Slot(int)
	def _group_button_changed(self, index):
		if index == self._button_group.checkedId():
			self._reset_view()
			match index:
				case 0:
					self.tree_main.set_headers(["Delivery\nNumber", "Date", "Client", "Dual\nLocations", "Products", ""])
					self.tree_content.set_headers(["Product", "Product SKU", "Client SKU", "Quantity", ""])
					buttons = [
						["New Order", "new_delivery", 0],
						["Edit Order", "edit_delivery", 1],
						["Generate Delivery Order", "generate_delivery", 2],
						["Add Item", "new_item", 3],
						["Edit Item", "edit_item", 4]
					]
				case 1:
					self.tree_main.set_headers(["No", "Product", "SKU", "Quantity", "Discontinued", ""])
					self.tree_content.set_headers(["Date", "Source", "Quantity", ""])
					buttons = [
						["New Product", "new_product", 0],
						["Edit Product", "edit_product", 1],
						["Add Stock", "new_stock", 3],
						["Edit Stock", "edit_stock", 4]
					]
				case 2:
					self.tree_main.set_headers(["No", "Name", "Custom SKU", "Dual Locations", ""])
					self.tree_content.set_headers(["Product", "Product SKU", "Client SKU", ""])
					buttons = [
						["New Client", "new_client", 0],
						["Edit Client", "edit_client", 1],
						["Add Client SKU", "new_client_sku", 3],
						["Edit Client SKU", "edit_client_sku", 4]
					]
				case _:
					buttons = []
			for button in buttons:
				self._header_button[button[2]].setText(button[0])
				self._header_button[button[2]].setObjectName(button[1])
				self._header_button[button[2]].setVisible(True)
			self._header_button[0].setEnabled(True)
			self._panels[0].setDisabled(False)
			self._panels[1].setDisabled(False)
			# self.tree_main.setDisabled(False)
			# self.tree_content.setDisabled(False)
			self._tree_main_update(index)

	def _header_button_pressed(self):
		disable_main = True
		disable_content = True
		current_panel = -1
		for idx in range(2, len(self._panels)):
			self._panels[idx].setVisible(False)
		match self.sender().objectName():
			case "new_delivery":
				for item in self._widgets0:
					item.clear_all()
				for k, v in sorted(self._data["client"].items(), key=lambda x:x[1]["name"]):
					self._widgets0[0].addItem(v["name"], k)
				buttons = [
					["Add", "add_delivery", -2],
					["Cancel", "cancel", -1]
				]
				for button in buttons:
					self._widgets0[button[2]].setText(button[0])
					self._widgets0[button[2]].setObjectName(button[1])
				current_panel = 4
			case "edit_delivery":
				if self.tree_main.selectedItems():
					for item in self._widgets0:
						item.clear_all()
					for k, v in sorted(self._data["client"].items(), key=lambda x: x[1]["name"]):
						self._widgets0[0].addItem(v["name"], k)
					data = self.tree_main.selectedItems()[0].data(0, Qt.ItemDataRole.UserRole)
					self._widgets0[0].setCurrentText(data["client"]["name"])
					self._widgets0[1].setText(data["order"])
					self._widgets0[2].setDate(
						QDate.fromString(time.strftime("%Y-%m-%d", time.localtime(data["date"])), "yyyy-MM-dd"))
					buttons = [
						["Update", "update_delivery", -2],
						["Cancel", "cancel", -1]
					]
					for button in buttons:
						self._widgets0[button[2]].setText(button[0])
						self._widgets0[button[2]].setObjectName(button[1])
					current_panel = 4
				else:
					disable_main = False
					disable_content = False
			case "new_item":
				if self.tree_main.selectedItems():
					for item in self._widgets1:
						item.clear_all()
					data = self.tree_main.selectedItems()[0].data(0, Qt.ItemDataRole.UserRole)
					used = [data["details"][i]["product"] for i in data["details"]]
					for k, v in sorted(self._data["product"].items(), key=lambda x: x[1]["name"]):
						if not v["discontinued"] and k not in used:
							self._widgets1[0].addItem(v["name"], k)
					if data["client"]["location"]["dual"]:
						self._widgets1[1].setText(f"""{data["client"]["location"]["label1"]} Quantity:""")
						self._widgets1[3].setText(f"""{data["client"]["location"]["label2"]} Quantity:""")
						self._widgets1[3].setVisible(True)
						self._widgets1[4].setVisible(True)
					else:
						self._widgets1[1].setText("Quantity:")
						self._widgets1[3].setText("")
						self._widgets1[3].setVisible(False)
						self._widgets1[4].setVisible(False)

					buttons = [
						["Add", "add_item", -2],
						["Cancel", "cancel", -1]
					]
					for button in buttons:
						self._widgets1[button[2]].setText(button[0])
						self._widgets1[button[2]].setObjectName(button[1])
					current_panel = 7
				else:
					disable_main = False
					disable_content = False
			case "edit_item":
				if self.tree_main.selectedItems() and self.tree_content.selectedItems():
					for item in self._widgets1:
						item.clear_all()
					data = self.tree_main.selectedItems()[0].data(0, Qt.ItemDataRole.UserRole)
					for k, v in sorted(self._data["product"].items(), key=lambda x: x[1]["name"]):
						if not v["discontinued"]:
							self._widgets1[0].addItem(v["name"], k)
					if data["client"]["location"]["dual"]:
						self._widgets1[1].setText(f"""{data["client"]["location"]["label1"]} Quantity:""")
						self._widgets1[3].setText(f"""{data["client"]["location"]["label2"]} Quantity:""")
						self._widgets1[3].setVisible(True)
						self._widgets1[4].setVisible(True)
					else:
						self._widgets1[1].setText("Quantity:")
						self._widgets1[3].setText("")
						self._widgets1[3].setVisible(False)
						self._widgets1[4].setVisible(False)
					data = self.tree_content.selectedItems()[0].data(0, Qt.ItemDataRole.UserRole)
					self._widgets1[0].setCurrentText(data["product_name"])
					self._widgets1[2].setValue(data["location1"])
					self._widgets1[4].setValue(data["location2"])
					buttons = [
						["Update", "update_item", -2],
						["Cancel", "cancel", -1]
					]
					for button in buttons:
						self._widgets1[button[2]].setText(button[0])
						self._widgets1[button[2]].setObjectName(button[1])
					current_panel = 7
				else:
					disable_main = False
					disable_content = False
			case "new_product":
				for item in self._widgets2:
					item.clear_all()
				buttons = [
					["Add", "add_product", -2],
					["Cancel", "cancel", -1]
				]
				for button in buttons:
					self._widgets2[button[2]].setText(button[0])
					self._widgets2[button[2]].setObjectName(button[1])
				current_panel = 5
			case "edit_product":
				if self.tree_main.selectedItems():
					data = self.tree_main.selectedItems()[0].data(0, Qt.ItemDataRole.UserRole)
					self._widgets2[0].setText(data["name"])
					self._widgets2[1].setText(data["sku"])
					self._widgets2[2].setChecked(data["discontinued"])
					buttons = [
						["Update", "update_product", -2],
						["Cancel", "cancel", -1]
					]
					for button in buttons:
						self._widgets2[button[2]].setText(button[0])
						self._widgets2[button[2]].setObjectName(button[1])
					current_panel = 5
				else:
					disable_main = False
					disable_content = False
			case "new_stock":
				if self.tree_main.selectedItems():
					for item in self._widgets3:
						item.clear_all()
					self._widgets3[0].addItems(["New Shipment", "Stock Adjustment"])
					buttons = [
						["Add", "add_stock", -2],
						["Cancel", "cancel", -1]
					]
					for button in buttons:
						self._widgets3[button[2]].setText(button[0])
						self._widgets3[button[2]].setObjectName(button[1])
					current_panel = 6
				else:
					disable_main = False
					disable_content = False
			case "edit_stock":
				if self.tree_main.selectedItems() and self.tree_content.selectedItems():
					for item in self._widgets3:
						item.clear_all()
					self._widgets3[0].addItems(["New Shipment", "Stock Adjustment"])
					data = self.tree_content.selectedItems()[0].data(0, Qt.ItemDataRole.UserRole)
					self._widgets3[0].setCurrentText(data["source"])
					self._widgets3[1].setValue(data["amount"])
					self._widgets3[2].setDate(
						QDate.fromString(time.strftime("%Y-%m-%d", time.localtime(data["date"])), "yyyy-MM-dd"))
					buttons = [
						["Save", "save_stock", -2],
						["Cancel", "cancel", -1]
					]
					for button in buttons:
						self._widgets3[button[2]].setText(button[0])
						self._widgets3[button[2]].setObjectName(button[1])
					current_panel = 6
				else:
					disable_main = False
					disable_content = False
			case "new_client":
				for item in self._widgets4:
					item.clear_all()
				buttons = [
					["Add", "add_client", -2],
					["Cancel", "cancel", -1]
				]
				for button in buttons:
					self._widgets4[button[2]].setText(button[0])
					self._widgets4[button[2]].setObjectName(button[1])
				current_panel = 2
			case "edit_client":
				if self.tree_main.selectedItems():
					data = self.tree_main.selectedItems()[0].data(0, Qt.ItemDataRole.UserRole)
					self._widgets4[0].setText(data["name"])
					self._widgets4[1].setText(data["address1"])
					self._widgets4[2].setText(data["address2"])
					self._widgets4[3].setText(data["postcode"])
					self._widgets4[4].setText(data["city"])
					self._widgets4[5].setText(data["state"])
					self._widgets4[6].setChecked(data["location"]["dual"])
					self._widgets4[7].setText(data["location"]["label1"])
					self._widgets4[8].setText(data["location"]["label2"])
					buttons = [
						["Update", "update_client", -2],
						["Cancel", "cancel", -1]
					]
					for button in buttons:
						self._widgets4[button[2]].setText(button[0])
						self._widgets4[button[2]].setObjectName(button[1])
					current_panel = 2
				else:
					disable_main = False
					disable_content = False
			case "new_client_sku":
				if self.tree_main.selectedItems():
					for item in self._widgets5:
						item.clear_all()
					data = self.tree_main.selectedItems()[0].data(0, Qt.ItemDataRole.UserRole)
					used = [data["custom_sku"][i]["product"] for i in data["custom_sku"]]
					for k, v in sorted(self._data["product"].items(), key=lambda x: x[1]["name"]):
						if not v["discontinued"] and k not in used:
							self._widgets5[0].addItem(v["name"], k)
					buttons = [
						["Add", "add_client_sku", -2],
						["Cancel", "cancel", -1]
					]
					for button in buttons:
						self._widgets5[button[2]].setText(button[0])
						self._widgets5[button[2]].setObjectName(button[1])
					current_panel = 3
				else:
					disable_main = False
					disable_content = False
			case "edit_client_sku":
				if self.tree_main.selectedItems() and self.tree_content.selectedItems():
					for item in self._widgets5:
						item.clear_all()
					data = self.tree_content.selectedItems()[0].data(0, Qt.ItemDataRole.UserRole)
					self._widgets5[0].addItem(data["product_name"], data["product_index"])
					self._widgets5[1].setText(data["client_sku"])
					buttons = [
						["Save", "save_client_sku", -2],
						["Cancel", "cancel", -1]
					]
					for button in buttons:
						self._widgets5[button[2]].setText(button[0])
						self._widgets5[button[2]].setObjectName(button[1])
					current_panel = 3
				else:
					disable_main = False
					disable_content = False
			case _:
				disable_main = False
				disable_content = False
				print("_header_button_pressed", self.sender().objectName())
		self._panels[0].setDisabled(disable_main)
		self._panels[1].setDisabled(disable_content)
		# self.tree_main.setDisabled(disable_main)
		# self.tree_content.setDisabled(disable_content)
		if current_panel != -1:
			self._panels[current_panel].setVisible(True)

	def _panels_button_pressed(self):
		reset_views = False
		reset_buttons = True
		match self.sender().objectName():
			case "add_delivery":
				client = self._widgets0[0].currentData(Qt.ItemDataRole.UserRole)
				order = self._widgets0[1].text()
				if client and order:
					idx = f"""{len(self._data["delivery"]):04}"""
					self._data["delivery"][idx] = {
						"index": idx,
						"client": client,
						"order": order,
						"date": self._widgets0[2].dateTime().toSecsSinceEpoch() + 28800,
						"details": {}
					}
					self._tree_main_update(0)
					reset_views = True
			case "update_delivery":
				client = self._widgets0[0].currentData(Qt.ItemDataRole.UserRole)
				order = self._widgets0[1].text()
				if self.tree_main.selectedItems() and client and order:
					idx = self.tree_main.selectedItems()[0].data(0, Qt.ItemDataRole.UserRole)["index"]
					self._data["delivery"][idx]["client"] = client
					self._data["delivery"][idx]["order"] = order
					self._data["delivery"][idx]["date"] = self._widgets0[2].dateTime().toSecsSinceEpoch() + 28800
					self._tree_main_update(0)
					reset_views = True
			case "add_item":
				product = self._widgets1[0].currentData(Qt.ItemDataRole.UserRole)
				quantity = self._widgets1[2].value()
				if self.tree_main.selectedItems() and product and quantity:
					data = self.tree_main.selectedItems()[0].data(0, Qt.ItemDataRole.UserRole)
					idx = f"""{len(self._data["delivery"][data["index"]]["details"]):04}"""
					self._data["delivery"][data["index"]]["details"][idx] = {
						"index": idx,
						"product": product,
						"location1": quantity,
						"location2": self._widgets1[4].value() if self._widgets1[4].isVisible() else 0,
					}
					self._tree_main_update(0)
					reset_views = True
			case "update_item":
				product = self._widgets1[0].currentData(Qt.ItemDataRole.UserRole)
				quantity = self._widgets1[2].value()
				if self.tree_main.selectedItems() and self.tree_content.selectedItems() and product and quantity:
					idx1 = self.tree_main.selectedItems()[0].data(0, Qt.ItemDataRole.UserRole)["index"]
					idx2 = self.tree_content.selectedItems()[0].data(0, Qt.ItemDataRole.UserRole)["index"]
					self._data["delivery"][idx1]["details"][idx2]["product"] = product
					self._data["delivery"][idx1]["details"][idx2]["location1"] = quantity
					self._data["delivery"][idx1]["details"][idx2]["location2"] = self._widgets1[4].value()
					self._tree_main_update(0)
					reset_views = True
			case "add_product":
				if all(self._widgets2[i].text() for i in range(2)):
					idx = f"""{len(self._data["product"]):04}"""
					self._data["product"][idx] = {
						"index": idx,
						"name": self._widgets2[0].text(),
						"sku": self._widgets2[1].text(),
						"quantity": {},
						"discontinued": self._widgets2[2].isChecked()
					}
					self._tree_main_update(1)
					reset_views = True
			case "update_product":
				if self.tree_main.selectedItems() and all(self._widgets2[i].text() for i in range(2)):
					idx = self.tree_main.selectedItems()[0].data(0, Qt.ItemDataRole.UserRole)["index"]
					self._data["product"][idx]["name"] = self._widgets2[0].text()
					self._data["product"][idx]["sku"] = self._widgets2[1].text()
					self._data["product"][idx]["discontinued"] = self._widgets2[2].isChecked()
					self._tree_main_update(1)
					reset_views = True
			case "add_stock":
				sb_val = self._widgets3[1].value()
				if (
						(self.tree_main.selectedItems() and sb_val) and
						(
								(self._widgets3[0].currentIndex() == 0 and sb_val > 0) or
								(self._widgets3[0].currentIndex() != 0)
						)
				):
					idx1 = self.tree_main.selectedItems()[0].data(0, Qt.ItemDataRole.UserRole)["index"]
					idx2 = f"""{len(self._data["product"][idx1]["quantity"]):04}"""
					self._data["product"][idx1]["quantity"][idx2] = {
						"index": idx2,
						"source": self._widgets3[0].currentText(),
						"amount": sb_val,
						"date": self._widgets3[2].dateTime().toSecsSinceEpoch() + 28800
					}
					self._tree_main_update(1)
					reset_views = True
			case "save_stock":
				sb_val = self._widgets3[1].value()
				if (
						(self.tree_main.selectedItems() and self.tree_content.selectedItems() and sb_val) and
						(
								(self._widgets3[0].currentIndex() == 0 and sb_val > 0) or
								(self._widgets3[0].currentIndex() != 0)
						)
				):
					idx1 = self.tree_main.selectedItems()[0].data(0, Qt.ItemDataRole.UserRole)["index"]
					idx2 = self.tree_content.selectedItems()[0].data(0, Qt.ItemDataRole.UserRole)["index"]
					self._data["product"][idx1]["quantity"][idx2] = {
						"index": idx2,
						"source": self._widgets3[0].currentText(),
						"amount": sb_val,
						"date": self._widgets3[2].dateTime().toSecsSinceEpoch() + 28800
					}
					self._tree_main_update(1)
					reset_views = True
			case "add_client":
				dual = self._widgets4[6].isChecked()
				label1 = self._widgets4[7].text()
				label2 = self._widgets4[8].text()
				if (
						all(self._widgets4[i].text() for i in range(6)) and
						((dual and label1 and label2) or not dual)
				):
					idx = f"""{len(self._data["client"]):04}"""
					self._data["client"][idx] = {
						"index": idx,
						"name": self._widgets4[0].text(),
						"address1": self._widgets4[1].text(),
						"address2": self._widgets4[2].text(),
						"postcode": self._widgets4[3].text(),
						"city": self._widgets4[4].text(),
						"state": self._widgets4[5].text(),
						"custom_sku": {},
						"location": {"dual": dual, "label1": label1, "label2": label2}
					}
					self._tree_main_update(2)
					reset_views = True
			case "update_client":
				if self.tree_main.selectedItems() and all(self._widgets4[i].text() for i in range(6)):
					dual = self._widgets4[6].isChecked()
					label1 = self._widgets4[7].text()
					label2 = self._widgets4[8].text()
					if (dual and label1 and label2) or not dual:
						idx = self.tree_main.selectedItems()[0].data(0, Qt.ItemDataRole.UserRole)["index"]
						self._data["client"][idx]["name"] = self._widgets4[0].text()
						self._data["client"][idx]["address1"] = self._widgets4[1].text()
						self._data["client"][idx]["address2"] = self._widgets4[2].text()
						self._data["client"][idx]["postcode"] = self._widgets4[3].text()
						self._data["client"][idx]["city"] = self._widgets4[4].text()
						self._data["client"][idx]["state"] = self._widgets4[5].text()
						self._data["client"][idx]["location"]["dual"] = dual
						self._data["client"][idx]["location"]["label1"] = label1
						self._data["client"][idx]["location"]["label2"] = label2
						self._tree_main_update(2)
						reset_views = True
			case "add_client_sku":
				product = self._widgets5[0].currentData(Qt.ItemDataRole.UserRole)
				custom_sku = self._widgets5[1].text()
				if self.tree_main.selectedItems() and product and custom_sku:
					idx1 = self.tree_main.selectedItems()[0].data(0, Qt.ItemDataRole.UserRole)["index"]
					idx2 = f"""{len(self._data["client"][idx1]["custom_sku"]):04}"""
					self._data["client"][idx1]["custom_sku"][idx2] = {
						"index": idx2,
						"product": product,
						"sku": custom_sku
					}
					self._tree_main_update(2)
					reset_views = True
			case "save_client_sku":
				custom_sku = self._widgets5[1].text()
				if self.tree_main.selectedItems() and self.tree_content.selectedItems() and custom_sku:
					idx = self.tree_main.selectedItems()[0].data(0, Qt.ItemDataRole.UserRole)["index"]
					data = self.tree_content.selectedItems()[0].data(0, Qt.ItemDataRole.UserRole)
					self._data["client"][idx]["custom_sku"][data["index"]]["sku"] = custom_sku
					self._tree_main_update(2)
					reset_views = True
			case _:
				reset_views = True
				reset_buttons = False
				print("_panel_button_pressed", self.sender().objectName())
		if reset_views:
			for idx in range(2, len(self._panels)):
				self._panels[idx].setVisible(False)
			self._panels[0].setDisabled(False)
			self._panels[1].setDisabled(False)
			# self.tree_main.setDisabled(False)
			# self.tree_content.setDisabled(False)
		if reset_buttons:
			for idx in range(1, len(self._header_button)):
				self._header_button[idx].setEnabled(False)

	def _tree_main_update(self, index):
		Storage().data = self._data
		self.tree_main.clear()
		self.tree_content.clear()
		match index:
			case 0:
				for i in sorted(self._data["delivery"], reverse=True):
					data = self._data["delivery"][i].copy()
					data["client"] = self._data["client"][data["client"]].copy()
					TreeItemDelivery(parent=self.tree_main, data=data)
			case 1:
				for i in sorted(self._data["product"], reverse=True):
					TreeItemProduct(parent=self.tree_main, data=self._data["product"][i])
			case 2:
				for i in sorted(self._data["client"], reverse=True):
					TreeItemClient(parent=self.tree_main, data=self._data["client"][i])
			case _:
				print(index)
		self.tree_main.resize_tree()
		self.tree_content.resize_tree()

	def _tree_main_item_selected(self):
		if self.tree_main.selectedItems():
			self.tree_content.clear()
			for item in (self._header_button[1], self._header_button[2], self._header_button[3]):
				item.setEnabled(True if item.isVisible() else False)
			self._header_button[4].setEnabled(False)
			item = self.tree_main.selectedItems()[0]
			idx = item.data(0, Qt.ItemDataRole.UserRole)["index"]
			tmp = {}
			match item.recordType:
				case "delivery":
					client_lk = self._data[item.recordType][idx]["client"]
					for i in self._data[item.recordType][idx]["details"]:
						prod_lk = self._data[item.recordType][idx]["details"][i]["product"]
						csku_lk = self._data["client"][client_lk]["custom_sku"]
						tmp[self._data["product"][prod_lk]["name"]] = {
							"index": i,
							"product_name": self._data["product"][prod_lk]["name"],
							"product_index": self._data["product"][prod_lk]["index"],
							"product_sku": self._data["product"][prod_lk]["sku"],
							"client_sku": csku_lk[i]["sku"] if csku_lk and i in csku_lk else "N/A",
							"location1": self._data[item.recordType][idx]["details"][i]["location1"],
							"location2": self._data[item.recordType][idx]["details"][i]["location2"]
						}
					for i in sorted(tmp):
						TreeItemItems(parent=self.tree_content, data=tmp[i])
				case "product":
					for i in self._data[item.recordType][idx]["quantity"]:
						tmp[f"""{self._data[item.recordType][idx]["quantity"][i]["date"]}_{i}"""] = {
							"index": self._data[item.recordType][idx]["quantity"][i]["index"],
							"date": self._data[item.recordType][idx]["quantity"][i]["date"],
							"source": self._data[item.recordType][idx]["quantity"][i]["source"],
							"amount": self._data[item.recordType][idx]["quantity"][i]["amount"]
						}
					for i in sorted(tmp, reverse=True):
						TreeItemStock(parent=self.tree_content, data=tmp[i])
				case "client":
					for i in self._data[item.recordType][idx]["custom_sku"]:
						prod_lk = self._data[item.recordType][idx]["custom_sku"][i]["product"]
						tmp[self._data["product"][prod_lk]["name"]] = {
							"index": i,
							"product_name": self._data["product"][prod_lk]["name"],
							"product_index": self._data["product"][prod_lk]["index"],
							"product_sku": self._data["product"][prod_lk]["sku"],
							"client_sku": self._data[item.recordType][idx]["custom_sku"][i]["sku"]
						}
					for i in sorted(tmp, reverse=True):
						TreeItemCustomSKU(parent=self.tree_content, data=tmp[i])
				case _:
					print(self.tree_main.selectedItems()[0].recordType)
			self.tree_content.resize_tree()

	def _tree_content_item_selected(self):
		if self.tree_content.selectedItems():
			self._header_button[4].setEnabled(True)


if __name__ == '__main__':
	app = QApplication()
	app.setWindowIcon(QIcon(APP_ICON))
	main = MainUI()
	main.setStyleSheet(stylesheet())
	app.exec()