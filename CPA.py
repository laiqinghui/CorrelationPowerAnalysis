import numpy as np
from ToolBox import ToolBox


class CPA():

    hypothesis = None
    plainTexts = None
    tracesPoints = None
    key = None
    toolbox = ToolBox()

    def __init__(self, keySize = 16):
        self.key = np.zeros(keySize)


    def setTracesPointsAndPT(self, tracesPoints, plainTexts):

        self.tracesPoints = tracesPoints
        self.plainTexts = plainTexts


    def Analyse(self):

        key = ""

        for i in range(1, len(self.key) + 1, 1):

            self.InitHypothesis(i)

            corrMatrix =  self.Correlate(self.hypothesis, self.tracesPoints)

            matrixR = np.zeros(256)
            # Get max correlation value from among the traces data points
            for j in range(256):
                matrixR[j] = max(abs(corrMatrix[j]))

            # Get index of highest correalation value out of the 256 permutations
            index = np.argmax(matrixR)

            key += format(index, '02X')

        return key


    def Correlate(self, A, B):

        # Transpose data
        A = A.T
        B = B.T

        # Rowwise mean of input arrays & subtract from input arrays themeselves
        A_mA = A - A.mean(1)[:, None]
        B_mB = B - B.mean(1)[:, None]

        # Sum of squares across rows
        ssA = (A_mA ** 2).sum(1)
        ssB = (B_mB ** 2).sum(1)

        # Finally get corr coeff
        # print("A_mA shape: ", A_mA.shape, "B_mB shape: ", B_mB.shape)
        # print("np.dot(A_mA, B_mB.T) shape: ", np.dot(A_mA, B_mB.T).shape, "np.sqrt(np.dot(ssA[:, None], ssB[None])) shape", np.sqrt(np.dot(ssA[:, None], ssB[None])).shape)
        # A_mA shape:  (256, 150) B_mB.T shape:  (150, 1719)
        return np.dot(A_mA, B_mB.T) / np.sqrt(np.dot(ssA[:, None], ssB[None]))



    def InitHypothesis(self, byteNumber):


        keyHyp = [i for i in range(256)]
        self.hypothesis = np.zeros((len(self.plainTexts), len(keyHyp)))

        for i in range(len(self.plainTexts)):


            subPT = self.plainTexts[i][0][2*(byteNumber-1):2*byteNumber]
            # print("current subpt: ", subPT)

            for j in range(len(keyHyp)):

                sboxResult = self.toolbox.Sbox(int(subPT, 16)^keyHyp[j])
                self.hypothesis[i][j] = self.toolbox.HammingWeight(sboxResult)






