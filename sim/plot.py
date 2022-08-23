import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

#plt.rcParams["figure.figsize"] = (10,6)

def pltplane(display):
    """
    変数displayから、描画するxy面の各成分に対応する粒子座標成分を抽出する

    Args:
        display int : xy面それぞれに対応する粒子の座標成分を指定 (1:x, 2:y, 3:z)
                    -> 例：13 ... x-z面内の軌跡
    """
    ix = int(str(display)[0])-1
    iy = int(str(display)[1])-1
    label = ['x', 'y', 'z']
    return(ix, iy, label[ix], label[iy])

def get_minmax(data, ix, iy):
    xyminmax = np.min(data.r[:,ix]), np.max(data.r[:,ix]), np.min(data.r[:,iy]), np.max(data.r[:,iy])
    return xyminmax

# ver.2
def framesize(xyminmax, max_size=6):
    """
    アスペクト比を揃えた図のサイズを取得

    Args:
        xyminmax float(4) : 作図する計算データのx, yそれぞれの最小・最大値（get_minmaxで取得しておく　）
        max_size float    : 大きい方の軸のサイズ（デフォルトは10）

    Returns:
        xf, yf float : plt.figure(figsize=(xf, yf))となる
    """
    aspect_ratio = (xyminmax[3]-xyminmax[2])/(xyminmax[1]-xyminmax[0])
    if aspect_ratio < 1:
        xf = max_size
        yf = xf*aspect_ratio
    else:
        yf = max_size
        xf = yf/aspect_ratio
    return xf, yf

# ver.1
def traceplot(data, interval=0.01, display=12, skip=20, max_size=6):
    """
    粒子軌道を時間とともにトレースしながら描画.

    Args:
        data           : testparticleクラスのインスタンス
        interval float : 時間ステップ毎の線画の時間間隔（単位：秒、デフォルトは0.01）
        display  int   : 関数pltplane参照（デフォルトは12）
        skip int       : スキップするステップ数（描画の時間短縮のため。デフォルトは20）
        max_size int   : アスペクト比で大きい次元側の図の出力サイズ（デフォルトは6）
    """

    ix, iy, labelx, labely = pltplane(display)
    xyminmax = get_minmax(data, ix, iy)
    xf, yf = framesize(xyminmax, max_size=max_size)

    #fig, ax = plt.subplots(1,1)
    fig = plt.figure(figsize=(xf, yf))
    ax = fig.subplots(1,1)
    ax.set_xlim(xyminmax[0], xyminmax[1])
    ax.set_ylim(xyminmax[2], xyminmax[3])
    ax.set_xlabel(labelx)
    ax.set_ylabel(labely)
    plt.tight_layout()

    for i in range(0, data.itmax, skip):
        line, = ax.plot(data.r[0:i,ix], data.r[0:i,iy], color='k', linestyle='--', lw=1)
        point, = ax.plot(data.r[i,ix], data.r[i,iy], color='k', marker='o', markersize=10)
        plt.pause(interval)
        if i < data.itmax-1:
            line.remove()
            point.remove()
    ax.plot(data.r[:,ix], data.r[:,iy], color='k', linestyle='--', lw=1)
    ax.plot(data.r[data.itmax-1, ix], data.r[data.itmax-1, iy], color='k', marker='o', markersize=10)

# ver.2
def traceplot2(data, interval=100, display=12, skip=20, max_size=6, save=False, filename='trace.mp4', auto_scale=True):
    """
    粒子軌道を時間とともにトレースしながら描画（動画保存にも対応：要ffmpeg or ImageMagick） 
    保存するファイルはmp4前提、動画GIFにするならani.save(..., write='***')のところをimagemagickにする

    Args:
        data            : testparticleクラスのインスタンス
        interval float  : ファイル保存時の時間ステップ毎の線画の時間間隔（単位：ms、デフォルトは100）
        display  int    : 関数pltplane参照（デフォルトは12）
        skip int        : スキップするステップ数（描画の時間短縮のため。デフォルトは20）
        max_size int    : アスペクト比で大きい次元側の図の出力サイズ（デフォルトは6）
        save bool       : ファイルに保存する場合はTrue（デフォルトはFalse〜画面に表示する）
        filename str    : 保存するときのファイル名（デフォルトは'trace.mp4'）
        auto_scale bool : Trueの場合、描画範囲をデータの最大・最小値で定める（Falseの場合、xmin, xmax, ymin, ymaxの入力を促される）
    """

    ix, iy, labelx, labely = pltplane(display)
    if auto_scale:
        xyminmax = get_minmax(data, ix, iy)
    else:
        print('Input the plot range: xmin, xmax, ymin, ymax')
        xmin, xmax, ymin, ymax = map(float, input().split())
        xyminmax = xmin, xmax, ymin, ymax
    xf, yf = framesize(xyminmax, max_size=max_size)

    fig = plt.figure(figsize=(xf, yf))
    ax = fig.subplots()

    ax.set_xlim(xyminmax[0], xyminmax[1])
    ax.set_ylim(xyminmax[2], xyminmax[3])
    ax.set_xlabel(labelx)
    ax.set_ylabel(labely)

    if save:
        ims = []

    for i in range(0, data.itmax, skip):
        line, = ax.plot(data.r[0:i,ix], data.r[0:i,iy], color='k', linestyle='--', lw=1)
        point, = ax.plot(data.r[i,ix], data.r[i,iy], color='k', marker='o', markersize=10)
        plt.tight_layout()
        if save:
            ims.append([line, point])
        else:
            plt.pause(0.01)
            line.remove()
            point.remove()
    if save:
        ani = animation.ArtistAnimation(fig, ims, interval=interval)
        ani.save(filename, writer='ffmpeg')
    else:
        ax.plot(data.r[:,ix], data.r[:,iy], color='k', linestyle='--', lw=1)
        ax.plot(data.r[data.itmax-1, ix], data.r[data.itmax-1, iy], color='k', marker='o', markersize=10)
        plt.tight_layout()

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
