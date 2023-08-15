# Webservice for Next Event Prediction using different Predictive Process Monitoring Techniques

## What is this project?

This is a web application to analyze event logs and train predictive models in order to conduct next event predictions. The implemented techniques are Long Stort-Term Memory, Convolutional Neural Network and Decision Tree.

## How to run the project?

### 1. Clone repository
```
git clone https://gitlab.lrz.de/wiebkefreitag/ppm-web-app
```

### 2. Start virtual environment
```
python3 -m venv venv && source venv/bin/activate
```

### 3. Install Dependencies and Build Frontend
```
cd frontend             
npm install      
npm run build
```

### 4. Install Dependencies and Start Web Application
```
pip install -r requirements.txt 
python main.py
```

In case of error `[Errno 28] No space left on device while installing TensorFlow`:
```
TMPDIR=/home/students/<id>/pip-cache/ pip install --cache-dir=/home/students/<id>/pip-cache/ --build /home/students/<id>/pip-cache/ tensorflow==2.12.0
```

### Endpoints
Endpoints can be found at ```/docs```

### Additional Information
- the application is run on port '9999'
- the folder 'RESULTS' contains data and scripts for the Bachelor's Thesis
- the event logs of the data collection are located in folder 'DATASETS'