import numpy as np
import matplotlib.pyplot as plt

plt.rcParams["figure.figsize"] = (10,6)

def pltplane(display):
    """
    変数displayから、描画するxy面の各成分に対応する粒子座標成分を記す

    Args:
        display int : xy面それぞれに対応する粒子の座標成分を指定 (1:x, 2:y, 3:z)
                    -> 例：13 ... x-z面内の軌跡
    """
    ix = int(str(display)[0])-1
    iy = int(str(display)[1])-1
    label = ['x', 'y', 'z']
    return(ix, iy, label[ix], label[iy])

def traceplot(data, interval=0.01, display=12):
    """
    粒子軌道を時間とともにトレースしながら描画.

    Args:
        data           : testparticleクラスのインスタンス
        interval float : 時間ステップ毎の線画の時間間隔（単位：秒、デフォルトは0.01）
        display  int   : 関数pltplane参照（デフォルトは12）
    """

    fig, ax = plt.subplots(1,1)

    ix, iy, labelx, labely = pltplane(display)
    xmin = np.min(data.r[:,ix])
    xmax = np.max(data.r[:,ix])
    ymin = np.min(data.r[:,iy])
    ymax = np.max(data.r[:,iy])
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)
    ax.set_xlabel(labelx)
    ax.set_ylabel(labely)
    plt.tight_layout()

    for i in range(data.itmax):
        #line, = ax.plot(data.r[0:i,ix], data.r[0:i,iy], color='b')
        point, = ax.plot(data.r[i,ix], data.r[i,iy], color='b', marker='o', markersize=10)
        plt.pause(interval)
        if i < data.itmax-1:
            #line.remove()
            point.remove()
    ax.plot(data.r[:,ix], data.r[:,iy], color='k', linestyle='--', lw=1)

def orbplot(data, display=12, show_label=True):
    """
    計算結果から粒子軌道を描く

    Args:
        display int     : xy面それぞれに対応する粒子の座標成分を指定 (1:x, 2:y, 3:z)
        show_label bool : 複数の粒子軌道を描く場合にはFalseを指定することでラベルを省略
    """
    ix, iy, labelx, labely = pltplane(display)
    plt.plot(data.r[:,ix], data.r[:,iy])
    if(show_label):
        plt.xlabel(labelx)
        plt.ylabel(labely)
    plt.tight_layout()

def energycheck(data):
    """
    粒子の運動エネルギーの初期値からのずれの時間発展をグラフにする
    """
    e0 = data.v[0,0]**2 + data.v[0,1]**2 + data.v[0,2]**2
    energy = data.v[:,0]**2 + data.v[:,1]**2 + data.v[:,2]**2
    plt.plot(data.time, (energy-e0)/e0)
    plt.xlabel('Time')
    plt.ylabel(r'$\Delta E/E_0$')
    plt.tight_layout()
