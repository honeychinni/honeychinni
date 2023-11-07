class Proposer:
    def __init__(self):
        self.v = None
        self.p_num = 0
        self.acks = 0
        self.promises = {}

    def propose(self, client_value, acceptors):
        self.p_num = max(self.p_num, max(a.p_num for a in acceptors)) + 1
        self.v = client_value
        self.acks = 0
        self.promises = {}
        print(f"Proposer sends <Prepare, {self.p_num}> to all acceptors")
        for acceptor in acceptors:
            acceptor.receive_prepare(self.p_num)

    def promise(self, n, promise, acceptors):
        if n != self.p_num:
            return  
        self.promises[promise] = True
        if len(self.promises) >= (len(acceptors) + 1) // 2:
            if any(self.promises):
                self.v = max(self.promises, key=self.promises.get)
            print(f"Proposer sends <Accept, {self.p_num}, {self.v}> to all acceptors")
            for acceptor in acceptors:
                acceptor.receive_accept(self.p_num, self.v)

    def accepted(self, n, acceptors, learners):
        if n != self.p_num:
            return 
        self.acks += 1
        if self.acks >= (len(acceptors) + 1) // 2:
            print(f"Proposer sends <Decide, {self.v}> to all learners")
            for learner in learners:
                learner.receive_decide(self.v)

    def nack(self, n):
        if n != self.p_num:
            return  
        self.abort()
        self.p_num = 0 

    def abort(self):
        pass

class Acceptor:
    def __init__(self):
        self.p_num = 0

    def receive_prepare(self, p_num):
        pass
        
    def receive_accept(self, p_num, value):
        pass



#Acceptor code
class Acceptor:
    def __init__(self):
        self.accepted_num = 0
        self.promised_num = 0
        self.accepted_value = None

    def on_prepare(self, n, sender):
        if self.promised_num < n:
            self.promised_num = n
            self.persist_state()
            promise_message = self.promise(self.accepted_num, self.accepted_value)
            print(f"Acceptor sends <Promise, {n}, {promise_message}> to {sender}")
        else:
            print(f"Acceptor sends <Nack, {n}> to {sender}")

    def on_accept(self, n, v, sender):
        if self.promised_num <= n:
            self.promised_num = n
            self.accepted_num = n
            self.accepted_value = v
            self.persist_state()
            print(f"Acceptor sends <Accepted, {n}> to {sender}")
        else:
            print(f"Acceptor sends <Nack, {n}> to {sender}")

    def persist_state(self):
       
        print("State persisted on disk.")

    def promise(self, accepted_num, accepted_value):
        return f"promise({accepted_num}, {accepted_value})"



acceptor = Acceptor()
acceptor.on_prepare(5, "Proposer1")
acceptor.on_accept(6, "Value", "Proposer2")

#Learner Code
class Learner:
    def receive_decide(self, value):
        pass
proposer = Proposer()
acceptors = [Acceptor() for _ in range(5)]
learners = [Learner() for _ in range(3)]
proposer.propose("some_value", acceptors)
class Learner:
    def __init__(self):
        self.decided_value = None

    def on_decide(self, v):
        if self.decided_value is None:
            self.decided_value = v
            self.learn(v)

    def learn(self, v):
        
        print(f"Learning: {v}")


learner = Learner()
learner.on_decide("SomeValue")
