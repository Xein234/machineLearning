import machineLearning as ml
import pytest as pt
def func(x):
    return x + 1

# def test_answer():
#     assert func(3) == 5

# def test_2():
#     assert func(4) == 5

def testClusterCreationAndEquals():
    assert ml.Cluster([1]) == ml.Cluster([1])
    assert ml.Cluster([3,3]) == ml.Cluster([3,3])
    assert ml.Cluster([3,3], [3,3], [3,3]) == ml.Cluster([3,3], [3,3], [3,3])
    assert ml.Cluster([2,2], [3,3]) == ml.Cluster([3,3], [2,2])

def testClusterRaises():
    with pt.raises(BaseException): ml.Cluster()
