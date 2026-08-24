"""Generate unofficial, independently recalculated thermodynamics answers for 2003-2008.

The source question PDFs are not modified.  This script is intentionally data-driven so
that the derivation text in the generated PDFs can be audited against the corresponding
HTML pages and the audit report.
"""

from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
)


ROOT = Path(__file__).resolve().parents[1]
FONT_PATH = Path(r"C:\Windows\Fonts\yumin.ttf")
if not FONT_PATH.exists():
    raise FileNotFoundError(f"Japanese font not found: {FONT_PATH}")
pdfmetrics.registerFont(TTFont("YuMincho", str(FONT_PATH)))


def para(text: str, style: ParagraphStyle) -> Paragraph:
    """Make a Japanese-safe paragraph; formulas are kept as readable plain text."""
    return Paragraph(escape(text).replace("\n", "<br/>") , style)


styles = getSampleStyleSheet()
TITLE = ParagraphStyle(
    "TitleJP", parent=styles["Title"], fontName="YuMincho", fontSize=17,
    leading=23, alignment=TA_CENTER, spaceAfter=5 * mm,
)
SUBTITLE = ParagraphStyle(
    "SubtitleJP", parent=styles["Normal"], fontName="YuMincho", fontSize=9,
    leading=13, alignment=TA_CENTER, textColor="#444444", spaceAfter=4 * mm,
)
H1 = ParagraphStyle(
    "H1JP", parent=styles["Heading1"], fontName="YuMincho", fontSize=13,
    leading=17, spaceBefore=5 * mm, spaceAfter=2 * mm, textColor="#17365d",
)
H2 = ParagraphStyle(
    "H2JP", parent=styles["Heading2"], fontName="YuMincho", fontSize=10.5,
    leading=15, spaceBefore=3 * mm, spaceAfter=1.5 * mm, textColor="#244062",
)
BODY = ParagraphStyle(
    "BodyJP", parent=styles["BodyText"], fontName="YuMincho", fontSize=9.2,
    leading=14, alignment=TA_LEFT, wordWrap="CJK", spaceAfter=1.8 * mm,
)
NOTE = ParagraphStyle(
    "NoteJP", parent=BODY, fontSize=8.2, leading=12, textColor="#555555",
    leftIndent=4 * mm, rightIndent=2 * mm,
)
FORMULA = ParagraphStyle(
    "FormulaJP", parent=BODY, fontSize=9, leading=14, leftIndent=6 * mm,
    rightIndent=3 * mm, backColor="#f4f7fb", borderPadding=2 * mm,
    spaceBefore=1 * mm, spaceAfter=2 * mm,
)


def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("YuMincho", 7.5)
    canvas.setFillColorRGB(0.35, 0.35, 0.35)
    canvas.drawString(18 * mm, 10 * mm, "非公式解説 - 問題原本からの独立再計算")
    canvas.drawRightString(192 * mm, 10 * mm, f"{doc.page}")
    canvas.restoreState()


def build_pdf(year: str, era: str, source_name: str, sections: list[dict]) -> Path:
    out_dir = ROOT / "pdfs" / "answer" / f"{year}_unofficial"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"thermo_{year}_{era}_answer.pdf"
    doc = SimpleDocTemplate(
        str(out_path), pagesize=A4, leftMargin=17 * mm, rightMargin=17 * mm,
        topMargin=15 * mm, bottomMargin=17 * mm, title=f"熱力学 {year} 非公式解説",
        author="GTT10.github.io academic audit",
    )
    story = [
        para(f"熱力学 {year}年度 問題解説・独立再計算", TITLE),
        para("非公式解説。問題PDFを読み取り、全大問・全小問を原本から独立に検算した記録です。公式解答ではありません。", SUBTITLE),
        para(f"問題原本: pdfs/question/{source_name}", NOTE),
        para("符号は、特記しない限り熱量を系への流入正、仕事を気体が外部へした仕事正とします。図は原本の状態番号・矢印を文章で再現しています。", NOTE),
        Spacer(1, 2 * mm),
    ]
    for section in sections:
        story.append(para(section["title"], H1))
        for block in section["blocks"]:
            kind = block[0]
            text = block[1]
            if kind == "h2":
                story.append(para(text, H2))
            elif kind == "formula":
                story.append(para(text, FORMULA))
            elif kind == "note":
                story.append(para(text, NOTE))
            else:
                story.append(para(text, BODY))
    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    return out_path


