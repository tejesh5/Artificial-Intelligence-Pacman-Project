#!/usr/bin/python
# python runScript.py -l genLarge3G2 -x 2000 -y 2000 -r 10 -f IdentityExtractor
import argparse
import subprocess
import glob
import pandas as pd
import matplotlib.pyplot as plt
import plotGraphs
from Ttest import convergenceEstimator
from scipy.stats import ttest_ind, ttest_rel

# Create a parser object
parser = argparse.ArgumentParser()

# Add a positional argument
# parser.add_argument("command", help="The command to run")


LAYOUTS = [ "powerClassic", "capsuleClassic", "contestClassic", "mediumClassic", "mediumGrid", "openClassic", "originalClassic" \
            "smallClassic", "smallGrid", "testClassic", "trappedClassic", "trickyClassic"]
AGENTS = ["TrueOnlineSarsaAgent", "ApproximateQAgent"]

# Add optional arguments
parser.add_argument("-a", "--agent", help="agent", default = AGENTS)
parser.add_argument("-x", "--numTrain", help="Num Train", default = 2000)
parser.add_argument("-r", "--runs", help="runs", default = 3)
parser.add_argument("-y", "--numTest", help="Num Test", default = 2000)
parser.add_argument("-c", "--csvFile", help="CSV File", default = "result.csv")
parser.add_argument("-m", "--lamda", help="Lambda", default = 0.6)
parser.add_argument("-f", "--extractor", help="featureExtractor", default = "SimpleExtractor")
parser.add_argument('-l', '--layouts', dest='layouts',
                  help='Comma separated layouts. e.g. "smallGrid,mediumGrid"', default="smallGrid")
# Parse the arguments
args = parser.parse_args()

# runs each agents with passing appropriate parameters
def runAgents(layouts):
    lamda_str = str(args.lamda).replace(".", "-")
    for agent in args.agent:
        for layout in layouts:
            layout_str = layout
            # Create a CSV file name based on layouts and parameters
            csvFile = f"csvs/{agent}_{layout_str}_{args.extractor}_{lamda_str}.csv"
            command = f"python pacman.py -p {agent} -a extractor={args.extractor},lamda={args.lamda} -l {layout} -x {str(args.numTrain)} -n {str(args.numTest)} --csvFile {csvFile}" 
            for i in range(int(args.runs)):
                cmd = command
                # if there was an existing csv with same name then remove it
                if i == 0: cmd = command + " --clearCSV"
                print(f" \n\n\n -------------------------- Agent: {agent} -- running {i+1} step -------------------------- \n\n\n")
                # Run the commands 
                x = subprocess.Popen(cmd.split())
                x.wait()

# to create csvs and plots directories
def createDirectories(layouts):
    # for creating csvs folder
    if not glob.glob(f"csvs"):
        x = subprocess.Popen(f"mkdir csvs".split())
        x.wait()
    # for creating plots folder
    if not glob.glob(f"plots"):
        x = subprocess.Popen(f"mkdir plots".split())
        x.wait()


def runTTest(layouts):
    csvFolder = f"csvs/"
    files = list(glob.glob(csvFolder+'/*.csv'))
    for file in files:
        # Fetch the layout_name from the csv file name
        layout_name = file[:-4].split('/')[-1].split('_')[1]
        # To check if we want to run ttest on this layout
        if layout_name in layouts:
            if 'TrueOnlineSarsaAgent' in file:
                approxQAgent = file.replace('TrueOnlineSarsaAgent', 'ApproximateQAgent')
                if approxQAgent in files:
                    # get the convergence episode for both using this file
                    sarsaConvergedEps, QConvergedEps = convergenceEstimator(file, approxQAgent, int(args.numTrain), 50)
                    res = ttest_rel(sarsaConvergedEps, QConvergedEps)
                    print(f"\n\n p-value for this layout between True online SARSA and Approximate Q learning based on convergence is = {res.pvalue}")
                    if res.pvalue < 0.05:
                        print("There is a performance differencce between True online SARSA and Approximate Q learning")
                    else:
                        print("There is not much significant performance difference between True online SARSA and Approximate Q learning")


if __name__ == '__main__':
    layouts = args.layouts.split(',')
    createDirectories(layouts)
    runAgents(layouts)
    # plotGraphs(layouts)
    runTTest(layouts)



