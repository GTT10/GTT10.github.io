"""Generate the missing unofficial mechanics solutions for 2003-2008.

The source data below is deliberately kept in plain text so the same checked
derivations are used in the HTML explanation pages and in the PDF answer
booklets.  It is not a replacement for the scanned question PDFs: the audit
report records the independent checks and the assumptions used here.
"""

from __future__ import annotations

import html
import os
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import KeepTogether, Paragraph, SimpleDocTemplate, Spacer


ROOT = Path(__file__).resolve().parents[1]
FONT_PATH = Path(r"C:\Windows\Fonts\yumin.ttf")
FONT_NAME = "YuMinchoMaterials"


def block(kind: str, text: str) -> dict[str, str]:
    return {"kind": kind, "text": text}


def section(number: str, title: str, blocks: list[dict[str, str]]) -> dict[str, object]:
    return {"number": number, "title": title, "blocks": blocks}


DATA: dict[int, dict[str, object]] = {
    2003: {
        "era": "H15",
        "question": "pdfs/question/2003_H15_april/materials_2003_H15_question.pdf",
        "sections": [
            section("1", "3本の斜材と中央材で支えられた節点", [
                block("problem", "同じ長さ l、断面積 A、縦弾性係数 E、線膨張係数 alpha の棒 A, B, C。上端は同一水平面の剛体に固定され、下端 O でピン結合される。中央棒 B は鉛直、外側の棒 A, C は鉛直から theta。自重は無視する。"),
                block("assumption", "下向きを節点変位 delta の正、棒の引張力を正とする。c = cos(theta) と置く。"),
                block("step", "(1) 節点 O の下向き荷重 P。適合条件より、中央棒の伸びは delta、外側棒の伸びは delta*c。したがって N_B = EA*delta/l、N_A = N_C = EA*delta*c/l。鉛直方向の釣合いは N_B + 2*c*N_A = P。"),
                block("answer", "(1) delta = P*l/[EA*(1+2*c^2)]。応力は sigma_B = P/[A*(1+2*c^2)]、sigma_A = sigma_C = P*c/[A*(1+2*c^2)]。いずれも引張。"),
                block("step", "(2) 荷重なしで全体を t だけ昇温。e = alpha*t と置く。適合条件は delta/l = e + N_B/(EA)、c*delta/l = e + N_A/(EA)。釣合いは N_B + 2*c*N_A = 0。"),
                block("answer", "(2) delta = e*l*(1+2*c)/(1+2*c^2)。sigma_B = E*e*2*c*(1-c)/(1+2*c^2)、sigma_A = sigma_C = -E*e*(1-c)/(1+2*c^2)。0<c<1 なら中央棒は引張、外側棒は圧縮。"),
            ]),
            section("2", "3点支持連続ばりと2つの集中荷重", [
                block("problem", "長さ 2l、等間隔の支持 A, B, C をもつ連続ばりに、AB と BC の各中央へ下向き荷重 P。縦弾性係数 E、断面二次モーメント I。"),
                block("assumption", "左端から右向きに x を測り、曲げモーメントは下側引張りを正とする。対称性から R_A = R_C。"),
                block("step", "たわみの適合条件 y(A)=y(B)=y(C)=0 と対称条件 y'(B)=0 を、各区間で EI*y''=M(x) に代入する。AB の M(x) は 0<=x<=l/2 で R_A*x、l/2<=x<=l で R_A*x-P*(x-l/2)。右半分は対称で、l<=x<=3l/2 では R_A*x+R_B*(x-l)-P*(x-l/2)、3l/2<=x<=2l ではさらに -P*(x-3l/2) を加える。"),
                block("answer", "反力は R_A=R_C=5P/16、R_B=11P/8。曲げモーメントは A で 0、各荷重点で +5P*l/32、B で M_B=-3P*l/16、C で 0。せん断力は A から左荷重点まで +5P/16、そこから B まで -11P/16、B から右荷重点まで +11P/16、右荷重点から C まで -5P/16。"),
                block("answer", "B 点の曲げ応力を正方形断面一辺 a で評価すると、I=a^4/12、Z=I/(a/2)=a^3/6。最大値の大きさは |sigma_B|max=|M_B|/Z=9P*l/(8a^3)。"),
            ]),
            section("3", "応力と連続体の釣合い", [
                block("problem", "連続体力学における力と応力の定義、英語名称、および直交座標 O-xyz に対する3次元の応力の釣合い方程式を問う。"),
                block("answer", "(1) 力は物体の運動状態を変える相互作用で、単位は N。応力は面に作用する力を面積で割った局所量で、法線成分を normal stress、接線成分を shear stress と呼ぶ。力は剛体・質点の全体量、応力は連続体内部の面ごとの分布量である。"),
                block("answer", "(2) 力 = force、応力 = stress。法線応力 = normal stress、せん断応力 = shear stress。"),
                block("step", "微小要素 dx*dy*dz の各面に作用する応力を、反対面の値をテイラー展開して足し合わせる。物体力を無視すると各方向の一次項がゼロになる。"),
                block("answer", "(3) x 方向: d(sigma_x)/dx + d(tau_xy)/dy + d(tau_zx)/dz = 0。y 方向: d(tau_xy)/dx + d(sigma_y)/dy + d(tau_yz)/dz = 0。z 方向: d(tau_zx)/dx + d(tau_yz)/dy + d(sigma_z)/dz = 0。"),
            ]),
        ],
    },
    2004: {
        "era": "H16",
        "question": "pdfs/question/2004_H16_april/materials_2004_H16_question.pdf",
        "sections": [
            section("1", "中実棒と中空円筒の組合せ棒", [
                block("problem", "長さ l の中実円柱 A と中空円筒 B を同軸に配置し、剛体円板 C, D で両端を固定する。各材料の E, alpha, A を E1, alpha1, A1 および E2, alpha2, A2 とする。"),
                block("assumption", "2本は同じ端板間変位を受ける。D0 = E1*A1 + E2*A2 と置く。"),
                block("step", "(1) 軸方向荷重 P では共通ひずみ epsilon = lambda/l。力の釣合い P=(E1*A1+E2*A2)*epsilon。"),
                block("answer", "(1) sigma_1=E1*P/D0、sigma_2=E2*P/D0、lambda=P*l/D0。"),
                block("step", "(2) B だけを t だけ昇温し、外力なし。共通変位 delta に対して sigma_1=E1*delta/l、sigma_2=E2*(delta/l-alpha2*t)。全軸力 E1*A1*delta/l + E2*A2*(delta/l-alpha2*t)=0。"),
                block("answer", "(2) delta/l=E2*A2*alpha2*t/D0。sigma_1=E1*E2*A2*alpha2*t/D0（A は引張）、sigma_2=-E1*E2*A1*alpha2*t/D0（B は圧縮）。組合せ棒の伸び lambda=l*E2*A2*alpha2*t/D0。"),
            ]),
            section("2", "AC に等分布荷重を受ける片端固定他端支持ばり", [
                block("problem", "長さ 2l のばり AB。A は固定端、B は単純支持端、C は A から l の位置。AC のみに等分布荷重 w。E, I は一定。原図の x は B から左向きだが、計算は A から右向きの s を使う。"),
                block("assumption", "下側引張りの曲げモーメントを正、上向き反力を正とする。A からの距離を s とし、B の変位 y(2l)=0 を使う。"),
                block("step", "原図の x（B から左向き）で切断すると、0<=x<=l では M(x)=R_B*x、l<=x<=2l では M(x)=R_B*x-w*(x-l)^2/2。たわみの基礎式は EI*y''=M。A の固定端条件は y(2l)=0, y'(2l)=0、B の支持条件は y(0)=0。"),
                block("step", "B の反力を未知とし、固定端片持ちばりの B 点たわみを重ね合わせる。AC の w によるたわみは 7*w*l^4/(24*E*I)、B の上向き反力 R_B によるたわみは 8*R_B*l^3/(3*E*I)。適合条件より R_B=7*w*l/64。"),
                block("answer", "反力 R_A=57*w*l/64、R_B=7*w*l/64。固定端外力モーメントの大きさは M_A=9*w*l^2/32（反時計回り）。A から右向き s=2l-x で書けば、内部曲げモーメントは 0<=s<=l で M(s)=-9*w*l^2/32+(57*w*l/64)*s-w*s^2/2、l<=s<=2l で M(s)=-9*w*l^2/32+(57*w*l/64)*s-w*l*(s-l/2)。"),
                block("answer", "せん断力（s を A から右向き）は 0<s<l で V=57*w*l/64-w*s、l<s<2l で V=-7*w*l/64。SFD は C で傾きがゼロになり、B で +7*w*l/64 跳ぶ。BMD は M(A)=-18*w*l^2/64、M(C)=+7*w*l^2/64、M(B)=0。原図の x を使うなら s=2l-x で、0<=x<=l では M=7*w*l*x/64、l<=x<=2l では M=w*l^2*(-32+71*x/l-32*(x/l)^2)/64。"),
            ]),
            section("3", "円棒のねじり", [
                block("problem", "直径 d の中実丸棒にねじりモーメント T。極断面二次モーメント、比ねじれ角、表面の応力状態、最大主応力を求める。"),
                block("answer", "(1) Ip=integral(r^2 dA)=pi*d^4/32。"),
                block("answer", "(2) 比ねじれ角 theta = T/(G*Ip)=32*T/(pi*G*d^4)。全長 l のねじれ角は l*theta。"),
                block("step", "(3) 半径 r のせん断応力は tau(r)=T*r/Ip で半径に比例する。表面 r=d/2 で最大。"),
                block("answer", "(3) tau_max=16*T/(pi*d^3)。表面では法線応力 0、せん断応力 tau_max の純せん断状態。"),
                block("answer", "(4) 純せん断の主応力は +tau_max と -tau_max。最大主応力 sigma_1=16*T/(pi*d^3)。"),
            ]),
        ],
    },
    2005: {
        "era": "H17",
        "question": "pdfs/question/2005_H17_april/materials_2005_H17_question.pdf",
        "sections": [
            section("1", "両端固定棒の熱応力と3区間の軸力", [
                block("problem", "直径 d の丸棒 AB を両壁に固定する。材料は E, alpha。"),
                block("answer", "(1) 温度上昇 t で両端間距離が変わらないため、0=alpha*t+sigma/E。したがって sigma=-E*alpha*t（圧縮）。"),
                block("step", "(2) 長さ 3l、断面積 A=pi*d^2/4、左から AC, CD, DB の3区間。C には左向き P、D には右向き P。引張軸力を正とする。節点の釣合いから N2=N1+P、N3=N1。両端固定の適合条件は (N1+N2+N3)*l/(A*E)=0。"),
                block("answer", "(2) N1=N3=-P/3、N2=2P/3。従って sigma_1=sigma_3=-P/(3A)=-4P/(3*pi*d^2)、sigma_2=2P/(3A)=8P/(3*pi*d^2)。"),
            ]),
            section("2", "中央区間に等分布荷重を受ける両端固定ばり", [
                block("problem", "長さ 3l の両端固定ばり AB。中央区間 CD（A から l から 2l）だけに w。対称性から R_A=R_B=w*l/2。"),
                block("assumption", "A から右向きに x、下側引張りの内部曲げモーメントを正とする。固定端の内部値を M_A と書く。"),
                block("step", "0<=x<=l では M=M_A+(w*l/2)*x。l<=x<=2l では M=M_A+(w*l/2)*x-w*(x-l)^2/2。両端固定なので y(0)=0, y'(0)=0、中央 x=3l/2 で対称性 y'(3l/2)=0。EI*y''=M を積分すると M_A=-13*w*l^2/36。"),
                block("answer", "M(x)=M_A+(w*l/2)*x（0<=x<=l）、M(x)=M_A+(w*l/2)*x-w*(x-l)^2/2（l<=x<=2l）。右半分は対称。M(C)=M(D)=5*w*l^2/36、M(中央)=19*w*l^2/72、端部内部値は -13*w*l^2/36。"),
                block("answer", "SFD は A から C まで +w*l/2、CD 上で傾き -w、D で -w*l/2、D から B まで -w*l/2。BMD は上の2式と対称性で描ける。"),
            ]),
            section("3", "3次元応力の釣合いと面応力", [
                block("problem", "点 A(x,y,z) の応力成分 sigma_x, sigma_y, sigma_z, tau_xy, tau_yz, tau_zx。物体力は無視。微小要素、法線方向 (l,m,n) の面、面の法線成分を求める。"),
                block("step", "微小直方体の各面の力を釣り合わせ、反対面の応力を一次展開する。"),
                block("answer", "(1) d(sigma_x)/dx+d(tau_xy)/dy+d(tau_zx)/dz=0、d(tau_xy)/dx+d(sigma_y)/dy+d(tau_yz)/dz=0、d(tau_zx)/dx+d(tau_yz)/dy+d(sigma_z)/dz=0。"),
                block("step", "(2) 応力テンソル S=[[sigma_x,tau_xy,tau_zx],[tau_xy,sigma_y,tau_yz],[tau_zx,tau_yz,sigma_z]]。単位法線 n=(l,m,n) に対し p=S*n。"),
                block("answer", "(2) p_x=sigma_x*l+tau_xy*m+tau_zx*n、p_y=tau_xy*l+sigma_y*m+tau_yz*n、p_z=tau_zx*l+tau_yz*m+sigma_z*n。"),
                block("answer", "(3) sigma_n=n^T*p=l*p_x+m*p_y+n*p_z。すなわち sigma_n=n^T*S*n。"),
            ]),
        ],
    },
    2006: {
        "era": "H18",
        "question": "pdfs/question/2006_H18_april/materials_2006_H18_question.pdf",
        "sections": [
            section("1", "自重を受ける柱と断面積分布", [
                block("problem", "長さ l、直径 d の柱の上に質量 M の円板を載せ、下端を固定。柱の E, 密度 rho, 線膨張係数 alpha、重力加速度 g。x は上端から下向き。"),
                block("assumption", "圧縮応力の大きさを正として計算し、符号付き応力は負とする。A=pi*d^2/4。"),
                block("answer", "(1) 自重を無視すると sigma=-M*g/A、全縮み lambda=M*g*l/(A*E)。"),
                block("step", "(2) x 断面より上側には円板 M と柱の上から x までの質量 rho*A*x がある。"),
                block("answer", "(2) sigma(x)=-(M*g/A+rho*g*x)、lambda=integral_0^l (M*g/A+rho*g*x)/E dx=M*g*l/(A*E)+rho*g*l^2/(2E)。"),
                block("step", "(3) 断面積 A(x)、上端 A(0)=A とし、圧縮応力の大きさを一定 sigma0 とする。断面の軸力は sigma0*A(x)=g*(M+rho*integral_0^x A(s) ds)。微分して sigma0*A'(x)=rho*g*A(x)。"),
                block("answer", "(3) sigma0=M*g/A。A(x)=A*exp(rho*A*x/M)。全縮み lambda=sigma0*l/E=M*g*l/(A*E)。"),
                block("answer", "(4) 温度上昇による伸び alpha*DeltaT*l と、一定圧縮応力による縮み sigma0*l/E を相殺する。DeltaT=sigma0/(E*alpha)=M*g/(A*E*alpha)。"),
            ]),
            section("2", "全長に等分布荷重を受ける3点支持ばり", [
                block("problem", "長さ 2l のばり AB を A, C, B の3点で支持し、全長に等分布荷重 w。AC=CB=l、E, I は一定。"),
                block("assumption", "A から右向きに x、下側引張りの曲げを正とする。"),
                block("step", "曲げモーメントは 0<=x<=l で M=R_A*x-w*x^2/2、l<=x<=2l で M=R_A*x+R_C*(x-l)-w*x^2/2。y(A)=y(C)=y(B)=0、対称性 y'(C)=0 を用いる。"),
                block("answer", "R_A=R_B=3*w*l/8、R_C=5*w*l/4。SFD は AC で V=3*w*l/8-w*x、CB で V=13*w*l/8-w*x。BMD は上記2式。M(C)=-w*l^2/8、正曲げ極値は x=3l/8 と 13l/8 で 9*w*l^2/128。"),
                block("answer", "円形断面直径 d の断面係数 Z=pi*d^3/32。最大曲げ応力は C の負曲げで生じ、sigma_max=(w*l^2/8)/Z=4*w*l^2/(pi*d^3)。"),
            ]),
            section("3", "薄肉円筒の軸・周方向応力", [
                block("problem", "内半径 r、肉厚 t の薄肉円筒。両端は剛体板で閉じ、外向き軸荷重 W と内圧 p。E, nu。"),
                block("assumption", "薄肉膜理論を使い、引張応力を正とする。"),
                block("answer", "(1) p=0 では sigma_z=W/(2*pi*r*t)、sigma_theta=0。epsilon_z1=W/(2*pi*r*t*E)、epsilon_theta1=-nu*W/(2*pi*r*t*E)。"),
                block("answer", "(2) W=0 では sigma_theta=p*r/t、sigma_z=p*r/(2*t)。epsilon_z2=p*r/(E*t)*(1/2-nu)、epsilon_theta2=p*r/(E*t)*(1-nu/2)。"),
                block("step", "(3) W と p の同時作用では sigma_z=W/(2*pi*r*t)+p*r/(2*t)、sigma_theta=p*r/t。半径不変 epsilon_theta=(sigma_theta-nu*sigma_z)/E=0。"),
                block("answer", "(3) W=2*pi*p*r^2*(1/nu-1/2)=pi*p*r^2*(2/nu-1)。"),
            ]),
        ],
    },
    2007: {
        "era": "H19",
        "question": "pdfs/question/2007_H19_april/materials_2007_H19_question.pdf",
        "sections": [
            section("1", "逆円すい棒の自重・温度上昇", [
                block("problem", "長さ l、上端直径 d、下端が点の円すい棒を上端で固定。E, 密度 rho, 線膨張係数 alpha、重力加速度 g。原図の矢印どおり x は下端の先端から上向きに測る。"),
                block("assumption", "上端 x=l の断面積を A0=pi*d^2/4 とする。相似より A(x)=A0*(x/l)^2。棒の軸方向を引張り正とする。"),
                block("step", "(1) x 断面より下にある円すい部分の体積は integral_0^x A(s) ds=A0*x^3/(3*l^2)。その重量を断面積 A(x) で割る。"),
                block("answer", "(1) sigma(x)=rho*g*x/3。先端で 0、上端で最大 rho*g*l/3。"),
                block("step", "(2) 自重による伸びは lambda=integral_0^l sigma(x)/E dx。"),
                block("answer", "(2) lambda=rho*g*l^2/(6E)。"),
                block("step", "(3) 一様温度上昇は自由熱ひずみ alpha*DeltaT を加える。下端は自由端なので温度上昇自体は軸応力を増やさず、応力は自重分のまま。"),
                block("answer", "(3) lambda=rho*g*l^2/(6E)+alpha*DeltaT*l、sigma_max=rho*g*l/3（上端）。"),
                block("audit", "「下方より x」は図の x 矢印が先端から上向きであることと一致する。先端側の重量を積分するため応力は rho*g*x/3 となり、有限値である。"),
            ]),
            section("2", "中央集中荷重を受ける片端固定他端支持ばり", [
                block("problem", "長さ 2l の一端固定他端支持ばり AB。中央 C に集中荷重 P。E, I は一定。"),
                block("assumption", "A から右向き x、下側引張りの内部曲げモーメントを正とする。B のたわみは 0。"),
                block("step", "片持ちばりとして、C の荷重 P による B 点たわみは 5P*l^3/(6EI)。B の上向き反力 R_B によるたわみは 8R_B*l^3/(3EI)。適合条件から R_B=5P/16。"),
                block("answer", "R_A=11P/16、R_B=5P/16、固定端外力モーメントの大きさ M_A=3P*l/8。内部 M(x)=-3P*l/8+(11P/16)*x（0<=x<=l）、M(x)=-3P*l/8+(11P/16)*x-P*(x-l)（l<=x<=2l）。"),
                block("answer", "SFD は AC で +11P/16、CB で -5P/16、B で +5P/16 跳ぶ。BMD は A で -3P*l/8、C で +5P*l/16、B で 0。"),
                block("answer", "(3) C 断面を正方形 a*a とすると Z=a^3/6。C の曲げ応力は sigma=-(M_C/Z)*(y/(a/2))、表面最大値 sigma_max(C)=|5P*l/16|/(a^3/6)=15P*l/(8a^3)。"),
                block("answer", "(4) AC 中点では V=11P/16。平均せん断応力 tau_mean=V/a^2=11P/(16a^2)、長方形断面の最大値 tau_max=3V/(2a^2)=33P/(32a^2)。"),
            ]),
            section("3", "平面応力の面応力ベクトル", [
                block("problem", "単位厚さの平板に一様な正の sigma_x, sigma_y, tau_xy。AC 面の外向き単位法線 n=(l,m)。"),
                block("answer", "(1) 応力テンソル S=[[sigma_x,tau_xy],[tau_xy,sigma_y]]。面応力ベクトル (p_x,p_y)=(l,m)*S。よって p_x=l*sigma_x+m*tau_xy、p_y=l*tau_xy+m*sigma_y。"),
                block("answer", "(2) 図の正の接線方向 t=(-m,l) とする。sigma_n=(p_x,p_y)*(l,m)^T、tau_n=(p_x,p_y)*(-m,l)^T=-m*p_x+l*p_y。"),
                block("step", "(3) sigma_n=(l,m)*S*(l,m)^T、tau_n=(l,m)*S*(-m,l)^T=(p_x,p_y)*(-m,l)^T。左の行列は面に沿った応力成分の変換、右の列は法線または接線方向の射影である。"),
                block("answer", "(4) tau_xy=0 なら p_x=sigma_x*l、p_y=sigma_y*m、l^2+m^2=1。したがって (p_x/sigma_x)^2+(p_y/sigma_y)^2=1（sigma_x,sigma_y が非零の場合）。p_x-p_y 平面では楕円。"),
            ]),
        ],
    },
    2008: {
        "era": "H20",
        "question": "pdfs/question/2008_H20_april/materials_2008_H20_question.pdf",
        "sections": [
            section("1", "段付き丸棒の軸応力と熱応力", [
                block("problem", "直径 d1、長さ l1 の棒を両端に2本、直径 d2、長さ l2 の棒を中央に1本直列につないだ段付き棒。材料定数は外側 E1, alpha1、中央 E2, alpha2。"),
                block("assumption", "A1=pi*d1^2/4、A2=pi*d2^2/4。引張力を正とする。"),
                block("answer", "(1) 両端引張荷重 P では直列なので各棒の軸力は P。sigma_1=P/A1、sigma_2=P/A2。全伸び lambda=P*(2*l1/(E1*A1)+l2/(E2*A2))。"),
                block("step", "(2) 両端固定で温度が t K 上昇。直列全体の伸びが 0。圧縮軸力を N とすると、機械的変形 N*(2*l1/(E1*A1)+l2/(E2*A2)) と熱伸び t*(2*alpha1*l1+alpha2*l2) の和が 0。"),
                block("answer", "(2) N=-t*(2*alpha1*l1+alpha2*l2)/(2*l1/(E1*A1)+l2/(E2*A2))。sigma_1=N/A1、sigma_2=N/A2（通常の正の t では圧縮）。"),
            ]),
            section("2", "ばね支持端をもつ片持ちばり", [
                block("problem", "長さ l の片持ちばり AB。A 固定、B にばね定数 k の鉛直ばねを取り付け、全長に等分布荷重 w。E, I は一定。原図は下向き y。"),
                block("assumption", "下向きたわみ y を正、内部曲げは下側引張りを正、ばね反力 R_B は上向きとする。"),
                block("step", "A から x を測ると、未知反力を含む内部曲げは M(x)=-M_A+R_A*x-w*x^2/2。A の境界は y(0)=0、y'(0)=0。B の条件は R_B=k*y(l)。"),
                block("step", "片持ちばりの B 点たわみを重ね合わせると y(l)=w*l^4/(8EI)-R_B*l^3/(3EI)。ばね条件から R_B/k=y(l)。"),
                block("answer", "R_B=3*k*w*l^4/[8*(3*E*I+k*l^3)]、y(l)=3*w*l^4/[8*(3*E*I+k*l^3)]、R_A=w*l-R_B、M_A=w*l^2/2-R_B*l。"),
                block("answer", "SFD は V(x)=R_A-w*x（0<x<l）。BMD は M(x)=-M_A+R_A*x-w*x^2/2 で、M(0)=-M_A、M(l)=0。k=0 では通常の片持ちばり、k -> infinity では剛支点の極限にも一致する。"),
            ]),
            section("3", "平面応力の一般化フック則と面応力", [
                block("problem", "等方弾性体 E, nu, G。平面応力 sigma_z=0 のもとで sigma_x, sigma_y, tau_xy とひずみ成分、面の応力ベクトルを求める。"),
                block("answer", "(1) epsilon_x=(sigma_x-nu*sigma_y)/E、epsilon_y=(sigma_y-nu*sigma_x)/E、gamma_xy=tau_xy/G。G=E/[2*(1+nu)]。"),
                block("answer", "(2) epsilon_z=-nu*(sigma_x+sigma_y)/E。"),
                block("answer", "(3) x 軸に垂直な面の法線 n=(1,0) では p1=(sigma_x,tau_xy)、|p1|=sqrt(sigma_x^2+tau_xy^2)。"),
                block("answer", "(4) y 軸に垂直な面 n=(0,1) では p2=(tau_xy,sigma_y)、|p2|=sqrt(sigma_y^2+tau_xy^2)。"),
                block("answer", "(5) 一般の n=(l,m) では p_nx=sigma_x*l+tau_xy*m、p_ny=tau_xy*l+sigma_y*m、|p_n|=sqrt(p_nx^2+p_ny^2)。"),
            ]),
        ],
    },
}