COMMON = {
    "2003": {
        "era": "H15_april",
        "source": "2003_H15_april/thermo_2003_H15_question.pdf",
        "sections": [
            {
                "title": "第1問 - 逆カルノー型冷凍機",
                "blocks": [
                    ("body", "仮定: 理想気体、1→2と3→4は可逆断熱、2→3は高温THでの等温圧縮、4→1は低温TLでの等温膨張です。矢印は冷凍機として1→2→3→4→1、4→1でQ1を吸収、2→3でQ2を放出します。P-V図では二つの等温線を断熱線が結び、T-S図では等温過程が水平線、可逆断熱過程が鉛直線になります。"),
                    ("h2", "(1) 状態図と熱の向き"),
                    ("body", "P-V図では低温等温線上の4→1が膨張、高温等温線上の2→3が圧縮です。T-S図では1→2と3→4が断熱、4→1の面積がQ1、2→3の面積がQ2の大きさです。熱量はT-S図でQ=∫T dSに対応します。"),
                    ("h2", "(2) 成績係数"),
                    ("formula", "第一法則より W_in = Q2 - Q1。可逆性より Q2/TH = Q1/TL。したがって COP_R = Q1/W_in = TL/(TH - TL)。"),
                    ("h2", "(3)(4) 断熱が不可逆の場合"),
                    ("body", "不可逆断熱では熱交換がなくてもエントロピー生成があるため、断熱区間はT-S図で右向きにずれます。具体的な曲線は摩擦などの散逸モデルがないと一意に決まりません。エントロピー収支は Q2/TH - Q1/TL = S_gen >= 0 であり、可逆時よりCOPは低下します。Q1とQ2は各等温線区間の下の面積として示します。"),
                ],
            },
            {
                "title": "第2問 - ノズル・絞りとJoule-Thomson効果",
                "blocks": [
                    ("body", "図の制御体積は定常流れ、質量流量m、入口出口の速度w1,w2、圧力P、温度T、比体積v、エンタルピーhを持ち、QLは外部へ失う熱量の大きさです。位置エネルギーは無視します。"),
                    ("h2", "エネルギー収支"),
                    ("formula", "m(h1 + w1^2/2) = m(h2 + w2^2/2) + QL。熱損失も速度差も無視できる絞りでは h1 = h2。"),
                    ("h2", "(1) Joule-Thomson係数"),
                    ("body", "与式 dh = cp dT + [v - T(∂v/∂T)P] dP と、h一定の条件を組み合わせます。"),
                    ("formula", "mu_JT = (∂T/∂P)_h = [T(∂v/∂T)_P - v]/cp。mu_JT=0となる温度が反転温度です。"),
                    ("h2", "(2) Calderbankの状態式"),
                    ("formula", "v = RT/P + a - b T^(-10/3)。T(∂v/∂T)_P - v = (13/3)b T^(-10/3) - a。反転温度 Ti = (13b/(3a))^(3/10) (a,b>0)。"),
                    ("h2", "(3)(4) 理想気体の温度・エントロピー"),
                    ("body", "理想気体v=RT/Pではmu_JT=0です。速度を無視する絞りならh一定からT2=T1。圧力がP1からP2へ下がるとき、比エントロピー変化は次式です。"),
                    ("formula", "Δs = cp ln(T2/T1) - R ln(P2/P1) = R ln(P1/P2)。全エントロピー変化は mR ln(P1/P2) で、P2<P1なら正です。"),
                ],
            },
            {
                "title": "第3問 - 再熱・抽気を含むRankineサイクル",
                "blocks": [
                    ("body", "図の状態列はd-e-f-a1-x-a2-b-c-dです。f→a1がボイラ、a1→xが第1段タービン、x→a2が再熱、a2→b→cが第2段タービン、c→dが復水器、d→e→fが給水加熱器とポンプです。bで質量mbを抽気し、残りがcへ流れるとします。"),
                    ("h2", "外部供給熱"),
                    ("formula", "初期蒸気質量をmとすると q_in = (ha1 - hf) + (ha2 - hx)。"),
                    ("h2", "抽気率とタービン仕事"),
                    ("formula", "直接接触給水加熱器なら mb hb + (m-mb) hd = m he、y=mb/m=(he-hd)/(hb-hd)。"),
                    ("formula", "w_t = (ha1-hx) + (ha2-hb) + (1-y)(hb-hc) = (ha1-hx)+(ha2-hc)-y(hb-hc)。η_th=w_t/q_in。"),
                    ("body", "抽気がない場合との差は、単位初期質量あたりΔw=y(hb-hc)だけ減少します。ポンプ仕事を含める定義なら、図のポンプ仕事を別途加えた正味仕事を使用します。"),
                ],
            },
        ],
    },
    "2004": {
        "era": "H16_april",
        "source": "2004_H16_april/thermo_2004_H16_question.pdf",
        "sections": [
            {
                "title": "第1問 - 可逆断熱変化",
                "blocks": [
                    ("body", "理想気体、κ=cp/cv一定、状態1(P1,T1,V1)から状態2(P2,T2,V2)への可逆断熱変化です。"),
                    ("formula", "mc_v dT = -P dV、P=mRT/V より dT/T = -(κ-1)dV/V。したがって TV^(κ-1)=一定、PV^κ=一定、T P^((1-κ)/κ)=一定。"),
                    ("h2", "仕事の比"),
                    ("body", "断熱線ではdP=-κP dV/Vです。ゆえに、同じ区間を絶対仕事で積分した仕事WTと、通常の境界仕事W12の大きさは |WT|=κ|W12|。同じ入力仕事の符号規約なら W12/WT=1/κ です。"),
                ],
            },
            {
                "title": "第2問 - 変形サイクルの熱効率とエントロピー",
                "blocks": [
                    ("body", "1→2は断熱圧縮、2→3は定容加熱、3→4は等温膨張、4→5は断熱膨張、5→1は定容放熱です。ε=V1/V2、ξ=P3/P2、ρ=V4/V3とし、κ一定とします。"),
                    ("formula", "T2/T1=ε^(κ-1), P2/P1=ε^κ; T3/T2=ξ; V4=ρV3; T4=T3; V5=V1; T5/T1=ξρ^(κ-1)。"),
                    ("h2", "各過程の熱量"),
                    ("formula", "Q12=Q45=0。Q23=mc_v T1 ε^(κ-1)(ξ-1)。Q34=mR T1 ε^(κ-1)ξ lnρ。Q51=mc_v T1[1-ξρ^(κ-1)]。"),
                    ("formula", "η=1 - mc_v T1(ξρ^(κ-1)-1) / {mc_v T1 ε^(κ-1)(ξ-1)+mR T1 ε^(κ-1)ξ lnρ}。"),
                    ("h2", "エントロピー変化"),
                    ("formula", "ΔS12=0、ΔS23=mR lnξ/(κ-1)、ΔS34=mR lnρ、ΔS45=0、ΔS51=-mR lnξ/(κ-1)-mR lnρ。総和は0。"),
                ],
            },
            {
                "title": "第3問 - 湿り空気線図",
                "blocks": [
                    ("body", "乾き空気質量ma、水蒸気質量mw、分圧Pa,Pw、飽和蒸気圧Ps、相対湿度φを使います。絶対湿度x=mw/ma、φ=Pw/Psです。"),
                    ("formula", "x=(Ra/Rw)(Pw/Pa)=0.622 φPs/(P-φPs)。"),
                    ("body", "P=1013 hPaの線図読取りとして、12℃・φ=0.30ではPs≈1.402 kPa、x1≈0.00259 kg/kg乾き空気。24℃まで加熱しても水分を加えなければxは不変。26℃・φ=0.70ではPs≈3.361 kPa、x2≈0.01479。"),
                    ("formula", "加えた水分 = x2-x1 ≈ 0.01220 kg/kg乾き空気 = 12.2 g/kg乾き空気。線図読取りのため末尾桁は近似です。"),
                ],
            },
        ],
    },
    "2005": {
        "era": "H17_april",
        "source": "2005_H17_april/thermo_2005_H17_question.pdf",
        "sections": [
            {
                "title": "第1問 - 真空への自由膨張",
                "blocks": [
                    ("body", "熱容量を無視できる剛体容器A,Bをコックで連結し、Aに気体、Bを真空としてコックを開きます。外界との熱交換はありません。"),
                    ("h2", "(1) 第一法則"),
                    ("formula", "Q=0、容器は剛体で境界仕事W=0。したがって ΔU=Q-W=0。"),
                    ("h2", "(2)(3) 温度変化と理想気体"),
                    ("body", "du=cv dT + [T(∂P/∂T)_v-P]dv と du=0から、-(∂T/∂v)_u=[T(∂P/∂T)_v-P]/cv。理想気体P=RT/vでは括弧内が0なので、Joule係数は0です。"),
                    ("h2", "(4) 平衡状態"),
                    ("body", "理想気体の内部エネルギーは温度だけの関数です。したがって最初のAの温度Tが最終平衡でも変わらず、A,B双方の気体は同じTになります。開放直後の局所的な非平衡過程の温度分布は問題条件だけでは一意に定まりません。"),
                ],
            },
            {
                "title": "第2問 - 定容加熱を含む理想気体サイクル",
                "blocks": [
                    ("body", "1→2は可逆断熱圧縮、2→3は定圧膨張（Q1流入）、3→1は定容放熱（Q2の大きさ）です。ε=V1/V2、κ一定で、3→1が定容なのでV3=V1です。"),
                    ("formula", "P2=P1ε^κ、T2=T1ε^(κ-1)、P3=P2、T3=T1ε^κ。"),
                    ("h2", "熱量・熱効率"),
                    ("formula", "Q1=mc_p T1 ε^(κ-1)(ε-1)。Q2=mc_v T1(ε^κ-1)（放熱の大きさ）。η=1-(ε^κ-1)/[κ ε^(κ-1)(ε-1)]。"),
                    ("h2", "仕事と平均有効圧"),
                    ("formula", "W=Q1-Q2=P1V1[(κ-1)ε^κ-κε^(κ-1)+1]/(κ-1)。p_me=P1 ε[(κ-1)ε^κ-κε^(κ-1)+1]/[(κ-1)(ε-1)]。"),
                ],
            },
            {
                "title": "第3問 - 二つの熱源と最大仕事",
                "blocks": [
                    ("body", "各熱源の質量をm、比熱をc、初期温度をTA>TB、熱機関停止後の共通温度をTFとします。外界への熱交換はなく、熱源の比熱は一定です。"),
                    ("formula", "(1) W=mc(TA-TF)-mc(TF-TB)=mc(TA+TB-2TF)。"),
                    ("formula", "(2) ΔS=mc ln(TF/TA)+mc ln(TF/TB) >= 0 より TF^2>=TATB、したがってTF>=sqrt(TATB)。"),
                    ("formula", "(3) 最大仕事は可逆限界TF=sqrt(TATB)で、Wmax=mc(TA+TB-2sqrt(TATB))=mc(sqrt(TA)-sqrt(TB))^2。"),
                ],
            },
        ],
    },
    "2006": {
        "era": "H18_april",
        "source": "2006_H18_april/thermo_2006_H18_question.pdf",
        "sections": [
            {
                "title": "第1問 - ポリトロープ変化",
                "blocks": [
                    ("body", "閉じた理想気体、P V^n=一定、κ=cp/cvとします。P-V図ではn=0が水平な定圧線、n=1が等温線、n=κが可逆断熱線、n→∞が垂直な定容線です。"),
                    ("formula", "W12=∫P dV=(P2V2-P1V1)/(1-n)=mR(T2-T1)/(1-n) (n≠1)。"),
                    ("formula", "Q12=ΔU+W12=mc_v(T2-T1)(κ-n)/(1-n)。したがって平均比熱 c_bar=Q12/[m(T2-T1)]=c_v(κ-n)/(1-n)。"),
                    ("body", "n=1ではW12=mRT ln(V2/V1)、ΔU=0。n=κではQ=0、n=0ではcp、n→∞ではcvに対応します。熱量Qは系への流入を正としました。"),
                ],
            },
            {
                "title": "第2問 - 等温膨張を含むサイクル",
                "blocks": [
                    ("body", "1→2は可逆断熱圧縮、2→3は等温膨張、3→4は可逆断熱膨張、4→1は定容放熱です。ε=V1/V2、φ=V3/V2です。"),
                    ("formula", "V2=V1/ε、T2=T1ε^(κ-1)、V3=φV2、T3=T2、V4=V1、T4=T1φ^(κ-1)。"),
                    ("formula", "q12=q34=0、q23=mR T1 ε^(κ-1) lnφ、q41=mc_v T1[1-φ^(κ-1)]。"),
                    ("formula", "η=1-[φ^(κ-1)-1]/[(κ-1)ε^(κ-1)lnφ]。ΔS12=0、ΔS23=mRlnφ、ΔS34=0、ΔS41=-mRlnφ。"),
                ],
            },
            {
                "title": "第3問 - 再熱なしRankineサイクルの湿り蒸気",
                "blocks": [
                    ("body", "状態1はP1,T1の過熱蒸気、1→2は等エントロピータービン、2→3は凝縮、3→4はポンプ、4→5はボイラ、5→1は過熱器です。P2の飽和表の値を添字'（液）と''（蒸気）で表します。"),
                    ("formula", "s2=s1=s'2+x2(s''2-s'2) より x2=(s1-s'2)/(s''2-s'2)。h2=h'2+x2(h''2-h'2)。"),
                    ("formula", "タービン仕事 wt=h1-h2。h3=h'2、ポンプ仕事wp=h4-h3。η_th=[(h1-h2)-(h4-h3)]/(h1-h4)=1-(h2-h3)/(h1-h4)。"),
                    ("formula", "x2=0.9、潜熱L2=h''2-h'2がボイラ・過熱器熱量qin=h1-h4の半分ならqin=2L2、qout=h2-h3=0.9L2。よって η=1-0.9/2=0.55。"),
                ],
            },
        ],
    },
    "2007": {
        "era": "H19_april",
        "source": "2007_H19_april/thermo_2007_H19_question.pdf",
        "sections": [
            {
                "title": "第1問 - ピストンを用いた排気",
                "blocks": [
                    ("body", "初期状態はV1、P1=2P0、T1です。問題文の仮想ピストンの経路を、外部圧力P0に抗して最終状態まで動かす一つの閉じた系の境界仕事として解釈します。漏れ・摩擦・位置エネルギー・運動エネルギーは無視し、熱損失の大きさはQL=P0V1/[2(κ-1)]です。"),
                    ("formula", "初期質量 m=2P0V1/(RT1)。最終圧力P0なのでP0V2=mRT2。第一法則 mcv(T2-T1)=-QL-P0(V2-V1)。"),
                    ("formula", "QL=mcvT1/4、P0V1=mRT1/2を代入すると mcpT2=mc_vT1+P0V1-QL、したがって T2/T1=(2κ+1)/(4κ)。"),
                    ("note", "注意: 問題文の仮想ピストン経路を上記のように読んだ結果です。第1段階を別個の可逆断熱過程と仮定する解釈は印刷条件だけからは確定せず、別の答えになり得るため採用していません。"),
                ],
            },
            {
                "title": "第2問 - cv=αTのセミ理想気体サイクル",
                "blocks": [
                    ("body", "1→2可逆断熱圧縮、2→3定容加熱、3→4可逆断熱膨張、4→1定容放熱のサイクルです。印刷された条件はcv=αTですが、ηを圧縮比εと単一のκだけで表せとも指定しています。cv=αTならκ=1+R/(αT)は温度依存なので、この指定は数学的に不足しています。以下は印刷条件に忠実な独立計算です。"),
                    ("formula", "u=αT^2/2+C、ds=αdT+R dV/V。δ=(R/α)lnεと置けば、断熱区間でT2=T1+δ、T4=T3-δ。"),
                    ("formula", "q12=q34=0、q23=mα(T3^2-T2^2)/2、q41=mα(T1^2-T4^2)/2。ΔS12=ΔS34=0、ΔS23=mα(T3-T2)、ΔS41=mα(T1-T4)。"),
                    ("formula", "η=1-[(T3-δ)^2-T1^2]/[T3^2-(T1+δ)^2]。κ1=1+R/(αT1)を使ってもδ/T1=lnε/(κ1-1)であり、なおT3/T1が必要です。"),
                    ("note", "もし問題のcv=αTが誤植で、通常の一定cvを意図した場合だけ、標準Ottoサイクルのη=1-ε^(1-κ)が得られます。ただしこれは印刷された物性条件とは別モデルなので、断定せず曖昧さとして残します。P-V図では定容線が垂直、T-S図では可逆断熱が垂直で、定容過程はds=αdTにより直線になります。"),
                ],
            },
            {
                "title": "第3問 - 二つの気体の定圧混合",
                "blocks": [
                    ("body", "気体A,Bを断熱的に定圧混合します。各質量、定圧比熱、初期温度をm1,cp1,T1およびm2,cp2,T2、T1>T2とします。外部への熱交換はなく、組成混合による別のエントロピー項は問題データにないため含めません。"),
                    ("formula", "Tm=(m1cp1T1+m2cp2T2)/(m1cp1+m2cp2)。ΔSA=m1cp1 ln(Tm/T1)、ΔSB=m2cp2 ln(Tm/T2)。"),
                    ("formula", "cp1=cp2=cp、m1=m2=m、T1=2T2ならTm=3T2/2=3T1/4、ΔS_total=mcp ln(9/8)>0。"),
                    ("note", "異なる気体の混合エントロピーを含めるには分子量・分圧・混合体積など追加条件が必要です。"),
                ],
            },
        ],
    },
    "2008": {
        "era": "H20_april",
        "source": "2008_H20_april/thermo_2008_H20_question.pdf",
        "sections": [
            {
                "title": "第1問 - エントロピーと仕事",
                "blocks": [
                    ("body", "質量mの理想気体、cpとR一定を仮定します。"),
                    ("formula", "T dS = mcp dT - mRT dP/P、すなわち dS=mcp dT/T-mR dP/P。"),
                    ("formula", "ΔS=mcp ln(T2/T1)-mR ln(P2/P1)。可逆断熱ならΔS=0なので P/T^[κ/(κ-1)] =一定、P2/P1=(T2/T1)^[κ/(κ-1)]。"),
                    ("body", "T-S図の補助等容線を状態1から状態2の温度まで引くと、その等容線の面積∫T dS=mc_v(T2-T1)が圧縮仕事の大きさに対応します。可逆断熱線そのものはS一定の鉛直線なので面積はありません。"),
                ],
            },
            {
                "title": "第2問 - ノズルの速度とエクセルギー効率",
                "blocks": [
                    ("body", "入口速度を無視し、断熱・軸仕事なし・位置エネルギー無視の定常ノズルとします。"),
                    ("formula", "h1=h2+w2^2/2、よって w2=sqrt[2(h1-h2)]。hをkJ/kgで入れるなら w2=sqrt[2000(h1-h2)] m/s。"),
                    ("body", "摩擦を含む実際の断熱流れではΔs>0です。基準状態の流れエクセルギー差h1-h2に対し、不可逆損失はT0Δsなので、"),
                    ("formula", "η_ex=(h1-h2)/(h1-h2+T0Δs)。"),
                    ("formula", "可逆断熱理想気体ならT2/T1=(P2/P1)^[(κ-1)/κ]、cp=κR/(κ-1)、w2=sqrt{[2κ/(κ-1)]RT1[1-(P2/P1)^((κ-1)/κ)]}。"),
                ],
            },
            {
                "title": "第3問 - 湿り空気と露点",
                "blocks": [
                    ("body", "絶対湿度x=mw/ma、相対湿度φ=Pw/Psを定義します。Pa=P-Pwです。"),
                    ("formula", "x=(Ra/Rw)(Pw/Pa)=0.622 φPs/(P-φPs)。"),
                    ("body", "t1=30℃、φ=0.5、P=1 barで、表からPs(30℃)=0.0424 barを使うとPw=0.0212 bar。缶を冷却して結露が始まる温度はPs(t2)=0.0212 barです。"),
                    ("formula", "表のPs(18℃)=0.0206 bar、Ps(20℃)=0.0234 barなので、表の2℃刻みの回答はt2=18℃以下。連続補間なら露点は約18.4℃です。"),
                ],
            },
        ],
    },
}


def main() -> None:
    outputs = []
    for year in ("2003", "2004", "2005", "2006", "2007", "2008"):
        item = COMMON[year]
        outputs.append(build_pdf(year, item["era"], item["source"], item["sections"]))
    for path in outputs:
        print(path)


if __name__ == "__main__":
    main()
