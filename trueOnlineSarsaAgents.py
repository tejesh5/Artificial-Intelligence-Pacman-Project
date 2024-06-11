from game import *
from qlearningAgents import PacmanQAgent
from featureExtractors import *
import matplotlib.pyplot as plt
import glob
import pandas as pd
import util


class TrueOnlineSarsaAgent(PacmanQAgent):
    def __init__(self, extractor='IdentityExtractor', **args):
        PacmanQAgent.__init__(self, **args)
        self.featExtractor = util.lookup(extractor, globals())()
        self.weights = util.Counter()
        if "lamda" in dir(args): self.lamda = args['lamda']
        if "lr" in dir(args): self.alpha = args['lr']
        if "gamma" in dir(args): self.discount = args['gamma']
        if "eps" in dir(args): self.epsilon = args['eps']
        # print(args)
        
    def getWeights(self):
        return self.weights

    def getQValue(self, state, action):
        """
          Should return Q(state,action) = w * featureVector
          where * is the dotProduct operator
        """
        "*** YOUR CODE HERE ***"
        return  self.featExtractor.getFeatures(state, action) *  self.getWeights()

        # util.raiseNotDefined()

    def startEpisode(self):
        """
          Called by environment when new episode is starting
        """
        PacmanQAgent.startEpisode(self) 
        self.Qold = 0
        self.eligibility_trace = util.Counter()


    def getAction(self, state):
        legalActions =self.getLegalActions(state)
        action =None
        chance =util.flipCoin(self.epsilon)
        if (chance):
            action =  random.choice(legalActions) if legalActions \
            else None
            return action 
        action =  self.computeActionFromQValues(state)
        self.doAction(state, action)
        return action

    def update(self, state, action, nextState, reward):
        # x - feture function
        # z - self.eligibility_trace
        # w - self.weights
        # gamma -  self.discount 
        # lambda - self.lamda
        # Qold - store old Qold
        # fetch the next action based on Q val
        nextAction = self.getAction(nextState)
        # Q  <- w.T * x
        QVal = self.getQValue(state, action)
        # get Q val: Q' <- w.T * x'
        if nextAction is None:
            nextQVal = 0.0
        else:
            nextQVal = self.getQValue(nextState, nextAction)
        # delta - R + gamma*Q' - Q
        difference = reward + self.discount * nextQVal - QVal
        # fetch the features
        features = self.featExtractor.getFeatures(state, action) #nextState, nextAction
        sumEleFeatures = sum([self.eligibility_trace[feature_key] * features[feature_key] for feature_key in features])

        # updating the z and w
        for feature_key in features:
            # z <- gammma*lambda*z + (1-alpha*gamma*lambda*z.T*x)*x
            self.eligibility_trace[feature_key] = self.discount * self.lamda * self.eligibility_trace[feature_key] + \
            (1 - self.alpha * self.discount * self.lamda * sumEleFeatures) * features[feature_key]

            # w<-w + alpha(delta+Q-Qold)z-alpha(Q-Qold)x
            self.weights[feature_key] += self.alpha * (difference + QVal - self.Qold) * self.eligibility_trace[feature_key]\
                                        - self.alpha * (QVal - self.Qold) * features[feature_key]
        self.Qold = nextQVal


    def final(self, state):
        "Called at the end of each game."
        # call the super-class final method
        PacmanQAgent.final(self, state)
        
        self.dataLog["Episode"].append(self.episodesSoFar)
        # self.dataLog["AvgRewards"].append(self.accumTrainRewards / float(self.episodesSoFar))
        self.dataLog["EpisodeRewards"].append(self.episodeRewards)
        # self.dataInfo.append([self.episodesSoFar, self.accumTrainRewards / float(self.episodesSoFar), self.episodeRewards, self.lamda, self.epsilon, self.alpha])
        # get the average of 100 episodes
        NUM_REW_UPDATE = 100
        self.windowRewards.append(state.getScore())
        if self.episodesSoFar > NUM_REW_UPDATE:
             self.windowRewards.pop(0)
        self.dataLog["AvgRewards"].append(sum(self.windowRewards)/len(self.windowRewards))

    def saveResults(self, csvFile):
        # if already a csv there then apend to that for each run else create new CSV
        if glob.glob(csvFile):
            existing_df = pd.read_csv(csvFile, index_col=0)
        else:
            existing_df = pd.DataFrame({"Episode": [], "AvgRewards": [], "EpisodeRewards": []})
        new_df = pd.DataFrame(self.dataLog)
        updated_df = pd.concat([existing_df, new_df], ignore_index=True)
        updated_df.to_csv(csvFile)