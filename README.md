# Project topic 4. Reinforcement Learning agent 📝

## CSE571 Artificial Intelligence 🚀

Implemented True online Sarsa(l) (page 307, Chapter 12) with linear function 
approximation from Reinforcement Learning: An Introduction, 2nd by Richard 
Sutton (http://incompleteideas.net/book/RLbook2020.pdf) to control the agent in 
the Pacman domain. 

* Compared the performance of True Online SARSA agent and converging behavior with the Approximate Q-learning agent (with linear function approximation). 
* Ran comparisons in different environments with different sizes and complexities. 
* Provided statistical analyses using student’s T-test or ANOVA test. 
* Ran the Statistical tests for comparing results with different sizes and complexities. 
* Created a script for creating different environments. 
* Collected results from many different runs for the different approaches and chose a test to 
meaningfully compare them in terms of convergence speed (i.e., how fast it 
converges to the optimal policy) in different environments. 

## Get Started ⚡️

The Goal of the Project is to compare the performance of an agent using 2 Reinforcement Learning Algorithms, we are using pacman for understanding the learning experiments. Pacman lives in a shiny blue world of twisting corridors and tasty round treats. Navigating 
this world efficiently will be Pacman's first step in mastering his domain.

- on-policy learning - True online Sarsa
- off-policy learning - Q-learning

#### Required packages 
pandas==1.1.5
matplotlib==3.3.4
numpy==1.19.5
scipy==1.5.4

## Directory Structure ✨
* csvs - Contains the results from running runScript for both agents.
    * small, large, medium, Huge, XLarge - results for different complexities
* plots - Contains the plots from running plotGraphs.
* ttestResults - Contains the results from running ttest on layout and categories(large, medium...) as well.

### Files :

* trueOnlineSarsaAgents.py : True Online SARSA agent implementation.
* runScript.py : An automated script to run both True Online SARSA and ApproximateQ agent.
* plotGraphs.py : To generate plots using the results in the CSV.
* Ttest.py : To run T-test on csv results and also for layout categorize.
* Layoutsgen.py : Automated Generation of layouts using DFS algorithm.
* randLayoutGen.py :  Automated Generation of layouts randomly.
   

## Commands ✨


### For any Pacman related help Run

```
pacman --help
```

#### QLearning Agent : 

```
python pacman.py -p ApproximateQAgent -a extractor=SimpleExtractor -x 2000 -n 2000 -l smallClassic
```

#### Sarsa Agent : 

```
python pacman.py -p TrueOnlineSarsaAgent -a extractor=SimpleExtractor -x 2000 -n 2000 -l smallClassic
```

### Automated Script Command : 

```
python runScript.py -l smallGrid,mediumGrid -x 2000 -y 2000 -r 5 
```

runScript runs TrueOnlineSARSA and ApproximateQ agent on the layouts specified, stores the result in the csvs and executed the T-test. Arguments for the runScript:
* -l : Layouts to run agents on. Separated by commas (No space).
* -r : Number of runs each agent does on that layout.
* -x : Number of Episodes to train.
* -y : Number of Episodes to test.
* -f : fetaure Extractor for agents.
* -m : lamda value for True OnlineSARSA agent.

### Plotting Graphs :
```
python plotGraphs.py -l smallGrid,mediumGrid
```
Plots the graph of True Online Sarsa and Approximate Q agent using the csv generated. Arguments for the plotGraphs:

* -l : Layouts to get the plots. Separated by commas (No space).

### T-test Execution :
```
python Ttest.py -s csvs/TrueOnlineSarsaAgent_genLarge3G4_SimpleExtractor_0-6.csv -q csvs/ApproximateQAgent_genLarge3G4_SimpleExtractor_0-6.csv
python Ttest.py -c genLarge
```
To run the T-test on the results from agents. For running on layout cases (small, large...) use -c. Arguments for Ttest :

* -s : CSV result file for True Online SARSA agent.
* -q : CSV result file for ApproximateQ agent.
* -c : For running on grouped layout cases.

### Layout Generation :
```
python Layoutsgen.py -g 3 -s 10 -p 3 -f 0.5 -o genLarge3G1
python randLayoutGen.py -r 5 -c 5 -g 3 -f 15 -l randLarge3G1
```
To get new auto-generated layouts using DFS algorithm use Layoutsgen.py. 
To get new auto-generated layouts randomly use randLayoutGen.py Arguments for LayoutsGen :

* -g : Number of ghosts.
* -s : Size of the grid.
* -p : Number of power pallets.
* -f : Probability of food generation.
* -o : File to save the new genrated layout.

