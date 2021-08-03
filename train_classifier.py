import joblib
from parsing_reviews import get_reviews
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import SGDClassifier
from sklearn.pipeline import Pipeline

train = get_reviews()

pipeline = Pipeline([('vectorizer', TfidfVectorizer(analyzer='char', max_df=0.8, ngram_range=(1, 15))),
                     ('classifier', SGDClassifier(random_state=42))])
pipeline.fit(train.text, train.label)

joblib.dump(pipeline, 'pipeline.pkl')
print("Classifier training completed")
