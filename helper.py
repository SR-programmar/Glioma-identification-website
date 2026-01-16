import tensorflow as tf
from os import listdir, remove
from os.path import join, isfile

# Local image directory
local_dir = "local_image"


# Returns true if extension is valid
def valid_extension(filename):
    extensions = {"png", "jpg", "jpeg"}
    return filename[-3:] in extensions

# Very first image of the local_dir
def first_img():
   return join(local_dir, listdir(local_dir)[0])
    
# Removes the first file from local_image directory
def clear_dir():
    if len(listdir(local_dir)) > 0:
      path = first_img()

      if isfile(path):
        remove(path)

# Predicts whether an image has Glioma or not
def predict_image():

  path = first_img()

  model = tf.keras.models.load_model("glioma_vs_normal.keras")

  raw_img = tf.io.read_file(path)

  # Only PNG and JPEG are acceptable
  if path[-3:] == "png":
     raw_img = tf.image.decode_png(raw_img, channels=3)
  else:
    raw_img = tf.image.decode_jpeg(raw_img, channels=3)
  

  img = tf.image.resize(raw_img, (224, 224))
  img = tf.expand_dims(img, axis=0)
  predictions = model.predict(img)
  probs = tf.nn.sigmoid(predictions)[0]

  chance_tumor = int(round(probs[0].numpy(), 2) * 100)
  chance_normal = int(round(probs[1].numpy(), 2) * 100)


  if chance_normal > chance_tumor:
    return f"Normal: {chance_normal}% Positive"
  else:
    return f"Glioma: {chance_tumor}% Positive"


