import sys

from PySide6.QtCore import (
	QTimer, QThread, QDir
)
from PySide6.QtWidgets import (
	QApplication, QSplashScreen, QMainWindow, QFileDialog
)

from view import *


APP_TITLE = "Inventory & Stock Manager"
APP_VERSION = "v0.0.1"
APP_SPLASH = app_path("splash.png")
APP_ICON = app_path("icon.ico")


class MainUI(QMainWindow):
	_thread = None
	_worker = None

	def __init__(self, parent=None):
		super().__init__(parent)
		self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
		self.setWindowTitle(APP_TITLE)
		self.setWindowIcon(QIcon(APP_ICON))
		self.resize(1280, 720)

	def setData(self, data):
		print(">>>", data)

	def setState(self, state):
		if state:
			# self.setStyleSheet(stylesheet())
			self.show()
		else:
			self.close()


class SplashUI(QSplashScreen):
	_thread = None
	_worker = None

	def __init__(self):
		super().__init__()
		self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.FramelessWindowHint)
		self.setPixmap(QPixmap(APP_SPLASH))
		self.setWindowTitle(APP_TITLE)
		QTimer.singleShot(500, self.initialize)
		self.show()

	# noinspection PyUnresolvedReferences
	def initialize(self):
		self._worker = InitializeApp({"version": APP_VERSION})
		self._thread = QThread()
		self._worker.moveToThread(self._thread)
		self._worker.progress.connect(self.showMessage)
		self._worker.data.connect(main.setData)
		self._worker.finished.connect(self.thread_ended)
		self._thread.started.connect(self._worker.run)
		self._thread.start()

	def mousePressEvent(self, event) -> None:  # disable default "click-to-dismiss" behaviour
		pass

	@Slot(bool)
	def thread_ended(self, state):
		self._thread.quit()
		self._thread.wait()
		main.setState(state=state)
		self.close()


if __name__ == '__main__':
	app = QApplication()
	app.setWindowIcon(QIcon(APP_ICON))
	main = MainUI()
	splash = SplashUI()
	app.exec()
