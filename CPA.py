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
        tracesPoints.transpose()
        self.tracesPoints = tracesPoints.astype(float)
        self.plainTexts = plainTexts

        print("tracesPoints", self.plainTexts)


    def Analyse(self):

        keyRecovered = ''

        for i in range(1, len(self.key) + 1, 1):
            self.InitHypothesis(i)
            corrMatrix =  self.Correlate(self.hypothesis, self.tracesPoints)
            # Will contain each guessed subkey's max correlaton
            matrixR = np.zeros(256)

            for j in range(256):
                matrixR[j] = max(abs(corrMatrix[j]))

            # Search through every subkey permutation to see get the one with highest correlation. This is the most probable subkey
            index = np.where(matrixR == np.amax(matrixR))

            keyRecovered += format(index[0][0], '02X')

        print("Key Recovered:" + keyRecovered)



    def Correlate(self, A, B):

        # Rowwise mean of input arrays & subtract from input arrays themeselves
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


            subPT = self.plainTexts[i][0][2*(byteNumber-1):2*byteNumber]
            print("current subpt: ", subPT)

            for j in range(len(keyHyp)):

                sboxResult = self.toolbox.Sbox(int(subPT, 16)^keyHyp[j])
                self.hypothesis[i][j] = self.toolbox.HammingWeight(sboxResult)






