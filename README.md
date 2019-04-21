# CorrelationPowerAnalysis
Implementation of a side-channel attack using Correlation Power Analysis with Python 

## Execute the program as a standalone executable:

The python program is build into a standalone executable which is built and tested on the Microsoft Windows 10 platform. There is no requirement to install any other packages in order to run the executable.

### How to use the executable:

1. Ensure that the demo waveform file (waveform374samples_327_2047.csv) and the executable file (Main.exe) are in the same directory.

2. Double click the "Main.exe" executable.

3. A terminal will pop up. Please do give it some time to load all the libraries at the back end. It should take around 15 seconds.

4. A user interface will be shown as below:

<img src="https://raw.githubusercontent.com/laiqinghui/CorrelationPowerAnalysis/master/media/InitUI.png" alt="alt text" width="100%" height="400">
    
5. The program will now ask for the name of the CSV file that contain the traces. Users may choose to analysis their own set of traces by placing the their own trace file in the same directory as the executable file and provide the name of their own waveform files. However, for this demo, please press enter to proceed with the demo waveform file as that file contains the traces collected during the lab experiment.

6. The program will now ask for the start index of the trace file which data will start to be used for processing. Users may also indicate the start of the index of their own waveform files. However, for this demo, please press enter to proceed with the setting for the default waveform file.

7. The program will now ask for the end index of the trace file which data are stop to be considered for processing. Users may also indicate the end of the index of their own waveform files. However, for this demo, please press enter to proceed with the setting for the default waveform file.

8. The program will now ask for the maximum number of traces that will be use for processing (Processing will start from 10 to this specified amount in steps of 10). Users may also indicate the maximum number of traces to be used for analysis in their own waveform files. However, for this demo, please press enter to use all traces available in the trace file.

9. The program will start the processing of data. The sample output of the program will be as such:

<img src="https://raw.githubusercontent.com/laiqinghui/CorrelationPowerAnalysis/master/media/results.png" alt="alt text" width="100%" height="400">

Two plots will be produced as well. The details of the results and plots will be discussed in the accompanying report.

<img src="https://raw.githubusercontent.com/laiqinghui/CorrelationPowerAnalysis/master/media/plot1.png" alt="alt text" width="100%" height="500">

<img src="https://raw.githubusercontent.com/laiqinghui/CorrelationPowerAnalysis/master/media/plot2.png" alt="alt text" width="100%" height="500">

## Execute the program from source:

The project is built with Python 3.7.1 with Anaconda as the package manager.

Dependencies for this project:
1) Numpy
2) Pandas
2) Matplotlib

### Steps to execute the program from source:

1) Install Anaconda 3.7 or install Python 3.7.1 along with the necessary packages required as stated above.
2) Clone this repository
3) Execute the python script by opening cmd in Windows or terminal in Linux and keying in:

    cd 'root directory of the repo'

    python Main.py

