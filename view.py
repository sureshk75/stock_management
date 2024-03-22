from PySide6.QtCore import (
	Property, QPropertyAnimation, QSize, Slot
)
from PySide6.QtGui import (
	QPainter, QIcon, QValidator
)
from PySide6.QtWidgets import (
	QAbstractButton, QAbstractItemView, QButtonGroup, QComboBox, QDoubleSpinBox, QFrame, QGraphicsDropShadowEffect,
	QGridLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QStackedWidget, QSizePolicy, QSpinBox, QTableView,
	QTextBrowser, QTreeWidget, QTreeWidgetItem, QVBoxLayout, QWidget, QInputDialog, QDialog, QDialogButtonBox,
	QFormLayout
)

from model import *


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
		selection-color: {"rgb(217, 217, 217)" if darkmode else "rgb(30, 144, 255)"}; 
		selection-background-color: transparent;
	}}

	/*----- QAbstractButton -----*/
	QAbstractButton[prop_type="0"] {{
		color: {"rgb(204, 204, 204)" if darkmode else "rgb(30, 144, 255)"};
		background: {"rgb(90, 90, 90)" if darkmode else "rgb(179, 179, 179)"};
	}}
	QAbstractButton[prop_type="0"]:disabled {{
		color: {"rgba(204, 204, 204, 0.2)" if darkmode else "rgba(30, 144, 255, 0.2)"};
		background: {"rgba(90, 90, 90, 0.2)" if darkmode else "rgba(179, 179, 179, 0.2)"};
	}}
	QAbstractButton[prop_type="1"] {{
		font-size: 14px;
		font-weight: 500;
		margin: 8px;
	}}
	QAbstractButton[prop_type="1"]:checked {{
		border-bottom: 2px solid {"rgb(230, 230, 230)" if darkmode else "rgb(30, 144, 255)"};
		color: {"rgb(230, 230, 230)" if darkmode else "rgb(30, 144, 255)"};
	}}
	QAbstractButton[prop_type="1"]:!checked {{
		border-bottom: 2px solid transparent;
		color: {"rgb(128, 128, 128)" if darkmode else "rgb(89, 89, 89)"};
	}}
	QAbstractButton[prop_type="2"] {{
		color: {"rgb(104, 104, 104)" if darkmode else "rgb(242, 242, 242)"};
		background: {"rgba(204, 204, 204, 0.5)" if darkmode else "rgba(30, 144, 255, 0.5)"};
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
		background: {"rgba(204, 204, 204, 0.2)" if darkmode else "rgba(30, 144, 255, 0.2)"};
	}}
	QAbstractButton[prop_type="2"]:hover {{
		background: {"rgba(204, 204, 204, 0.8)" if darkmode else "rgba(30, 144, 255, 0.8)"};
	}}
	QAbstractButton[prop_type="2"]:pressed {{
		background: {"rgba(204, 204, 204, 1.0)" if darkmode else "rgba(30, 144, 255, 1.0)"};
	}}
	QAbstractButton[prop_type="3"] {{
		color: {"rgb(45, 45, 45)" if darkmode else "rgb(230, 230, 230)"};
		background: {"rgba(204, 204, 204, 0.5)" if darkmode else "rgba(30, 144, 255, 0.5)"};
		border: none;
		border-radius: 12px;
		font-size: 14px;
		font-weight: 500;
		height: 24px;
		padding-left: 8px;
		padding-right: 8px;
	}}
	QAbstractButton[prop_type="3"]:disabled {{
		background: {"rgba(204, 204, 204, 0.2)" if darkmode else "rgba(30, 144, 255, 0.2)"};
	}}
	QAbstractButton[prop_type="3"]:hover {{
		background: {"rgba(204, 204, 204, 0.8)" if darkmode else "rgba(30, 144, 255, 0.8)"};
	}}
	QAbstractButton[prop_type="3"]:pressed {{
		background: {"rgba(204, 204, 204, 1.0)" if darkmode else "rgba(30, 144, 255, 1.0)"};
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
		padding-bottom: 4px;
		padding-top: 4px;
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
	#CustomContainer {{
		background: qlineargradient(
		spread:pad, x1: 0, y1: 0, x2: 0, y2: 1,
		stop:0 {"rgb(80, 80, 80)" if darkmode else "rgb(237, 237, 237)"},
		stop:1 {"rgb(48, 48, 48)" if darkmode else "rgb(212, 212, 212)"});
		border-radius: 8px;
	}}
	#CustomFilterBar, #CustomTextBrowser {{
		background: {"rgb(104, 104, 104)" if darkmode else "rgb(242, 242, 242)"};
		border: 1px solid transparent;
		border-radius: 6px;
	}}
	"""


class BasePushButton(QPushButton):

	def __init__(self, text, parent=None, checkable=True, objectname=None, prop_type="1", conn=None):
		super().__init__(parent)
		self.setProperty("prop_type", prop_type)
		self.setCheckable(checkable)
		self.setText(text)
		if objectname:
			self.setObjectName(objectname)
		if conn:
			self.toggled.connect(conn) if self.isCheckable() else self.clicked.connect(conn)


class BaseLabel(QLabel):

	def __init__(self, parent=None, text="", prop_type="0", italic=False):
		super().__init__(parent)
		self.setFixedHeight(28)
		self.setProperty("prop_type", prop_type)
		self.setText(text)
		if italic:
			font = self.font()
			font.setItalic(True)
			self.setFont(font)


class BaseLineEdit(QLineEdit):
	def __init__(self, parent=None, text="", width=None, validate=None):
		super().__init__(parent)
		self.setFixedHeight(28)
		self.setPlaceholderText(text)
		if validate:
			if validate.isnumeric():
				self.setInputMask(validate)
			else:
				self.setValidator(EntryValidator(self, validate_type=validate))
		if width:
			self.setMaxLength(width)

	@property
	def entry(self):
		value = self.text()
		return value if value else None


class BaseSpinBox(QSpinBox):
	def __init__(self, parent=None, min_value=1, max_value=999999):
		super().__init__(parent)
		self.setFixedHeight(28)
		self.setProperty("prop_type", "1")
		self.setRange(min_value, max_value)
		self.setAlignment(Qt.AlignmentFlag.AlignCenter)

	@property
	def entry(self):
		value = self.value()
		return value if value else None


class BaseToggleButton(QAbstractButton):

	def __init__(self, parent=None, state=False, conn=None):
		super().__init__(parent)
		self.setProperty("prop_type", "0")
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
			animate = QPropertyAnimation(self, b'offset', self)
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


class CustomContainer(QFrame):
	def __init__(self, parent=None, is_vertical=True, is_expanding=True, width=0):
		super().__init__(parent)
		self.setObjectName("CustomContainer")
		self.setSizePolicy(
			QSizePolicy.Policy.Expanding,
			QSizePolicy.Policy.Expanding if is_expanding else QSizePolicy.Policy.Fixed
		)
		self.setLayout(QVBoxLayout(self) if is_vertical else QHBoxLayout(self))
		self.setGraphicsEffect(QGraphicsDropShadowEffect(
			parent=self,
			offset=0,
			blurRadius=10,
			color=Qt.GlobalColor.black,
			enabled=True
		))
		if width:
			self.setFixedWidth(width)

	def addLayout(self, *args):
		self.layout().addLayout(*args)

	def addStretch(self):
		self.layout().addStretch()

	def addWidget(self, *args):
		self.layout().addWidget(*args)


class CustomDialog(QDialog):

	def __init__(self, data, parent=None):
		super().__init__(parent)
		layout = QFormLayout(self)
		self._item = []
		self._data = data

		for key, value in self._data.items():
			self._item.append(BaseLineEdit(
				text=value[0]
			))
			if value[1]:
				self._item[-1].setText(value[1])
			layout.addRow(key, self._item[-1])

		button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel, self)
		layout.addWidget(button_box)
		button_box.accepted.connect(self.accept)
		button_box.rejected.connect(self.reject)

	def get_update(self):
		data = {}
		for key, value in self._data.items():
			for item in self._item:
				if item.placeholderText() == value[0]:
					data[key] = [value[0], item.text()]
					break
		return data


class CustomStack(QWidget):
	displayChanged = Signal(bool)
	fileOperation = Signal(bool)

	def __init__(self, version, parent=None):
		super().__init__(parent)
		layout = QVBoxLayout(self)
		layout.setContentsMargins(0, 0, 0, 0)
		layout.setSpacing(0)
		self._item = []

		header = QWidget()
		header_layout = QHBoxLayout(header)
		header_layout.setContentsMargins(-1, -1, -1, 0)
		layout.addWidget(header)
		self._item.append(QHBoxLayout())
		header_layout.addLayout(self._item[-1])
		header_layout.addStretch()

		self._item.append(QStackedWidget())
		layout.addWidget(self._item[-1])

		self._item.append(QButtonGroup())
		self._item[-1].idToggled.connect(self._item[1].setCurrentIndex)

		self._item.append(CustomToggle(
			text="Dark Mode",
			image="darkmode",
			state=False
		))
		header_layout.addWidget(self._item[-1])
		self._item[-1].stateChanged.connect(self._state_changed)

		header_layout.addWidget(BaseLabel(
			text=version,
			prop_type="4"
		))

	def _state_changed(self):
		self.displayChanged.emit(self._item[3].value)

	# noinspection PyTypeChecker
	def addWidget(self, widget, text):
		self._item.append(BasePushButton(
			text=text,
			checkable=True,
			prop_type="1"
		))
		self._item[0].addWidget(self._item[-1])
		if not len(self._item[2].buttons()):
			self._item[-1].setChecked(True)
		self._item[2].addButton(self._item[-1], len(self._item[2].buttons()))
		self._item[1].addWidget(widget)


class CustomToggle(QWidget):
	stateChanged = Signal()

	def __init__(self, parent=None, text=None, image=None, size=24, tooltip=False, state=False, stored=None, conn=None):
		super().__init__(parent)
		self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
		size = 24 if size > 24 else 18 if size < 18 else size
		layout = QHBoxLayout(self)
		layout.setContentsMargins(0, 0, 0, 0)
		layout.setSpacing(4)
		self._item = []
		self._has_icon = False
		self._stored = stored
		if image:
			self._item.append(QLabel())
			self._item[-1].setFixedSize(size, 24)
			self._item[-1].setPixmap(QPixmap(name_to_pix(text=image)).scaled(size, size, Qt.KeepAspectRatio))
			self._item[-1].setEnabled(state)
			layout.addWidget(self._item[-1])
			self._has_icon = True
		if self._has_icon and tooltip:
			self._item[-1].setToolTip(text)
		else:
			self._item.append(BaseLabel(
				text=text,
				prop_type="2"
			))
			layout.addWidget(self._item[-1])
		self._item.append(BaseToggleButton(
			state=state,
			conn=self._stateChanged
		))
		layout.addWidget(self._item[-1])
		if conn:
			self.stateChanged.connect(conn)

	@Slot(bool)
	def _stateChanged(self, state):
		if self._has_icon:
			self._item[0].setEnabled(state)
		self.stateChanged.emit()

	@property
	def value(self):
		if self._stored:
			return self._stored if self._item[-1].isChecked() else 0
		return self._item[-1].isChecked()


class CustomTree(QTreeWidget):
	modifyData = Signal(dict)

	def __init__(self, parent=None, header=None):
		super().__init__(parent)
		self.setAlternatingRowColors(True)
		self.setUniformRowHeights(False)
		self.setIndentation(8)
		self.setRootIsDecorated(True)
		self.setItemsExpandable(True)
		self.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
		self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
		if header:
			self.setHeaderLabels(header)
			font = self.header().font()
			font.setItalic(True)
			self.header().setFont(font)
			self.header().setDefaultAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
			self.header().setStretchLastSection(True)
		self.setHeaderHidden(False if header else True)
		self.itemChanged.connect(self._dataChanged)

	def _dataChanged(self):
		data = {}
		root = self.invisibleRootItem()
		for idx in range(root.childCount()):
			item_data = root.child(idx).data(0, Qt.ItemDataRole.UserRole)
			print(item_data)
		print("DATA Changed")

	def setData(self, data):
		if data["idx"] < 0:
			if data["type"] == 0:
				pass
			elif data["type"] == 1:
				pass
			elif data["type"] == 2:
				TreeItemStock(parent=self, data=data)
			elif data["type"] == 3:
				TreeItemClient(parent=self, data=data)
		else:
			self.invisibleRootItem().child(data["idx"]).value = data
		self.header().setStretchLastSection(False)
		for idx in range(self.columnCount()):
			self.resizeColumnToContents(idx)
		self.header().setStretchLastSection(True)


class ContentClient(QFrame):
	stateChanged = Signal(dict)

	def __init__(self, parent=None):
		super().__init__(parent)
		layout = QGridLayout(self)
		self._item = []
		self._modify_idx = -1

		layout.addWidget(BaseLabel(text="Company:"), 0, 0, 1, 1)
		self._item.append(BaseLineEdit(
			validate="allcaps"
		))
		layout.addWidget(self._item[-1], 0, 1, 1, 3)
		layout.addWidget(BaseLabel(text="Address:"), 1, 0, 1, 1)
		self._item.append(BaseLineEdit(
			validate="title"
		))
		layout.addWidget(self._item[-1], 1, 1, 1, 3)
		self._item.append(BaseLineEdit(
			validate="title"
		))
		layout.addWidget(self._item[-1], 2, 1, 1, 3)
		layout.addWidget(BaseLabel(text="Postcode:"), 3, 0, 1, 1)
		self._item.append(BaseLineEdit(
			validate="00000"
		))
		layout.addWidget(self._item[-1], 3, 1, 1, 1)
		layout.addWidget(BaseLabel(text="State:"), 3, 2, 1, 1)
		self._item.append(BaseLineEdit(
			validate="title"
		))
		layout.addWidget(self._item[-1], 3, 3, 1, 1)
		layout.addWidget(QWidget(), 0, 4, 1, 3)
		layout.addWidget(BasePushButton(
			text="Save",
			checkable=False,
			prop_type="3",
			objectname="save",
			conn=self._button_pressed
		), 0, 5, 1, 1)
		layout.addWidget(BasePushButton(
			text="Cancel",
			checkable=False,
			prop_type="3",
			objectname="cancel",
			conn=self._button_pressed
		), 0, 6, 1, 1)
		self.setVisible(False)

	def _button_pressed(self):
		if self.sender().objectName() == "save":
			if all([self._item[idx].entry for idx in range(5)]):
				data = {"type": 3, "idx": self._modify_idx}
				for idx, key in enumerate(["name", "address1", "address2", "postcode", "state"]):
					data[key] = self._item[idx].entry
					self._item[idx].clear()
				self.stateChanged.emit(data)
		else:
			self.stateChanged.emit({})

	def data(self, data):
		self._item[0].setText(data["name"])
		self._item[1].setText(data["address1"])
		self._item[2].setText(data["address2"])
		self._item[3].setText(data["postcode"])
		self._item[4].setText(data["state"])
		self._modify_idx = data["idx"]


class ContentStock(QFrame):
	stateChanged = Signal(dict)

	def __init__(self, parent=None):
		super().__init__(parent)
		layout = QHBoxLayout(self)
		self._item = []
		self._modify_idx = -1

		layout.addWidget(BaseLabel(text="Name:"))
		self._item.append(BaseLineEdit(
			validate="allcaps"
		))
		layout.addWidget(self._item[-1])
		layout.addWidget(BaseLabel(text="SKU:"))
		self._item.append(BaseLineEdit(
			validate="allcaps"
		))
		layout.addWidget(self._item[-1])
		layout.addWidget(BaseLabel(text="Description:"))
		self._item.append(BaseLineEdit(
			validate="title"
		))
		layout.addWidget(self._item[-1], 1)
		layout.addWidget(BaseLabel(text="Quantity:"))
		self._item.append(BaseSpinBox())
		self._item[-1].setDisabled(True)
		layout.addWidget(self._item[-1])
		layout.addWidget(QWidget())
		layout.addWidget(BasePushButton(
			text="Save",
			checkable=False,
			prop_type="3",
			objectname="save",
			conn=self._button_pressed
		))
		layout.addWidget(BasePushButton(
			text="Cancel",
			checkable=False,
			prop_type="3",
			objectname="cancel",
			conn=self._button_pressed
		))
		self.setVisible(False)

	def _button_pressed(self):
		if self.sender().objectName() == "save":
			if all([self._item[idx].entry for idx in range(4)]):
				data = {"type": 2, "idx": self._modify_idx}
				for idx, key in enumerate(["name", "sku", "desc", "qty"]):
					data[key] = self._item[idx].entry
					self._item[idx].clear() if idx < 3 else self._item[idx].setValue(self._item[idx].minimum())
				self.stateChanged.emit(data)
				self._modify_idx = -1
		else:
			self.stateChanged.emit({})

	def data(self, data):
		self._item[0].setText(data["name"])
		self._item[1].setText(data["sku"])
		self._item[2].setText(data["desc"])
		self._item[3].setValue(data["qty"])
		self._modify_idx = data["idx"]


class TreeItemClient(QTreeWidgetItem):

	def __init__(self, data, parent=None):
		super().__init__(parent)
		self.treeWidget().blockSignals(True)
		self._item = []
		self._item.append(BasePushButton(
			text="Modify Entry",
			checkable=False,
			prop_type="2",
			conn=self._button_modify
		))
		self.treeWidget().setItemWidget(self, 4, self._item[-1])
		self._item.append(BasePushButton(
			text="Custom SKU",
			checkable=False,
			prop_type="2",
			conn=self._button_custom
		))
		self.treeWidget().setItemWidget(self, 5, self._item[-1])
		self.treeWidget().blockSignals(False)
		self.value = data

	# noinspection PyUnresolvedReferences
	def _button_modify(self):
		self.treeWidget().modifyData.emit(self.value)

	def _button_custom(self):
		print("Custom!!!")

	@property
	def value(self):
		return self.data(0, Qt.ItemDataRole.UserRole)

	@value.setter
	def value(self, data):
		self.treeWidget().blockSignals(True)
		self.setText(0, data["name"])
		self.setText(1, data["address1"])
		self.setText(2, data["postcode"])
		self.setText(3, data["state"])
		self.treeWidget().blockSignals(False)
		if data["idx"] < 0:
			data["idx"] = self.treeWidget().indexFromItem(self, 0).row()
		self.setData(0, Qt.ItemDataRole.UserRole, data)


class TreeItemStock(QTreeWidgetItem):

	def __init__(self, data, parent=None):
		super().__init__(parent)
		self.treeWidget().blockSignals(True)
		self._item = []
		self._item.append(BasePushButton(
			text="Modify Entry",
			checkable=False,
			prop_type="2",
			conn=self._button_modify
		))
		self.treeWidget().setItemWidget(self, 4, self._item[-1])
		self._item.append(BasePushButton(
			text="Add Stock",
			checkable=False,
			prop_type="2",
			conn=self._button_custom
		))
		self.treeWidget().setItemWidget(self, 5, self._item[-1])
		self.treeWidget().blockSignals(False)
		self.value = data

	# noinspection PyUnresolvedReferences
	def _button_modify(self):
		self.treeWidget().modifyData.emit(self.value)

	def _button_custom(self):
		num, ok = QInputDialog.getInt(self.treeWidget(), "Title", "Add New Stock Received:", 1)
		if ok:
			data = self.value
			data["qty"] += num
			self.value = data

	@property
	def value(self):
		return self.data(0, Qt.ItemDataRole.UserRole)

	@value.setter
	def value(self, data):
		self.treeWidget().blockSignals(True)
		self.setText(0, data["name"])
		self.setText(1, data["sku"])
		self.setText(2, data["desc"])
		self.setText(3, f"""{data["qty"]:,}""")
		self.treeWidget().blockSignals(False)
		if data["idx"] < 0:
			data["idx"] = self.treeWidget().indexFromItem(self, 0).row()
		self.setData(0, Qt.ItemDataRole.UserRole, data)


class EntryValidator(QValidator):
	def __init__(self, parent, validate_type="allcaps"):
		super().__init__(parent)
		self._type = validate_type

	def validate(self, string, pos):
		match self._type:
			case "title":
				return QValidator.State.Acceptable, string.title(), pos
			case _:
				return QValidator.State.Acceptable, string.upper(), pos


class StackTab1(QWidget):

	def __init__(self, parent=None):
		super().__init__(parent)
		layout = QGridLayout(self)
		layout.setContentsMargins(-1, 8, -1, -1)


class StackTab2(QWidget):

	def __init__(self, parent=None):
		super().__init__(parent)
		self._data = {}

	def setData(self, data):
		self._data = data


class StackTab3(QWidget):

	def __init__(self, parent=None):
		super().__init__(parent)
		layout = QVBoxLayout(self)
		layout.setContentsMargins(-1, 8, -1, -1)
		self._item = [CustomTree(header=["Item", "SKU", "Description", "Quantity", "", "", ""])]
		self._item[-1].modifyData.connect(self._modify_data)
		self._data = {}

		container = CustomContainer(is_vertical=False)
		layout.addWidget(container)

		content_layout = QVBoxLayout()
		container.addLayout(content_layout)

		self._item.append(ContentStock())
		content_layout.addWidget(self._item[-1])
		self._item[-1].stateChanged.connect(self._state_changed)
		content_layout.addWidget(self._item[0])

		button_layout = QVBoxLayout()
		container.addLayout(button_layout)

		self._item.append(BasePushButton(
			text="New",
			checkable=False,
			prop_type="3",
			objectname="new",
			conn=self._button_pressed
		))
		button_layout.addWidget(self._item[-1])
		button_layout.addStretch()

	def _button_pressed(self):
		self._item[0].setEnabled(False)
		self._item[1].setVisible(True)
		self._item[2].setEnabled(False)

	@Slot(dict)
	def _modify_data(self, data):
		self._item[1].data(data=data)
		self._button_pressed()

	@Slot(dict)
	def _state_changed(self, data):
		if data:
			self._item[0].setData(data=data)
		self._item[0].setEnabled(True)
		self._item[1].setVisible(False)
		self._item[2].setEnabled(True)

	def setData(self, data):
		self._data = data


class StackTab4(QWidget):

	def __init__(self, parent=None):
		super().__init__(parent)
		layout = QVBoxLayout(self)
		layout.setContentsMargins(-1, 8, -1, -1)
		self._item = [CustomTree(header=["Company", "Address", "Postcode", "State", "", "", ""])]
		self._item[-1].modifyData.connect(self._modify_data)
		self._data = {}

		container = CustomContainer(is_vertical=False)
		layout.addWidget(container)

		content_layout = QVBoxLayout()
		container.addLayout(content_layout)

		self._item.append(ContentClient())
		content_layout.addWidget(self._item[-1])
		self._item[-1].stateChanged.connect(self._state_changed)
		content_layout.addWidget(self._item[0])

		button_layout = QVBoxLayout()
		container.addLayout(button_layout)

		self._item.append(BasePushButton(
			text="New",
			checkable=False,
			prop_type="3",
			objectname="new",
			conn=self._button_pressed
		))
		button_layout.addWidget(self._item[-1])
		button_layout.addStretch()

	def _button_pressed(self):
		self._item[0].setEnabled(False)
		self._item[1].setVisible(True)
		self._item[2].setEnabled(False)

	@Slot(dict)
	def _modify_data(self, data):
		self._item[1].data(data=data)
		self._button_pressed()

	@Slot(dict)
	def _state_changed(self, data):
		if data:
			self._item[0].setData(data=data)
		self._item[0].setEnabled(True)
		self._item[1].setVisible(False)
		self._item[2].setEnabled(True)

	def setData(self, data):
		self._data = data
