from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.ticker import AutoMinorLocator
from matplotlib.ticker import MultipleLocator
from matplotlib.ticker import FuncFormatter
import math
########BIEU DO THONG KE MA LOI TUNG NGAY TRONG THANG CUA 1 SLOT
class SlotYieldChart(
    FigureCanvasQTAgg
):

    def __init__(self):

        self.figure = Figure(
            figsize=(24, 4)
        )

        super().__init__(
            self.figure
        )
        self.setMinimumWidth(
            2500
        )

    def update_chart(
            self,
            slots,
            fails,
            yields,
            eqp,
            handler,
            zone
    ):

        self.figure.clear()

        ax1 = self.figure.add_subplot(
            111
        )

        # =========================
        # FAIL BAR
        # =========================

        max_fail = max(fails) if fails else 0

        upper = max(
            5,
            max_fail + 1
        )

        ax1.set_ylim(
            0,
            upper
        )

        ax1.yaxis.set_major_locator(
            MultipleLocator(2)
        )
        ax1.yaxis.set_minor_locator(
            AutoMinorLocator(2)
        )

        bars = ax1.bar(
            slots,
            fails,
            color="red",
            width=0.5,
            label="Prime FAIL"
        )

        ax1.set_ylabel(
            "Prime FAIL"
        )

        ax1.set_xlabel(
            "Slot"
        )

        ax1.set_xticks(
            slots
        )

        ax1.grid(
            which="major",
            axis="y",
            color="#D9D9D9",
            linewidth=0.8
        )

        ax1.grid(
            which="minor",
            axis="y",
            color="#EEEEEE",
            linewidth=0.5
        )

        ax1.set_axisbelow(True)

        for bar in bars:

            height = bar.get_height()

            ax1.text(
                bar.get_x()
                + bar.get_width() / 2,
                height + 0.2,
                str(int(height)),
                ha="center",
                fontsize=8
            )

        # =========================
        # YIELD LINE
        # =========================

        ax2 = ax1.twinx()

        ax2.plot(
            slots,
            yields,
            color="blue",
            marker="o",
            linewidth=2,
            label="Prime Yield (%)"
        )

        valid_yields = [
            y
            for y in yields
            if y is not None
        ]

        # if valid_yields:
        #     min_yield = min(valid_yields)
        #
        #     lower = math.floor(min_yield)
        #
        #     ax2.set_ylim(
        #         lower,
        #         100
        #     )
        if valid_yields:

            min_yield = min(valid_yields)

            lower = max(
                90,
                math.floor(min_yield - 1)
            )

            if lower >= 100:
                lower = 99

            ax2.set_ylim(
                lower,
                100
            )
            ax2.yaxis.set_major_locator(
                MultipleLocator(1)
            )
            ax2.yaxis.set_major_formatter(
                FuncFormatter(
                    lambda x, pos: f"{int(x)}%"
                )
            )


        ax2.set_ylabel(
            "Prime Yield (%)"
        )

        for x, y in zip(
                slots,
                yields
        ):

            if y is None:
                continue

            ax2.annotate(
                f"{y:.2f}",
                (x, y),
                textcoords="offset points",
                xytext=(0, 8),
                ha="center",
                fontsize=8
            )
        # =========================
        # LEGEND
        # =========================

        h1, l1 = ax1.get_legend_handles_labels()

        h2, l2 = ax2.get_legend_handles_labels()

        ax1.legend(
            h1 + h2,
            l1 + l2,
            loc="upper center",
            bbox_to_anchor=(0.5, 1.15),
            ncol=2
        )
        # Bỏ viền
        for ax in [ax1, ax2]:

            for spine in [
                "top",
                "bottom",
                "left",
                "right"
            ]:
                ax.spines[spine].set_visible(False)

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
        ax1.tick_params(
            axis="y",
        )

        ax2.tick_params(
            axis="y",
        )

        self.figure.tight_layout(
            rect=[
                0,
                0,
                1,
                0.90
            ]
        )

        self.draw()