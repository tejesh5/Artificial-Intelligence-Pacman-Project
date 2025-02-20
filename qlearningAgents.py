# qlearningAgents.py
# ------------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from game import *
from learningAgents import ReinforcementAgent
from featureExtractors import *
import glob
import random,util,math
import pandas as pd

class QLearningAgent(ReinforcementAgent):
    """
      Q-Learning Agent

      Functions you should fill in:
        - computeValueFromQValues
        - computeActionFromQValues
        - getQValue
        - getAction
        - update

      Instance variables you have access to
        - self.epsilon (exploration prob)
        - self.alpha (learning rate)
        - self.discount (discount rate)

      Functions you should use
        - self.getLegalActions(state)
          which returns legal actions for a state
    """
    def __init__(self, **args):
        "You can initialize Q-values here..."
        ReinforcementAgent.__init__(self, **args)

        "*** YOUR CODE HERE ***"
        self.values = util.Counter()

    def getQValue(self, state, action):
        """
          Returns Q(state,action)
          Should return 0.0 if we have never seen a state
          or the Q node value otherwise
        """
        "*** YOUR CODE HERE ***"
        return  self.values[( state, action)]
        util.raiseNotDefined()


    def computeValueFromQValues(self, state):
        """
          Returns max_action Q(state,action)
          where the max is over legal actions.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return a value of 0.0.
        """
        "*** YOUR CODE HERE ***"
        all_actions = self.getLegalActions( state)
        max_val = float( "-inf")
        for  act in  all_actions:
            max_val = max( max_val, self.getQValue( state, act))
        return max_val if all_actions \
             else 0
        # util.raiseNotDefined()

    def computeActionFromQValues(self, state):
        """
          Compute the best action to take in a state.  Note that if there
          are no legal actions, which is the case at the terminal state,
          you should return None.
        """
        "*** YOUR CODE HERE ***"
        # util.raiseNotDefined()
        all_actions  = self.getLegalActions( state)
        action = None
        max_val =  float( '-inf')
        for act in all_actions:
            q_val = self.getQValue(state, act)
            if q_val > max_val: action = act
            elif q_val == max_val: action =  random.choice([ action, act])
            max_val = max( max_val, q_val)
        return action

    def getAction(self, state):
        """
          Compute the action to take in the current state.  With
          probability self.epsilon, we should take a random action and
          take the best policy action otherwise.  Note that if there are
          no legal actions, which is the case at the terminal state, you
          should choose None as the action.

          HINT: You might want to use util.flipCoin(prob)
          HINT: To pick randomly from a list, use random.choice(list)
        """
        # Pick Action
        legalActions =self.getLegalActions(state)
        action =None
        "*** YOUR CODE HERE ***"
        chance =util.flipCoin(self.epsilon)
        if (chance):
            action =  random.choice(legalActions) if legalActions \
            else None
            return action
        action =  self.computeActionFromQValues(state)
        return action
        # util.raiseNotDefined()
        

    def update(self, state, action, nextState, reward):
        """
          The parent class calls this to observe a
          state = action => nextState and reward transition.
          You should do your Q-Value update here

          NOTE: You should never call this function,
          it will be called on your behalf
        """
        "*** YOUR CODE HERE ***"
        Q = self.getQValue(state, action)
        Q_next = self.computeValueFromQValues(nextState)
        a = self.alpha
        self.values[(state, action)] = (((1 - a) * Q) + (a * \
                                        (reward + self.discount * Q_next)))
        return None
        # util.raiseNotDefined()

    def getPolicy(self, state):
        return self.computeActionFromQValues(state)

    def getValue(self, state):
        return self.computeValueFromQValues(state)


class PacmanQAgent(QLearningAgent):
    "Exactly the same as QLearningAgent, but with different default parameters"

    def __init__(self, epsilon=0.05,gamma=0.8,alpha=0.2, numTraining=0, **args):
        """
        These default parameters can be changed from the pacman.py command line.
        For example, to change the exploration rate, try:
            python pacman.py -p PacmanQLearningAgent -a epsilon=0.1

        alpha    - learning rate
        epsilon  - exploration rate
        gamma    - discount factor
        numTraining - number of training episodes, i.e. no learning after these many episodes
        """
        args['epsilon'] = epsilon
        args['gamma'] = gamma
        args['alpha'] = alpha
        args['numTraining'] = numTraining
        self.windowRewards = []
        self.dataLog = {"Episode": [], "AvgRewards": [], "EpisodeRewards": []}
        self.index = 0  # This is always Pacman
        QLearningAgent.__init__(self, **args)

    def getAction(self, state):
        """
        Simply calls the getAction method of QLearningAgent and then
        informs parent of action for Pacman.  Do not change or remove this
        method.
        """
        act=  QLearningAgent.getAction( self,state)
        self.doAction( state,act)
        return  act


class ApproximateQAgent(PacmanQAgent):
    """
       ApproximateQLearningAgent

       You should only have to overwrite getQValue
       and update.  All other QLearningAgent functions
       should work as is.
    """
    def __init__(self, extractor='IdentityExtractor', **args):
        self.featExtractor = util.lookup(extractor, globals())()
        PacmanQAgent.__init__(self, **args)
        self.weights = util.Counter()

    def getWeights(self):
        return self.weights

    def getQValue(self, state, action):
        """
          Should return Q(state,action) = w * featureVector
          where * is the dotProduct operator
        """
        "*** YOUR CODE HERE ***"
        return  self.featExtractor.getFeatures( state, action) *  self.getWeights()

        # util.raiseNotDefined()

    def update(self, state, action, nextState, reward):
        """
           Should update your weights based on transition
        """
        "*** YOUR CODE HERE ***"
        q_val = self.getQValue( state, action)
        q_next  =self.computeValueFromQValues(nextState)
        update  = (reward + \
                ((self.discount * q_next) - q_val))
        weights = self.getWeights()
        feat_func = self.featExtractor.getFeatures(state, action)

        for k in feat_func.keys(): feat_func[k] = feat_func[k] *  (self.alpha *update)

        for k, real_update in feat_func.items():
            weights[k] =  weights[k] + real_update

    def final(self, state):
        "Called at the end of each game."
        # call the super-class final method
        PacmanQAgent.final(self, state)
        
        self.dataLog["Episode"].append(self.episodesSoFar)
        # self.dataLog["AvgRewards"].append(self.accumTrainRewards / float(self.episodesSoFar))
        self.dataLog["EpisodeRewards"].append(self.episodeRewards)
        # self.dataInfo.append([self.episodesSoFar, self.accumTrainRewards / float(self.episodesSoFar), self.episodeRewards, self.lamda, self.epsilon, self.alpha])
        NUM_REW_UPDATE = 100
        self.windowRewards.append(state.getScore())
        if self.episodesSoFar > NUM_REW_UPDATE:
             self.windowRewards.pop(0)
        self.dataLog["AvgRewards"].append(sum(self.windowRewards)/len(self.windowRewards))

    def saveResults(self, csvFile):
        if glob.glob(csvFile):
            existing_df = pd.read_csv(csvFile, index_col=0)
        else:
            existing_df = pd.DataFrame({"Episode": [], "AvgRewards": [], "EpisodeRewards": []})
        new_df = pd.DataFrame(self.dataLog)
        updated_df = pd.concat([existing_df, new_df], ignore_index=True)
        updated_df.to_csv(csvFile)
        # conn = sqlite3.connect(f"{csvFile}.db")
        # updated_df.to_sql(name=f"{csvFile}", con=conn, index=False)
