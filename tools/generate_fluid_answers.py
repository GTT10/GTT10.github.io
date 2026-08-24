#!/usr/bin/env python3
"""Generate the unofficial fluid-mechanics answers for 2003--2008.

The source PDFs are intentionally not touched.  This script writes UTF-8
uplatex sources to tmp/pdfs and compiles each one with the TeX Live tools
already used by the repository.  The generated PDFs are the only published
artifacts.
"""

from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
SOURCE_DIR = REPO / "tmp" / "pdfs" / "fluid-missing-2003-2008" / "answer-src"
ANSWER_DIR = REPO / "pdfs" / "answer"
TEX_BIN = Path(os.environ.get("TEXLIVE_BIN", r"C:\texlive\2025\bin\windows"))
UPLATEX = TEX_BIN / "uplatex.exe"
DVIPDFMX = TEX_BIN / "dvipdfmx.exe"
LUALATEX = TEX_BIN / "lualatex.exe"


COMMON_PREAMBLE = r"""\documentclass[a4paper,11pt]{ltjsarticle}
\usepackage{amsmath,amssymb,geometry,enumitem}
\usepackage{luatexja-fontspec}
\setmainjfont{HaranoAjiMincho}
\setsansjfont{HaranoAjiGothic}
\geometry{top=18mm,bottom=18mm,left=18mm,right=18mm}
\setlength{\parindent}{0pt}
\setlength{\parskip}{3pt}
\setlist{nosep,leftmargin=*}
\newcommand{\dd}{\,\mathrm d}
\newcommand{\Rey}{\mathrm{Re}}
\newcommand{\St}{\mathrm{St}}
\newcommand{\Eu}{\mathrm{Eu}}
\begin{document}
"""


