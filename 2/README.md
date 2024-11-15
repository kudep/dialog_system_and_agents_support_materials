## 2. Работа с HTTP-запросами
- Примеры запросов и ответов в формате JSON.
- Поддержка Server-Sent Events (SSE) для потоковых данных.
- Обработка запросов с разными модальностями:
  - Картинки.
  - Звук/видео.


### 1. Примеры запросов и ответов в формате JSON

#### Пример 1: Текстовая классификация
Запрос:
```json
{
  "text": "This is a great product! Highly recommend it."
}
```

Ответ:
```json
{
  "label": "positive",
  "score": 0.98
}
```

---

#### Пример 2: Извлечение сущностей (NER)
Запрос:
```json
{
  "text": "John works at OpenAI in San Francisco."
}
```

Ответ:
```json
[
  {
    "entity": "PERSON",
    "value": "John",
    "start": 0,
    "end": 4
  },
  {
    "entity": "ORG",
    "value": "OpenAI",
    "start": 14,
    "end": 20
  },
  {
    "entity": "GPE",
    "value": "San Francisco",
    "start": 24,
    "end": 37
  }
]
```

---

### 2. Поддержка Server-Sent Events (SSE) для потоковых данных

Описание:
SSE позволяет клиенту получать данные от сервера в режиме реального времени. Подходит для потоковых ответов, таких как генерация текста или трансляция событий.

Пример реализации SSE-сервера на Flask:
```python
from flask import Flask, Response
import time

app = Flask(__name__)

def generate_events():
    for i in range(1, 6):
        yield f"data: {{\"message\": \"Step {i}\"}}\n\n"
        time.sleep(1)

@app.route('/stream')
def stream():
    return Response(generate_events(), content_type='text/event-stream')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
```

Клиентский запрос:
```javascript
const eventSource = new EventSource("http://localhost:5000/stream");

eventSource.onmessage = function(event) {
    console.log("New message:", event.data);
};
```

---

### 3. Обработка запросов с разными модальностями

#### 3.1 Картинки

Описание:
Для обработки изображений используется передача файлов в формате `multipart/form-data` или кодировка в Base64.

Пример API для классификации изображения:
Запрос:
```json
{
  "image": "/9j/4AAQSkZJRgABAQAAAQABAAD/..."  // Base64-кодированное изображение
}
```

Ответ:
```json
{
  "label": "cat",
  "confidence": 0.95
}
```

Flask-пример обработки изображения:
```python
from flask import Flask, request, jsonify
from PIL import Image
import base64
import io

app = Flask(__name__)

@app.route('/classify', methods=['POST'])
def classify():
    data = request.json
    image_data = base64.b64decode(data['image'])
    image = Image.open(io.BytesIO(image_data))
    # Заглушка модели:
    result = {"label": "cat", "confidence": 0.95}
    return jsonify(result)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
```

---

#### 3.2 Звук

Описание:
Передача аудиофайлов осуществляется через `multipart/form-data` или ссылку на удалённый файл.

Пример API для распознавания речи:
Запрос:
- Передача через `multipart/form-data`:
  ```
  POST /transcribe HTTP/1.1
  Content-Type: multipart/form-data; boundary=----WebKitFormBoundary
  ------WebKitFormBoundary
  Content-Disposition: form-data; name="file"; filename="audio.wav"
  Content-Type: audio/wav
  ------WebKitFormBoundary--
  ```

Ответ:
```json
{
  "transcription": "Hello, how can I help you?"
}
```

Flask-пример обработки звука:
```python
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/transcribe', methods=['POST'])
def transcribe():
    file = request.files['file']
    # Заглушка распознавания:
    transcription = "Hello, how can I help you?"
    return jsonify({"transcription": transcription})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
```

---

#### 3.3 Видео

Описание:
Для обработки видео используется передача ссылок на файлы или загрузка через `multipart/form-data`. Обработка может включать распознавание объектов, событий или лиц.

Пример API для анализа видео:
Запрос:
```json
{
  "video_url": "https://example.com/video.mp4"
}
```

Ответ:
```json
{
  "detected_objects": [
    {"label": "car", "timestamp": "00:00:10", "confidence": 0.98},
    {"label": "person", "timestamp": "00:00:15", "confidence": 0.93}
  ]
}
```

Flask-пример анализа видео:
```python
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    video_url = data['video_url']
    # Заглушка анализа:
    result = {
        "detected_objects": [
            {"label": "car", "timestamp": "00:00:10", "confidence": 0.98},
            {"label": "person", "timestamp": "00:00:15", "confidence": 0.93}
        ]
    }
    return jsonify(result)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
```

---

Эти примеры и описания показывают, как обрабатывать запросы с различными модальностями и форматами данных.