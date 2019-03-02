#    Copyright (C) 2019 Greenweaves Software Limited
#
#    This is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This software is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with GNU Emacs.  If not, see <http://www.gnu.org/licenses/>

from align import create_distance_matrix
from Bio.SubsMat.MatrixInfo import blosum62
import numpy as np

# https://web.stanford.edu/class/cs262/presentations/lecture2.pdf

def san_kai(s,t, replace_score=blosum62,sigma=11,epsilon=1):
    def score(pair):
        def reverse(pair):
            a,b=pair
            return (b,a)
        return replace_score[pair] if pair in replace_score else replace_score[reverse(pair)]     
    F     = create_distance_matrix(len(s)+1,len(t)+1)
    G     = create_distance_matrix(len(s)+1,len(t)+1)
    H     = create_distance_matrix(len(s)+1,len(t)+1)
    V     = create_distance_matrix(len(s)+1,len(t)+1)
    moves = {}
    for i in range(1,len(s)+1):
        V[i][0] = - (sigma + epsilon *(i-1))
        
    for j in range(1,len(t)+1):
        V[0][j] = - (sigma + epsilon *(j-1))
        
    for i in range(1,len(s)+1):
        for j in range(1,len(t)+1):
            history = []
            F[i][j] = V[i-1][j-1] + score((s[i-1],t[j-1]))
            history.append((i-1,j-1,s[i-1],t[j-1]))
            G[i][j] = max(V[i-1][j]-sigma, G[i-1][j]-epsilon)
            history.append((i-1,j,s[i-1],'-'))
            H[i][j] = max(V[i][j-1]-sigma, H[i][j-1]-epsilon)
            history.append((i,j-1,'-',t[j-1]))
            choices = [F[i][j], G[i][j], H[i][j]]
            index   = np.argmax(choices)
            V[i][j] = choices[index]
            moves[(i,j)] = history[index]
    
    i  = len(s)
    j  = len(t)
    ss = []
    ts = []
    while i>0 and j > 0:
        i,j,s0,t0=moves[(i,j)]
        ss.append(s0)
        ts.append(t0)
    return V[len(s)][len(t)],ss[::-1],ts[::-1]

def ba5j(s,t):
    score,s1,t1 = san_kai([s0 for s0 in s],[t0 for t0 in t])
    return score,''.join(s1),''.join(t1)

if __name__=='__main__':
    import os, os.path
    with open(os.path.join(r'C:\Users\Simon\Downloads','rosalind_ba5j(4).txt'),'r') as f:
        strings=[]
        for line in f:
            strings.append(line.strip())
        score,s,t=ba5j(strings[0],strings[1])
        with open('ba5j.txt','w') as o:
            o.write('{0}\n'.format(score))
            o.write('{0}\n'.format(s))
            o.write('{0}\n'.format(t))