BODY_2003 = r"""
\section*{大問1　相似則（レイノルズ数）}
\textbf{問題の要約}: 内径 $1\,\mathrm{m}$ の管を平均速度 $30\,\mathrm{cm/s}$ で流れる油を、内径 $2\,\mathrm{cm}$ の水模型で相似実験する。油の比重は $0.8$、粘度（粘性係数）は水の $40$ 倍である。\
\textbf{仮定}: 幾何学的相似とレイノルズ数相似を採用する。密度を $\rho_o=0.8\rho_w$、粘度を $\mu_o=40\mu_w$ とする。\
\textbf{独立計算}:
\[
 \frac{\rho_o V_oD_o}{\mu_o}=\frac{\rho_w V_wD_w}{\mu_w}
 \quad\Longrightarrow\quad
 V_w=\frac{\rho_o}{\rho_w}\frac{\mu_w}{\mu_o}\frac{D_o}{D_w}V_o
 =0.8\times\frac1{40}\times\frac{1}{0.02}\times0.30.
\]
\textbf{最終答}: $V_w=0.30\,\mathrm{m/s}=30\,\mathrm{cm/s}$.（粘度比を掛けるのではなく割る点に注意。）

\section*{大問2　茶葉のパラドックス}
\textbf{問題の要約}: 茶を円周方向にかき混ぜてから放置したとき、茶葉がどこへ集まるか、理由を説明する。\
\textbf{仮定}: 容器底の壁面摩擦を無視しない。自由表面付近と底面付近で角速度が異なる過渡流れを考える。\
\textbf{独立計算・説明}: 回転流の半径方向圧力勾配はおおよそ $\partial p/\partial r=\rho u_\theta^2/r$ で外向きである。しかし底面の粘着条件のため底面近くの旋回速度は小さく、同じ圧力勾配を支える遠心力が不足する。その結果、底面近くでは半径方向内向きの流れが生じ、中心で上昇し、上部で外向きに戻る二次循環ができる。\
\textbf{最終答}: 茶葉は底面の中心付近に集まる。遠心力で外へ飛ぶという一様回転の議論だけでは、底面境界層と二次流を落としているため不十分である。

\section*{大問3　糸を巻いた軽い円筒}
\textbf{問題の要約}: 紙製の軽い円筒中央に糸を約20回巻き、糸端を持って円筒を水平に静かに落とす。運動を図示し、理由を説明する。\
\textbf{仮定}: 糸は円筒から滑らず、円筒の軸は水平を保つ。糸の端は上方で固定され、円筒は糸をほどきながら落下する。\
\textbf{独立計算}: 巻き半径を $r$、質量を $M$、軸まわり慣性モーメントを $I$、下向き加速度を $a$、角加速度を $\alpha$ とする。滑りなし条件は $a=r\alpha$。力とモーメントの釣合いは
\[
 Mg-T=Ma,\qquad Tr=I\alpha=I\frac{a}{r}.
\]
したがって
\[
 a=\frac{Mg}{M+I/r^2},\qquad
 T=\frac{Mg\,I}{I+Mr^2},\qquad
 \alpha=\frac{a}{r}.
\]
薄肉中空円筒なら $I\simeq Mr^2$ なので $a\simeq g/2$。\
\textbf{最終答}: 円筒の重心は鉛直下向きに落ち、糸は上端でほどけ、円筒は軸まわりに回転する（回転方向は糸の巻き方向で決まる）。運動は単純自由落下ではなく、重力の一部が回転エネルギーに移る。

\section*{大問4　底孔からの流出}
\textbf{問題の要約}: 半径 $R$、高さ $H$ の開放円筒容器を満水にし、底中央の半径 $r$ の小孔（$R\gg r$）から水が下向きに速度 $v$ で流出する。出口での縮流はない。\
\textbf{仮定}: 水は非粘性、自由表面と出口は大気圧、出口速度分布は一様。板は孔から距離 $H$ 下に固定し、板上の薄い水膜の重量は無視する。\
\textbf{(1) 水面低下速度}: 連続の式より
\[
 \pi R^2(-\dot H)=\pi r^2v,
 \qquad |\dot H|=\frac{r^2}{R^2}v.
\]
\textbf{最終答}: 水面の下降速度は $r^2v/R^2$（下向きを正に取れば $\dot z_s=-r^2v/R^2$）。\
\textbf{(2) 出口速度}: 自由表面と孔の間でベルヌーイを適用し、$R\gg r$ から自由表面速度を無視すると
\[
 \frac{v^2}{2}=gH,\qquad v=\sqrt{2gH}.
\]
\textbf{(3) 板への力}: 孔から板まで自由落下するので、板直前の速度と断面積は
\[
 V_H=\sqrt{v^2+2gH}=\sqrt{2}\,v,\qquad
 A_HV_H=\pi r^2v.
\]
板直前の下向き運動量流束は
\[
 F=\rho A_HV_H^2=\rho\pi r^2vV_H
 =\sqrt{2}\rho\pi r^2v^2=2\sqrt{2}\rho gH\pi r^2.
\]
\textbf{最終答}: 板が受ける力は下向きに $F=2\sqrt{2}\rho gH\pi r^2$。出口断面をそのまま板まで保つ、または落下中の重力加速を無視する簡略化なら $\rho\pi r^2v^2$ になるが、原本の「孔より下方 $H$」を含む非粘性自由噴流では前者を採用する。

\section*{大問5　球の抵抗と終端速度}
\textbf{問題の要約}: 同じ半径で質量だけ異なる球を自由落下させ、終端速度の表 $m[\mathrm g]=(1,2,3,4)$、$v[\mathrm{cm/s}]=(0,1,2,3)$ を得た。抵抗は速度のべき乗に比例する。質量1 gと2 gを細い糸で連結したときの終端速度を求める。\
\textbf{仮定と注意}: 同じ半径なら浮力 $B$ は共通である。表の $m=1\,\mathrm g$ で $v=0$ は、浮力を無視する仮定とは両立しない。したがって表を物理的に整合させるには $B=1\,\mathrm{gf}$ と読む（この点は原本設問の曖昧さとして監査に記録した）。抵抗を $R=kv^n$ と置く。\
\textbf{(1) 独立計算}: 終端条件 $mg-B=kv^n$ に表を代入すると、$m-1$ は $v$ に比例する。よって $n=1$、単位を g--cm/s で書けば $R=(m-1)g$ かつ $k=g/(1\,\mathrm{cm/s})$。\
\textbf{(2) 独立計算}: 連結球では外力の有効重量は $(1+2-2)\,\mathrm{gf}=1\,\mathrm{gf}$、抵抗は同じ速度で $2kv$。したがって
\[
 2kv=1\,\mathrm{gf},\qquad v=0.5\,\mathrm{cm/s}.
\]
\textbf{最終答}: 抵抗は $v$ に一次比例し、連結時の終端速度は $0.5\,\mathrm{cm/s}$（浮力を無視する別解釈では表の $v=0$ が説明できず、数値解は定まらない）。

\section*{大問6　流線検査空間の運動量収支とEuler方程式}
\textbf{問題の要約}: 流線を中心軸とする流管について、流線方向座標を $s$、断面1から下流へ微小距離 $\Delta s$ の断面を2とする。断面積を $A$、流速を $W$、密度を $\rho$、圧力を $p$、単位質量当たりの外力の流線方向成分を $F$ とし、断面1--2間を固定検査空間として質量と運動量の出入りを求める。\
\textbf{符号}: $s$ の正方向を下流、断面1からの流入を正、断面2からの流出を正として、運動量は $s$ 成分を記す。\
\textbf{(1) 断面1から流入する質量・運動量}: 一様断面近似より
\[
 m_1=\rho_1A_1W_1\Delta t,\qquad M_1=\rho_1A_1W_1^2\Delta t.
\]
\textbf{(2) 断面2から流出する質量・運動量}:
\[
 m_2=\rho_2A_2W_2\Delta t,\qquad M_2=\rho_2A_2W_2^2\Delta t.
\]
\textbf{(3) 時刻 $t=0$ に検査空間が保有する量}:
\[
 m_0=\int_{s_1}^{s_2}\rho(s,0)A(s)\dd s,\qquad
 M_0=\int_{s_1}^{s_2}\rho(s,0)A(s)W(s,0)\dd s.
\]
\textbf{(4) 時刻 $t=\Delta t$ に保有する量}:
\[
 m_{\Delta t}=\int_{s_1}^{s_2}\rho(s,\Delta t)A(s)\dd s,\qquad
 M_{\Delta t}=\int_{s_1}^{s_2}\rho(s,\Delta t)A(s)W(s,\Delta t)\dd s.
\]
\textbf{(5) 連続の式}: 質量収支 $m_{\Delta t}-m_0=m_1-m_2$ を $\Delta t\to0$, $\Delta s\to0$ として
\[
 \boxed{\frac{\partial(\rho A)}{\partial t}+\frac{\partial(\rho AW)}{\partial s}=0}.
\]
定常なら $\rho_1A_1W_1=\rho_2A_2W_2$ である。\
\textbf{(6) 圧力による流線方向の力積}: 断面1、断面2、流管側壁の力積はそれぞれ
\[
 I_1=p_1A_1\Delta t,\qquad I_2=-p_2A_2\Delta t,\qquad
 I_s=-\Delta t\int_{S_w}p\,n_s\dd S,
\]
ここで $n_s$ は検査空間外向き法線の $s$ 成分である。従って $I_p=I_1+I_2+I_s$、微小流管では
\[
 I_p=-A\frac{\partial p}{\partial s}\Delta s\,\Delta t.
\]
\textbf{(7) 外力による力積}:
\[
 I_F=\Delta t\int_{CV}\rho F\dd V\simeq\rho AF\Delta s\,\Delta t.
\]
\textbf{(8) 運動量収支とEuler方程式}:
\[
 M_{\Delta t}-M_0=M_1-M_2+I_p+I_F.
\]
極限を取り、保存形と連続の式を組み合わせると
\[
 \frac{\partial(\rho AW)}{\partial t}+\frac{\partial(\rho AW^2)}{\partial s}
 =-A\frac{\partial p}{\partial s}+\rho AF,
\qquad
 \boxed{\frac{\partial W}{\partial t}+W\frac{\partial W}{\partial s}
 =-\frac1\rho\frac{\partial p}{\partial s}+F}.
\]
重力だけなら $F=-g\,\dd z/\dd s$ である。
"""


