from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from matplotlib.ticker import FuncFormatter


class HandlerZoneChart(FigureCanvasQTAgg):

    def __init__(self):

        self.fig = Figure(
            figsize=(5, 3),
            dpi=100
        )

        super().__init__(self.fig)

        self.ax1 = self.fig.add_subplot(111)
        self.ax2 = self.ax1.twinx()

        self.fig.subplots_adjust(
            left=0.08,
            right=0.92,
            top=0.85,
            bottom=0.18
        )

    def clear_chart(self):

        self.ax1.clear()
        self.ax2.clear()

        self.draw()

    def plot_data(
            self,
            monthly_data,
            title=""
    ):

        self.ax1.clear()
        self.ax2.clear()

        if not monthly_data:
            self.draw()
            return

        zones = []
        qtys = []
        fails = []
        yields = []

        for row in monthly_data:

            zones.append(row[0])

            qtys.append(
                int(row[1] or 0)
            )

            fails.append(
                int(row[3] or 0)
            )

            yields.append(
                float(
                    str(row[4]).replace(
                        "%",
                        ""
                    )
                )
            )

        # ==================================
        # FAIL BAR
        # ==================================

        bars = self.ax1.bar(
            zones,
            fails,
            width=0.45,
            color="tomato",
            label="Fail"
        )

        # ==================================
        # IN AREA
        # ==================================

        self.ax1.fill_between(
            zones,
            qtys,
            alpha=0.35,
            color="#AFC6D9",
            edgecolor="#6B9CC8",
            linewidth=1.2,
            label="In"
        )

        # ==================================
        # YIELD LINE
        # ==================================

        self.ax2.plot(
            zones,
            yields,
            marker="o",
            linewidth=2.5,
            color="green",
            label="Yield"
        )

        # ==================================
        # LABEL FAIL
        # ==================================

        for bar in bars:

            height = bar.get_height()

            self.ax1.annotate(
                f"{int(height)}",
                (
                    bar.get_x() + bar.get_width() / 2,
                    height
                ),
                textcoords="offset points",
                xytext=(0, 3),
                ha="center",
                fontsize=8
            )

        # ==================================
        # LABEL YIELD
        # ==================================

        for x, y in zip(
                zones,
                yields
        ):

            self.ax2.annotate(
                f"{y:.2f}%",
                (x, y),
                textcoords="offset points",
                xytext=(0, 8),
                ha="center",
                fontsize=8,
                color="green"
            )

        # ==================================
        # SCALE QTY
        # ==================================

        max_qty = max(qtys) if qtys else 0

        if max_qty == 0:

            self.ax1.set_ylim(
                0,
                1
            )

        else:

            self.ax1.set_ylim(
                0,
                max_qty * 1.15
            )

        # ==================================
        # SCALE YIELD
        # ==================================

        min_yield = min(yields)

        if min_yield < 95:

            self.ax2.set_ylim(
                int(min_yield),
                100
            )

        else:

            self.ax2.set_ylim(
                95,
                100
            )

        self.ax2.yaxis.set_major_formatter(
            FuncFormatter(
                lambda x, pos: f"{x:.0f}%"
            )
        )

        # ==================================
        # TITLE
        # ==================================

        self.ax1.set_title(
            title,
            fontsize=11,
            fontweight="bold"
        )

        self.ax1.set_ylabel("")
        self.ax2.set_ylabel("")

        # ==================================
        # GRID
        # ==================================

        self.ax1.grid(
            axis="y",
            linestyle="--",
            linewidth=0.8,
            alpha=0.35,
            color="#C8C8C8"
        )

        self.ax1.set_axisbelow(True)

        # ==================================
        # REMOVE BORDER
        # ==================================

        for ax in [self.ax1, self.ax2]:

            ax.spines["top"].set_visible(False)
            ax.spines["left"].set_visible(False)
            ax.spines["right"].set_visible(False)
            ax.spines["bottom"].set_visible(False)

        # ==================================
        # REMOVE TICKS
        # ==================================

        self.ax1.tick_params(
            axis="both",
            which="both",
            length=0
        )

        self.ax2.tick_params(
            axis="both",
            which="both",
            length=0
        )

        # ==================================
        # LEGEND
        # ==================================

        h1, l1 = self.ax1.get_legend_handles_labels()
        h2, l2 = self.ax2.get_legend_handles_labels()

        self.ax1.legend(
            h1 + h2,
            l1 + l2,
            loc="upper center",
            bbox_to_anchor=(0.5, 1.20),
            ncol=3,
            frameon=False
        )

        self.draw()