import numpy as np
from itertools import combinations
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
        assert len(vectors[0]) > 0
        assert all(len(vectors[0]) == len(vector) for vector in vectors[1:])

        key = lambda v: list(v) if isinstance(v, np.ndarray) else v
        return tuple(sorted(vectors, key=key))
            

    @staticmethod
    def minkowsky(a,b):
        return (sum(  abs(a-b)**len(a)  ))**(1/len(a))

    @staticmethod
    def manhattan(a,b):
        return sum(abs(a-b))

    # tuple collecting helps here. (?)
    def findClosests(*clusters):
        _assertAllSame(map(lambda x: getattr(x, 'distanceMetric'), clusters))
        combinationsBetween2Clusters = combinations(clusters, 2)
        return min(((  a.distance(b), (a,b)) for a,b in combinations(
                   clusters, 2  )), key=lambda x: x[0])

    def __iter__(self): return iter(self.vectors)

    def __or__(self, other):
        return self.__class__(*(tuple(self)+tuple(other)))

    def mergeClosests(*clusters):
        '''returns a tuple of the_2_closests_Clusters_merged_in_to_1, followed
        by the_other_clusters_that_weren't_merged'''
        _assertAllSame(map(lambda x: hasattr(x, 'findClosests'), clusters))
        return set(clusters) - set(clusters[0].findClosests(*clusters))
        #special case: len(clusters)==0
        #i think mergeClosests and findClosests must be in other class

    def distance(self, other):
        allLinkageDists = [getattr(self, self.distanceMetric)(a,b) for a,b in
                          cartesianProduct(self.vectors, other.vectors)]
        # import ipdb;ipdb.set_trace()
        return {'single':  min(allLinkageDists),
                'complete':max(allLinkageDists),
                'average': mean(allLinkageDists)}[self.linkage]
        
    def __repr__(self):
        #this is a good solution, sublclassing np.array or
        #np.ndarray for a custom repr or str method, is too wierd DO NOT TRY IT
        #LMAO, it requires too much knowledge and reading by me and other
        #people reading this code
        def reguarlySpacedVectorRepr(vector):
            return '[%s]' % ', '.join(map(repr, vector))
        return 'C{%s}' % ', '.join(map(reguarlySpacedVectorRepr, self.vectors))

    def __eq__(self, other):
        return set(tuple(e) for e in self) == set(tuple(e) for e in other)
    
class ClusterGrop:
    def __init__(self, *clusters):
        self.clusters = clusters
    
        
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

    # Cluster((1,2),(2,3)) | Cluster([1]) -> assertion Error
    assert Cluster([3, 3]) == Cluster([3, 3])
    assert Cluster([1]) == Cluster([1])
    assert Cluster([3, 3], [3, 3], [3, 3]) == Cluster([3, 3], [3, 3], [3, 3])
    assert Cluster((2, 2)) | Cluster((3, 3)) == Cluster([2,2],[3,3])
    assert cluster1 | {(1,2)} == Cluster([0, 0], [2, 2], [1, 2])
    # import ipdb; ipdb.set_trace()
    #the string of the following is wrong
    cluster3 = Cluster([-10,-9], [-11, -12])
    import ipdb; ipdb.set_trace()
    repr(cluster3)
    #[repr(e) for e in arr]