BODY_2005 = r"""
\section*{大問1　球の抵抗の相似実験}
\textbf{問題の要約}: 一様気流中の直径 $d_0$ の球の抵抗を、直径 $d_0/10$ の模型と、実機流体の $1000$ 倍の密度・$10$ 倍の粘度を持つ液体で調べる。実機速度を $u_0$、模型で測った抵抗を $F_1$ とする（実機マッハ数は十分小さい）。\\
\textbf{仮定}: 幾何学相似に加えて Reynolds 数相似を満たし、Mach 数の影響は無視する。$L_m=L_o/10$、$\rho_m=1000\rho_o$、$\mu_m=10\mu_o$ とする。\\
\textbf{(1) 模型速度}:
\[
 Re_m=\frac{\rho_m u_mL_m}{\mu_m}
 =\frac{1000}{10\,10}\frac{u_m}{u_0}Re_o
 =10\frac{u_m}{u_0}Re_o.
\]
従って $Re_m=Re_o$ より
\[
 \boxed{u_m=\frac{u_0}{10}}.
\]
\textbf{(2) 抵抗の換算}: 相似が成立すれば抗力係数 $C_D$ は同じで、$F=\tfrac12C_D\rho u^2S$、$S_m=S_o/100$。したがって
\[
 \frac{F_1}{F_o}=\frac{\rho_m}{\rho_o}\left(\frac{u_m}{u_0}\right)^2\frac{S_m}{S_o}
 =1000\times\frac1{100}\times\frac1{100}=\frac1{10},
 \qquad \boxed{F_o=10F_1}.
\]

\section*{大問2　傾斜面上の薄膜流れ}
\textbf{問題の要約}: 傾斜角 $\theta$ の斜面を、密度 $\rho$、粘度 $\mu$ の液膜が厚さ $h$ 一定で定常に流れ下る。$x$ を斜面下向き、$y$ を斜面から垂直外向きとし、速度を $(u,v)$、圧力を $p$、重力加速度を $g$ とする。\\
\textbf{(1) $x,y$ 方向の運動方程式}: 重力成分は $(g\sin\theta,-g\cos\theta)$ なので、一般の二次元式は
\[
 \rho\left(\frac{\partial u}{\partial t}+u\frac{\partial u}{\partial x}+v\frac{\partial u}{\partial y}\right)
 =-\frac{\partial p}{\partial x}+\mu\left(\frac{\partial^2u}{\partial x^2}+\frac{\partial^2u}{\partial y^2}\right)+\rho g\sin\theta,
\]
\[
 \rho\left(\frac{\partial v}{\partial t}+u\frac{\partial v}{\partial x}+v\frac{\partial v}{\partial y}\right)
 =-\frac{\partial p}{\partial y}+\mu\left(\frac{\partial^2v}{\partial x^2}+\frac{\partial^2v}{\partial y^2}\right)-\rho g\cos\theta.
\]
\textbf{(2) 速度・圧力分布}: 完全発達流れ $u=u(y),v=0$ とし、自由表面 $y=h$ で $p=p_0$、せん断応力 $\mu u'(h)=0$、壁面で $u(0)=0$ とする。自由表面圧力一定なので $p_x=0$。従って
\[
 p_y=-\rho g\cos\theta,\qquad \mu u''+\rho g\sin\theta=0,
\]
\[
 \boxed{p(y)=p_0+\rho g\cos\theta(h-y)},\qquad
 \boxed{u(y)=\frac{\rho g\sin\theta}{\mu}\left(hy-\frac{y^2}{2}\right)},\qquad 0\le y\le h.
\]
\textbf{(3) 壁面せん断応力}:
\[
 \tau_{xy}(y)=\mu u'(y)=\rho g\sin\theta(h-y),
 \qquad \boxed{\tau_{xy}(0)=\rho g h\sin\theta}.
\]
これは流体の応力成分であり、斜面が受ける接線力は反作用の $-\tau_{xy}(0)$ である。\\

\section*{大問3　一様流中の時計回り渦に働く力}
\textbf{問題の要約}: 無限遠で $x$ 方向速度 $U_\infty$、圧力 $p_\infty$ の一様流に、原点を中心とする時計回りの渦糸（循環の大きさ $\Gamma$）を置く。$x$ 方向 $2L$、$y$ 方向 $2h$ の長方形検査領域 $ABCD$（面外単位長さ）で運動量収支を行う。\\
\textbf{符号規約}: $W=\phi+i\psi$、$\dd W/\dd z=u-iv$、$\Gamma>0$ は時計回りの大きさとする。$\gamma=\Gamma/(2\pi)$ と置く。\\
\textbf{(1) 複素速度ポテンシャル}: 時計回り渦は $u_\theta=-\gamma/r$ なので
\[
 \boxed{W=U_\infty z+i\gamma\log z}.
\]
\textbf{(2) 速度と圧力}:
\[
 \frac{\dd W}{\dd z}=U_\infty+\frac{i\gamma}{z},\qquad
 u=U_\infty+\frac{\gamma y}{x^2+y^2},\qquad v=-\frac{\gamma x}{x^2+y^2}.
\]
Bernoulli の定数を無限遠で合わせると
\[
 \boxed{p=p_\infty-\rho U_\infty\gamma\frac{y}{r^2}-\frac{\rho\gamma^2}{2r^2}},
 \qquad r^2=x^2+y^2.
\]
\textbf{(3) 面 $AB$ から流入する運動量}: $AB$ は $x=-L$ の左面なので、流入（法線は $+x$）の単位時間運動量は
\[
 \dot P_{x,AB}=\rho\int_{-h}^{h}u(-L,y)^2\dd y,\qquad
 \dot P_{y,AB}=\rho\int_{-h}^{h}u(-L,y)v(-L,y)\dd y.
\]
\textbf{(4) 面 $AD$ から流入する運動量}: $AD$ は $y=-h$ の下面で、内向き法線は $+y$。流入部分（本符号規約では $v>0$、すなわち $-L\le x<0$）は
\[
 \dot P_{x,AD}^{\rm in}=\rho\int_{-L}^{0}u(x,-h)v(x,-h)\dd x,\qquad
 \dot P_{y,AD}^{\rm in}=\rho\int_{-L}^{0}v(x,-h)^2\dd x.
\]
運動量定理には、流出部分 $0<x\le L$ も含む符号付き全区間の流束を用いる。\\
\textbf{(5) $y$ 方向運動量収支}: 渦が流体に及ぼす力を $F_y^{\rm fluid}$ とする。長方形の外向き圧力力の $y$ 成分と、正味流出運動量を
\[
 P_y=\int_{-L}^{L}\{p(x,-h)-p(x,h)\}\dd x,
\]
\[
 I_y=\rho\int_{-h}^{h}\{u(L,y)v(L,y)-u(-L,y)v(-L,y)\}\dd y
 +\rho\int_{-L}^{L}\{v(x,h)^2-v(x,-h)^2\}\dd x
\]
と書けば、定常運動量定理は $I_y=P_y+F_y^{\rm fluid}$。従って渦が受ける力は $F_y=-F_y^{\rm fluid}=P_y-I_y$ である。\\
\textbf{(6) 代入計算}: $v(x,h)^2=v(x,-h)^2$ なので上下面の運動量流束は相殺し、
\[
 I_y=-4\rho U_\infty\gamma\tan^{-1}\frac{h}{L},\qquad
 P_y=4\rho U_\infty\gamma\tan^{-1}\frac{L}{h}.
\]
よって $\tan^{-1}(h/L)+\tan^{-1}(L/h)=\pi/2$ から
\[
 \boxed{F_y=2\pi\rho U_\infty\gamma=\rho U_\infty\Gamma\quad(+y\text{向き})}.
\]
（流体が渦に及ぼす力は $-y$ 向き。）\\

\section*{大問4　球座標の連続の式}
\textbf{問題の要約}: 球座標 $(r,\theta,\phi)$ の圧縮性三次元非定常流れについて、速度成分を $(V_r,V_\theta,V_\phi)$ とする。$\theta$ は $+z$ 軸からの極角、$\phi$ は $xy$ 平面への射影と $+x$ 軸のなす角である。\\
\textbf{独立計算}: 微小体積 $\dd V=r^2\sin\theta\,\dd r\dd\theta\dd\phi$ の質量収支を取る。半径、極角、方位角方向の正味流出を差分化すると
\[
 \frac{\partial\rho}{\partial t}r^2\sin\theta\,\dd r\dd\theta\dd\phi
 +\frac{\partial(r^2\rho V_r)}{\partial r}\dd r\dd\theta\dd\phi
 +\frac{\partial(\sin\theta\rho V_\theta)}{\partial\theta}r\,\dd r\dd\theta\dd\phi
 +\frac{\partial(\rho V_\phi)}{\partial\phi}r\,\dd r\dd\theta\dd\phi=0.
\]
従って
\[
 \boxed{\frac{\partial\rho}{\partial t}
 +\frac1{r^2}\frac{\partial(r^2\rho V_r)}{\partial r}
 +\frac1{r\sin\theta}\frac{\partial(\sin\theta\rho V_\theta)}{\partial\theta}
 +\frac1{r\sin\theta}\frac{\partial(\rho V_\phi)}{\partial\phi}=0}.
\]
"""


