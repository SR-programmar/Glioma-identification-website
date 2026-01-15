import tensorflow as tf
from os import listdir, remove
from os.path import join, isfile


# Returns true if extension is valid
def valid_extension(filename):
    extensions = {"png", "jpg", "jpeg"}
    return filename[-3:] in extensions
    
# Removes the first file from local_image directory
def clear_dir():
    
    path = join("local_image", listdir("local_image")[0])

    if isfile(path):
        remove(path)

# Predicts whether an image has Glioma or not
def predict_image():

  path = join("local_image", listdir("local_image")[0])

  model = tf.keras.models.load_model("glioma_vs_normal.keras")

  raw_img = tf.io.read_file(path)
  raw_img = tf.image.decode_jpeg(raw_img, channels=3)

  img = tf.image.resize(raw_img, (224, 224))
  img = tf.expand_dims(img, axis=0)
  predictions = model.predict(img)
  probs = tf.nn.sigmoid(predictions)[0]

  chance_normal = round(probs[0].numpy(), 2) * 100
  chance_tumor = round(probs[1].numpy(), 2) * 100

  print(f"Normal: {chance_normal}%")
  print(f"Tumor: {chance_tumor}%")

  if chance_normal > chance_tumor:
    return f"Normal {chance_normal}% Positive"
  else:
    return f"Tumor: {chance_tumor}% Positive"


