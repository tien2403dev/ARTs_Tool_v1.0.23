from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from matplotlib.ticker import FuncFormatter

class YieldChart(FigureCanvasQTAgg):

    def __init__(self):

        self.fig = Figure(
            figsize=(10, 4)
        )

        super().__init__(self.fig)

        # self.ax = self.fig.add_subplot(111)

    def plot_data(self, data):

        self.fig.clear()

        ax1 = self.fig.add_subplot(111)

        eqps = []
        qtys = []
        ppms = []
        yields = []

        for row in data:

            if row[0] == "Total":
                continue

            eqps.append(row[0])

            qtys.append(
                float(row[1])
            )

            ppms.append(
                float(row[4])
            )

            yield_value = str(
                row[5]
            ).replace("%", "")

            yields.append(
                float(yield_value)
            )

        # =========================
        # AREA (IN)
        # =========================

        ax1.fill_between(
            eqps,
            qtys,
            alpha=0.25,
            label="In"
        )

        # Chỉ giữ grid ngang
        ax1.grid(
            axis="y",
            linestyle="--",
            alpha=0.3
        )

        # =========================
        # BAR (PPM)
        # =========================

        bars = ax1.bar(
            eqps,
            ppms,
            width=0.35,
            label="Fail PPM"
        )

        for bar in bars:

            value = bar.get_height()

            ax1.text(
                bar.get_x() + bar.get_width() / 2,
                value,
                f"{value:.1f}",
                ha="center",
                va="bottom",
                fontsize=8
            )

        # =========================
        # YIELD
        # =========================

        ax2 = ax1.twinx()

        ax2.plot(
            eqps,
            yields,
            marker="o",
            linewidth=2,
            label="Yield"
        )

        for x, y in zip(eqps, yields):

            ax2.text(
                x,
                y + 0.2,
                f"{y:.2f}%",
                ha="center",
                fontsize=9
            )

        ax2.set_ylim(
            90,
            100.5
        )
        ax2.yaxis.set_major_formatter(
            FuncFormatter(lambda x, pos: f"{x:.0f}%")
        )

        # =========================
        # REMOVE BORDER
        # =========================

        for spine in ax1.spines.values():
            spine.set_visible(False)

        for spine in ax2.spines.values():
            spine.set_visible(False)

        # =========================
        # REMOVE TICK MARKS
        # =========================

        ax1.tick_params(
            axis="both",
            length=0
        )

        ax2.tick_params(
            axis="both",
            length=0
        )

        # =========================
        # REMOVE AXIS LABEL
        # =========================

        ax2.set_ylabel("")

        # =========================
        # TITLE
        # =========================

        ax1.set_title(
            "",
            loc="left",
            fontsize=12,
            fontweight="bold"
        )

        # =========================
        # LEGEND CENTER
        # =========================

        lines1, labels1 = ax1.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()

        ax1.legend(
            lines1 + lines2,
            labels1 + labels2,
            loc="upper center",
            bbox_to_anchor=(0.5, 1.15),
            ncol=3,
            frameon=False
        )

        self.fig.tight_layout()

        self.draw()

    def clear_chart(self):

        self.fig.clear()

        self.draw()