from matplotlib.backends.backend_qtagg import (
    FigureCanvasQTAgg as FigureCanvas
)

from matplotlib.figure import Figure

from matplotlib.ticker import MultipleLocator
from matplotlib.ticker import AutoMinorLocator
import numpy as np


class SlotDailyChart(FigureCanvas):

    def __init__(self):

        self.figure = Figure(
            figsize=(12, 5)
        )

        super().__init__(
            self.figure
        )

        # self.setMinimumWidth(
        #     2500
        # )

    def update_chart(
            self,
            dates,
            yields,
            scrap_series,
            eqp,
            handler,
            zone,
            slot
    ):

        self.figure.clear()
        # format date
        display_dates = []

        for d in dates:

            d = str(d)

            if len(d) == 8:
                display_dates.append(
                    f"{d[6:8]}/{d[4:6]}"
                )
            else:
                display_dates.append(d)

        # ====================================
        # Yield (%)
        # LEFT AXIS
        # ====================================

        ax1 = self.figure.add_subplot(
            111
        )

        # ====================================
        # Fail Qty
        # RIGHT AXIS
        # ====================================

        ax2 = ax1.twinx()

        x = np.arange(
            len(dates)
        )

        # ====================================
        # STACK BAR
        # ====================================

        bottom = np.zeros(
            len(dates)
        )

        colors = [
            "#4E79A7",
            "#F28E2B",
            "#E15759",
            "#76B7B2",
            "#59A14F",
            "#EDC948",
            "#B07AA1",
            "#FF9DA7",
            "#9C755F",
            "#BAB0AC"
        ]

        for idx, (
                scrap_code,
                values
        ) in enumerate(
            scrap_series.items()
        ):

            bars = ax2.bar(
                x,
                values,
                width=0.6,
                bottom=bottom,
                label=scrap_code,
                color=colors[
                    idx % len(colors)
                ]
            )

            # hiện số trên cột

            for bar, value in zip(
                    bars,
                    values
            ):

                if value > 0:

                    ax2.text(
                        bar.get_x()
                        + bar.get_width() / 2,
                        bar.get_y()
                        + value,
                        str(value),
                        ha="center",
                        va="bottom",
                        fontsize=7
                    )

            bottom += np.array(
                values
            )

        # ====================================
        # YIELD LINE
        # ====================================

        ax1.plot(
            x,
            yields,
            color="black",
            marker="o",
            linewidth=1.5,
            label="Prime Yield"
        )

        for xi, yi in zip(
                x,
                yields
        ):

            if yi is None:
                continue

            ax1.annotate(
                f"{yi:.2f}%",
                (
                    xi,
                    yi
                ),
                xytext=(0, 5),
                textcoords="offset points",
                ha="center",
                fontsize=7,
                color="red"
            )

        # ====================================
        # X AXIS
        # ====================================

        ax1.set_xticks(x)

        ax1.set_xticklabels(
            display_dates,
            fontsize=8
        )

        ax1.set_xlabel(
            "Date"
        )

        # ====================================
        # LEFT Y AXIS
        # Yield
        # ====================================

        ax1.set_ylabel(
            "Prime Yield (%)"
        )

        ax1.set_ylim(
            0,
            105
        )

        max_fail = max(
            bottom
        ) if len(bottom) else 0

        ax2.set_ylim(
            0,
            max_fail + 2
        )

        ax2.set_ylabel(
            "Fail Qty"
        )

        ax2.yaxis.set_major_locator(
            MultipleLocator(1)
        )

        # ====================================
        # GRID
        # ====================================

        ax1.grid(
            which="major",
            axis="y",
            color="#D9D9D9",
            linewidth=0.8
        )
        ax1.grid(
            which="minor",
            axis="y",
            color="#F2F2F2",
            linewidth=0.5
        )
        ax1.set_axisbelow(True)
        ax2.yaxis.set_minor_locator(
            AutoMinorLocator(2)
        )

        # ====================================
        # REMOVE BORDER
        # ====================================

        for ax in [ax1, ax2]:

            for spine in [
                "top",
                "bottom",
                "left",
                "right"
            ]:
                ax.spines[spine].set_visible(False)

        # ====================================
        # REMOVE TICK MARK
        # (GIỮ LẠI LABEL)
        # ====================================

        ax1.tick_params(
            axis="both",
            which="both",
            length=0
        )

        ax2.tick_params(
            axis="both",
            which="both",
            length=0
        )

        # ====================================
        # LEGEND
        # ====================================

        h1, l1 = (
            ax1.get_legend_handles_labels()
        )

        h2, l2 = (
            ax2.get_legend_handles_labels()
        )

        ax1.legend(
            h2 + h1,
            l2 + l1,
            loc="lower center",
            bbox_to_anchor=(0.5, 1.02),
            ncol=6,
            fontsize=8,
            frameon=False
        )

        # ====================================
        # NO TITLE
        # ====================================

        self.figure.tight_layout()

        self.draw()