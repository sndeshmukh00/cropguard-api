from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import numpy as np
from io import BytesIO
from PIL import Image
import tensorflow as tf
from os import environ as env

app = FastAPI()

# Import MongoDB Atlas client
import mongo_db

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Loading trained model
MODEL = tf.keras.models.load_model("./saved_models/1")

# Loading model labels
with open("rice_disease_names.txt", 'r') as f:
    CLASS_NAMES = f.read().split('\n')

@app.get("/ping")
async def ping():
    return f"{env['ENV_NAME']} Api is alive"

def read_file_as_image(data) -> np.ndarray:
    image = np.array(Image.open(BytesIO(data)))
    return image

@app.post("/predict")
async def predict(
    file: UploadFile = File(...)
):
    image = read_file_as_image(await file.read())
    # Resize the image to the desired shape (256x256)
    image = resize_image(image, (256, 256))

    img_batch = np.expand_dims(image, 0)

    predictions = MODEL.predict(img_batch)
    index = np.argmax(predictions[0])

    class_name = CLASS_NAMES[np.argmax(predictions[0])]
    confidence_score = np.max(predictions[0])

    # Retrieving data from MongoDB Atlas
    disease_data = mongo_db.open_mongo_diseases(index)
    print(disease_data)
    disease_name = disease_data['name']
    caused_by=disease_data['caused_by']
    about=disease_data['about']
    cure=disease_data['cure']

    return {
        'class': class_name,
        'confidence': float(confidence_score),
        'name': disease_name,
        'caused_by': caused_by,
        'about': about,
        'cure': cure
    }

def resize_image(image, size):
    # Resize the image to the desired size using PIL
    image = Image.fromarray(image)
    image = image.resize(size)
    # Convert the resized image back to a numpy array
    image = np.array(image)
    return image

if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=8000)
