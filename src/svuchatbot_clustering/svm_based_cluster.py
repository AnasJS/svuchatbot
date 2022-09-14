from sklearn import svm

class MySVM:
    def __init__(self, X, Y):
        self.X = X
        self.Y = Y
        self.clf = svm.SVC()

    def fit(self):
        print(self.X)
        print(self.Y)
        self.clf.fit(self.X, self.Y)

    def predict(self, X):
        print(self.clf)
        self.clf.predict(X)

#**************************************************************

X = [[0, 0], [1, 1]]
y = [0, 1]
_svm = MySVM(X, y)

_svm.fit()
_svm.predict([1., 2.])