# https://towardsdatascience.com/object-detection-with-10-lines-of-code-d6cb4d86f606
FROM tensorflow/tensorflow:1.15.2-py3

ENV DEBIAN_FRONTEND noninteractive

ENV TENSORFLOW_MODEL ssd_mobilenet_v1_coco_2017_11_17

WORKDIR /

RUN apt-get update

RUN pip3 install --upgrade pip

RUN apt-get install -y python-pil python-lxml python-tk unzip 

# It is safer and recomended by Tensorflow to compile protobufs with this specific release
ADD https://github.com/google/protobuf/releases/download/v3.0.0/protoc-3.0.0-linux-x86_64.zip protobuf.zip
RUN unzip protobuf.zip
RUN chmod +rx /bin/protoc

COPY ./ /

RUN pip3 install --upgrade -r requirements.pip

ADD https://github.com/tensorflow/models/archive/master.zip models-master.zip
RUN unzip models-master.zip -d /tmp
RUN cp -R /tmp/models-master/research/object_detection /object_detection
RUN rm -rf /tmp/models-master

# Compile Protos 
RUN ./bin/protoc object_detection/protos/*.proto --python_out=.

# Download object detection models
ADD http://download.tensorflow.org/models/object_detection/${TENSORFLOW_MODEL}.tar.gz  /tmp/model.tar.gz

RUN mkdir -p /model

RUN tar -xvzf /tmp/model.tar.gz --one-top-level -C /tmp

RUN cp /tmp/model/${TENSORFLOW_MODEL}/frozen_inference_graph.pb /model

#Add needed paths

ENV PYTHONPATH "${PYTHONPATH}:/object_detection"

ENV PYTHONPATH "${PYTHONPATH}:/object_detection/models/research"

ENV PYTHONPATH "${PYTHONPATH}:/object_detection/models/research/slim"

EXPOSE 8080

CMD python /app/waiter.py
