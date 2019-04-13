import sys, getopt, math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from CPA import CPA


def main(argv):
    # inputfilename, startpt, endpt = getInputsArgv(argv)
    inputfilename, startpt, endpt, numTraces = getInputs()
    print("Processing ", inputfilename, "...")
    print()
    pt, ct, tracesPoints = processCSV(inputfilename, startpt, endpt)
    if numTraces == -1:
        VisualizeTracesDifferences(pt, ct, tracesPoints)
    else:
        VisualizeTracesDifferences(pt, ct, tracesPoints[:numTraces])


def VisualizeCorrSingle(matrixRelations, byteNo):

    matrixRelation = matrixRelations[byteNo]
    fig, axs = plt.subplots(1, 1)
    axs.stem(matrixRelation)
    axs.grid()
    # axs.stem(index, matrixRelation[index])
    axs.stem([abs(matrixRelation).argmax()], [matrixRelation[abs(matrixRelation).argmax()]], linefmt="C1-",
             markerfmt="C1o")

    axs.set_xlabel('All possible sub-key guesses')
    axs.set_ylabel('Correlation Value')
    plt.title("Correlation plot for byte "+ str(byteNo))
    plt.show()


def VisualizeCorrAll(traceSets, matrixRelationMatList, keysize):
    # Will be size of 16
    ylistContainer = []

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
    figures[figIndex].subplots_adjust(hspace=0.7, wspace=0.7)

    for index, ylist in enumerate(ylistContainer):

        if plotIndex > numOfPlotsPerFig:
            figIndex += 1
            figures[figIndex] = plt.figure()
            figures[figIndex].subplots_adjust(hspace=0.7, wspace=0.7)
            plotIndex = 1
        ax = figures[figIndex].add_subplot(numOfRowsPerFig, numOfColPerFig, plotIndex)
        for y in ylist:
            ax.plot(traceSets, y)
        ax.set_title('Key byte ' + str(index))
        ax.set_xlabel('No. of traces')
        ax.set_ylabel('Correlation Value')
        plotIndex += 1

    plt.show()


def VisualizeTracesDifferences(pt, ct, tracesPoints):
    keysize = 16
    # print("Range count", (math.floor(len(tracesPoints)/10)*10)+10)
    traceSets = range(10, (math.floor(len(tracesPoints) / 10) * 10) + 10, 10)
    cpaObjs = []
    # Will contain temp 16 sets of 20 (256 by 1) matrices for concat
    matrixRelationMatList = np.empty(shape=(keysize, len(traceSets)), dtype=object)

    print("Starting CPA procedure with increasing number of traces now...")

    for index1, tracesPointsLen in enumerate(traceSets):
        print("Working with ", tracesPointsLen, " traces now...")
        cpa = CPA(keysize)
        # Set data points
        cpa.SetTracesPointsAndPT(tracesPoints[:tracesPointsLen], pt[:tracesPointsLen])
        # Do CPA
        print("Doing Correlational Power Analysis...")
        key = cpa.Analyse()
        print("Key recovered with ", tracesPointsLen, " traces is ", [hex(k) + "|" + chr(k) for k in key])
        # Size of 16
        currentMatrixRelations = cpa.GetMatrixRelations()
        # Populate matrix data for plotting later
        for index2, eachByteRelation in enumerate(currentMatrixRelations):
            # Tranpose from 1 x 256 to 256 x1
            matrixRelationMatList[index2][index1] = (np.array(eachByteRelation).reshape(len(eachByteRelation), 1))

        cpaObjs.append(cpa)

    # print("matrixRelationMatList.shape", matrixRelationMatList.shape)

    print("Plotting single sub-key byte correlation plot...")
    VisualizeCorrSingle(cpaObjs[index1].GetMatrixRelations(), 0)
    VisualizeCorrSingle(cpaObjs[index1].GetMatrixRelations(), 1)
    print("Plotting all key bytes correlation plot...")
    VisualizeCorrAll(traceSets, matrixRelationMatList, keysize)


def getInputs():
    defaultCSV = "waveform374samples_327_2047.csv"
    defaultStart = 327
    defaultEnd = 2047
    defaultNumTraces = -1

    print("Welcome to Power Analysis Tool!")
    print("===============================")
    print()
    inputfilename = input(
        "Please enter the name of the waveform file (Press <enter> to use default file): ") or defaultCSV
    print("File chosen: ", inputfilename)
    startpt = int(input("Please enter the start index (Press <enter> to use default start index): ") or defaultStart)
    print("Start index: ", startpt)
    endpt = int(input("Please enter the end index (Press <enter> to use default end index): ") or defaultEnd)
    print("End index: ", endpt)
    numTraces = int(input(
        "Please enter the max no. of traces to be use for analysis.\nNo. of trace will start from 10 and end at this amount in steps of 10 (Press <enter> to use all traces available in the file): ") or defaultNumTraces)
    print("No. of traces to use: ", numTraces if numTraces != -1 else 'All')
    print()

    return inputfilename, startpt, endpt, numTraces


def getInputsArgv(argv):
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
    print("First 5 rows of processed data: ")
    print(dataTraces.head())
    print()

    return pt.values, ct.values, dataTraces.values


if __name__ == "__main__":
    main(sys.argv[1:])
