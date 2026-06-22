from matplotlib.backends.backend_qtagg import (
    FigureCanvasQTAgg as FigureCanvas
)

from matplotlib.figure import Figure

from matplotlib.ticker import MultipleLocator
from matplotlib.ticker import AutoMinorLocator
import numpy as np


class ModelDailyChart(FigureCanvas):

    def __init__(self):

        self.figure = Figure(
            figsize=(12, 6)
        )

        super().__init__(
            self.figure
        )

    def update_chart(
            self,
            dates,
            yields,
            scrap_series
    ):

        self.figure.clear()

        ax1 = self.figure.add_subplot(
            111
        )

        ax2 = ax1.twinx()

        x = np.arange(
            len(dates)
        )

        bottom = np.zeros(
            len(dates)
        )

        colors = [
            "#4E79A7",
            "#F28E2B",
            "#59A14F",
            "#E15759",
            "#B07AA1",
            "#76B7B2",
            "#EDC948",
            "#9C755F",
            "#FF9DA7",
            "#BAB0AC"
        ]

        for idx, (
                scrap_code,
                values
        ) in enumerate(
            scrap_series.items()
        ):

            bars = ax1.bar(
                x,
                values,
                width=0.55,
                bottom=bottom,
                label=scrap_code,
                color=colors[
                    idx % len(colors)
                ]
            )

            for bar, value in zip(
                    bars,
                    values
            ):

                if value <= 0:
                    continue

                ax1.text(
                    bar.get_x()
                    + bar.get_width() / 2,
                    bar.get_y()
                    + value / 2,
                    str(value),
                    ha="center",
                    va="center",
                    fontsize=7,
                    color="white"
                )

            bottom += np.array(values)

        # =======================
        # Yield Line
        # =======================

        ax2.plot(
            x,
            yields,
            color="gray",
            linewidth=1.5,
            marker="o",
            markersize=3,
            label="Prime Yield"
        )

        for xi, yi in zip(
                x,
                yields
        ):

            ax2.annotate(
                f"{yi:.2f}%",
                (
                    xi,
                    yi
                ),
                textcoords="offset points",
                xytext=(0, 8),
                ha="center",
                fontsize=7,
                color="red"
            )

        # =======================
        # X Axis
        # =======================

        ax1.set_xticks(x)

        ax1.set_xticklabels(
            dates,
            fontsize=7
        )

        # =======================
        # Left Axis
        # =======================

        max_fail = max(bottom) if len(bottom) else 0

        ax1.set_ylim(
            0,
            max(
                1,
                max_fail * 1.1
            )
        )

        ax1.set_ylabel(
            "Fail Qty"
        )

        ax1.yaxis.set_major_locator(
            MultipleLocator(
                max(
                    1,
                    int(max_fail / 10)
                )
            )
        )

        # =======================
        # Right Axis
        # =======================

        valid_yields = [
            y
            for y in yields
            if y is not None
        ]

        if valid_yields:

            min_yield = min(valid_yields)

            lower = max(
                95,
                min_yield - 1
            )

            if lower >= 100:
                lower = 99

            ax2.set_ylim(
                lower,
                100
            )

        ax2.set_ylabel(
            "Prime Yield (%)"
        )

        # =======================
        # Grid
        # =======================

        # ax1.grid(
        #     axis="y",
        #     linestyle="-",
        #     linewidth=0.5,
        #     alpha=0.25
        # )
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

        ax1.set_axisbelow(
            True
        )

        # =======================
        # Border
        # =======================

        for spine in [
            "top",
            "left",
            "right",
            "bottom"
        ]:
            ax1.spines[
                spine
            ].set_visible(False)

        for spine in [
            "top",
            "left",
            "right",
            "bottom"
        ]:
            ax2.spines[
                spine
            ].set_visible(False)

        ax1.tick_params(
            axis="both",
            length=0
        )

        ax2.tick_params(
            axis="both",
            length=0
        )

        # =======================
        # Legend
        # =======================

        h1, l1 = ax1.get_legend_handles_labels()

        h2, l2 = ax2.get_legend_handles_labels()

        ax1.legend(
            h1 + h2,
            l1 + l2,
            loc="upper center",
            bbox_to_anchor=(0.5, 1.18),
            ncol=min(
                len(l1) + 1,
                12
            ),
            fontsize=8,
            frameon=False
        )

        self.figure.tight_layout(
            rect=[0, 0, 1, 0.88]
        )

        self.draw()