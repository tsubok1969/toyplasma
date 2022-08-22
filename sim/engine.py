import numpy as np
import sim.field as field

def eqm(data, r, v):
    """
    ローレンツ力の運動方程式で、位置・速度情報をdt進める.

    Args:
        data : 計算用クラス（testparticle）のインスタンス
        r float : 粒子位置 (要素数3の配列 [x, y, z]=[r[0], r[1], r[2]])
        v float : 粒子速度 (要素数3の配列 [vx, vy, vz]=[v[0], v[1], v[2]])

    Returns:
        rr float : 更新された位置
        vr float : 更新された速度
    """
    mf, ef = field.emfld(r, data.type)

    vr = data.charge/data.mass * (np.cross(v, mf) + ef) * data.dt
    rr = v * data.dt
    return(rr, vr)

def RungeKutta(data, r, v):
    """
    Runge-Kutta法による近似解.

    Args:
        data : 計算用クラス（testparticle）のインスタンス
        r : 粒子位置（要素数3の配列、[x, y, z]=[r[0], r[1], r[2]]）
        v : 粒子速度（要素数3の配列、[vx, vy, vz]=[v[0], v[1], v[2]]）

    Returns:
        rout : dt更新後の粒子位置の近似解
        vout : dt更新後の粒子速度の近似解
    """
    r1, v1 = eqm(data, r, v)
    r2, v2 = eqm(data, r+0.5*r1, v+0.5*v1)
    r3, v3 = eqm(data, r+0.5*r2, v+0.5*v2)
    r4, v4 = eqm(data, r+r3, v+v3)
    rout = r + (r1 + 2.0*r2 + 2.0*r3 + r4)/6.0
    vout = v + (v1 + 2.0*v2 + 2.0*v3 + v4)/6.0
    return(rout, vout)
