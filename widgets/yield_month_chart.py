import numpy as np

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from matplotlib.ticker import MultipleLocator
from datetime import datetime
from matplotlib.ticker import FuncFormatter
class YieldMonthChart(FigureCanvasQTAgg):

    def __init__(self):

        self.fig = Figure(
            figsize=(12, 5)
        )

        super().__init__(self.fig)

    def plot_data(
            self,
            data,
            selected_codes,
            all_scrap_codes
    ):
        if not data:
            self.fig.clear()
            self.draw()
            return
        # print("Selected codes =", selected_codes)
        # print("All codes count =", len(all_scrap_codes))

        self.fig.clear()

        ax_ppm = self.fig.add_subplot(111)

        # ==========================
        # DATE
        # ==========================

        dates = []

        in_qty = []

        cum_yield = []

        # for row in data:
        #
        #     date_text = str(row[0])
        #
        #     day = date_text[-2:]
        #
        #     dates.append(day)
        for row in data:
            date_text = str(row[0])

            display_date = datetime.strptime(
                date_text,
                "%Y%m%d"
            ).strftime(
                "%d/%m"
            )

            dates.append(
                display_date
            )

            in_qty.append(
                int(row[1] or 0)
            )

            yield_text = str(row[4]).replace("%", "")

            cum_yield.append(
                float(yield_text)
            )
            # cum_yield.append(
            #     float(row[4] or 0)
            # )

        # ==========================
        # IN AREA
        # ==========================

        ax_in = ax_ppm
        ax_ppm.fill_between(
            dates,
            in_qty,
            alpha=0.15,
            label="In"
        )

        # ax_in.fill_between(
        #     dates,
        #     in_qty,
        #     alpha=0.15,
        #     label="In"
        # )
        ax_in.grid(
            which="minor",
            axis="y",
            color="#F2F2F2",
            linewidth=0.5
        )

        ax_in.set_yticks([])

        ax_in.spines["right"].set_visible(
            False
        )

        # ==========================
        # ERROR STACK BAR
        # ==========================

        code_to_col = {
            code: idx + 5
            for idx, code in enumerate(all_scrap_codes)
        }

        bottom = np.zeros(
            len(dates)
        )

        bar_handles = []

        for code in selected_codes:

            # print("Processing", code)

            if code not in code_to_col:
                # print("Not found:", code)
                continue

            col_index = code_to_col[code]
            # for row in data[:3]:
            #     print(row[0], row[col_index])
            #
            # print("Column =", col_index)

            values = []

            for row in data:

                value = row[col_index]

                if value == "":
                    value = 0

                values.append(
                    float(value)
                )

            bars = ax_ppm.bar(
                dates,
                values,
                bottom=bottom,
                width=0.55,
                label=code
            )

            bar_handles.append(
                bars
            )

            bottom += np.array(
                values
            )

        # ==========================
        # CUM YIELD
        # ==========================

        ax_yield = ax_ppm.twinx()

        line = ax_yield.plot(
            dates,
            cum_yield,
            marker="o",
            linewidth=2,
            label="Cum Yield (%)"
        )

        # ==========================
        # LABEL
        # ==========================

        for x, y in zip(
                dates,
                cum_yield
        ):
            ax_yield.text(
                x,
                y + 0.03,
                f"{y:.2f}%",
                ha="center",
                fontsize=8
            )

        # ==========================
        # AXIS
        # ==========================

        ax_ppm.set_ylabel(
            "PPM"
        )

        ax_yield.set_ylabel(
            "Cum Yield (%)"
        )

        ax_ppm.set_xlabel(
            "Day"
        )

        ax_ppm.grid(
            axis="y",
            alpha=0.3
        )

        # ==========================
        # YIELD RANGE
        # ==========================

        ymin = min(cum_yield)

        ymax = max(cum_yield)


        margin = (
            ymax - ymin
        ) * 0.2

        if margin == 0:
            margin = 0.5

        ax_yield.set_ylim(
            ymin - margin,
            ymax + margin
        )
        ax_yield.yaxis.set_major_formatter(
            FuncFormatter(
                lambda x, pos: f"{x:.0f}%"
            )
        )

        # ==========================
        # LEGEND
        # ==========================

        h1, l1 = ax_ppm.get_legend_handles_labels()

        h2, l2 = ax_yield.get_legend_handles_labels()

        # h3, l3 = ax_in.get_legend_handles_labels()
        ##xet chieu cao theo du lieu
        max_ppm = max(bottom) if len(bottom) else 0

        upper = (
                (int(max_ppm / 2000) + 1)
                * 2000
        )

        ax_ppm.set_ylim(
            0,
            upper
        )

        ax_ppm.yaxis.set_major_locator(
            MultipleLocator(1000)
        )

        ax_ppm.legend(
             h1 + h2,
             l1 + l2,
            loc="upper center",
            bbox_to_anchor=(0.5, 1.15),
            ncol=8,
            frameon=False
        )


        # ==========================
        # TITLE
        # ==========================

        ax_ppm.set_title(
            ""
        )
        # Bỏ viền
        for ax in [ax_ppm, ax_yield, ax_in]:
            for spine in ax.spines.values():
                spine.set_visible(False)

        # Bỏ tick
        for ax in [ax_ppm, ax_yield, ax_in]:
            ax.tick_params(axis="both", which="both", length=0)

        # Chỉ giữ grid ngang mờ
        ax_ppm.set_axisbelow(True)

        ax_ppm.grid(
            axis="y",
            which="major",
            linestyle="--",
            linewidth=0.8,
            # alpha=0.3,
            color="#D9D9D9"
        )

        ax_yield.grid(False)

        self.fig.tight_layout()

        self.draw()
