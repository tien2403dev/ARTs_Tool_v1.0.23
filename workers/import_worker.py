from PyQt5.QtCore import (
    QThread,
    pyqtSignal
)

from services.excel_service import (
    load_excel_files
)

from services.sqlite_service import (
    SQLiteService
)


class ImportWorker(QThread):

    progress = pyqtSignal(int)

    finished = pyqtSignal()

    error = pyqtSignal(str)

    def __init__(self, files):

        super().__init__()

        self.files = files

    def run(self):

        try:

            df = load_excel_files(
                self.files,
                self.progress.emit
            )

            db = SQLiteService()

            skipped_dates = db.insert_dataframe(df)

            db.conn.execute("ANALYZE")
            db.conn.commit()

            if skipped_dates:
                self.error.emit(
                    "Skipped existing File Date(s):\n\n"
                    + "\n".join(skipped_dates)
                )

            self.finished.emit()

        except Exception as e:

            self.error.emit(
                str(e)
            )