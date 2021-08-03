import joblib


class SentimentClassifier(object):
    def __init__(self):
        self.pipeline = joblib.load('pipeline.pkl')

    @staticmethod
    def get_prediction_text(prediction):
        if prediction == 1:
            return "Это положительный отзыв"
        elif prediction == 0:
            return "Это отрицательный отзыв"
        elif prediction == -1:
            return "Ошибка оценки отзыва"
        else:
            return "Неожиданный результат"

    def predict_text(self, text):
        try:
            return self.pipeline.predict([text])[0]
        except:
            return -1

    def get_prediction_message(self, text):
        prediction = self.predict_text(text)
        return self.get_prediction_text(prediction)
