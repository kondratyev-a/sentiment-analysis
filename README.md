Для запуска демонстрации необходимо:
1. Запустить файл train_classifier.py и дождаться завершения.
2. Запустить файл demo.py (я запускал через pycharm).
3. Открыть в браузере http://localhost/sentiment-analysis
4. Ввести текст отзыва и нажать Оценить.
5. Примеры работы алгоритма можно посмотреть в папке screenshots


2. Описание файлов

1.2 Основные файлы
static/css/main.css - стили для визуального оформления страницы
templates/main.html - шаблон веб-страницы с демонстрацией
demo.py - основной скрипт
sentiment_classifier.py - модель для оценки отзыва
pipeline.pkl - сохраненный Pipeline

1.2 Вспомогательные файлы
parsing_reviews.py - парсинг данных
classifier_test.py - тест работы классификатора без веб обвязки
products_sentiment_train.tsv - отзывы для тренировки модели
train_classifier.py - обучение классификатора и сохранение его в файл pipeline.pkl
logs.txt - история работы классификатора
screenshots - примеры работы алгоритма