def register_font() -> None:
    if not FONT_PATH.exists():
        raise FileNotFoundError(f"Japanese font not found: {FONT_PATH}")
    pdfmetrics.registerFont(TTFont(FONT_NAME, str(FONT_PATH)))


def pdf_text(value: str) -> str:
    return html.escape(value).replace("\n", "<br/>")


def add_page_number(canvas, doc) -> None:
    canvas.saveState()
    canvas.setFont(FONT_NAME, 8)
    canvas.setFillColor(colors.HexColor("#666666"))
    canvas.drawString(18 * mm, 12 * mm, "岡山大学大学院入試 材料力学 非公式解答")
    canvas.drawRightString(192 * mm, 12 * mm, f"{doc.page}")
    canvas.restoreState()


def pdf_styles() -> dict[str, ParagraphStyle]:
    return {
        "title": ParagraphStyle("materials-title", fontName=FONT_NAME, fontSize=16, leading=22, alignment=TA_CENTER, spaceAfter=8),
        "subtitle": ParagraphStyle("materials-subtitle", fontName=FONT_NAME, fontSize=9, leading=14, alignment=TA_CENTER, textColor=colors.HexColor("#555555"), spaceAfter=12),
        "section": ParagraphStyle("materials-section", fontName=FONT_NAME, fontSize=13, leading=19, textColor=colors.HexColor("#123e57"), spaceBefore=10, spaceAfter=6),
        "problem": ParagraphStyle("materials-problem", fontName=FONT_NAME, fontSize=9.5, leading=16, leftIndent=5, rightIndent=5, spaceAfter=7),
        "assumption": ParagraphStyle("materials-assumption", fontName=FONT_NAME, fontSize=9.2, leading=15, leftIndent=9, rightIndent=5, textColor=colors.HexColor("#444444"), spaceAfter=7),
        "step": ParagraphStyle("materials-step", fontName=FONT_NAME, fontSize=9.5, leading=16, leftIndent=9, rightIndent=5, spaceAfter=7),
        "answer": ParagraphStyle("materials-answer", fontName=FONT_NAME, fontSize=9.6, leading=16, leftIndent=9, rightIndent=5, backColor=colors.HexColor("#f1f7fa"), borderColor=colors.HexColor("#b7d1dc"), borderWidth=0.4, borderPadding=5, spaceAfter=8),
        "audit": ParagraphStyle("materials-audit", fontName=FONT_NAME, fontSize=8.8, leading=14, leftIndent=9, rightIndent=5, textColor=colors.HexColor("#555555"), spaceAfter=7),
        "label": ParagraphStyle("materials-label", fontName=FONT_NAME, fontSize=8.6, leading=12, textColor=colors.HexColor("#123e57"), spaceAfter=2),
    }


