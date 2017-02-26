import pickle
import logging
import os

logging.basicConfig(filename='log/predictor.log',level=logging.DEBUG)

class predictor:
    def __init__(self):
        self.model = None
        self.vector = None

    def load_model(self):
        try:
            with open(os.getcwd()+"/model/model_general.sav", "rb") as f:
                self.model = pickle.load(f)

            with open(os.getcwd()+"/model/vectorizer_general.sav", "rb") as f:
                self.vector = pickle.load(f)
        except:
            logging.error('FAILED LOAD MODEL')

    def predict(self,str):
        try:
            a = self.model.predict(self.vector.transform([str]).toarray())[0]
            return(a)
        except:
            logging.error('FAILED TO PREDICT')
            pass