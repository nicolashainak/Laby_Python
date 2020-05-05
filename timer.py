from threading import Timer,Thread,Event


class PerpetualTimer():

    def __init__(self,fps,tick):
        self.fps=fps
        self.tick = tick
        self.thread = None #Timer(self.t,self.handle_function)
        self.isrunning=False
        self.run()
        
    def handle_function(self):
        #controle du temps depart stop decider combien on attend ou non +s=cancel et restart 
        # //regarder si on peu chanegr la valeur dans pyton du timer 
        assert self.thread is not None
        assert self.isrunning 
        self.tick()
        self.thread.cancel()
        self.thread = Timer(1/self.fps,self.handle_function)
        self.thread.start()

    def set_fps(self,fps):
        #convertir fps en seconde 
        self.fps=fps    
        if self.isrunning:
            self.cancel()
            self.start()
        
    
    def run(self):
        if (self.isrunning):
            return 
        self.thread = Timer(1/self.fps,self.handle_function)
        self.thread.start()
        self.isrunning=True   

    def running(self):
        return self.isrunning
    
    #peut etre enlever
    def start(self):
        if (self.isrunning):
            return 
        self.thread = Timer(1/self.fps,self.handle_function)
        self.thread.start()
        self.isrunning=True

    def cancel(self):
        if self.isrunning:
            self.thread.cancel()
            self.thread=None
            self.isrunning=False

def printer():
    print ('ipsem lorem')

#t = perpetualTimer(5,printer)
#t.start()