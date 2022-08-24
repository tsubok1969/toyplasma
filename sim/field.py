import numpy as np

def emfld(r, type=0):
    """
    テスト粒子計算用の電磁場プロファイルの指定.

    Args:
        r float  : 粒子位置（要素数3の配列、[x, y, z]=[r[0], r[1], r[2]）
        type int : プロファイルの指定（ここで利用者がカスタマイズ）

    Returns:
        mf float : 磁場（要素数3の配列）
        ef float : 電場（要素数3の配列）
    """
    if type==0: # simple gyration
        bx = by = 0.0
        bz = 1.0
        ex = ey = ez = 0.0
    elif type==1: # ExB drift
        bx = by = 0.0
        bz = 1.0
        ex = ez = 0.0
        ey = 0.1
    elif type==2: # gradient drift
        b1 = 1.0
        b2 = 3.5
        bx = by = 0.0
        bz = 0.5*(b2-b1)*(r[0]>0)+b1
        ex = ez = 0.0
        ey = 0.0
    elif type==3:
        print('Comment out this line when you use your customized profile')
        # your customization here

    mf = np.array([bx, by, bz])
    ef = np.array([ex, ey, ez])
    return(mf, ef)
