import joblib
from parsing_reviews import get_reviews
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import SGDClassifier
from sklearn.pipeline import Pipeline
from pathlib import Path


class SentimentClassifier(object):
    def __init__(self):
        filename = 'pipeline.pkl'

        trained_model = Path(filename)
        if trained_model.is_file():
            self.pipeline = joblib.load(filename)
        else:
            self.train_classifier()

    @staticmethod
    def get_prediction_text(prediction):
        if prediction == 1:
            return "Is is positive review"
        elif prediction == 0:
            return "Is is negative review"
        elif prediction == -1:
            return "Evaluation error"
        else:
            return "Unexpected result"

    def predict_text(self, text):
        try:
            return self.pipeline.predict([text])[0]
        except:
            return -1

    def get_prediction_message(self, text):
        prediction = self.predict_text(text)
        return self.get_prediction_text(prediction)

    def train_classifier(self):
        train = get_reviews()

        print("Start training classifier")
        self.pipeline = Pipeline([('vectorizer', TfidfVectorizer(analyzer='char', max_df=0.8, ngram_range=(1, 15))),
                                  ('classifier', SGDClassifier(random_state=42))])
        self.pipeline.fit(train.text, train.label)

        joblib.dump(self.pipeline, 'pipeline.pkl')
        print("Classifier training completed")