BODY_2004 = r"""
\section*{大問1　間隔 $2h$ の平行平板間流れ}
\textbf{問題の要約}: $y=-h$ の平板は静止、$y=h$ の平板は $x$ 方向に一定速度 $U>0$ で移動する。非圧縮性粘性流体の二次元定常流れに一定の $p_x=\partial p/\partial x$ がある。\
\textbf{仮定}: $u=u(y)$、$v=0$、重力なし、$\mu$ 一定。境界条件は $u(-h)=0$、$u(h)=U$。\
\textbf{(1) 基礎式}: $x$ 方向の運動方程式は
\[
 0=-p_x+\mu\frac{\dd^2u}{\dd y^2},\qquad u(-h)=0,\quad u(h)=U.
\]
\textbf{(2) 速度分布}: 2回積分して
\[
 u(y)=\frac{U}{2}\left(1+\frac{y}{h}\right)+\frac{p_x}{2\mu}(y^2-h^2).
\]
\textbf{(3) 無流量条件}: 単位幅流量
\[
 Q=\int_{-h}^{h}u\dd y=Uh-\frac{2p_xh^3}{3\mu}.
\]
従って $Q=0$ なら
\[
 \boxed{p_x=\frac{3\mu U}{2h^2}}.
\]
\textbf{(4) 壁面せん断応力}: $\tau_{xy}=\mu u'=\mu U/(2h)+p_xy$。上壁 $y=h$ では
\[
 \tau_{xy}(h)=\frac{2\mu U}{h},
\]
下壁 $y=-h$ では
\[
 \tau_{xy}(-h)=-\frac{\mu U}{h}.
\]
符号は流体に作用する $+x$ 向きの応力成分であり、平板が受ける応力は法線の向きに応じた反作用となる。

\section*{大問2　移動板に当たる円形噴流}
\textbf{問題の要約}: 大気圧 $p_0$ 中の面積 $A$ のノズルから密度 $\rho$ の水が速度 $q$ で噴出し、前方の大きな板に垂直衝突する。板は噴流と同方向へ速度 $u$ で動く。粘性・重力・板移動による周囲空気の運動は無視する。\
\textbf{仮定}: $q>u$、板に固定した座標系で衝突後は板に沿う円環状流れとなり、相対速度の大きさは保存される。\
\textbf{(1) ノズルの運動量流束}: 固定ノズルから出る質量流量は $\rho Aq$、$x$ 運動量の単位時間流出は
\[
 \boxed{\rho Aq^2}.
\]
\textbf{(2) 板に沿う速度}: 板座標系で入口相対速度は $w=q-u$。非粘性・大気圧一定の流線で、十分遠方の板面上の相対速度は
\[
 \boxed{w=q-u}.
\]
実験室系の速度ベクトルは板の法線速度 $u$ と、板内の半径方向速度 $w\boldsymbol e_r$ の和である。\
\textbf{(3) 最大圧力}: 衝突点は相対流れのよどみ点なので
\[
 \boxed{p_{\max}=p_0+\frac12\rho(q-u)^2}.
\]
\textbf{(4) 板に働く力}: 板に固定した検査体積で相対質量流量は $\rho A(q-u)$、法線方向の相対運動量変化は $q-u$。従って前面が受ける合力は
\[
 \boxed{F=\rho A(q-u)^2}
\]
（噴流の進行方向、すなわち板を押す向き）。後面は大気圧 $p_0$ なので、前後圧力差の合力もこの値になる。局所最大圧力 $p_{\max}$ と面積平均圧力を同一視しない。

\section*{大問3　流線に沿う一次元オイラー方程式}
\textbf{問題の要約}: 流線を中心軸とする流管の断面1,2間（流線方向座標 $s$、距離 $\Delta s$）を検査空間とする。断面積 $A$、流速 $W$、密度 $\rho$、圧力 $p$、単位質量当たり外力の流線方向成分 $F$ を用いて、質量・運動量の出入りから式を導く。\
\textbf{仮定}: 断面内は一次元一様、断面1の上流向きを流入正、側壁圧力の流線方向成分は積分して扱う。\
\textbf{(1) 断面1からの流入}:
\[
 m_1=\rho_1A_1W_1\Delta t,\qquad M_1=\rho_1A_1W_1^2\Delta t.
\]
\textbf{(2) 断面2からの流出}:
\[
 m_2=\rho_2A_2W_2\Delta t,\qquad M_2=\rho_2A_2W_2^2\Delta t.
\]
\textbf{(3) 時刻 $t=0$ の保有量}:
\[
 m_0=\int_{s_1}^{s_2}\rho A\dd s,\qquad M_0=\int_{s_1}^{s_2}\rho AW\dd s.
\]
\textbf{(4) 時刻 $t=\Delta t$ の保有量}:
\[
 m_{\Delta t}=\int_{s_1}^{s_2}\rho(s,t+\Delta t)A(s)\dd s,\qquad
 M_{\Delta t}=\int_{s_1}^{s_2}\rho AW(s,t+\Delta t)\dd s.
\]
\textbf{(5) 連続の式}: 質量収支 $m_{\Delta t}-m_0=m_1-m_2$ から
\[
 \frac{\partial}{\partial t}(\rho A)+\frac{\partial}{\partial s}(\rho AW)=0.
\]
定常なら $\rho_1A_1W_1=\rho_2A_2W_2$。\
\textbf{(6) 圧力力積}: 断面1の力積は $I_1=p_1A_1\Delta t$、断面2は $I_2=-p_2A_2\Delta t$。側壁は
\[
 I_s=\Delta t\int_{S_w}(-p\,\boldsymbol n\cdot\boldsymbol e_s)\dd S,
\]
従って $I_p=I_1+I_2+I_s$。微小流管では $I_p=-A(\partial p/\partial s)\Delta s\Delta t$。\
\textbf{(7) 外力力積}:
\[
 I_F=\Delta t\int_{CV}\rho F\dd V\simeq \rho AF\Delta s\Delta t.
\]
\textbf{(8) 運動量収支}:
\[
 M_{\Delta t}=M_0+M_1-M_2+I_p+I_F.
\]
微分化すると保存形
\[
 \frac{\partial(\rho AW)}{\partial t}+\frac{\partial(\rho AW^2)}{\partial s}
 =-A\frac{\partial p}{\partial s}+\rho AF.
\]
これと連続の式を組み合わせ、$A\ne0$ として
\[
 \boxed{\frac{\partial W}{\partial t}+W\frac{\partial W}{\partial s}
 =-\frac1\rho\frac{\partial p}{\partial s}+F}.
\]
これは流線に沿う一次元オイラー方程式である。重力だけなら $F=-g\,\dd z/\dd s$。
"""


