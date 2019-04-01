import numpy as np
import matplotlib.pyplot as plt
from ToolBox import ToolBox


class CPA():

    hypothesis = None
    plainTexts = None
    tracesPoints = None
    key = None
    matrixRelations = []
    toolbox = ToolBox()

    def __init__(self, keySize=16):
        self.key = np.zeros(keySize)

    def setTracesPointsAndPT(self, tracesPoints, plainTexts):

        self.tracesPoints = tracesPoints
        self.plainTexts = plainTexts

    def Analyse(self):

        key = ""

        for i in range(1, len(self.key) + 1, 1):

            self.InitHypothesis(i)

            # Shape of hypothesis: (373, 256)
            # Shape of tracesPoints: (373, 1719)
            # Shape of corrMatrix: (256, 1719)
            corrMatrix = self.Correlate(self.hypothesis, self.tracesPoints)

            matrixRelation = np.zeros(256)
            # Get max correlation value from among the traces data points
            for j in range(256):
                matrixRelation[j] = max(abs(corrMatrix[j]))

            # Get index of highest correalation value out of the 256 permutations
            index = np.argmax(matrixRelation)

            # Store subkey i guesses matrix and its correspoding highest score index for visualization purposes
            self.matrixRelations.append((matrixRelation, index))

            key += format(index, '02X')

        return key

    def Correlate(self, A, B):

        # Transpose data
        A = A.T
        B = B.T

        # print("Shape of A: ", A.shape)
        # print("Shape of B: ", B.shape)

        # Rowwise mean of input arrays & subtract from input arrays themeselves
        # Mean normalization
        A_mA = A - A.mean(1)[:, None]
        B_mB = B - B.mean(1)[:, None]

        # Sum of squares across rows
        ssA = (A_mA ** 2).sum(1)
        ssB = (B_mB ** 2).sum(1)

        # Finally get corr coeff
        return np.dot(A_mA, B_mB.T) / np.sqrt(np.dot(ssA[:, None], ssB[None]))

    def InitHypothesis(self, byteNumber):

        keyHyp = [i for i in range(256)]
        self.hypothesis = np.zeros((len(self.plainTexts), len(keyHyp)))

        for i in range(len(self.plainTexts)):


            subPT = self.plainTexts[i][0][2 * (byteNumber - 1):2 * byteNumber]

            for j in range(len(keyHyp)):
                sboxResult = self.toolbox.Sbox(int(subPT, 16) ^ keyHyp[j])
                self.hypothesis[i][j] = self.toolbox.HammingWeight(sboxResult)

    def GetMatrixRelations(self):

        return self.matrixRelations

    def VisualizeCorr(self, matrixRelation, index):

        fig, axs = plt.subplots(1,1)
        axs.stem(matrixRelation)
        axs.grid()
        # axs.stem(index, matrixRelation[index])
        axs.stem([index], [matrixRelation[index]], linefmt ="C1-", markerfmt = "C1o")

        plt.show()