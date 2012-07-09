class PDA(object):
    def __init__(self,Q,SIGMA,GAMMA,epsilon,q0,F):
        self.Q = Q
        self.SIGMA = SIGMA
        self.GAMMA = GAMMA
        self.epsilon = epsilon
        self.q0 = q0
        self.F = F
        self.stack = []
        self.state = q0
        self.input = tuple()

    def compute(curr_tup):
        if curr_tup not in epsilon:
            