BODY_2006 = r"""
\section*{大問1　質量保存則}
\textbf{問題の要約}: 非粘性二次元流れの長方形検査領域 $x_1\le x\le x_2$、$y_1\le y\le y_2$ について、図の (I),(II) の意味を説明し、連続方程式を積分形・微分形・ラグランジュ微分形で示す。\
\textbf{仮定}: 面外単位長さ、$x,y$ 正方向の速度成分を $u,v$ とする。\
\textbf{(1) 符号}: 図の (I) は右面 $BC$ と上面 $DC$ を通る流出質量流量に負号を付けたもの、(II) は左面 $AD$ と下面 $AB$ から流入する質量流量である。蓄積率は「流入−流出」だから
\[
 \frac{\partial}{\partial t}\iint_{ABCD}\rho\dd x\dd y
 =-\int_{y_1}^{y_2}(\rho u)_{x_2}\dd y+\int_{y_1}^{y_2}(\rho u)_{x_1}\dd y
 -\int_{x_1}^{x_2}(\rho v)_{y_2}\dd x+\int_{x_1}^{x_2}(\rho v)_{y_1}\dd x.
\]
\textbf{(2) 任意領域での連続方程式}: ガウスの定理を使い、任意の領域で
\[
 \iint\left[\frac{\partial\rho}{\partial t}+\frac{\partial(\rho u)}{\partial x}+\frac{\partial(\rho v)}{\partial y}\right]\dd x\dd y=0,
\]
従って
\[
 \boxed{\frac{\partial\rho}{\partial t}+\frac{\partial(\rho u)}{\partial x}+\frac{\partial(\rho v)}{\partial y}=0}.
\]
\textbf{(3) ラグランジュ微分形}: $D/Dt=\partial_t+u\partial_x+v\partial_y$ と展開すると
\[
 \boxed{\frac{D\rho}{Dt}+\rho\left(\frac{\partial u}{\partial x}+\frac{\partial v}{\partial y}\right)=0}.
\]
一定密度なら $\partial_xu+\partial_yv=0$。

\section*{大問2　傾いた一様流と二重極}
\textbf{問題の要約}: 複素速度ポテンシャル
\[
 W=Uz e^{-i\alpha}+\frac{A}{z}e^{i\alpha},\qquad z=x+iy,\quad U,A>0,\quad0<\alpha<\frac\pi2
\]
で与えられる二次元流れについて、複素速度、よどみ点、流れ関数 $\Psi$=0 の流線、流れの種類を求める。\
\textbf{仮定}: $W=\phi+i\Psi$、$\dd W/\dd z=u-iv$ の規約を採用する。$z=re^{i\theta}$ とする。\
\textbf{(1) 複素速度とよどみ点}:
\[
 \frac{\dd W}{\dd z}=Ue^{-i\alpha}-\frac{A e^{i\alpha}}{z^2}.
\]
よどみ点は $\dd W/\dd z=0$ より、$a=\sqrt{A/U}$ として
\[
 z=\pm ae^{i\alpha},\qquad (x,y)=\bigl(\pm a\cos\alpha,\ \pm a\sin\alpha\bigr).
\]
\textbf{(2) 流れ関数と $\Psi=0$}:
\[
 \Psi=\operatorname{Im}W=\left(Ur-\frac Ar\right)\sin(\theta-\alpha)
 =\left(U-\frac A{r^2}\right)(y\cos\alpha-x\sin\alpha).
\]
したがって $\Psi=0$ は、$r=a$ の円と、中心を通り角度 $\alpha$ の直線（直線上のよどみ点を含む）である。\
\textbf{(3) 流れの説明}: 一様流 $U$ と、一様流に対して角度 $\alpha$ だけ向きを合わせた強さ $A$ の二重極の重ね合わせで、円 $r=a$ は非貫入境界となる。円柱まわりの非粘性ポテンシャル流（迎角 $\alpha$）として解釈できる。

\section*{大問3　固体回転（強制渦）}
\textbf{問題の要約}: 軸対称流れで $u_r=0,u_z=0,u_\theta=Cr$（$C>0$）の渦度を求め、名称を答える。\
\textbf{独立計算}: 円筒座標で
\[
 \omega_z=\frac1r\frac{\partial(ru_\theta)}{\partial r}
 =\frac1r\frac{\partial(Cr^2)}{\partial r}=2C,
 \qquad \omega_r=\omega_\theta=0.
\]
\textbf{最終答}: 渦度は $\boldsymbol\omega=2C\boldsymbol e_z$。角速度 $C$ の剛体回転と同じなので、強制渦（solid-body vortex）である。

\section*{大問4　平板境界層のオーダー評価}
\textbf{問題の要約}: 一様速度 $U$ の非圧縮性流れが平板に沿って進む。$x=L$ で境界層厚さ $\delta$、境界層外縁の $y$ 方向速度 $V$ を用い、$V/U=O(\delta/L)$ と $\delta=O(L/\sqrt{\Rey})$ を示す。\
\textbf{仮定}: $L$ を $x$ 方向代表長さ、$\delta$ を $y$ 方向代表長さ、$u=O(U)$、$v=O(V)$、$\Rey=UL/\nu\gg1$ とする。圧力勾配は外部流れのオーダーに含め、平板上の標準的な境界層スケーリングを行う。\
\textbf{(1) 連続の式}:
\[
 \frac{\partial u}{\partial x}+\frac{\partial v}{\partial y}=0
 \quad\Longrightarrow\quad \frac UL\sim\frac V\delta,
 \qquad\boxed{\frac VU=O\left(\frac\delta L\right)}.
\]
\textbf{(2) 境界層厚さ}: $x$ 運動方程式の対流項は $O(U^2/L)$、粘性項は $O(\nu U/\delta^2)$。両者を釣り合わせると
\[
 \frac{U^2}{L}\sim\frac{\nu U}{\delta^2},
 \qquad \frac{\delta^2}{L^2}\sim\frac{\nu}{UL}=\frac1{\Rey},
 \qquad\boxed{\delta=O\left(\frac L{\sqrt{\Rey}}\right)}.
\]
図の外縁速度 $V$ はこの結果と連続の式から $V/U=O(\Rey^{-1/2})$ のオーダーになる。
"""


