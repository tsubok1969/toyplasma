import numpy as np
from tqdm import trange
#import matplotlib.pyplot as plt

import sim.field as field
import sim.plot as plot
import sim.engine as eng

class testparticle():
    """
    テスト粒子の軌道計算を行う。
    インスタンス作成時に、時間ステップ幅・総時間ステップ数・初期位置、速度・電磁場プロファイル・電荷・質量を入力
    """
    def __init__(self, dt=None, itmax=None, r0=None, v0=None, type=None, charge=1.0, mass=1.0):
        if dt==None:
            print('Delta T:')
            self.dt = float(input())
        else:
            self.dt = dt
        if itmax==None:
            print('Number of steps:')
            self.itmax = int(input())
        else:
            self.itmax = itmax
        if r0==None:
            print('Initial position (x, y, z):')
            x, y, z = map(float, input().split())
            self.r0 = np.array([x, y, z])
        else:
            self.r0 = r0
        if v0==None:
            print('Initial velocity (vx, vy, vz):')
            x, y, z = map(float, input().split())
            self.v0 = np.array([x, y, z])
        else:
            self.v0 = v0
        if type==None:
            print('Choose the field profile')
            print('1: simple gyration')
            print('2: ExB drift')
            print('3: gradient drift')
            print('4: Your customization')
            self.type = int(input())-1

        self.charge = charge
        self.mass = mass

    def run(self, mode='show', interval=0.01):
        """
        指定された時間ステップ数まで運動を更新する

        Args:
            mode int        : デフォルトで'show'...粒子軌道の線画も行う
                            -> 'trace'...粒子軌道をトレースしながら表示する
            interval  float : 時間ステップ毎の線画の時間間隔
        """
        r = rtmp = np.array(self.r0)
        v = vtmp = np.array(self.v0)
        time = 0.0
        for i in trange(self.itmax-1):
            #rtmp, vtmp = self.RungeKutta(rtmp, vtmp)
            rtmp, vtmp = eng.RungeKutta(self, rtmp, vtmp)
            r = np.append(r, rtmp)
            v = np.append(v, vtmp)
            time = np.append(time, (i+1)*self.dt)

        r = r.reshape(self.itmax, 3)
        v = v.reshape(self.itmax, 3)

        self.r = r
        self.v = v
        self.time = time
        
        if mode=='show':
            plot.orbplot(self)
        elif mode=='trace':
            plot.traceplot(self, interval=interval)
