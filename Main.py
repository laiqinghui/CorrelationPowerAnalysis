import sys, getopt
import pandas as pd
from CPA import CPA


def main(argv):
    inputfilename, startpt, endpt = getInputs(argv)
    print("Processing ", inputfilename, "...")
    pt, ct, tracesPoints = processCSV(inputfilename, startpt, endpt)
    keysize = 16
    traceSets = range(10, 210, 10)

    # Init CPA object
    cpa = CPA(keysize, len(traceSets))

    for tracesPointsLen in range(100, 110, 10):

        # Set data points
        cpa.setTracesPointsAndPT(tracesPoints[:tracesPointsLen], pt[:tracesPointsLen])
        # Do CPA
        print("Doing Correlational Power Aalysis...")
        key = cpa.Analyse()
        cpa.VisualizeCorr(cpa.GetMatrixRelations()[0][0], cpa.GetMatrixRelations()[0][1])

        print("Key(Hex): ", key)
        print("Key(Text): ", bytearray.fromhex(str(key)).decode())


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

    dframe = pd.read_csv(filename)
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
