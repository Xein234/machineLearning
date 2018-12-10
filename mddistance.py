import numpy as np
from  itertools import combinations
from statistics import mean
from itertools import product as cartesianProduct

# *tuple vs tuple
def _assertAllSame(iterable):
    iterator = iter(iterable)
    try:
        formerElement = next(iterator)
    #make more especifict this except
    except:
        return
    for e in iterator:
        assert e == formerElement
        formerElement = e


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
        _assertAllSame(map(len, vectors))

        return tuple(np.array(v) for v in vectors)


    @staticmethod
    def minkowsky(a,b):
        return (sum(  abs(a-b)**len(a)  ))**(1/len(a))

    @staticmethod
    def manhattan(a,b):
        return sum(abs(a-b))

    def findClosests(*clusters):
    #TODO: sacar el producto carteciano y unir el par mas cercano
        #aquí si puedes optimizar.
        # map(self.distance, combinations(clusters, 2))
        _assertAllSame(map(lambda x: getattr(x, 'distanceMetric'), clusters))
        combinationsBetween2Clusters = combinations(clusters, 2)
        return min(((  a.distance(b), (a,b)) for a,b in combinations(
                   clusters, 2  )), key=lambda x: x[0])

    def distance(self, other:'Cluster'):
        #TODO:optimize latter
        allLinkageDists = [getattr(self, self.distanceMetric)(a,b) for a,b in
                          cartesianProduct(self.vectors, other.vectors)]
        import ipdb;ipdb.set_trace()
        return {'single':  min(allLinkageDists),
                'complete':max(allLinkageDists),
                'average': mean(allLinkageDists)}[self.linkage]
        
        # make a func that uses pipe to merge 2 clusters
        
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
