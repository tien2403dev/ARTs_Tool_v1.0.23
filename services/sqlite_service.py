import sqlite3
import sys
import os
from pathlib import Path
from datetime import datetime
import pandas as pd
def get_app_dir():
    """
    Trả về thư mục gốc của ứng dụng.

    - Khi chạy bằng Python:
        ARTs_App/

    - Khi chạy bằng EXE:
        Thư mục chứa file exe
    """

    if getattr(sys, "frozen", False):
        return Path(sys.executable).parent

    return Path(__file__).resolve().parent.parent


APP_DIR = get_app_dir()

# DB_DIR = APP_DIR / "database" db lưu trực tiếp trên project làm ảnh hưởng khi có nhiều người dùng
##update db lưu trên máy của từng người để không làm ảnh hương khi có nhiều nguowif dùng cùng lúc
# DB_DIR = (
#         Path(os.getenv("LOCALAPPDATA"))
#         / "ARTs_App"
#         / "database"
# )
#
# DB_PATH = DB_DIR / "app.db"
DB_DIR = APP_DIR / "database"

DB_PATH = DB_DIR / "app.db"

class SQLiteService:

    def __init__(self):

        DB_DIR.mkdir(
            parents=True,
            exist_ok=True
        )

        self.conn = sqlite3.connect(
            DB_PATH,
            check_same_thread=False
        )

        self.create_table()
        self.create_indexes()

    def create_table(self):

        cursor = self.conn.cursor()

        # cursor.execute("""
        #                CREATE TABLE IF NOT EXISTS data
        #                (
        #                    ID
        #                    INTEGER
        #                    PRIMARY
        #                    KEY
        #                    AUTOINCREMENT,
        #
        #                    LOTID
        #                    TEXT,
        #                    File_Date
        #                    TEXT,
        #                    EQP
        #                    TEXT,
        #                    Handler
        #                    TEXT,
        #                    ZONE
        #                    TEXT,
        #                    SLOT
        #                    INTEGER,
        #                    Model
        #                    TEXT,
        #                    Qty
        #                    INTEGER,
        #                    Fail
        #                    INTEGER,
        #                    SCRAP
        #                    TEXT
        #                )
        #                """)
        cursor.execute("""
                       CREATE TABLE IF NOT EXISTS data
                       (
                           ID
                           INTEGER
                           PRIMARY
                           KEY
                           AUTOINCREMENT,

                           LOTID
                           TEXT,
                           File_Date
                           TEXT,
                           Datetime
                           TEXT,

                           EQP
                           TEXT,
                           Handler
                           TEXT,
                           ZONE
                           TEXT,
                           SLOT
                           INTEGER,
                           Model
                           TEXT,
                           Qty
                           INTEGER,
                           Fail
                           INTEGER,
                           SCRAP
                           TEXT
                       )
                       """)

        cursor.execute("""
                       CREATE TABLE IF NOT EXISTS eqp_master
                       (
                           EQP
                           TEXT
                           PRIMARY
                           KEY
                       )
                       """)

        cursor.execute("""
                       CREATE TABLE IF NOT EXISTS handler_master
                       (
                           Handler
                           TEXT
                           PRIMARY
                           KEY
                       )
                       """)

        cursor.execute("""
                       CREATE TABLE IF NOT EXISTS zone_master
                       (
                           Zone
                           TEXT
                           PRIMARY
                           KEY
                       )
                       """)

        cursor.execute("""
                       CREATE TABLE IF NOT EXISTS slot_master
                       (
                           Slot
                           TEXT
                           PRIMARY
                           KEY
                       )
                       """)

        cursor.execute("""
                       CREATE TABLE IF NOT EXISTS model_master
                       (
                           Model
                           TEXT
                           PRIMARY
                           KEY
                       )
                       """)

        cursor.execute("""
                       CREATE TABLE IF NOT EXISTS date_master
                       (
                           File_Date
                           TEXT
                           PRIMARY
                           KEY
                       )
                       """)

        cursor.execute("""
                       CREATE TABLE IF NOT EXISTS scrap_master
                       (
                           Scrap_Code
                           TEXT
                           PRIMARY
                           KEY
                       )
                       """)
        ####TAO BANG CHO CAC BO LOC

        self.conn.commit()

    def update_master_tables(self, df):

        cursor = self.conn.cursor()

        # ===== EQP =====
        eqps = df["EQP"].dropna().astype(str).unique()
        cursor.executemany(
            "INSERT OR IGNORE INTO eqp_master(EQP) VALUES(?)",
            [(x,) for x in eqps]
        )

        # ===== Handler =====
        handlers = df["Handler"].dropna().astype(str).unique()
        cursor.executemany(
            "INSERT OR IGNORE INTO handler_master(Handler) VALUES(?)",
            [(x,) for x in handlers]
        )

        # ===== Zone =====
        zones = df["ZONE"].dropna().astype(str).unique()
        cursor.executemany(
            "INSERT OR IGNORE INTO zone_master(Zone) VALUES(?)",
            [(x,) for x in zones]
        )

        # ===== Slot =====
        slots = df["SLOT"].dropna().astype(str).unique()
        cursor.executemany(
            "INSERT OR IGNORE INTO slot_master(Slot) VALUES(?)",
            [(x,) for x in slots]
        )

        # ===== Model =====
        models = df["Model"].dropna().astype(str).unique()
        cursor.executemany(
            "INSERT OR IGNORE INTO model_master(Model) VALUES(?)",
            [(x,) for x in models]
        )

        # ===== Date =====
        dates = df["File_Date"].dropna().astype(str).unique()
        cursor.executemany(
            "INSERT OR IGNORE INTO date_master(File_Date) VALUES(?)",
            [(x,) for x in dates]
        )

        # ===== Scrap (giữ logic, không vectorize ở level 2) =====
        scrap_codes = set()

        for scrap_text in df["SCRAP"].dropna():
            scrap_text = str(scrap_text).strip()

            if scrap_text == "-":
                continue

            for item in scrap_text.split(","):
                item = item.strip()
                if not item:
                    continue

                code = item.split(":")[0].strip()

                if code == "0":
                    code = "0000"

                if code.isdigit() and len(code) == 4:
                    scrap_codes.add(code)

        cursor.executemany(
            "INSERT OR IGNORE INTO scrap_master(Scrap_Code) VALUES(?)",
            [(x,) for x in scrap_codes]
        )

        self.conn.commit()

    ###CHI THEM MOI KHONG CAP NHAT
    def insert_dataframe(self, df):

        cursor = self.conn.cursor()

        cursor.execute("BEGIN")

        try:

            dates = (
                df["File_Date"]
                .dropna()
                .astype(str)
                .unique()
                .tolist()
            )

            existing_dates = []

            for date in dates:

                if self.is_file_date_exists(date):
                    existing_dates.append(date)

            # Có bất kỳ ngày nào trùng
            if existing_dates:
                raise ValueError(
                    "Các File_Date sau đã tồn tại:\n\n"
                    +
                    "\n".join(existing_dates)
                    +
                    "\n\nVui lòng xóa File_Date cũ sau đó import lại."
                )

            # Insert date_master
            for date in dates:
                self.insert_file_date(date)

            self.update_master_tables(df)

            # df_db = df[
            #     [
            #         "LOTID",
            #         "File_Date",
            #         "EQP",
            #         "Handler",
            #         "ZONE",
            #         "SLOT",
            #         "Model",
            #         "QTY",
            #         "Fail",
            #         "SCRAP"
            #     ]
            # ].copy()
            df_db = df[
                [
                    "LOTID",
                    "File_Date",
                    "Datetime",
                    "EQP",
                    "Handler",
                    "ZONE",
                    "SLOT",
                    "Model",
                    "QTY",
                    "Fail",
                    "SCRAP"
                ]
            ].copy()

            df_db.rename(
                columns={
                    "QTY": "Qty"
                },
                inplace=True
            )

            df_db.to_sql(
                "data",
                self.conn,
                if_exists="append",
                index=False,
                chunksize=100000
            )

            self.conn.commit()

        except Exception:

            self.conn.rollback()

            raise

    ###INSERT NEU LOT ID TON TAI THI CAP NHAT NEU LOT ID CHUA CO THI THEM MOI
    # def insert_dataframe(self, df):
    #
    #     cursor = self.conn.cursor()
    #
    #     cursor.execute("BEGIN")
    #
    #     try:
    #
    #         # Cập nhật bảng master
    #         self.update_master_tables(df)
    #
    #         records = list(
    #             df[
    #                 [
    #                     "LOTID",
    #                     "File_Date",
    #                     "EQP",
    #                     "Handler",
    #                     "ZONE",
    #                     "SLOT",
    #                     "Model",
    #                     "QTY",
    #                     "Fail",
    #                     "SCRAP"
    #                 ]
    #             ].itertuples(
    #                 index=False,
    #                 name=None
    #             )
    #         )
    #
    #         cursor.executemany(
    #             """
    #             INSERT INTO data
    #             (LOTID,
    #              File_Date,
    #              EQP,
    #              Handler,
    #              ZONE,
    #              SLOT,
    #              Model,
    #              Qty,
    #              Fail,
    #              SCRAP)
    #             VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?) ON CONFLICT(LOTID)
    #             DO
    #             UPDATE SET
    #                 File_Date = excluded.File_Date,
    #                 EQP = excluded.EQP,
    #                 Handler = excluded.Handler,
    #                 ZONE = excluded.ZONE,
    #                 SLOT = excluded.SLOT,
    #                 Model = excluded.Model,
    #                 Qty = excluded.Qty,
    #                 Fail = excluded.Fail,
    #                 SCRAP = excluded.SCRAP
    #             """,
    #             records
    #         )
    #
    #         self.conn.commit()
    #
    #     except Exception as e:
    #
    #         print("ERROR:", repr(e))
    #
    #         self.conn.rollback()
    #
    #         raise

    # def debug_table_data(self):
    #
    #     cursor = self.conn.cursor()
    #
    #     cursor.execute(
    #         "PRAGMA table_info(data)"
    #     )
    #
    #     for row in cursor.fetchall():
    #         print(row)


    def create_indexes(self):

        cursor = self.conn.cursor()

        cursor.execute("""
                       CREATE INDEX IF NOT EXISTS idx_eqp_date
                           ON data (EQP, File_Date)
                       """)
        cursor.execute("""
                       CREATE INDEX IF NOT EXISTS idx_file_date_eqp
                           ON data (File_Date, EQP)
                       """)
        cursor.execute("""
                        CREATE INDEX IF NOT EXISTS idx_eqp_handler_date
                        ON data(EQP, Handler, File_Date);
                       """)
        cursor.execute("""
                        CREATE INDEX IF NOT EXISTS idx_eqp_handler_zone_date
                        ON data(
                            EQP,
                            Handler,
                            ZONE,
                            File_Date
                        );
                       """)
        cursor.execute("""
                       CREATE INDEX IF NOT EXISTS idx_eqp_handler_date_scrap
                        ON data(
                            EQP,
                            Handler,
                            File_Date,
                            SCRAP
                        );
                       """)
        cursor.execute("""
                       CREATE INDEX IF NOT EXISTS idx_eqp_handler_date_zone
                        ON data(
                            EQP,
                            Handler,
                            File_Date,
                            ZONE
                        );
                       """)
        cursor.execute("""
                       CREATE INDEX IF NOT EXISTS idx_data_consecutive
                           ON data (
                           EQP,
                           Handler,
                           ZONE,
                           SLOT,
                           Datetime
                           )
                       """)



        self.conn.commit()

    def get_all_data(self):

        cursor = self.conn.cursor()

        cursor.execute(
            "SELECT * FROM data"
        )

        return cursor.fetchall()

    def get_headers(self):

        cursor = self.conn.cursor()

        cursor.execute(
            "PRAGMA table_info(data)"
        )

        return [
            row[1]
            for row in cursor.fetchall()
        ]

    def close(self):

        if self.conn:
            self.conn.close()

    ##### LOẠI BỎ DỮ LIỆU TRÙNG LẶP CHO BỘ LỌC
    def get_distinct_values(
            self,
            column_name
    ):

        cursor = self.conn.cursor()

        table_map = {
            "EQP": ("eqp_master", "EQP"),
            "Handler": ("handler_master", "Handler"),
            "ZONE": ("zone_master", "Zone"),
            "SLOT": ("slot_master", "Slot"),
            "Model": ("model_master", "Model"),
            "File_Date": ("date_master", "File_Date")
        }

        table_name, field_name = table_map[column_name]

        if column_name == "SLOT":

            cursor.execute(
                f"""
                SELECT {field_name}
                FROM {table_name}
                ORDER BY CAST({field_name} AS INTEGER)
                """
            )

        else:

            cursor.execute(
                f"""
                SELECT {field_name}
                FROM {table_name}
                ORDER BY {field_name}
                """
            )

        return [
            str(row[0])
            for row in cursor.fetchall()
        ]

    ####LẤY SCRAP CODE CHO BỘ LỌC
    def get_scrap_codes(self):

        cursor = self.conn.cursor()

        cursor.execute("""
                       SELECT Scrap_Code
                       FROM scrap_master
                       ORDER BY CAST(Scrap_Code AS INTEGER)
                       """)

        return [row[0] for row in cursor.fetchall()]

    ####THOONGS KE DU LIEUU CHO HANDLER

    def get_handler_monthly_summary(
            self,
            eqp,
            handler,
            date_from,
            date_to
    ):

        cursor = self.conn.cursor()
        #############
        cursor.execute(
            """
            EXPLAIN QUERY PLAN
            SELECT
                ZONE,
                COALESCE(SUM(Qty),0),
                COALESCE(SUM(Fail),0)
            FROM data
            WHERE EQP = ?
              AND Handler = ?
              AND File_Date BETWEEN ? AND ?
            GROUP BY ZONE
            """,
            (
                eqp,
                str(handler),
                date_from,
                date_to
            )
        )

        for row in cursor.fetchall():
            print(row)

        cursor.execute(
            """
            SELECT
                ZONE, COALESCE (
                SUM (CAST (QTY AS INTEGER)), 0
                ) AS qty, COALESCE (
                SUM (CAST (Fail AS INTEGER)), 0
                ) AS fail
            FROM data
            WHERE EQP = ?
                AND Handler = ?
                AND File_Date BETWEEN ? AND ?
            GROUP BY ZONE
            """,
            (
                eqp,
                str(handler),
                date_from,
                date_to
            )
        )

        zone_data = {
            row[0]: (
                int(row[1] or 0),
                int(row[2] or 0)
            )
            for row in cursor.fetchall()
        }

        result = []

        for zone in ["A", "B", "C", "D", "E", "F"]:
            qty, fail = zone_data.get(
                zone,
                (0, 0)
            )

            passed = qty - fail

            yield_rate = (
                round(
                    passed * 100 / qty,
                    2
                )
                if qty > 0
                else 0
            )

            result.append(
                (
                    zone,
                    qty,
                    passed,
                    fail,
                    f"{yield_rate:.2f}%"
                )
            )

        return result

    ###daily summary

    def get_handler_daily_summary(
            self,
            eqp,
            handler,
            file_date
    ):

        cursor = self.conn.cursor()

        cursor.execute(
            """
            SELECT
                ZONE, COALESCE (
                SUM (CAST (QTY AS INTEGER)), 0
                ) AS qty, COALESCE (
                SUM (CAST (Fail AS INTEGER)), 0
                ) AS fail
            FROM data
            WHERE EQP = ?
              AND Handler = ?
              AND File_Date = ?
            GROUP BY ZONE
            """,
            (
                eqp,
                str(handler),
                file_date
            )
        )

        zone_data = {
            row[0]: (
                int(row[1] or 0),
                int(row[2] or 0)
            )
            for row in cursor.fetchall()
        }

        result = []

        for zone in ["A", "B", "C", "D", "E", "F"]:
            qty, fail = zone_data.get(
                zone,
                (0, 0)
            )

            passed = qty - fail

            yield_rate = (
                round(
                    passed * 100 / qty,
                    2
                )
                if qty > 0
                else 0
            )

            result.append(
                (
                    zone,
                    qty,
                    passed,
                    fail,
                    f"{yield_rate:.2f}%"
                )
            )

        return result

    ####HET TAB HANDLER

    ####LAY DU LIEU CHO TAB SUMMARY
    def get_summary_data(
            self,
            eqp,
            date_from,
            date_to
    ):

        cursor = self.conn.cursor()

        error_codes = self.get_scrap_codes()

        daily_summary = {}

        # ==================================================
        # Query 1: SQLite tổng hợp Qty/Fail theo ngày
        # ==================================================

        cursor.execute(
            """
            SELECT File_Date,
                   COALESCE(SUM(CAST(QTY AS INTEGER)), 0),
                   COALESCE(SUM(CAST(Fail AS INTEGER)), 0)
            FROM data
            WHERE EQP = ?
              AND File_Date BETWEEN ? AND ?
            GROUP BY File_Date
            """,
            (
                eqp,
                date_from,
                date_to
            )
        )

        for file_date, qty, fail in cursor.fetchall():
            daily_summary[file_date] = {
                "qty": int(qty or 0),
                "fail": int(fail or 0),
                "codes": {
                    code: 0
                    for code in error_codes
                }
            }

        # ==================================================
        # Query 2: Chỉ lấy SCRAP để đếm mã lỗi
        # ==================================================

        cursor.execute(
            """
            SELECT File_Date,
                   SCRAP
            FROM data
            WHERE EQP = ?
              AND File_Date BETWEEN ? AND ?
              AND SCRAP IS NOT NULL
              AND SCRAP != ''
              AND SCRAP != '-'
            """,
            (
                eqp,
                date_from,
                date_to
            )
        )

        for file_date, scrap_text in cursor:

            if file_date not in daily_summary:
                continue

            scrap_text = str(scrap_text).strip()

            for item in scrap_text.split(","):

                item = item.strip()

                if not item:
                    continue

                code = item.split(":")[0].strip()

                if code == "0":
                    code = "0000"

                if code in daily_summary[file_date]["codes"]:
                    daily_summary[file_date]["codes"][code] += 1

        # ==================================================
        # Tạo kết quả trả về
        # ==================================================

        result = []

        for file_date in sorted(daily_summary.keys()):

            qty = daily_summary[file_date]["qty"]

            fail = daily_summary[file_date]["fail"]

            out = qty - fail

            yield_rate = (
                round(
                    out * 100 / qty,
                    2
                )
                if qty > 0
                else 0
            )

            row = [
                file_date,
                qty,
                out,
                fail,
                f"{yield_rate:.2f}%"
            ]

            for code in error_codes:
                count = daily_summary[file_date]["codes"][code]

                row.append(
                    ""
                    if count == 0
                    else count
                )

            result.append(row)

        return result

    ####LAY DU LIEU TONG CA 4 HANDLER
    def get_handler_summary_data(
            self,
            eqp,
            handler,
            date_from,
            date_to
    ):

        cursor = self.conn.cursor()

        error_codes = self.get_scrap_codes()

        daily_summary = {}

        # ==========================================
        # Query 1
        # Tổng hợp Qty/Fail theo ngày
        # ==========================================

        cursor.execute(
            """
            SELECT File_Date,
                   COALESCE(
                           SUM(CAST(QTY AS INTEGER)),
                           0
                   ) AS qty,
                   COALESCE(
                           SUM(CAST(Fail AS INTEGER)),
                           0
                   ) AS fail
            FROM data
            WHERE EQP = ?
                AND Handler = ?
                AND File_Date BETWEEN ? AND ?
            GROUP BY File_Date
            """,
            (
                eqp,
                str(handler),
                date_from,
                date_to
            )
        )

        for file_date, qty, fail in cursor.fetchall():
            daily_summary[file_date] = {
                "qty": int(qty or 0),
                "fail": int(fail or 0),
                "codes": {
                    code: 0
                    for code in error_codes
                }
            }

        # ==========================================
        # Query 2
        # Chỉ xử lý Scrap
        # ==========================================

        cursor.execute(
            """
            SELECT File_Date,
                   SCRAP
            FROM data
            WHERE EQP = ?
                AND Handler = ?
                AND File_Date BETWEEN ? AND ?
              AND SCRAP IS NOT NULL
              AND SCRAP != ''
              AND SCRAP != '-'
            """,
            (
                eqp,
                str(handler),
                date_from,
                date_to
            )
        )

        for file_date, scrap_text in cursor:

            if file_date not in daily_summary:
                continue

            scrap_text = str(scrap_text).strip()

            for item in scrap_text.split(","):

                item = item.strip()

                if not item:
                    continue

                code = item.split(":")[0].strip()

                if code == "0":
                    code = "0000"

                if code in daily_summary[file_date]["codes"]:
                    daily_summary[file_date]["codes"][code] += 1

        # ==========================================
        # Tạo kết quả trả về
        # ==========================================

        result = []

        for file_date in sorted(daily_summary.keys()):

            qty = daily_summary[file_date]["qty"]

            fail = daily_summary[file_date]["fail"]

            out = qty - fail

            yield_rate = (
                round(
                    out * 100 / qty,
                    2
                )
                if qty > 0
                else 0
            )

            row = [
                file_date,
                qty,
                out,
                fail,
                f"{yield_rate:.2f}%"
            ]

            for code in error_codes:
                count = daily_summary[file_date]["codes"][code]

                row.append(
                    ""
                    if count == 0
                    else count
                )

            result.append(row)

        return result

    ####DU LIEU PPM CHO SUMMARY (TAT CA CAC HANDLER)
    def get_ppm_summary_data(
            self,
            summary_data
    ):

        result = []

        for row in summary_data:

            file_date = row[0]

            qty = int(row[1] or 0)

            out = row[2]

            fail = row[3]

            yield_rate = row[4]

            ppm_row = [
                file_date,
                qty,
                out,
                fail,
                yield_rate
            ]

            for value in row[5:]:
                error_qty = (
                    int(value)
                    if value != ""
                    else 0
                )

                ppm = (
                    round(
                        error_qty * 1000000 / qty,
                        0
                    )
                    if qty > 0
                    else 0
                )

                ppm_row.append(
                    "" if ppm == 0 else int(ppm)
                )

            result.append(
                ppm_row
            )
            # print(result)

        return result

    def get_ppm_headers(self):

        return [
            "Date",
            "In",
            "Out",
            "Fail",
            "Cum Yield"
        ] + self.get_scrap_codes()

    ####DU LIEU PPM CHO 4 HANDLER
    def get_handler_ppm_summary_data(
            self,
            summary_data
    ):

        result = []

        for row in summary_data:

            qty = int(row[1] or 0)

            ppm_row = row[:5]

            for value in row[5:]:
                error_qty = (
                    int(value)
                    if value != ""
                    else 0
                )

                ppm = (
                    round(
                        error_qty * 1000000 / qty,
                        0
                    )
                    if qty > 0
                    else 0
                )

                ppm_row.append(
                    "" if ppm == 0 else int(ppm)
                )

            result.append(ppm_row)

        return result

    def get_summary_headers(self):

        return [
            "Date",
            "In",
            "Out",
            "Fail",
            "Cum Yield"
        ] + self.get_scrap_codes()


    ####TAB ANALYZE##########
    ##tong hop theo tung thiet bi trong thang
    def get_monthly_eqp_summary(
            self,
            date_from,
            date_to
    ):

        cursor = self.conn.cursor()

        cursor.execute(
            """
            SELECT EQP,
                   COALESCE(SUM(CAST(QTY AS INTEGER)), 0),
                   COALESCE(SUM(CAST(Fail AS INTEGER)), 0)
            FROM data
            WHERE File_Date BETWEEN ? AND ?
            GROUP BY EQP
            ORDER BY EQP
            """,
            (
                date_from,
                date_to
            )
        )

        result = []

        total_in = 0
        total_fail = 0

        for eqp, qty, fail in cursor.fetchall():
            qty = int(qty or 0)

            fail = int(fail or 0)

            out = qty - fail

            ppm = (
                round(
                    fail * 1000000 / qty,
                    1
                )
                if qty > 0
                else 0
            )

            yield_rate = (
                round(
                    out * 100 / qty,
                    2
                )
                if qty > 0
                else 0
            )

            result.append(
                [
                    eqp,
                    qty,
                    out,
                    fail,
                    ppm,
                    f"{yield_rate:.2f}%"
                ]
            )

            total_in += qty
            total_fail += fail

        total_out = total_in - total_fail

        total_ppm = (
            round(
                total_fail * 1000000 / total_in,
                1
            )
            if total_in > 0
            else 0
        )

        total_yield = (
            round(
                total_out * 100 / total_in,
                2
            )
            if total_in > 0
            else 0
        )

        result.append(
            [
                "Total",
                total_in,
                total_out,
                total_fail,
                total_ppm,
                f"{total_yield:.2f}%"
            ]
        )

        return result

    def get_monthly_eqp_headers(self):

        return [
            "EQP ID",
            "In",
            "Out",
            "Fail Qty",
            "Fail PPM",
            "Yield"
        ]

    ###TONG HOP DU LIEU CAC MAY THEO TUNG NGAY DUOC CHON
    def get_daily_eqp_summary(
            self,
            file_date
    ):

        cursor = self.conn.cursor()

        cursor.execute(
            """
            SELECT EQP,
                   SUM(CAST(QTY AS INTEGER)),
                   SUM(CAST(Fail AS INTEGER))
            FROM data
            WHERE File_Date = ?
            GROUP BY EQP
            ORDER BY EQP
            """,
            (file_date,)
        )

        result = []

        total_in = 0
        total_fail = 0

        for eqp, qty, fail in cursor.fetchall():
            qty = int(qty or 0)
            fail = int(fail or 0)

            out = qty - fail

            ppm = (
                round(fail * 1000000 / qty, 0)
                if qty > 0
                else 0
            )

            yield_rate = (
                round(out * 100 / qty, 2)
                if qty > 0
                else 0
            )

            result.append([
                eqp,
                qty,
                out,
                fail,
                int(ppm),
                f"{yield_rate:.2f}%"
            ])

            total_in += qty
            total_fail += fail

        total_out = total_in - total_fail

        total_ppm = (
            round(
                total_fail * 1000000 / total_in,
                0
            )
            if total_in > 0
            else 0
        )

        total_yield = (
            round(
                total_out * 100 / total_in,
                2
            )
            if total_in > 0
            else 0
        )

        result.append([
            "Total",
            total_in,
            total_out,
            total_fail,
            int(total_ppm),
            f"{total_yield:.2f}%"
        ])

        return result

    def get_monthly_eqp_headers(self):

        return [
            "EQP",
            "In",
            "Out",
            "Fail",
            "Fail PPM",
            "Yield"
        ]

    ###LAY DANH SACH NGAY CHO BO LOC NGAY
    def get_dates_in_range(
            self,
            date_from,
            date_to
    ):

        cursor = self.conn.cursor()

        cursor.execute(
            """
            SELECT DISTINCT File_Date
            FROM data
            WHERE File_Date BETWEEN ? AND ?
            ORDER BY File_Date
            """,
            (
                date_from,
                date_to
            )
        )

        return [
            row[0]
            for row in cursor.fetchall()
        ]

    ###########LAY DU LIEU CHO SLOT

    def get_slot_summary(
            self,
            eqp,
            handler,
            zone,
            date_from=None,
            date_to=None,
            file_date=None
    ):

        cursor = self.conn.cursor()

        sql = """
              SELECT SLOT, \
                     COALESCE( \
                             SUM(CAST(Qty AS INTEGER)), \
                             0 \
                     ) AS qty, \
                     COALESCE( \
                             SUM(CAST(Fail AS INTEGER)), \
                             0 \
                     ) AS fail
              FROM data
              WHERE EQP = ?
                AND Handler = ?
                AND ZONE = ? \
              """

        params = [
            eqp,
            handler,
            zone
        ]

        # ===== Day =====

        if file_date:

            sql += """
                AND File_Date = ?
            """

            params.append(
                file_date
            )

        # ===== Month =====

        else:

            sql += """
                AND File_Date BETWEEN ? AND ?
            """

            params.extend(
                [
                    date_from,
                    date_to
                ]
            )

        sql += """
            GROUP BY SLOT
            ORDER BY CAST(SLOT AS INTEGER)
        """

        cursor.execute(
            sql,
            params
        )

        result = {}

        for slot, qty, fail in cursor.fetchall():
            qty = int(qty or 0)

            fail = int(fail or 0)

            passed = qty - fail

            yield_rate = (
                round(
                    passed * 100 / qty,
                    2
                )
                if qty > 0
                else 0
            )

            ppm = (
                round(
                    fail * 1000000 / qty,
                    0
                )
                if qty > 0
                else 0
            )

            result[int(slot)] = {
                "qty": qty,
                "pass": passed,
                "fail": fail,
                "yield": yield_rate,
                "ppm": int(ppm)
            }

        return result

    def get_slot_table_data(
            self,
            eqp,
            handler,
            zone,
            date_from=None,
            date_to=None,
            file_date=None
    ):

        slot_data = self.get_slot_summary(
            eqp=eqp,
            handler=handler,
            zone=zone,
            date_from=date_from,
            date_to=date_to,
            file_date=file_date
        )

        in_row = ["In"]

        pass_row = ["PASS"]

        fail_row = ["Prime FAIL"]

        yield_row = ["Prime Yield"]

        ppm_row = ["Fail PPM"]

        for slot in range(1, 49):

            data = slot_data.get(slot)

            if not data:
                in_row.append("")
                pass_row.append("")
                fail_row.append("")
                yield_row.append("")
                ppm_row.append("")

                continue

            in_row.append(
                data["qty"]
            )

            pass_row.append(
                data["pass"]
            )

            fail_row.append(
                data["fail"]
                if data["fail"] > 0
                else ""
            )

            yield_row.append(
                f'{data["yield"]:.2f}%'
            )

            ppm_row.append(
                data["ppm"]
                if data["ppm"] > 0
                else ""
            )

        return [
            in_row,
            pass_row,
            fail_row,
            yield_row,
            ppm_row
        ]

    def get_slot_headers(self):

        return (
                ["Slot"]
                +
                [
                    str(i)
                    for i in range(1, 49)
                ]
        )

    ###VE BIEU DO SLOT ON MONTH
    def get_slot_chart_data(
            self,
            eqp,
            handler,
            zone,
            date_from=None,
            date_to=None,
            file_date=None
    ):

        slot_data = self.get_slot_summary(
            eqp=eqp,
            handler=handler,
            zone=zone,
            date_from=date_from,
            date_to=date_to,
            file_date=file_date
        )

        slots = list(
            range(1, 49)
        )

        fails = []

        yields = []

        for slot in slots:

            data = slot_data.get(slot)

            if data:

                fails.append(
                    data["fail"]
                )

                yields.append(
                    data["yield"]
                )

            else:

                fails.append(0)

                yields.append(None)

        return (
            slots,
            fails,
            yields
        )

    ###LAY DU LIEU TUNG 1 SLOT TUNG NGAY TRONG CA THANG
    def get_slot_daily_summary(
            self,
            eqp,
            handler,
            zone,
            slot,
            date_from,
            date_to
    ):

        cursor = self.conn.cursor()

        error_codes = self.get_scrap_codes()

        daily_summary = {}

        # ======================================
        # Query 1
        # Input / Fail theo ngày
        # ======================================

        cursor.execute(
            """
            SELECT File_Date,
                   COALESCE(
                           SUM(CAST(Qty AS INTEGER)),
                           0
                   ) AS qty,
                   COALESCE(
                           SUM(CAST(Fail AS INTEGER)),
                           0
                   ) AS fail
            FROM data
            WHERE EQP = ?
              AND Handler = ?
              AND ZONE = ?
              AND SLOT = ?
              AND File_Date BETWEEN ?
              AND ?
            GROUP BY File_Date
            ORDER BY File_Date
            """,
            (
                eqp,
                handler,
                zone,
                str(slot),
                date_from,
                date_to
            )
        )

        for file_date, qty, fail in cursor.fetchall():
            daily_summary[file_date] = {
                "qty": int(qty or 0),
                "fail": int(fail or 0),
                "codes": {
                    code: 0
                    for code in error_codes
                }
            }

        # ======================================
        # Query 2
        # Đếm Scrap thực tế
        # ======================================

        cursor.execute(
            """
            SELECT File_Date,
                   SCRAP
            FROM data
            WHERE EQP = ?
              AND Handler = ?
              AND ZONE = ?
              AND SLOT = ?
              AND File_Date BETWEEN ?
              AND ?
              AND SCRAP IS NOT NULL
              AND SCRAP != ''
              AND SCRAP != '-'
            """,
            (
                eqp,
                handler,
                zone,
                str(slot),
                date_from,
                date_to
            )
        )

        for file_date, scrap_text in cursor:

            if file_date not in daily_summary:
                continue

            scrap_text = str(scrap_text).strip()

            for item in scrap_text.split(","):

                item = item.strip()

                if not item:
                    continue

                code = item.split(":")[0].strip()

                if code == "0":
                    code = "0000"

                if code in daily_summary[file_date]["codes"]:
                    daily_summary[file_date]["codes"][code] += 1

        # ======================================
        # Build table
        # ======================================

        result = []

        total_in = 0
        total_fail = 0

        for file_date in sorted(daily_summary.keys()):

            qty = daily_summary[file_date]["qty"]

            fail = daily_summary[file_date]["fail"]

            out = qty - fail

            total_in += qty
            total_fail += fail

            yield_rate = (
                round(
                    out * 100 / qty,
                    2
                )
                if qty > 0
                else 0
            )

            row = [
                file_date,
                qty,
                out,
                fail
            ]

            for code in error_codes:
                count = (
                    daily_summary[file_date]["codes"][code]
                )

                row.append(
                    count if count > 0 else ""
                )

            row.append(
                f"{yield_rate:.2f}%"
            )

            result.append(row)

        total_out = total_in - total_fail

        total_yield = (
            round(
                total_out * 100 / total_in,
                2
            )
            if total_in > 0
            else 0
        )

        return (
            result,
            total_fail,
            total_yield
        )

    def get_slot_daily_headers(self):

        return (
                [
                    "Date",
                    "Input",
                    "Output",
                    "Prime Fail"
                ]
                +
                self.get_scrap_codes()
                +
                [
                    "Prime Yield"
                ]
        )

    ###LAY DU LIEU VE BIEU DO CHO 1 SLOT TRONG THANG
    def get_slot_daily_chart_data(
            self,
            eqp,
            handler,
            zone,
            slot,
            date_from,
            date_to,
            selected_scraps
    ):

        data, _, _ = self.get_slot_daily_summary(
            eqp,
            handler,
            zone,
            slot,
            date_from,
            date_to
        )

        dates = []

        yields = []

        scrap_series = {
            code: []
            for code in selected_scraps
        }

        for row in data:

            dates.append(row[0])

            yields.append(
                float(
                    str(row[-1]).replace("%", "")
                )
            )

            for code in selected_scraps:
                idx = self.get_slot_daily_headers().index(
                    code
                )

                value = row[idx]

                scrap_series[code].append(
                    int(value)
                    if str(value).strip() != ""
                    else 0
                )

        return (
            dates,
            yields,
            scrap_series
        )

    ###BANG THONG KE SO LUONG MA LOI HANG NGAY CUA TAT CA CAC THIET BI TRONG MOT THANG
    def get_yield_fail_daily_headers(self):

        scrap_codes = self.get_scrap_codes()

        return (
                [
                    "Date",
                    "Input",
                    "Output",
                    "Prime Fail"
                ]
                +
                scrap_codes
                +
                [
                    "Prime Yield"
                ]
        )

    def get_yield_fail_daily_data(
            self,
            date_from,
            date_to
    ):

        cursor = self.conn.cursor()

        # =====================================
        # Tổng Qty / Fail theo ngày
        # =====================================

        cursor.execute(
            """
            SELECT File_Date,
                   SUM(CAST(Qty AS INTEGER))  AS qty,
                   SUM(CAST(Fail AS INTEGER)) AS fail
            FROM data
            WHERE File_Date BETWEEN ? AND ?
            GROUP BY File_Date
            ORDER BY File_Date
            """,
            (
                date_from,
                date_to
            )
        )

        daily_rows = cursor.fetchall()

        # =====================================
        # Danh sách mã lỗi
        # =====================================

        scrap_codes = self.get_scrap_codes()

        # =====================================
        # Đếm số lần xuất hiện mã lỗi thực tế
        # =====================================

        cursor.execute(
            """
            SELECT File_Date,
                   SCRAP
            FROM data
            WHERE File_Date BETWEEN ? AND ?
              AND SCRAP IS NOT NULL
              AND TRIM(SCRAP) <> ''
              AND SCRAP <> '-'
            """,
            (
                date_from,
                date_to
            )
        )

        scrap_map = {}

        for file_date, scrap_text in cursor.fetchall():

            if file_date not in scrap_map:
                scrap_map[file_date] = {
                    code: 0
                    for code in scrap_codes
                }

            scrap_text = str(scrap_text).strip()

            for item in scrap_text.split(","):

                item = item.strip()

                if not item:
                    continue

                code = item.split(":")[0].strip()

                if code == "0":
                    code = "0000"

                if code in scrap_map[file_date]:
                    scrap_map[file_date][code] += 1

        # =====================================
        # Build table
        # =====================================

        table_data = []

        total_fail = 0

        scrap_totals = {
            code: 0
            for code in scrap_codes
        }

        total_input = 0

        total_output = 0

        for file_date, qty, fail in daily_rows:

            qty = int(qty or 0)

            fail = int(fail or 0)

            output = qty - fail

            yield_rate = (
                round(
                    output * 100 / qty,
                    2
                )
                if qty > 0
                else 0
            )

            row = [
                datetime.strptime(
                    file_date,
                    "%Y%m%d"
                ).strftime("%d/%m"),
                qty,
                output,
                fail
            ]

            for code in scrap_codes:
                value = (
                    scrap_map
                    .get(file_date, {})
                    .get(code, 0)
                )

                row.append(
                    value if value > 0 else ""
                )

                scrap_totals[code] += value

            row.append(
                f"{yield_rate:.2f}%"
            )

            table_data.append(
                row
            )

            total_fail += fail

            total_input += qty

            total_output += output

        # =====================================
        # Total Row
        # =====================================

        total_row = [
            "",
            "",
            "",
            "Total Fail"
        ]

        for code in scrap_codes:
            value = scrap_totals[code]

            total_row.append(
                value if value > 0 else ""
            )

        total_row.append("")

        table_data.append(
            total_row
        )

        # =====================================
        # Total Yield
        # =====================================

        total_yield = (
            round(
                total_output * 100 / total_input,
                2
            )
            if total_input > 0
            else 0
        )

        return (
            table_data,
            total_fail,
            total_yield
        )

    def get_yield_fail_daily_chart_data(
            self,
            date_from,
            date_to,
            selected_scraps
    ):

        cursor = self.conn.cursor()

        daily_data = {}

        cursor.execute(
            """
            SELECT File_Date,
                   SUM(CAST(Qty AS INTEGER)),
                   SUM(CAST(Fail AS INTEGER))
            FROM data
            WHERE File_Date BETWEEN ? AND ?
            GROUP BY File_Date
            ORDER BY File_Date
            """,
            (
                date_from,
                date_to
            )
        )

        for file_date, qty, fail in cursor.fetchall():
            qty = int(qty or 0)

            fail = int(fail or 0)

            output = qty - fail

            yield_rate = (
                round(
                    output * 100 / qty,
                    2
                )
                if qty > 0
                else 0
            )

            daily_data[file_date] = {
                "yield": yield_rate,
                "codes": {}
            }

        cursor.execute(
            """
            SELECT File_Date,
                   SCRAP
            FROM data
            WHERE File_Date BETWEEN ? AND ?
              AND SCRAP IS NOT NULL
              AND SCRAP <> ''
              AND SCRAP <> '-'
            """,
            (
                date_from,
                date_to
            )
        )

        for file_date, scrap_text in cursor.fetchall():

            if file_date not in daily_data:
                continue

            for item in str(scrap_text).split(","):

                item = item.strip()

                if not item:
                    continue

                code = item.split(":")[0].strip()

                if code == "0":
                    code = "0000"

                if code not in selected_scraps:
                    continue

                daily_data[file_date]["codes"][code] = (
                        daily_data[file_date]["codes"].get(
                            code,
                            0
                        ) + 1
                )

        dates = []

        yields = []

        scrap_series = {
            code: []
            for code in selected_scraps
        }

        for file_date in sorted(daily_data.keys()):

            dates.append(
                datetime.strptime(
                    file_date,
                    "%Y%m%d"
                ).strftime("%d/%m")
            )

            yields.append(
                daily_data[file_date]["yield"]
            )

            for code in selected_scraps:
                scrap_series[code].append(
                    daily_data[file_date]["codes"].get(
                        code,
                        0
                    )
                )

        return (
            dates,
            yields,
            scrap_series
        )
    #####TABLE THONG KE TUNG MA SAN PHAM TREN TUNG THIET BI
    def get_model_daily_summary(
            self,
            model,
            date_from,
            date_to,
            eqp=None,
            handler=None,
            zone=None,
            slot=None
    ):

        cursor = self.conn.cursor()

        scrap_codes = self.get_scrap_codes()

        daily_summary = {}

        # =====================================
        # Build WHERE
        # =====================================

        where_clause = [
            "Model = ?",
            "File_Date BETWEEN ? AND ?"
        ]

        params = [
            model,
            date_from,
            date_to
        ]

        if (
                eqp
                and eqp != "Chọn EQP"
        ):
            where_clause.append(
                "EQP = ?"
            )
            params.append(eqp)

        if (
                handler
                and handler != "Chọn Handler"
        ):
            where_clause.append(
                "Handler = ?"
            )
            params.append(handler)

        if (
                zone
                and zone != "Chọn Zone"
        ):
            where_clause.append(
                "ZONE = ?"
            )
            params.append(zone)

        if (
                slot
                and slot != "Chọn Slot"
        ):
            where_clause.append(
                "SLOT = ?"
            )
            params.append(str(slot))

        where_sql = " AND ".join(
            where_clause
        )

        # =====================================
        # Query Qty / Fail
        # =====================================

        cursor.execute(
            f"""
            SELECT File_Date,
                   COALESCE(
                       SUM(CAST(Qty AS INTEGER)),
                       0
                   ) AS qty,
                   COALESCE(
                       SUM(CAST(Fail AS INTEGER)),
                       0
                   ) AS fail
            FROM data
            WHERE {where_sql}
            GROUP BY File_Date
            ORDER BY File_Date
            """,
            params
        )

        for file_date, qty, fail in cursor.fetchall():
            daily_summary[file_date] = {
                "qty": int(qty or 0),
                "fail": int(fail or 0),
                "codes": {
                    code: 0
                    for code in scrap_codes
                }
            }

        # =====================================
        # Query Scrap
        # =====================================

        cursor.execute(
            f"""
            SELECT File_Date,
                   SCRAP
            FROM data
            WHERE {where_sql}
              AND SCRAP IS NOT NULL
              AND TRIM(SCRAP) <> ''
              AND SCRAP <> '-'
            """,
            params
        )

        for file_date, scrap_text in cursor.fetchall():

            if file_date not in daily_summary:
                continue

            scrap_text = str(
                scrap_text
            ).strip()

            for item in scrap_text.split(","):

                item = item.strip()

                if not item:
                    continue

                code = item.split(":")[0].strip()

                if code == "0":
                    code = "0000"

                if code in daily_summary[file_date]["codes"]:
                    daily_summary[file_date]["codes"][code] += 1

        # =====================================
        # Build Result
        # =====================================

        result = []

        total_in = 0
        total_fail = 0
        scrap_totals = {
            code: 0
            for code in scrap_codes
        }

        total_output = 0

        for file_date in sorted(
                daily_summary.keys()
        ):

            qty = daily_summary[file_date]["qty"]

            fail = daily_summary[file_date]["fail"]

            output = qty - fail

            yield_rate = (
                round(
                    output * 100 / qty,
                    2
                )
                if qty > 0
                else 0
            )

            total_in += qty
            total_fail += fail
            total_output += output

            row = [
                datetime.strptime(
                    file_date,
                    "%Y%m%d"
                ).strftime("%d/%m"),
                qty,
                output,
                fail
            ]

            for code in scrap_codes:
                count = (
                    daily_summary[file_date]
                    ["codes"][code]
                )

                scrap_totals[code] += count

                row.append(
                    count if count > 0 else ""
                )

            row.append(
                f"{yield_rate:.2f}%"
            )

            result.append(row)
        # =====================================
        # TOTAL ROW
        # =====================================

        total_row = [
            "Total",
            total_in,
            total_output,
            total_fail
        ]
        total_out = (
                total_in - total_fail
        )
        total_yield = (
            round(
                total_out * 100 / total_in,
                2
            )
            if total_in > 0
            else 0
        )

        for code in scrap_codes:
            value = scrap_totals[code]

            total_row.append(
                value if value > 0 else ""
            )

        total_row.append(
            f"{total_yield:.2f}%"
        )

        result.append(
            total_row
        )

        return (
            result,
            total_fail,
            total_yield
        )

    def get_model_daily_headers(self):

        return (
                ["Date",
                 "Input",
                 "Output",
                 "Prime Fail"]
                +
                self.get_scrap_codes()
                +
                ["Prime Yield"]
        )

    #####LAY DU LIEU VE BIEU DO CHO TUNG MODEL
    def get_model_daily_chart_data(
            self,
            model,
            date_from,
            date_to,
            eqp=None,
            handler=None,
            zone=None,
            slot=None,
            selected_scraps=None
    ):

        cursor = self.conn.cursor()

        where_clause = [
            "Model = ?",
            "File_Date BETWEEN ? AND ?"
        ]

        params = [
            model,
            date_from,
            date_to
        ]

        if eqp and eqp != "Chọn EQP":
            where_clause.append("EQP = ?")
            params.append(eqp)

        if handler and handler != "Chọn Handler":
            where_clause.append("Handler = ?")
            params.append(handler)

        if zone and zone != "Chọn Zone":
            where_clause.append("ZONE = ?")
            params.append(zone)

        if slot and slot != "Chọn Slot":
            where_clause.append("SLOT = ?")
            params.append(str(slot))

        where_sql = " AND ".join(where_clause)

        # =====================================
        # Yield theo ngày
        # =====================================

        cursor.execute(
            f"""
            SELECT File_Date,
                   SUM(CAST(Qty AS INTEGER)),
                   SUM(CAST(Fail AS INTEGER))
            FROM data
            WHERE {where_sql}
            GROUP BY File_Date
            ORDER BY File_Date
            """,
            params
        )

        date_map = {}

        for file_date, qty, fail in cursor.fetchall():
            qty = int(qty or 0)

            fail = int(fail or 0)

            output = qty - fail

            yield_rate = (
                round(output * 100 / qty, 2)
                if qty > 0
                else 0
            )

            date_map[file_date] = {
                "yield": yield_rate
            }

        # =====================================
        # Scrap Series
        # =====================================

        if not selected_scraps:
            selected_scraps = []

        scrap_series = {
            code: []
            for code in selected_scraps
        }

        scrap_count_map = {
            file_date: {
                code: 0
                for code in selected_scraps
            }
            for file_date in date_map
        }

        cursor.execute(
            f"""
            SELECT File_Date,
                   SCRAP
            FROM data
            WHERE {where_sql}
              AND SCRAP IS NOT NULL
              AND TRIM(SCRAP) <> ''
              AND SCRAP <> '-'
            """,
            params
        )

        for file_date, scrap_text in cursor.fetchall():

            if file_date not in scrap_count_map:
                continue

            for item in str(scrap_text).split(","):

                item = item.strip()

                if not item:
                    continue

                code = item.split(":")[0].strip()

                if code == "0":
                    code = "0000"

                if code in scrap_count_map[file_date]:
                    scrap_count_map[file_date][code] += 1

        # =====================================
        # Build Output
        # =====================================

        dates = []

        yields = []

        for file_date in sorted(date_map.keys()):

            dates.append(
                datetime.strptime(
                    file_date,
                    "%Y%m%d"
                ).strftime("%d/%m")
            )

            yields.append(
                date_map[file_date]["yield"]
            )

            for code in selected_scraps:
                scrap_series[code].append(
                    scrap_count_map[file_date][code]
                )

        return (
            dates,
            yields,
            scrap_series
        )


    #####============QUẢN LÝ DATABASE
    def get_date_summary(self):

        query = """
                SELECT File_Date, \
                       COUNT(*) AS Total_Lots, \
                       SUM(Qty) AS Total_Qty
                FROM data
                GROUP BY File_Date
                ORDER BY File_Date DESC \
                """

        return pd.read_sql_query(
            query,
            self.conn
        )

    def search_date_summary(
            self,
            file_date
    ):

        query = """
                SELECT File_Date, \
                       COUNT(*) AS Total_Lots, \
                       SUM(Qty) AS Total_Qty
                FROM data
                WHERE File_Date = ?
                GROUP BY File_Date \
                """

        return pd.read_sql_query(
            query,
            self.conn,
            params=[file_date]
        )

    def delete_dates(
            self,
            dates
    ):

        cursor = self.conn.cursor()

        try:

            self.conn.execute("BEGIN")

            for date in dates:
                cursor.execute(
                    """
                    DELETE
                    FROM data
                    WHERE File_Date = ?
                    """,
                    (date,)
                )

                cursor.execute(
                    """
                    DELETE
                    FROM date_master
                    WHERE File_Date = ?
                    """,
                    (date,)
                )

            self.conn.commit()

        except Exception:

            self.conn.rollback()
            raise
    ####============QUẢN LÝ NHẬP DỮ LIỆU
    def is_file_date_exists(
            self,
            file_date
    ):

        cursor = self.conn.cursor()

        cursor.execute(
            """
            SELECT 1
            FROM date_master
            WHERE File_Date = ?
            """,
            (file_date,)
        )

        return cursor.fetchone() is not None

    def insert_file_date(
            self,
            file_date
    ):

        cursor = self.conn.cursor()

        cursor.execute(
            """
            INSERT INTO date_master
            (File_Date)
            VALUES (?)
            """,
            (file_date,)
        )
