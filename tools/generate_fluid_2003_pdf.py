#!/usr/bin/env python3
"""Generate the corrected non-official fluid-mechanics answer for 2003."""

from pathlib import Path

from pdf_booklet import build_booklet


ROOT = Path(__file__).resolve().parents[1]


SECTIONS = [
    {
        "title": "大問1　Reynolds数による相似",
        "blocks": [
            ("body", "油と水模型でRe=ρVD/μを一致させます。ρo=0.8ρw、μo=40μw、Do=1 m、Dw=0.02 m、Vo=0.30 m/sです。"),
            ("formula", "Vw=(ρo/ρw)(μw/μo)(Do/Dw)Vo=0.8×(1/40)×(1/0.02)×0.30。"),
            ("answer", "最終答: Vw=0.30 m/s=30 cm/s。"),
        ],
    },
    {
        "title": "大問2　茶葉のパラドックス",
        "blocks": [
            ("body", "底面の粘着条件により、底面近くの旋回速度は上部より小さくなります。一方、半径方向圧力勾配∂p/∂r≈ρuθ²/rは流れ全体で外向きです。底面近くでは遠心力がこの圧力勾配を支えるのに不足し、内向き流れが生じます。中心で上昇し、上部で外へ戻る二次循環になります。"),
            ("answer", "最終答: 茶葉は底面中央へ集まる。底面境界層を無視して『遠心力で外へ行く』だけでは説明できません。"),
        ],
    },
    {
        "title": "大問3　糸を巻いた軽い円筒",
        "blocks": [
            ("body", "原問だけでは運動条件が足りません。糸端を空間に固定して動かさず、糸は滑らず、たるまず、円筒軸は水平、糸の質量・伸びと空気抵抗は無視すると仮定します。巻き半径r、質量M、慣性モーメントIです。"),
            ("formula", "滑りなし: a=rα。並進: Mg-T=Ma。回転: Tr=Iα。"),
            ("formula", "a=Mg/(M+I/r^2)、T=MgI/(I+Mr^2)、α=a/r。"),
            ("answer", "最終答: 重心は鉛直下向きに落ち、糸をほどきながら軸回りに回転する。薄肉中空円筒I≈Mr^2ならa≈g/2。回転方向は糸の巻き方で決まります。"),
        ],
    },
    {
        "title": "大問4　底孔からの流出",
        "blocks": [
            ("body", "非粘性、自由表面と噴流は大気圧、R≫r、出口で縮流なし、板上の水膜重量は無視します。"),
            ("formula", "(1) πR^2[-dH/dt]=πr^2v  ⇒  水面下降速度の大きさ=(r^2/R^2)v。"),
            ("formula", "(2) v^2/2=gH  ⇒  v=√(2gH)。"),
            ("body", "孔からH下の板まで自由落下するため、板直前速度VH=√(v^2+2gH)=√2 v。流量保存からAH VH=πr^2vです。"),
            ("formula", "F=ρAH VH^2=ρπr^2vVH=√2 ρπr^2v^2=2√2 ρgHπr^2。"),
            ("answer", "(3) 板が受ける力は鉛直下向きにF=2√2 ρgHπr^2。これは落下中の加速と噴流収縮を含む結果です。"),
        ],
    },
    {
        "title": "大問5　球の抵抗と終端速度",
        "blocks": [
            ("body", "同半径球の浮力をB、抵抗をkv^nとします。表のm=1 g、v=0では抵抗がゼロなので、浮力を無視すると重力と釣り合わず、表自体が矛盾します。表全体が整合する条件は共通浮力B=1 gfです。"),
            ("formula", "終端条件 mg-B=kv^n。B=1 gfなら表からm-1がvに比例するためn=1、k=1 gf/(cm/s)。"),
            ("formula", "連結球: 重量3 gf - 浮力2 gf = 抵抗2kv  ⇒  v=0.5 cm/s。"),
            ("answer", "条件付き最終答: B=1 gfなら抵抗は速度に一次比例し、連結時v=0.5 cm/s。浮力を無視する読みでは数値解は定まりません。"),
        ],
    },
    {
        "title": "大問6　二次元微小検査領域の運動量収支",
        "blocks": [
            ("body", "原問どおり、左下を(x,y)とするΔx×Δy、紙面垂直方向単位長さの固定検査領域を取ります。ρは一定、速度は(u,v)。設問が列挙しない粘性力と体積力は省きます。"),
            ("formula", "(1) 左面流入: ρu^2ΔyΔt。右面流出: ρ[u^2+∂x(u^2)Δx]ΔyΔt。"),
            ("formula", "(2) 下面流入: ρuvΔxΔt。上面流出: ρ[uv+∂y(uv)Δy]ΔxΔt。"),
            ("formula", "(3) 左面圧力: pΔy。右面圧力: -[p+(∂p/∂x)Δx]Δy。合力=-(∂p/∂x)ΔxΔy。"),
            ("formula", "(4) 保有x運動量: tでρuΔxΔy、t+Δtでρ[u+(∂u/∂t)Δt]ΔxΔy。"),
            ("body", "(5) 保有量増分=流入-流出+圧力の力積として微小極限を取ります。"),
            ("formula", "ρ[∂u/∂t+∂(u^2)/∂x+∂(uv)/∂y]=-∂p/∂x。"),
            ("answer", "連続の式∂u/∂x+∂v/∂y=0より、∂u/∂t+u∂u/∂x+v∂u/∂y=-(1/ρ)∂p/∂x。"),
            ("formula", "(6a) Strouhal数 St=L/(UTc)=fL/U。非定常慣性/対流慣性。例: 円柱後流の渦放出周波数。"),
            ("formula", "(6b) Euler数 Eu=Δp/(ρU^2)。圧力力/慣性力。例: 管路・流体機械の圧力差の相似整理。"),
            ("note", "旧PDFの大問6は別年度の一次元流管問題へ置き換わっていました。本改訂版は2003年度原本の二次元検査領域に対応しています。"),
        ],
    },
]


def main() -> None:
    output = ROOT / "pdfs/answer/2003_unofficial/2003_fluid.pdf"
    build_booklet(
        output,
        title="流体力学 2003年度 問題解説・独立再計算",
        subtitle="非公式解説。問題PDF全3ページを画像で照合し、条件不足と全6問を改訂（2026-08-31）。",
        source="pdfs/question/2003_H15_april/fluid_2003_H15_question.pdf",
        sections=SECTIONS,
    )
    print(output.relative_to(ROOT))


if __name__ == "__main__":
    main()