def write_pdf(year: int, info: dict[str, object]) -> Path:
    out = ROOT / "pdfs" / "answer" / f"{year}_unofficial" / f"{year}_materials.pdf"
    out.parent.mkdir(parents=True, exist_ok=True)
    styles = pdf_styles()
    story = [
        Paragraph(f"材料力学 {year}年度 非公式解答・解説", styles["title"]),
        Paragraph("問題原本を読み取り、各小問を独立に再計算した学習用資料。符号規約と仮定を明記しています。", styles["subtitle"]),
    ]
    for index, sec in enumerate(info["sections"]):
        story.append(Paragraph(f"大問 {sec['number']}　{sec['title']}", styles["section"]))
        for item in sec["blocks"]:
            kind = item["kind"]
            label = {"problem": "問題の読み替え", "assumption": "仮定・符号", "step": "導出", "answer": "最終結果", "audit": "原本照合メモ"}[kind]
            story.append(KeepTogether([
                Paragraph(label, styles["label"]),
                Paragraph(pdf_text(item["text"]), styles[kind]),
            ]))
        if index != len(info["sections"]) - 1:
            story.append(Spacer(1, 4))
    doc = SimpleDocTemplate(
        str(out), pagesize=A4, rightMargin=18 * mm, leftMargin=18 * mm,
        topMargin=17 * mm, bottomMargin=19 * mm, title=f"材料力学 {year}年度 非公式解答",
        author="非公式学習資料",
    )
    doc.build(story, onFirstPage=add_page_number, onLaterPages=add_page_number)
    return out


