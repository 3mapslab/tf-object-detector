# This is a shameless copy of the amazing work by webrtcHacks (https://github.com/webrtcHacks/tfObjWebrtc) with a few minor tweaks to get it to
# work on my case. You can find the original code in webrtcHacks repository if you want.

import numpy as np
import os
import six.moves.urllib as urllib
import tarfile
import tensorflow as tf
import json

# Object detection imports
from object_detection.utils import label_map_util    ### CWH: Add object_detection path

# See if Tensorflow was executed correctly...
print("Running Tensorflow %s..." % (tf.__version__))

# Model Preparation

# What model to download.
MODEL_NAME = 'model'

# Path to frozen detection graph. This is the actual model that is used for the object detection.
PATH_TO_CKPT = MODEL_NAME + '/frozen_inference_graph.pb'

# List of the strings that is used to add correct label for each box.
PATH_TO_LABELS = os.path.join('object_detection/data', 'mscoco_label_map.pbtxt') ### CWH: Add object_detection path

NUM_CLASSES = 90

# Load a (frozen) Tensorflow model into memory.
detection_graph = tf.Graph()
with detection_graph.as_default():
  od_graph_def = tf.compat.v1.GraphDef()
  with tf.io.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
    serialized_graph = fid.read()
    od_graph_def.ParseFromString(serialized_graph)
    tf.import_graph_def(od_graph_def, name='')

# Loading label map
label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
category_index = label_map_util.create_category_index(categories)

detection_graph.as_default()
sess = tf.compat.v1.Session(graph=detection_graph)
# Definite input and output Tensors for detection_graph
image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
# Each box represents a part of the image where a particular object was detected.
detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
# Each score represent how level of confidence for each of the objects.
# Score is shown on the result image, together with the class label.
detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')
num_detections = detection_graph.get_tensor_by_name('num_detections:0')

# Helper code
def load_image_into_numpy_array(image):
  (im_width, im_height) = image.size
  return np.array(image.getdata()).reshape(
      (im_height, im_width, 3)).astype(np.uint8)

# added to put object in JSON
class Object(object):
    def toJSON(self):
        return json.dumps(self.__dict__)

def get_objects(image, target_class, threshold=0.5):
  image_np = load_image_into_numpy_array(image)
  # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
  image_np_expanded = np.expand_dims(image_np, axis=0)
  # Actual detection.
  (boxes, scores, classes, num) = sess.run(
      [detection_boxes, detection_scores, detection_classes, num_detections],
      feed_dict={image_tensor: image_np_expanded})

  classes = np.squeeze(classes).astype(np.int32)
  scores = np.squeeze(scores)
  boxes = np.squeeze(boxes)
  
  if target_class is not None:
      target_ids = []
      
      target_list = target_class.split(',')
      
      for line in category_index.values():
          if line['name'] in target_list: 
            target_ids.append(line['id'])
            break

      if len(target_ids) > 0:
          list_indices = []

          # Getting the indices of the objects where there was a detection of at least one of the target classes
          for target_id in target_ids:
              list_indices = list_indices + np.argwhere(classes == target_id).tolist()

          flatten = lambda list_of_lists: [item for sublist in list_of_lists for item in sublist] # lambda function that converts a lsit of lists into a single-dimension list
          
          # Flattening the list to enable the removal of duplicate indices
          flattened_list = flatten(list_indices)

          # Get distinct indices (in cases where the detection found more than one of the target classes)
          unique_indices = list(set(flattened_list))                  # Removing the duplicate indices with the set
          #unique_indices = np.array([[el] for el in unique_indices])  # Changing the list format into a list of lists, as is returned from the numpy argwhere function
          
          # Filtering out the results that were not found to be of the target class
          classes = np.squeeze(classes[unique_indices])
          scores = np.squeeze(scores[unique_indices])
          boxes = np.squeeze(boxes[unique_indices])

  output = []

  for c in range(0, len(classes)):
      class_name = category_index[classes[c]]['name']
      if scores[c] >= threshold:      # only return confidences equal or greater than the threshold
          # print(" object %s - score: %s, coordinates: %s" % (class_name, scores[c], boxes[c]))
          item = Object()
          item.class_name = class_name
          item.score = float(scores[c].item())
          item.y = float(boxes[c][0].item())
          item.x = float(boxes[c][1].item())
          item.height = float(boxes[c][2].item())
          item.width = float(boxes[c][3].item())
          output.append(item)
  
#   outputJson = json.dumps([ob.__dict__ for ob in output], indent=4, sort_keys=True, default=str)

  result = [ob.__dict__ for ob in output]
  return result