"""实践 1 原油宝报告的三张图：写入 结果/。用 conda 环境 ml 运行。"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

plt.rcParams["font.sans-serif"] = ["Heiti SC", "Songti SC", "Arial Unicode MS"]
plt.rcParams["axes.unicode_minus"] = False
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "结果")
os.makedirs(OUT, exist_ok=True)


def box(ax, xy, w, h, text, fc="#f4f6fb", ec="#33415c", fs=11, weight="normal"):
    p = FancyBboxPatch(xy, w, h, boxstyle="round,pad=0.02,rounding_size=0.03",
                       fc=fc, ec=ec, lw=1.4)
    ax.add_patch(p)
    ax.text(xy[0] + w / 2, xy[1] + h / 2, text, ha="center", va="center",
            fontsize=fs, weight=weight, linespacing=1.5)


def arrow(ax, p0, p1, text="", dy=0.05, both=True):
    style = "<->" if both else "->"
    ax.add_patch(FancyArrowPatch(p0, p1, arrowstyle=style, mutation_scale=16,
                                 lw=1.4, color="#33415c"))
    if text:
        ax.text((p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2 + dy, text,
                ha="center", va="bottom", fontsize=9.5, color="#33415c",
                linespacing=1.4)


# 图 1：中行在两个市场中的角色
fig, ax = plt.subplots(figsize=(10, 4.6))
ax.set_xlim(0, 10); ax.set_ylim(0, 4.6); ax.axis("off")
box(ax, (0.2, 1.0), 2.6, 2.6, "原油宝市场\n\n原油宝客户 1…n\n（账户记载的纸原油）\n\n全额交易，无杠杆\n现金结算", fc="#eef3ff")
box(ax, (3.9, 1.3), 2.2, 2.0, "中国银行\n\n做市商：双边报价\n经纪商：按结算价平仓", fc="#fff4e0", weight="bold")
box(ax, (7.2, 1.0), 2.6, 2.6, "WTI 原油期货市场\n\n交易所 + 期货投资者\n（标准化合约）\n\n保证金交易\n可能实物交割", fc="#eaf7ee")
arrow(ax, (2.85, 2.3), (3.85, 2.3), "互为\n交易对手")
arrow(ax, (6.15, 2.3), (7.15, 2.3), "对冲\n净头寸")
ax.text(5.0, 0.55, "两个市场只通过「报价参考」和「到期结算价」相连，客户与交易所之间没有直接关系",
        ha="center", fontsize=10, color="#555")
fig.savefig(os.path.join(OUT, "fig-01-交易角色.png"), dpi=200, bbox_inches="tight")
plt.close(fig)

# 图 2：全额无杠杆的多头，账户权益随价格变化
import numpy as np
S = np.linspace(-50, 40, 400)
fig, ax = plt.subplots(figsize=(7.5, 4.6))
ax.plot(S, S, color="#c0392b", lw=2.2, label="实际账户权益 $=S$（全额、无杠杆）")
ax.plot(S, np.maximum(S, 0), color="#2c7fb8", lw=2, ls="--",
        label="客户以为的账户权益（最多亏光本金）")
ax.fill_between(S, S, 0, where=(S < 0), color="#c0392b", alpha=0.12)
ax.axhline(0, color="#888", lw=0.8); ax.axvline(0, color="#888", lw=0.8)
ax.scatter([-37.63], [-37.63], color="#c0392b", zorder=5)
ax.annotate("2020-04-20 结算价\n$-37.63$ 美元/桶\n每桶倒欠 37.63 美元",
            xy=(-37.63, -37.63), xytext=(-47, -12), fontsize=10,
            arrowprops=dict(arrowstyle="->", color="#c0392b"))
ax.text(-47, -48, "穿仓区域：权益为负，客户倒欠银行", fontsize=10, color="#c0392b")
ax.set_xlabel("原油价格 $S$（美元/桶）"); ax.set_ylabel("每桶账户权益（美元）")
ax.set_xlim(-50, 40); ax.set_ylim(-52, 40)
ax.legend(loc="upper left", fontsize=9.5, frameon=False)
ax.grid(alpha=0.25)
fig.savefig(os.path.join(OUT, "fig-02-账户权益与价格.png"), dpi=200, bbox_inches="tight")
plt.close(fig)

# 图 3：原油宝关闭与结算价产生之间的时间差（北京时间）
fig, ax = plt.subplots(figsize=(9, 2.9))
ax.set_xlim(18, 29); ax.set_ylim(0, 1); ax.axis("off")
ax.plot([18, 29], [0.5, 0.5], color="#33415c", lw=2)
ax.axvspan(22, 26.5, ymin=0.38, ymax=0.62, color="#c0392b", alpha=0.25)
for x, lab, up in [(22, "22:00\n原油宝关闭\n（美东 10:00）", True),
                   (26.47, "次日 02:28-02:30\nWTI 结算价算出\n（美东 14:28-14:30）", True)]:
    ax.plot([x, x], [0.4, 0.6], color="#33415c", lw=2)
    ax.text(x, 0.72, lab, ha="center", va="bottom", fontsize=10, linespacing=1.5)
ax.text(24.25, 0.22, "约 4.5 小时：客户无权操作，只能按结算价自动平仓",
        ha="center", fontsize=10.5, color="#c0392b", weight="bold")
for h, lab in [(18, "4/20 18:00"), (24, "4/21 00:00"), (28, "4/21 04:00")]:
    ax.text(h, 0.4, lab, ha="center", va="top", fontsize=8.5, color="#777")
fig.savefig(os.path.join(OUT, "fig-03-时间差.png"), dpi=200, bbox_inches="tight")
plt.close(fig)
print("ok")
