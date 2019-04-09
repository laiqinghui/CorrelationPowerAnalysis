import sys, getopt, math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from CPA import CPA


def main(argv):

    inputfilename, startpt, endpt = getInputs(argv)
    print("Processing ", inputfilename, "...")
    pt, ct, tracesPoints = processCSV(inputfilename, startpt, endpt)
    VisualizeTracesDifferences(pt, ct, tracesPoints)
    # keysize = 16
    #
    #
    # # Init CPA object
    # cpa = CPA(keysize, len(traceSets))
    #
    #
    # for tracesPointsLen in range(100, 110, 10):
    #
    #     # Set data points
    #     cpa.SetTracesPointsAndPT(tracesPoints[:tracesPointsLen], pt[:tracesPointsLen])
    #     # Do CPA
    #     print("Doing Correlational Power Aalysis...")
    #     key = cpa.Analyse()
    #     # cpa.VisualizeCorrSingle(cpa.GetMatrixRelations()[0][0], cpa.GetMatrixRelations()[0][1])
    #
    #     print("Key(Hex): ", key)
    #     print("Key(Text): ", bytearray.fromhex(str(key)).decode())


def VisualizeTracesDifferences(pt, ct, tracesPoints):

    keysize = 16
    traceSets = range(10, 350, 10)
    cpaObjs = []
    # Will contain temp 16 sets of 20 (256 by 1) matrices for concat
    matrixRelationMatList = np.empty(shape=(keysize, len(traceSets)), dtype=object)
    # Will be size of 16
    ylistContainer = []


    for index1, tracesPointsLen in enumerate(traceSets):
        print("Working with ", tracesPointsLen, " traces now...")
        cpa = CPA(keysize)
        # Set data points
        cpa.SetTracesPointsAndPT(tracesPoints[:tracesPointsLen], pt[:tracesPointsLen])
        # Do CPA
        print("Doing Correlational Power Aalysis...")
        key = cpa.Analyse()
        print("Key recovered with ", tracesPointsLen, " traces is ", key)
        # Size of 16
        currentMatrixRelations = cpa.GetMatrixRelations()
        # Populate matrix data for plotting later
        for index2, eachByteRelation in enumerate(currentMatrixRelations):
            # Tranpose from 1 x 256 to 256 x1
            matrixRelationMatList[index2][index1] = (np.array(eachByteRelation).reshape(len(eachByteRelation), 1))


        cpaObjs.append(cpa)

    print("matrixRelationMatList.shape", matrixRelationMatList.shape)

    for m in matrixRelationMatList:
        # ylist will have a shape of (256 by 20)
        ylist = np.concatenate(m, axis=1)
        ylistContainer.append(ylist)


    # Plotting
    numOfRowsPerFig = 4
    numOfColPerFig = 4
    numOfPlotsPerFig = numOfRowsPerFig * numOfColPerFig
    numOfFigReq = math.ceil(keysize / numOfPlotsPerFig)
    figures = np.empty(shape=numOfFigReq, dtype=object)
    figIndex = 0
    plotIndex = 1
    figures[figIndex] = plt.figure()
    figures[figIndex].subplots_adjust(hspace=0.4, wspace=0.4)

    for index, ylist in enumerate(ylistContainer):
        if index > numOfPlotsPerFig:
            figIndex += 1
            figures[figIndex] = plt.figure()
            figures[figIndex].subplots_adjust(hspace=0.4, wspace=0.4)
            plotIndex = 1
        ax = figures[figIndex].add_subplot(numOfRowsPerFig, numOfColPerFig, plotIndex)
        for y in ylist:
            ax.plot(traceSets, y)
        ax.set_title(str(index))
        plotIndex += 1


    plt.show()




def getInputs(argv):
    if len(argv) < 3 and not ("-h" in argv):
        print("Wrong command format!")
        print("Please supply csv file and options. Use -h option for example command.")
        sys.exit(2)
    try:
        opts, args = getopt.getopt(argv, "hi:s:e:", ["ifile=", "startpt=", "endpt="])
    except getopt.GetoptError:
        print("Wrong command format!")
        print("Use -h option for example command")
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print("eg: Main.py -i waveform.csv -s 327 -e 2046 ")
            sys.exit(2)
        elif opt in ("-i", "--ifile"):
            inputfilename = arg
        elif opt in ("-s", "--startpt"):
            startpt = arg
        elif opt in ("-e", "--endpt"):
            endpt = arg
    print("Input file is ", inputfilename)

    return inputfilename, int(startpt), int(endpt)


def processCSV(filename, startpt, endpt):
    # index start at 0 conversion
    startpt -= 1
    endpt -= 1

    dframe = pd.read_csv(filename, header=None)
    dframe = dframe.dropna(axis=1, how='any')  # Cleanup data: Removes anything that's not a number
    # dframe.drop(dframe.columns[[i for i in range(endpt, dframe.shape[1], 1)]], axis=1, inplace=True)
    # dframe.drop(dframe.columns[[i for i in range(0, startpt + 1, 1)]], axis=1, inplace= True)
    pt = dframe.iloc[:, 0:1]
    ct = dframe.iloc[:, 1:2]
    dataTraces = dframe.iloc[:, startpt + 1:endpt]
    print("Processed data: ")
    print(dataTraces.head())

    return pt.values, ct.values, dataTraces.values


if __name__ == "__main__":
    main(sys.argv[1:])
