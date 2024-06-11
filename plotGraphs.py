# python plotGraphs.py -l genLarge4G1,genLarge4G2,genLarge4G3

import matplotlib.pyplot as plt
import pandas as pd
import glob
import argparse

def plotGraphAgents(SarsaCsv, qLearnCsv):
    # remove .csv
    # print(SarsaCsv, qLearnCsv)
    plt.figure()
    file = SarsaCsv[:-4]
    # csvFile = f"csvs/{agent}_{layout_str}_{args.extractor}_{lamda_str}"
    layout_name = file.split('/')[-1].split('_')[1]    
    # layout_name = ''.join(alldata)
    
    # get the data ready by grouping them based on episodes and taking mean
    sarsa_df = pd.read_csv(str(SarsaCsv))
    qLearn_df = pd.read_csv(str(qLearnCsv))
    sarsa_df = sarsa_df.groupby(['Episode'], as_index = False).mean()
    qLearn_df = qLearn_df.groupby(['Episode'], as_index = False).mean()
    sarsa_x = sarsa_df["Episode"]
    sarsa_y = sarsa_df["AvgRewards"]
    qlearn_x = qLearn_df["Episode"]
    qlearn_y = qLearn_df["AvgRewards"]

    # labels for each plot
    sarsalabelData = f"agent: TrueOnlineSarsaAgent, layout: {layout_name}"
    qLearnlabelData = f"agent: ApproximateQAgent, layout: {layout_name}"
    
    # plotting
    plt.plot(sarsa_x, sarsa_y, color='r', label=sarsalabelData, linewidth = 0.8)
    plt.plot(qlearn_x, qlearn_y, color='b', label=qLearnlabelData, linewidth = 0.8)
    plt.title("TrueOnlineSarsaAgent vs ApproximateQAgent")
    plt.xlabel("Episodes -->")
    plt.ylabel("AvgRewards over 100 episodes --> ")
    plt.legend()

    # save the plot
    plt.savefig(f'./plots/SARSAvsQ_{layout_name}')


def plotGraphs(layouts):
    # print(layouts)
    csvFolder = f"csvs/"
    files = list(glob.glob(csvFolder+'/*.csv'))
    for file in files:
        layout_name = file[:-4].split('/')[-1].split('_')[1]
        
        if layout_name in layouts:
            if 'TrueOnlineSarsaAgent' in file:
                approxQAgent = file.replace('TrueOnlineSarsaAgent', 'ApproximateQAgent')
                if approxQAgent in files:
                    plotGraphAgents(file, approxQAgent)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--layouts', dest='layouts',
                  help='Comma separated layouts. e.g. "smallGrid,mediumGrid"', default="smallGrid")
    args = parser.parse_args()
    layouts = args.layouts.split(',')
    plotGraphs(layouts)



