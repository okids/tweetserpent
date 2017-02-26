import pickle

class predictor:
    def __init__(self):
        self.model = None
        self.vector = None


    def load_model(self):
        with open("model_anies.sav", "rb") as f:
            self.model = pickle.load(f)

        with open("vectorizer_anies.sav", "rb") as f:
            self.vector = pickle.load(f)

    def prediksi(self,str):
        a = self.model.predict(self.vector.transform([str]).toarray())[0]
        if int(a) is 1:
            print('Sentimen Positif')
        else:
            print('Sentimen Negatif')