BODY_2007 = r"""
\section*{大問1　開放箱の側孔からの流出}
\textbf{問題の要約}: 上部が開いた大きな箱の側面下部の小孔から、密度 $\rho$ の流体が流出する。自由表面 A と孔 B の高低差は $h$、大気圧は $p_a$、重力加速度は $g$。ベルヌーイの定理を順に適用して流出速度を求める。\
\textbf{仮定}: 非粘性・定常・同一流線、大きな箱なので自由表面速度 $V_A$ は無視、AとBはともに大気圧。\
\textbf{(1) 圧力単位のベルヌーイ式}:
\[
 \frac p{\rho g}+\frac{V^2}{2g}+z=\text{const}.
\]
各項は順に圧力水頭、速度水頭、位置水頭。\
\textbf{(2) A--B 間}: $p_A=p_B=p_a$、$V_A\simeq0$、$z_A-z_B=h$ として
\[
 \frac{p_a}{\rho g}+z_A=\frac{p_a}{\rho g}+\frac{v^2}{2g}+z_B.
\]
粘性、縮流、流出係数を無視した理想式である点に注意する。\
\textbf{(3) 最終答}:
\[
 \boxed{v=\sqrt{2gh}}.
\]
実際には $v=C_d\sqrt{2gh}$ となり得るが、原本の仮定では $C_d=1$。

\section*{大問2　複素速度ポテンシャル}
\textbf{問題の要約}: $W=a\log z$（$a$ が実数または純虚数）の流れを速度場から説明し、$W=Uz+m\log z$ のよどみ点とその点を通る流線の流れ関数を求める。\
\textbf{規約}: $W=\phi+i\psi$、$\dd W/\dd z=u-iv$、$z=re^{i\theta}$、対数の枝は局所的に固定する。\
\textbf{(1) $a$ 実数}: $\dd W/\dd z=a/z$ より $u_r=a/r,u_\theta=0$。$a>0$ は原点からの点源、$a<0$ は吸込みで、流量は $2\pi a$。\
\textbf{(1) $a=ib$ 純虚数}: $\dd W/\dd z=ib/z$ より $u_r=0,u_\theta=-b/r$。これは原点の自由渦で、循環は $\Gamma=-2\pi b$（符号は角度と速度の規約に依存）。\
\textbf{(2) 一様流と点源}:
\[
 \frac{\dd W}{\dd z}=U+\frac mz=0
 \quad\Longrightarrow\quad z_s=-\frac mU,
\]
すなわちよどみ点は $(-m/U,0)$。この点では $r=m/U$、枝 $\theta=\pi$ を選べば
\[
 \psi=\operatorname{Im}(Uz+m\log z)=m\pi.
\]
\textbf{最終答}: よどみ点を通る分離流線は $\psi=m\pi$（対数の枝を $-\pi$ に取れば $-m\pi$ と表示されるが同じ流線）。

\section*{大問3　自由渦の渦度・循環・圧力}
\textbf{問題の要約}: $u_r=0,u_z=0,u_\theta=\Omega a^2/r$ の軸対称流れについて、渦の名称、渦度、原点まわりの循環、無限遠圧力 $p_a$ を用いた圧力分布を求める。\
\textbf{(1) 名称}: $ru_\theta=\Omega a^2$ 一定なので自由渦（ポテンシャル渦）。\
\textbf{(2) 渦度}: $r>0$ では
\[
 \omega_z=\frac1r\frac{\partial(ru_\theta)}{\partial r}=0.
\]
原点には特異な集中渦度があり、通常の点を除く領域ではゼロである。\
\textbf{(3) 循環}:
\[
 \Gamma=\oint u_\theta r\dd\theta=2\pi r\frac{\Omega a^2}{r}=\boxed{2\pi\Omega a^2}.
\]
\textbf{(4) 圧力}: 半径方向の運動方程式は $\dd p/\dd r=\rho u_\theta^2/r=\rho\Omega^2a^4/r^3$。$p(\infty)=p_a$ から
\[
 p(r)=p_a-\frac{\rho\Omega^2a^4}{2r^2}.
\]
原点近傍で負圧が発散するのは、粘性・有限コアを無視した理想自由渦の限界である。

\section*{大問4　極座標での連続の式}
\textbf{問題の要約}: 極座標 $(r,\theta)$ の二次元非定常圧縮性流れで、微小扇形検査空間 $\dd r\times r\dd\theta$（面外単位長さ）への質量出入りを考え、連続の式を導出する。\
\textbf{仮定}: 速度成分は $(v_r,v_\theta)$、密度は $\rho(r,\theta,t)$。\
\textbf{独立計算}: 検査空間の蓄積率は $\partial_t\rho\,r\dd r\dd\theta$。半径面の正味流出は $\partial_r(r\rho v_r)\dd r\dd\theta$、角度面の正味流出は $\partial_\theta(\rho v_\theta)\dd r\dd\theta$。流出と蓄積の和をゼロにすると
\[
 \frac{\partial\rho}{\partial t}\,r\dd r\dd\theta
 +\frac{\partial(r\rho v_r)}{\partial r}\dd r\dd\theta
 +\frac{\partial(\rho v_\theta)}{\partial\theta}\dd r\dd\theta=0.
\]
\textbf{最終答}:
\[
 \boxed{\frac{\partial\rho}{\partial t}+\frac1r\frac{\partial(r\rho v_r)}{\partial r}+\frac1r\frac{\partial(\rho v_\theta)}{\partial\theta}=0}.
\]

"""