def html_block(item: dict[str, str]) -> str:
    labels = {"problem": "問題の読み替え", "assumption": "仮定・符号", "step": "導出", "answer": "最終結果", "audit": "原本照合メモ"}
    text = html.escape(item["text"]).replace("\n", "<br>")
    return f'<div class="solution-block solution-block--{item["kind"]}"><h4>{labels[item["kind"]]}</h4><p>{text}</p></div>'


def write_html(year: int, info: dict[str, object]) -> Path:
    out = ROOT / "exams" / "materials" / f"{year}.html"
    qhref = "../../" + str(info["question"])
    ahref = f"../../pdfs/answer/{year}_unofficial/{year}_materials.pdf"
    prev_link = f'<a href="{year-1}.html">← {year-1}年度</a>' if year > 2003 else "<span></span>"
    next_link = f'<a href="{year+1}.html">{year+1}年度 →</a>' if year < 2024 else "<span></span>"
    sections = []
    for sec in info["sections"]:
        sections.append(f'<section class="solution-section" aria-labelledby="q{year}-{sec["number"]}"><h3 id="q{year}-{sec["number"]}">大問 {sec["number"]}　{html.escape(sec["title"])}</h3>{"".join(html_block(item) for item in sec["blocks"])}</section>')
    page = f'''<!DOCTYPE html>
<html lang="ja" data-page-status="available">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="岡山大学大学院入試 材料力学 {year}年度の問題原本と全問独立再計算による非公式解説。">
  <title>材料力学 {year}年度 非公式解答・解説</title>
  <link rel="stylesheet" href="../../css/style.css">
  <link rel="stylesheet" href="../../css/archive.css">
  <style>
    .solution-content {{ max-width: 1000px; margin: 0 auto; padding: 2rem 1rem 3rem; }}
    .solution-section {{ margin: 1.5rem 0; padding: 1.25rem; background: #fff; border: 1px solid #d8e3e8; border-radius: 10px; box-shadow: 0 4px 14px rgba(18,62,87,.06); }}
    .solution-section h3 {{ margin-top: 0; color: #123e57; border-bottom: 2px solid #d8e3e8; padding-bottom: .55rem; }}
    .solution-block {{ margin: .8rem 0; padding: .7rem .85rem; border-left: 4px solid #b7d1dc; }}
    .solution-block h4 {{ margin: 0 0 .35rem; font-size: .9rem; color: #345; }}
    .solution-block p {{ margin: 0; line-height: 1.8; white-space: normal; }}
    .solution-block--answer {{ background: #f1f7fa; border-left-color: #247a9b; }}
    .solution-block--assumption {{ color: #555; background: #fafafa; }}
    .solution-block--audit {{ color: #555; font-size: .92rem; background: #fffdf2; border-left-color: #caa94b; }}
    .source-note {{ max-width: 1000px; margin: 0 auto; padding: 0 1rem 1rem; color: #555; }}
    .source-note a {{ margin-right: 1rem; }}
  </style>
</head>
<body>
  <header class="header header--static"><div class="container header-content">
    <a class="logo logo-link" href="../../index.html">岡山大学大学院入試アーカイブ</a>
    <nav class="nav" aria-label="主要ナビゲーション"><ul class="nav-list">
      <li><a href="../../index.html" class="nav-link">ホーム</a></li>
      <li><a href="../../pages/material_mechanics.html" class="nav-link">材料力学一覧</a></li>
      <li><a href="../../about.html" class="nav-link">サイトについて</a></li>
    </ul></nav>
  </div></header>
  <main>
    <nav class="breadcrumb breadcrumb--static" aria-label="パンくずリスト"><div class="container"><a href="../../index.html">ホーム</a><span aria-hidden="true">/</span><a href="../../pages/material_mechanics.html">材料力学</a><span aria-hidden="true">/</span><span>{year}年度</span></div></nav>
    <section class="archive-hero"><div class="container archive-hero__inner">
      <p class="eyebrow">{year}年度（{info["era"]}）・全問再計算</p><h1>材料力学 {year}年度</h1>
      <p>問題原本の全ページを確認し、全大問・全小問を独立に導出した非公式解説です。</p>
      <div class="status-line"><span class="status-badge status-badge--available">問題・非公式解答PDF・詳細解説あり</span><span>原本を優先してご確認ください</span></div>
    </div></section>
    <section class="archive-content"><div class="container archive-layout"><div>
      <h2>原本と解答PDF</h2><div class="resource-grid">
        <a class="resource-card resource-card--question" href="{qhref}" target="_blank" rel="noopener"><span class="resource-kicker">原本</span><strong>問題PDFを開く</strong><span>全ページを確認した原本です。</span></a>
        <a class="resource-card resource-card--answer" href="{ahref}" target="_blank" rel="noopener"><span class="resource-kicker">非公式解答案</span><strong>解答PDFを開く</strong><span>このページと同じ導出を収録しています。</span></a>
      </div>
      <section class="study-guide"><h2>利用上の注意</h2><p>本ページと解答PDFは学習用の非公式資料です。記号、符号、単位、図の読み方は必ず問題原本と照合してください。</p><p>以下では各小問の問題条件、仮定、途中式、最終結果を順に示します。</p></section>
    </div><aside class="archive-note"><h2>検算状態</h2><p>問題PDFの全関連ページをPopplerで画像化して確認し、独立計算を行いました。</p><p>原本と解答PDFの疑義・解釈は監査記録に明記しています。</p><a href="../../about.html">詳しい利用案内を見る</a></aside></div></section>
    <section class="solution-content" aria-labelledby="solution-title"><h2 id="solution-title">年度別詳細解説</h2>{"".join(sections)}</section>
    <nav class="year-pagination container" aria-label="年度間ナビゲーション">{prev_link}<a href="../../pages/material_mechanics.html">年度一覧</a>{next_link}</nav>
  </main>
  <footer class="footer"><div class="container"><p class="footer-text">非公式・学習目的の岡山大学大学院入試アーカイブ</p><p class="footer-subtext">問題・解答案の正確性は必ず原本および信頼できる資料で確認してください。</p></div></footer>
</body></html>\n'''
    out.write_text(page, encoding="utf-8", newline="\n")
    return out


def main() -> None:
    register_font()
    for year, info in DATA.items():
        pdf = write_pdf(year, info)
        html_page = write_html(year, info)
        print(f"{year}: {pdf} ; {html_page}")


if __name__ == "__main__":
    main()
