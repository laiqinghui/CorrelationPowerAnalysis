import numpy as np
from ToolBox import ToolBox



class CPA():

    hypothesis = None
    plainText = None
    key = None
    toolbox = ToolBox()

    def __init__(self, numOfTraces = 100, keySize = 16):
        self.key = np.zeros(keySize)
        self.genTraces(numOfTraces)

    def genTraces(self, numOfTraces):
        pass

    def Analyse(self):

        for i in range(1, len(self.key) + 1, 1):
            self.InitHypothesis(i)
            continue



    def InitHypothesis(self, byteNumber):

        keyHyp = [i for i in range(256)]
        self.hypothesis = np.array((len(self.plainText), len(keyHyp)))

        for i in range(len(self.plainText)):

            subPT = plainText[i][2*(byteNumber-1):2*byteNumber]

            for j in range(len(self.keyHyp)):

                sboxResult = toolbox.Sbox(subPT^keyHyp[j])
                self.hypothesis[i][j] = toolbox.HammingWeight(sboxResult)