BODY_2008 = r"""
\section*{大問1　ゆるやかに径が変化する管}
\textbf{問題の要約}: 直径が $d_1$ から $d_2$ へゆるやかに変化する円形管内の非圧縮性・非粘性・定常流れ（密度 $\rho$）について、入口速度・圧力を $(V_1,p_1)$、出口を $(V_2,p_2)$ とする。重力は無視する。\
\textbf{仮定}: 流れは一次元、断面平均速度を使い、損失なし。\
\textbf{(1) ベルヌーイ}:
\[
 p_1+\frac12\rho V_1^2=p_2+\frac12\rho V_2^2.
\]
\textbf{(2) 出口圧力}: 連続の式 $A_1V_1=A_2V_2$ と $A\propto d^2$ より $V_2=(d_1/d_2)^2V_1$。従って
\[
 \boxed{p_2=p_1+\frac12\rho\left[V_1^2-\left(\frac{d_1}{d_2}\right)^4V_1^2\right]}.
\]
\textbf{(3) 入口の運動量流束}: 流れ方向を $x$ とすると
\[
 \boxed{\dot{P}_{x,1}=\rho A_1V_1^2=\rho\frac{\pi d_1^2}{4}V_1^2}.
\]

\section*{大問2　速度・流れ関数・自由渦}
\textbf{問題の要約}: $xy$ 平面の非圧縮性・非粘性・渦なし二次元流れで $\boldsymbol u=u\boldsymbol i+v\boldsymbol j$。流れ関数 $\psi$、速度ポテンシャル $\phi$、複素速度ポテンシャル $W$ を定義し、$u_\theta=C/r$ の自由渦を Cartesian 成分、循環、各ポテンシャルで表す。\
\textbf{規約}: $u=\partial_y\psi$、$v=-\partial_x\psi$、$u=\partial_x\phi$、$v=\partial_y\phi$、$W=\phi+i\psi$。\
\textbf{(1) 流れ関数}:
\[
 \boxed{u=\frac{\partial\psi}{\partial y},\qquad v=-\frac{\partial\psi}{\partial x}}.
\]
これは $\partial_xu+\partial_yv=0$ を恒等的に満たす。\
\textbf{(2) 速度ポテンシャル}: 渦なし条件から
\[
 \boxed{u=\frac{\partial\phi}{\partial x},\qquad v=\frac{\partial\phi}{\partial y}}.
\]
\textbf{(3) 複素ポテンシャル}: Cauchy--Riemann 関係により
\[
 \boxed{W=\phi+i\psi,\qquad \frac{\dd W}{\dd z}=u-iv}.
\]
\textbf{(4) 自由渦の速度}: $u_\theta=C/r$、$r^2=x^2+y^2$ から
\[
 \boxed{u=-\frac{Cy}{r^2},\qquad v=\frac{Cx}{r^2}}.
\]
\textbf{(5) 循環}:
\[
 \boxed{\Gamma=\int_0^{2\pi}\frac Cr r\dd\theta=2\pi C}.
\]
\textbf{(6) ポテンシャル}:
\[
 \boxed{\psi=-C\ln r+\text{const}},\qquad
 \boxed{\phi=C\theta+\text{const}},\qquad
 \boxed{W=-iC\log z+\text{const}}.
\]
原点は特異点であり、単連結領域全体で一価な $\phi$ を取れない。

\section*{大問3　移動平板間の粘性流れ}
\textbf{問題の要約}: $y=0$ の静止平板と $y=h$ の速度 $U$ で動く平板の間の定常二次元流れ。密度 $\rho$、粘度 $\mu$、圧力勾配 $p_x=\dd p/\dd x$ が与えられる。\
\textbf{仮定}: $u=u(y)$、$v=0$、非圧縮、重力なし。\
\textbf{(1) 力の釣合い}: 微小要素の $x$ 方向釣合い
\[
 0=-p_x+\frac{\dd\tau_{xy}}{\dd y},\qquad \tau_{xy}=\mu\frac{\dd u}{\dd y}.
\]
\textbf{(2) 速度分布}: 境界条件 $u(0)=0,u(h)=U$ を使って
\[
 \boxed{u(y)=\frac{Uy}{h}-\frac{p_x}{2\mu}y(h-y)},\qquad0\le y\le h.
\]
\textbf{(3) 下板の粘性力がゼロとなる勾配}:
\[
 \tau_{xy}(0)=\mu\frac Uh-\frac{p_xh}{2}=0
 \quad\Longrightarrow\quad
 \boxed{\frac{\dd p}{\dd x}=p_x=\frac{2\mu U}{h^2}}.
\]
この正の圧力勾配はクエット流れを押し戻し、下壁で速度勾配をゼロにする。
"""


