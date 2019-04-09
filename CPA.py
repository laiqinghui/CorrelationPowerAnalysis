import numpy as np
import matplotlib.pyplot as plt
from ToolBox import ToolBox


class CPA():
    toolbox = ToolBox()

    def __init__(self, keySize=16):
        self.traceSetCount = 0
        self.key = []
        self.keySize = keySize
        self.hypothesis = None
        self.plainTexts = None
        self.tracesPoints = None
        self.matrixRelation = None
        self.matrixRelations = []

        # self.CorrBytes = np.zeros(shape=(keySize, noOfTracesSet, 256))

    def SetTracesPointsAndPT(self, tracesPoints, plainTexts):

        self.tracesPoints = tracesPoints
        self.plainTexts = plainTexts

    def GetKey(self):
        return self.key

    def Analyse(self):

        for i in range(1, self.keySize + 1, 1):

            self.InitHypothesis(i)

            # Shape of hypothesis: (373, 256)
            # Shape of tracesPoints: (373, 1719)
            # Shape of corrMatrix: (256, 1719)
            corrMatrix = self.Correlate(self.hypothesis, self.tracesPoints)

            matrixRelation = np.zeros(256)
            # Get max correlation value from among the traces data points
            for j in range(256):
                # matrixRelation[j] = max(abs(corrMatrix[j]))
                # Get max value in abs form but preserve the sign
                matrixRelation[j] = corrMatrix[j][abs(corrMatrix[j]).argmax()]

            # Get index of highest correlation value out of the 256 permutations
            index = abs(matrixRelation).argmax()

            # Store subkey i guesses matrix for visualization purposes
            self.matrixRelation = matrixRelation
            self.matrixRelations.append(matrixRelation)

            # self.key += format(index, '02X')
            self.key.append(index)

        return self.key

    def Correlate(self, A, B):

        # Transpose data
        A = A.T
        B = B.T

        # print("Shape of A: ", A.shape)
        # print("Shape of B: ", B.shape)

        # Row-wise mean of input arrays & subtract from input arrays themselves
        # Mean normalization
        A_mA = A - A.mean(1)[:, None]
        B_mB = B - B.mean(1)[:, None]

        # Sum of squares across rows
        ssA = (A_mA ** 2).sum(1)
        ssB = (B_mB ** 2).sum(1)

        # Finally get corr coeff
        return np.dot(A_mA, B_mB.T) / np.sqrt(np.dot(ssA[:, None], ssB[None]))

    def InitHypothesis(self, byteNumber):

        # Initialise data structure
        keyHyp = [i for i in range(256)]
        self.hypothesis = np.zeros((len(self.plainTexts), len(keyHyp)))

        # Loop through all the traces
        for i in range(len(self.plainTexts)):

            # Get the current plain text byte via array slicing
            # Note that array is 3 dimensional due to conversion from Pandas frame
            # to Numpy array
            subPT = self.plainTexts[i][0][2 * (byteNumber - 1):2 * byteNumber]

            # Construct hypothetical data for each key-byte guesses
            for j in range(len(keyHyp)):
                # Do sbox transformation according to look-up table
                sboxResult = self.toolbox.Sbox(int(subPT, 16) ^ keyHyp[j])
                # Estimate hypothetical power consumption value as hamming weights
                self.hypothesis[i][j] = self.toolbox.HammingWeight(sboxResult)

    def GetMatrixRelations(self):

        return self.matrixRelations

    def VisualizeCorrSingle(self, matrixRelation, index):

        fig, axs = plt.subplots(1, 1)
        axs.stem(matrixRelation)
        axs.grid()
        # axs.stem(index, matrixRelation[index])
        axs.stem([index], [matrixRelation[index]], linefmt="C1-", markerfmt="C1o")

        plt.show()

    def VisualizeCorrAll(self, matrixRelation, index):

        currentByte = self.CorrBytes[0]
        fig, axs = plt.subplots(1, 1)
        axs.plot(matrixRelation)
        axs.grid()

        plt.show()
