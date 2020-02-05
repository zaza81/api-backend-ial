#install libraries
pip install -r requirements.txt

#runing the app
python app.py

#running tests
pytest .

#running tests with coverage
pytest . -v --cov-report html  --cov=app tests/