BODIES = {
    2003: BODY_2003,
    2004: BODY_2004,
    2005: BODY_2005,
    2006: BODY_2006,
    2007: BODY_2007,
    2008: BODY_2008,
}


def compile_one(year: int, body: str) -> None:
    year_dir = SOURCE_DIR / str(year)
    year_dir.mkdir(parents=True, exist_ok=True)
    tex_path = year_dir / f"{year}_fluid.tex"
    tex_path.write_text(
        COMMON_PREAMBLE
        + rf"\begin{{center}}\Large\textbf{{流体力学 {year}年度\quad 非公式解答案}}\\[3pt]"
        + r"\normalsize 問題原本を読み直した独立計算。符号規約は本文に明記。\end{center}\hrule\vspace{6pt}"
        + body
        + r"\vfill\hrule\small\textit{非公式資料。最終的な判断は問題原本・講義資料と照合してください。}\end{document}" + "\n",
        encoding="utf-8",
    )
    env = os.environ.copy()
    env.setdefault("SOURCE_DATE_EPOCH", "0")
    for _ in range(2):
        subprocess.run(
            [str(LUALATEX), "-interaction=nonstopmode", "-halt-on-error", "-file-line-error", tex_path.name],
            cwd=year_dir,
            env=env,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )
    output = ANSWER_DIR / f"{year}_unofficial" / f"{year}_fluid.pdf"
    output.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(year_dir / f"{year}_fluid.pdf", output)
    print(f"created {output.relative_to(REPO)}")


def main() -> None:
    if not LUALATEX.exists():
        raise SystemExit(f"LuaLaTeX not found under {TEX_BIN}")
    for year, body in BODIES.items():
        compile_one(year, body)


if __name__ == "__main__":
    main()
