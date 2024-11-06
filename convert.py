import tensorflow as tf

# Load your model
model = tf.keras.models.load_model('emotion_eye_combined_model_with_200_epochs.h5')

# Convert the model to TensorFlow Lite format
converter = tf.lite.TFLiteConverter.from_keras_model(model)
tflite_model = converter.convert()

# Save the TFLite model to a file
with open('android_model.tflite', 'wb') as f:
    f.write(tflite_model)
