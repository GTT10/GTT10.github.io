#!/usr/bin/env python3
"""Generate the corrected non-official mathematics answer for 2003."""

from pathlib import Path

from pdf_booklet import build_booklet


ROOT = Path(__file__).resolve().parents[1]


SECTIONS = [
    {
        "title": "大問1　sin x / x のTaylor展開",
        "blocks": [
            ("body", "正弦のMaclaurin展開をxで割ります。x=0は極限値1で連続に拡張します。"),
            ("formula", "sin x = x - x^3/3! + x^5/5! - x^7/7! + O(x^9)"),
            ("answer", "最終答: sin x / x = 1 - x^2/6 + x^4/120 - x^6/5040 + O(x^8)。"),
        ],
    },
    {
        "title": "大問2　シマスズキの個体数モデル",
        "blocks": [
            ("body", "t0年にp0匹を放流し、増殖数kp(t)と、個体数に依らない死滅数αからモデルを作ります。"),
            ("formula", "(1) dp/dt = kp - α、p(t0)=p0。"),
            ("formula", "(2) k≠0: p(t)=α/k + (p0-α/k) exp[k(t-t0)]。k=0: p(t)=p0-α(t-t0)。"),
            ("body", "(3) 原問は1880年の435匹が20年後に100万倍、α=0です。p0は比を取ると消えます。"),
            ("formula", "10^6 = exp(20k)  ⇒  k = ln(10^6)/20 = 0.3 ln 10。"),
            ("answer", "最終答: k ≈ 0.69 year^(-1)（有効数字2桁）。"),
        ],
    },
    {
        "title": "大問3　ベクトル関数の微分演算",
        "blocks": [
            ("body", "A=Ax i+Ay j+Az kとします。各成分は2回連続微分可能とし、混合偏微分の順序を交換できるものとします。"),
            ("formula", "(1) ∇²A=(∇²Ax)i+(∇²Ay)j+(∇²Az)k。"),
            ("formula", "∇(∇·A)=(∂x,∂y,∂z)^T (∂xAx+∂yAy+∂zAz)。"),
            ("formula", "恒等式: ∇×(∇×A)=∇(∇·A)-∇²A。"),
            ("answer", "(2) ∇×A=0なら、∇²A=∇(∇·A)。"),
        ],
    },
    {
        "title": "大問4　周期三角波のLaplace変換",
        "blocks": [
            ("body", "g(t)は周期2aで、0 <= t <= aではt/a、a < t <= 2aでは(2a-t)/aです。"),
            ("formula", "1周期積分 I = ∫[0,a](t/a)e^(-st)dt + ∫[a,2a]((2a-t)/a)e^(-st)dt = (1-e^(-as))^2/(a s^2)。"),
            ("answer", "(1) G(s)=I/(1-e^(-2as))=(1-e^(-as))/[a s^2(1+e^(-as))]=tanh(as/2)/(a s^2)、Re(s)>0。"),
            ("body", "(2) 周期aのf(t)では、[na,(n+1)a]ごとにt=na+τと置き、各積分からe^(-ans)をくくります。"),
            ("formula", "L[f]=Σ(n=0..∞) e^(-ans) ∫[0,a]f(τ)e^(-sτ)dτ = {∫[0,a]f(τ)e^(-sτ)dτ}/(1-e^(-as))。"),
            ("note", "旧PDFにあった『100万倍』の読み替えと、∇²Aを∇×Aとする誤記は採用していません。"),
        ],
    },
]


def main() -> None:
    output = ROOT / "pdfs/answer/2003_unofficial/2003_math.pdf"
    build_booklet(
        output,
        title="数学 2003年度 問題解説・独立再計算",
        subtitle="非公式解説。問題PDF本文を画像で照合し、全4問を原条件から計算し直した改訂版（2026-08-31）。",
        source="pdfs/question/2003_H15_april/math_2003_H15_question.pdf",
        sections=SECTIONS,
    )
    print(output.relative_to(ROOT))


if __name__ == "__main__":
    main()
