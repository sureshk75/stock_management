import json
import math
import os
import time

from PySide6.QtCore import (
	QAbstractTableModel, QModelIndex, QObject, QSortFilterProxyModel, Qt, Signal
)
from PySide6.QtGui import (
	QPixmap
)


def app_path(filename, directory="resource"):
	base_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), directory)
	if not os.path.exists(base_path):
		os.makedirs(base_path)
	abs_path = os.path.join(base_path, filename).replace("\\", "/")
	if os.path.isfile(abs_path):
		return abs_path
	elif ".png" in filename:
		return os.path.join(base_path, "default.png").replace("\\", "/")
	else:
		return None


class Database:

	def __init__(self):
		self._data = {}


class InitializeApp(QObject):
	finished = Signal(bool)
	progress = Signal(str)
	data = Signal(dict)

	def __init__(self, data):
		super().__init__()
		self._data = data

	def run(self):
		state = True
		data = {}
		if app_path(filename="data", directory="stored"):
			fd = open(app_path(filename="data", directory="stored"), "r")
			data = json.loads(fd.read())
		self.data.emit(data)
		time.sleep(1)
		self.finished.emit(state)
