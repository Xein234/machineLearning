import numpy as np
from  itertools import combinations
from statistics import mean
from itertools import product as cartesianProduct


def minkowsky(a,b):
    return Cluster.minkowsky(*Cluster._initVectors(a,b))

def manhattan(a,b):
    return Cluster.manhattan(*Cluster._initVectors(a,b))


class Cluster:
    def __init__(self, *vectors, distanceMetric='minkowsky', linkage='average'):
        self.vectors = self._initVectors(*vectors)
        assert linkage in {'single', 'complete', 'average'}
        assert distanceMetric in {'manhattan', 'minkowsky'}
        self.distanceMetric = distanceMetric
        self.linkage = linkage

    @staticmethod
    def _initVectors(*vectors):
        assert len(vectors) > 0
        assert any(map(len,vectors))
        formerElementLen = len(vectors[0])
        for v in vectors[1:]:
            assert len(v) == formerElementLen
            formerElementLen = len(v)

        return tuple(np.array(v) for v in vectors)


    @staticmethod
    def minkowsky(a,b):
        return (sum(  abs(a-b)**len(a)  ))**(1/len(a))

    @staticmethod
    def manhattan(a,b):
        return sum(abs(a-b))

    # def mergeClosest(*clusters):
    #TODO: sacar el producto carteciano y unir el par mas cercano

    def distance(self, other:'Cluster'):
        #TODO:optimize latter
        allLinkageDists = [getattr(self, self.distanceMetric)(a,b) for a,b in
                          cartesianProduct(self.vectors, other.vectors)]
        #pero te puedes ahorrar la mitad ^^^^^ (cual seria el nombre de esa f.?)
        import ipdb;ipdb.set_trace()
        return {'single':  min(allLinkageDists),
                'complete':max(allLinkageDists),
                'average': mean(allLinkageDists)}[self.linkage]
        
        
if __name__ == '__main__':
    # import ipdb; ipdb.set_trace()
    vectors1 = (0,0),(2,2)
    vectors2 = (5,3),(-1,-1),(1,1)
    assert minkowsky(*vectors1) == 2* 2**(1/2)

    cluster1 = Cluster(*vectors1)
    cluster2 = Cluster(*vectors2)

    cluster1.distance(cluster2)
    cluster2.distanceMetric, cluster2.distanceMetric = ('manhattan',)*2
    # import ipdb; ipdb.set_trace()
    cluster2.distance(cluster1)
    cluster2.distance(cluster2)
