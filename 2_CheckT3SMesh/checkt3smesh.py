#!/usr/bin/env python3
# coding: utf-8
import time
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
from scipy.spatial import ConvexHull
from numba import njit, prange


def main():
    fname = input('Enter mesh filename (with extension): ')
    try:
        with open(fname, 'r') as f:
            fbc = input('Enter boundary filename (with extension): ')
            try:
                bc = np.loadtxt(fbc)[:,-2].astype(np.int64)
            except IOError:
                bc = np.zeros(0, dtype=np.int64)
                print('\'' + fbc + '\' not found: ignoring boundary nodes')
                pass
            print('Analyzing mesh...')
            Nnode = np.nan
            Nelem = np.nan
            Ncomm = 0
            for line in f:
                if line.startswith('#') or line.startswith(':'):
                    Ncomm += 1
                if ':NodeCount' in line:
                    Nnode = np.int64(line.split()[-1])
                if ':ElementCount' in line:
                    Nelem = np.int64(line.split()[-1])
                if np.isnan(Nnode) is False and np.isnan(Nelem) is False:
                    break
            if np.isnan(Nnode) or np.isnan(Nelem):
                if np.isnan(Nnode):
                    print('NodeCount not found\nAdd this \':NodeCount X\' to top of file, X is an integer')
                if np.isnan(Nelem):
                    print('ElementCount not found\nAdd this \':ElementCount X\' to top of file, X is an integer')
                return
    except FileNotFoundError:
        print('\'' + fname + '\' not found')
        return
        
    node = np.loadtxt(fname,comments=[':','#'],max_rows=Nnode)[:,:2]
    elem = np.loadtxt(fname,comments=[':','#'],skiprows=Nnode+Ncomm,dtype=np.int64)

    @njit()
    def vor(Nnode,Nelem,node,elem,bc):
        counts = np.zeros(Nnode, dtype=np.int64)
        for i in range(Nnode):
            counts[i] = elem.flatten()[elem.flatten()==i+1].size
            if bc[bc==i+1].size > 0:
                counts[i] += 3
        polygonXYList = []
        x, y = node[:,0], node[:,1]
        for i in range(Nnode):
            polygonXY = np.zeros((counts[i],2))
            k = 0
            for j in range(Nelem):
                if elem[j][elem[j]==i+1].size > 0:
                    a, b, c = elem[j] - 1
                    polygonXY[k,:] = np.linalg.solve(np.array([[x[a]-x[b],y[a]-y[b]],[x[a]-x[c],y[a]-y[c]]]), np.array([(x[a]**2-x[b]**2+y[a]**2-y[b]**2)/2,(x[a]**2-x[c]**2+y[a]**2-y[c]**2)/2]))
                    k += 1
                    if bc[bc==i+1].size == 1:
                        for p, q in zip([a,b,c], [b,c,a]):
                            if bc[bc==p+1].size == 1 and bc[bc==q+1].size == 1:
                                d = p if q == i else q
                                polygonXY[k,:] = np.array([(x[i]+x[d])/2, (y[i]+y[d])/2])
                                k += 1
                        if k == counts[i] - 1:
                            polygonXY[k,:] = np.array([x[i], y[i]])
                            break
                    else:
                        if k == counts[i]:
                            break
            if bc.size > 0:
                polygonXYList.append(polygonXY)
            else:
                if polygonXY[:,0].size > 2:
                    polygonXYList.append(polygonXY)
        return polygonXYList

    print('NodeCount %d' % Nnode)
    print('ElementCount %d' % Nelem)
    print('Computing Voronoi diagram...')
    start = time.time()
    polygonXYList = vor(Nnode,Nelem,node,elem,bc)
    print('Computation time cost = %.3f sec' % (time.time() - start))
    print('Now plotting...')

    patches = []
    for polygonXY in polygonXYList:
        hull = ConvexHull(polygonXY)
        patches.append(Polygon(polygonXY[hull.vertices,:], closed=True))   
    p = PatchCollection(patches, cmap=matplotlib.cm.copper, alpha=.5, edgecolors='grey')
    p.set_array(np.array(100*np.random.rand(len(patches))))
    
    fig, ax = plt.subplots(figsize=(9,9))
    ax.add_collection(p)

    patches = []
    for i in range(Nelem):
        tri = np.zeros((3,2))
        for j in range(3):
            tri[j] = node[elem[i,j]-1]
        patches.append(Polygon(tri, closed=True))
    p = PatchCollection(patches, edgecolors='k', linewidths=.2, facecolors='none')
    ax.add_collection(p)
        
    plt.axis('equal')
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    main()
