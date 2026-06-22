import pandas as pd

def load_excel_files(
    files,
    progress_callback=None
):

    all_data = []

    for idx, excel_file in enumerate(files):

        # df = pd.read_excel(
        #     excel_file,
        #     dtype=str,
        #     usecols=[
        #         "File_Date",
        #         "EQPID",
        #         "LOTID",
        #         "ZONE",
        #         "SLOT",
        #         "FULLSITE",
        #         "BIN",
        #         "SCRAP",
        #         "QTY",
        #         "BCODE"
        #     ]
        # )
        ##doc them cot date
        df = pd.read_excel(
            excel_file,
            dtype=str,
            usecols=[
                "File_Date",
                "Date",  # thêm
                "EQPID",
                "LOTID",
                "ZONE",
                "SLOT",
                "FULLSITE",
                "BIN",
                "SCRAP",
                "QTY",
                "BCODE"
            ]
        )

        if "SCRAP" in df.columns:

            def fix_scrap(value):

                if pd.isna(value):
                    return ""

                value = str(value)

                if "day" not in value.lower():
                    return value

                try:

                    day_part, time_part = value.split(",")

                    days = int(
                        day_part.split()[0]
                    )

                    hours = int(
                        time_part.strip().split(":")[0]
                    )

                    return str(
                        days * 24 + hours
                    )

                except Exception:

                    return value

            df["SCRAP"] = (
                df["SCRAP"]
                .apply(fix_scrap)
            )
            df["Time"] = (
                df["Date"]
                .fillna("")
                .astype(str)
                .str.extract(
                    r"\d+-(\d{2}:\d{2}:\d{2})"
                )
            )
        df["Datetime"] = pd.to_datetime(
            df["File_Date"].astype(str)
            + " "
            + df["Time"].astype(str),
            format="%Y%m%d %H:%M:%S",
            errors="coerce"
        )
        df["Datetime"] = (
            df["Datetime"]
            .dt.strftime("%Y-%m-%d %H:%M:%S")
        )

        df["Fail"] = (
            df["BIN"]
            .fillna("")
            .astype(str)
            .str.count("[2-9]")
        )

        df["Handler"] = (
            df["EQPID"]
            .fillna("")
            .astype(str)
            .str[-1]
        )

        df["EQP"] = (
            df["EQPID"]
            .fillna("")
            .astype(str)
            .str[:-1]
        )

        df["Model"] = (
            df["BCODE"]
            .fillna("")
            .astype(str)
            .str.slice(12, 17)
        )

        all_data.append(df)

        if progress_callback:

            percent = int(
                ((idx + 1) / len(files))
                * 100
            )

            progress_callback(percent)

    result = pd.concat(
        all_data,
        ignore_index=True
    )

    print(
        "TOTAL ROWS:",
        len(result)
        # print(result)
    )

    return result