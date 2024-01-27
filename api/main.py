from fastapi import FastAPI, File, UploadFile
import uvicorn
import numpy as np
from io import BytesIO
from PIL import Image
import tensorflow as tf
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# making a global variable for load the cnn model

#MODEL = tf.keras.models.load_model("../../Proteger_v1/models/proteger_model")
MODEL = tf.keras.models.load_model("../../Proteger_v1/models/proteger.h5")

# making the global variable for disease type - class name
#all-proteger_v1
CLASS_NAMES = ["Apple___Apple_scab", "Apple___Black_rot", "Apple___Cedar_apple_rust", "Apple___healthy", "Blueberry___healthy", "Cherry___Powdery_mildew", "Cherry___healthy", "Corn___Cercospora_leaf_spot Gray_leaf_spot", "Corn___Common_rust", "Corn___Northern_Leaf_Blight", "Corn___healthy", "Grape___Black_rot", "Grape___Esca_Black_Measles", "Grape___Leaf_blight", "Grape___healthy", "Orange___Citrus_greening", "Peach___Bacterial_spot", "Peach___healthy", "Pepper___Bacterial_spot", "Pepper___healthy", "Potato___Early_blight", "Potato___Late_blight", "Potato___healthy", "Raspberry___healthy", "Soybean___healthy", "Squash___Powdery_mildew", "Strawberry___Leaf_scorch", "Strawberry___healthy", "Tomato___Bacterial_spot", "Tomato___Early_blight", "Tomato___Late_blight", "Tomato___Leaf_Mold", "Tomato___Septoria_leaf_spot", "Tomato___Spider_mites Two-spotted_spider_mite", "Tomato___Target_Spot", "Tomato___Tomato_Yellow_Leaf_Curl_Virus", "Tomato___Tomato_mosaic_virus", "Tomato___healthy"]

@app.get("/ping")
async def ping():
    return "hello, I am alive"


# binary image converted to numpy array
def read_file_as_image(data) -> np.ndarray:
    image = np.array(Image.open(BytesIO(data)))
    return image

# getting the image to the backend and a file
@app.post("/predict")
async def predict(
        file: UploadFile = File(...)
):
    image = read_file_as_image(await file.read())
    # give the numpy array to the model
    img_batch = np.expand_dims(image, 0)
    predictions = MODEL.predict(img_batch)
    #get the predicted class
    predicted_class = CLASS_NAMES[np.argmax(predictions[0])]
    #get the accuracy
    confidence = np.max(predictions[0])
    return {
        'class': predicted_class,
        'confidence': float(confidence)
    }


if __name__ == "__main__":
    uvicorn.run(app, host='localhost', port=8000)
