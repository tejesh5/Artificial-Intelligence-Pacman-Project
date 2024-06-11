# python Ttest.py -s sarsaCSV -q ApproxQCSV
# python Ttest.py -c genLarge
 
import pandas as pd
from scipy.stats import ttest_ind, ttest_rel
import glob
import argparse
import random

def convergenceEstimator(sarsa, q, episodes, tolerance):
    sarsa_df = pd.read_csv(sarsa, index_col = 0)
    q_df = pd.read_csv(q, index_col = 0)
    totalRows = int(len(sarsa_df))
    sarsaConvergedEps = []
    QConvergedEps = []
    sarsa_idealRewards = sum(sarsa_df['AvgRewards'][totalRows-100:totalRows]) / 100
    q_idealRewards = sum(q_df['AvgRewards'][totalRows-100:totalRows]) / 100
    window = 12
    # get the convergence episode for sarsda
    run = 1
    epi = 0
    while epi < len(sarsa_df['Episode']):
        if (sarsa_df['AvgRewards'][epi] ) > sarsa_idealRewards-tolerance and \
            (sarsa_df['AvgRewards'][epi]) < sarsa_idealRewards+tolerance:
            sarsaConvergedEps.append(epi+1 - ((run-1) * episodes))
            epi = run * episodes
            run += 1
            continue
        epi += 1

    # get the convergence episode for sarsda
    run = 1
    epi = 0
    while epi < len(q_df['Episode']):
        if (q_df['AvgRewards'][epi] ) > q_idealRewards-tolerance and \
            (q_df['AvgRewards'][epi] ) < q_idealRewards+tolerance:
            QConvergedEps.append(epi+1 - ((run-1) * episodes))
            epi = run * episodes
            run += 1
            continue
        epi += 1
    # randomly fetch 5 samples
    sarsaConvergedEps, QConvergedEps = sarsaConvergedEps, QConvergedEps
    sarsaconvergedeps, QconvergedEps = random.choice(sarsaConvergedEps), random.choice(QConvergedEps)
    return sarsaConvergedEps, QConvergedEps


def runAvgedTtest(layout_case):
    csvFolder = f"csvs/"
    files = list(glob.glob(csvFolder+'/*.csv'))
    # get all the files in the csv folder
    trueOnlineSarsaFiles = []
    ApproximateQAgentFiles = []
    # list to store convergence episode
    allSarsaConv = []
    allQConv = []
    # separating the files into trueOnlineSarsa and ApproximateQLearning
    for file in files:
        if layout_case in file:
            if 'TrueOnlineSarsaAgent' in file:
                trueOnlineSarsaFiles.append(file)
            if 'ApproximateQAgent' in file:
                ApproximateQAgentFiles.append(file)
    # Get the convergence episodes for each results
    for file in trueOnlineSarsaFiles:
        approxQAgent = file.replace('TrueOnlineSarsaAgent', 'ApproximateQAgent')
        if approxQAgent in ApproximateQAgentFiles:
            sarsaConvergedEps, QConvergedEps = convergenceEstimator(file, approxQAgent, 2000, 50)
            allSarsaConv.extend(sarsaConvergedEps)
            allQConv.extend(QConvergedEps)
    return allSarsaConv, allQConv


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--sarsa', dest='sarsa', help='CSV file for SARSA', default="")
    parser.add_argument('-q', '--Q', dest='Q', help='CSV file for approx Q', default="")
    parser.add_argument('-c', '--case', dest='case', help='To run on similar cases', default="")
    args = parser.parse_args()
    # if user passes layout class then run averaged Ttest
    if args.case:
        sarsaConvergedEps, QConvergedEps = runAvgedTtest(args.case)
    else:
        sarsaConvergedEps, QConvergedEps = convergenceEstimator(args.sarsa, args.Q, 2000, 50)
    # get the p-value using the convergence of TrueOnlinseSarsa and approximatreQ
    res = ttest_rel(sarsaConvergedEps, QConvergedEps)
    print(res.pvalue)

