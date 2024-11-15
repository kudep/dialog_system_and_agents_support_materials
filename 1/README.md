
## 1. Структура диалоговой системы

Вспоминаем структуру с лекции [здесь](https://docs.google.com/presentation/d/1stT-hwl3eaMJhICEVprsNoVcOcX2X29xF1WB8xTfJbw/edit?usp=sharing)


Технологии размещения моделей:
- В одном процессе.
- Разделенные на отдельные процессы:
  - В отдельном процессе
  - Docker-сервисы.
  - Кластеры Kubernetes.
  - Системы, доступные через API.


### Сравнительная таблица

| Метод                | Простота | Масштабируемость | Производительность | Отказоустойчивость | Сложность внедрения |
| -------------------- | -------- | ---------------- | ------------------ | ------------------ | ------------------- |
| В одном процессе     | +++      | -                | +++                | -                  | +                   |
| В отдельном процессе | ++       | +                | ++                 | +                  | +                   |
| Docker-сервисы       | ++       | ++               | ++                 | ++                 | ++                  |
| Kubernetes-кластеры  | +        | +++              | ++                 | +++                | ---                 |
| Системы через API    | ++       | ++               | +                  | ++                 | ++                  |

Каждый подход выбирается исходя из требований проекта, уровня нагрузки, бюджета и наличия ресурсов для поддержки инфраструктуры.



### Примеры запуска сервиса для каждой технологии размещения моделей

---

#### **1. В одном процессе**
Пример: сервис на Python, объединяющий модель и API в одном процессе.

```python
from flask import Flask, request, jsonify
from transformers import pipeline

app = Flask(__name__)
model = pipeline("text-classification")

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    prediction = model(data['text'])
    return jsonify(prediction)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
```

Запуск:
```bash
python service.py
```

---

#### **2. В отдельном процессе**
Пример: отдельно запущенный процесс для модели и для API.

**Сервис модели (model_service.py):**
```python
from transformers import pipeline
from flask import Flask, request, jsonify

app = Flask(__name__)
model = pipeline("text-classification")

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    prediction = model(data['text'])
    return jsonify(prediction)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001)
```

**Сервис API (api_service.py):**
```python
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

MODEL_URL = "http://localhost:5001/predict"

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    response = requests.post(MODEL_URL, json=data)
    return response.json()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
```

Запуск:
```bash
python model_service.py & python api_service.py
```

---

#### **3. Docker-сервисы**
Пример Dockerfile для модели:

**Dockerfile:**
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY model_service.py .

CMD ["python", "model_service.py"]
```

**Файл `docker-compose.yml`:**
```yaml
version: "3.9"
services:
  model-service:
    build: .
    ports:
      - "5001:5001"
  api-service:
    image: python:3.9-slim
    working_dir: /app
    volumes:
      - ./api_service.py:/app/api_service.py
    command: python api_service.py
    ports:
      - "5000:5000"
```

Запуск:
```bash
docker-compose up
```

---

#### **4. Kubernetes-кластеры**
Пример для модели и API в Kubernetes.

**Деплоймент модели (`model-deployment.yaml`):**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: model-service
spec:
  replicas: 2
  selector:
    matchLabels:
      app: model
  template:
    metadata:
      labels:
        app: model
    spec:
      containers:
      - name: model
        image: your-docker-hub/model-service:latest
        ports:
        - containerPort: 5001
---
apiVersion: v1
kind: Service
metadata:
  name: model-service
spec:
  selector:
    app: model
  ports:
    - protocol: TCP
      port: 5001
      targetPort: 5001
```

**Деплоймент API (`api-deployment.yaml`):**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-service
spec:
  replicas: 1
  selector:
    matchLabels:
      app: api
  template:
    metadata:
      labels:
        app: api
    spec:
      containers:
      - name: api
        image: your-docker-hub/api-service:latest
        ports:
        - containerPort: 5000
---
apiVersion: v1
kind: Service
metadata:
  name: api-service
spec:
  selector:
    app: api
  ports:
    - protocol: TCP
      port: 5000
      targetPort: 5000
```

Запуск:
```bash
kubectl apply -f model-deployment.yaml
kubectl apply -f api-deployment.yaml
```

---

#### **5. Системы через API**
Пример использования готового API (например, OpenAI API):

```python
import openai
from flask import Flask, request, jsonify

app = Flask(__name__)
openai.api_key = "your-openai-api-key"

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=data['text'],
        max_tokens=50
    )
    return jsonify(response)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
```

Запуск:
```bash
python api_service.py
```

---

Эти примеры помогут организовать запуск сервиса с учетом выбранной технологии.