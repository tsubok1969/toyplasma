import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D

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

def traceplot(data, interval=200, display=12, skip=100, auto_scale=True, max_size=6, \
    save=False, filename='trace', gif=False):
    """
    粒子軌道を時間とともにトレースしながら描画（動画保存にも対応：要ffmpeg or ImageMagick） 
    保存するファイルはmp4前提、動画GIFにするならani.save(..., write='***')のところをimagemagickにする

    Args:
        data            : testparticleクラスのインスタンス
        interval float  : ファイル保存時の時間ステップ毎の線画の時間間隔（単位：ms、デフォルトは200）
        display  int    : 関数pltplane参照（デフォルトは12）
        skip int        : スキップするステップ数（描画の時間短縮のため。デフォルトは100）
        auto_scale bool : Trueの場合、描画範囲をデータの最大・最小値で定める（Falseの場合、xmin, xmax, ymin, ymaxの入力を促される）
        max_size int    : アスペクト比で大きい次元側の図の出力サイズ（デフォルトは6）
        save bool       : ファイルに保存する場合はTrue（デフォルトはFalse〜画面に表示する）
        filename str    : 保存するときのファイル名（デフォルトは'trace'）
        gif bool        : Trueの場合、動画GIFで保存する

    Examples:
        計算済みのインスタンスdataを用い、yx面内の軌道を50ステップおきに表示する動画を'hoge.mp4'として保存する
        >>> plot.traceplot(data, interval=100, display=21, skip=50, save=True, filename='hoge')
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
        if gif:
            file = filename + '.gif'
            writer = 'imagemagick'
        else:
            file = filename + '.mp4'
            writer = 'ffmpeg'
        ani.save(file, writer=writer)
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

    Examples:
        計算済みのインスタンスdataを用い、xz面内の軌道を描く
        >>> plot.orbplot(data, display=13)
    """
    ix, iy, labelx, labely = pltplane(display)
    plt.plot(data.r[:,ix], data.r[:,iy])
    if(show_label):
        plt.xlabel(labelx)
        plt.ylabel(labely)
    plt.tight_layout()

def traceplot3d(data, interval=200, skip=100, auto_scale=True, max_size=6, azim=60.0, elev=20.0, \
    save=False, filename='trace', gif=False):
    """
    粒子軌道を3次元空間内で時間とともにトレースしながら描画

    Args: (traceplotと共通以外)
        elev float : 3D視点の仰角
        azim float : 3D視点の方位角

    Examples:
        計算済みのインスタンスdataを用い、200ステップおきに軌道を表示する動画を'orbit.gif'に保存する
        >>> plot.traceplot3d(data, skip=200, filename='orbit', gif=True)
    """
    fig = plt.figure(figsize=(max_size, max_size))
    ax = fig.add_subplot(projection='3d')

    if auto_scale:
        xyminmax = get_minmax(data, 0, 1)
        yzminmax = get_minmax(data, 1, 2)
    else:
        print('Input the plot range: xmin, xmax, ymin, ymax, zmin, zmax')
        xmin, xmax, ymin, ymax, zmin, zmax = map(float, input().split())
        xyminmax = xmin, xmax, ymin, ymax
        yzminmax = ymin, ymax, zmin, zmax

    ax.set_xlim(xyminmax[0], xyminmax[1])
    ax.set_ylim(xyminmax[2], xyminmax[3])
    ax.set_zlim(yzminmax[2], yzminmax[3])
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    ax.view_init(elev=elev, azim=azim)

    if save:
        ims = []

    for i in range(0, data.itmax, skip):
        line, = ax.plot3D(data.r[0:i,0], data.r[0:i,1], data.r[0:i,2], color='k', linestyle='--', lw=1)
        point, = ax.plot3D(data.r[i,0], data.r[i,1], data.r[i,2], color='k', marker='o', markersize=10)
        if save:
            ims.append([line, point])
        else:
            plt.pause(0.01)
            line.remove()
            point.remove()
    if save:
        ani = animation.ArtistAnimation(fig, ims, interval=interval)
        if gif:
            file = filename + '.gif'
            writer = 'imagemagick'
        else:
            file = filename + '.mp4'
            writer = 'ffmpeg'
        ani.save(file, writer=writer)
    ax.plot3D(data.r[:,0], data.r[:,1], data.r[:,2], color='k', linestyle='--', lw=1)
    ax.plot3D(data.r[data.itmax-1,0], data.r[data.itmax-1,1], data.r[data.itmax-1,2], color='k', marker='o', markersize=10)

def orbplot3d(data, show_label=True, max_size=6, azim=60.0, elev=20.0):
    """
    3次元空間内の粒子軌道を描く

    Args: (orbplotと共通以外)
        elev float : 3D視点の仰角
        azim float : 3D視点の方位角
    """
    fig = plt.figure(figsize=(max_size, max_size))
    ax = fig.add_subplot(projection='3d')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    ax.view_init(elev=elev, azim=azim)

    ax.plot3D(data.r[:,0], data.r[:,1], data.r[:,2], color='k', lw=1)
    ax.plot3D(data.r[0,0], data.r[0,1], data.r[0,2], color='b', marker='o', markersize=10)
    ax.plot3D(data.r[data.itmax-1,0], data.r[data.itmax-1,1], data.r[data.itmax-1,2], color='r', marker='o', markersize=10)
    plt.tight_layout()

def energycheck(data, dev=True):
    """
    粒子の運動エネルギーの時間発展をプロット
    
    Arggs:
        data     : testparticleクラスのインスタンス
        dev bool : Trueでは初期値からのずれ（デフォルト）、Falseではv^2
    """
    e0 = data.v[0,0]**2 + data.v[0,1]**2 + data.v[0,2]**2
    energy = data.v[:,0]**2 + data.v[:,1]**2 + data.v[:,2]**2
    if dev:
        y = (energy - e0)/e0
        labely = r'$\Delta E/E_0$'
    else:
        y = energy
        labely = r'$E$'
    #plt.plot(data.time, (energy-e0)/e0)
    plt.plot(data.time, y)
    plt.xlabel('Time')
    #plt.ylabel(r'$\Delta E/E_0$')
    plt.ylabel(labely)
    plt.tight_layout()
