<a href="https://github.com/triedeti/tf-object-detector">

# tf-object-detector

</a>

> A small component for you to start processing images and recognizing their content. Based on the amazing work by https://github.com/webrtcHacks/tfObjWebrtc


[![AppGif](https://github.com/triedeti/tf-object-detector/blob/master/docs/img/object_detector.gif?raw=true)]()

## Disclaimer

This is our effort to dockerize the work done by https://github.com/webrtcHacks/tfObjWebrtc maintaining most of the original code. 
_So why didn't we use his server image? (or better yet: why did we create this image in the first place?):_
 
 - We included waitress to mediate requests to the flask API;
 - We forced all working versions of python packages, base images and so on, to keep this as stable as possible;
 - We turned this into a self-contained (micro)service so that you can use it in your architecture without any hussle;
 - You can even modify or add things to the base docker image, to tune it further if you would like;
 - Open source the full code,  `Dockerfile` included;
 - Removed sample code from within the flask api;

It was our sole intention to contribute to the community what we had to do to get this to work on our own projects :heart: 

As you can see here, object detection runs in realtime returning a JSON of the objects detected in each frame. You simply have to post an image to the service and it will return something like this:

```javascript
[
    {
        "class_name": "car",
        "height": 0.5318315029144287,
        "score": 0.7755758762359619,
        "width": 0.7912412881851196,
        "x": 0.5782610177993774,
        "y": 0.3312181532382965
    },
    {
        "class_name": "car",
        "height": 0.4864712953567505,
        "score": 0.512231171131134,
        "width": 0.5383723974227905,
        "x": 0.4695549011230469,
        "y": 0.4001152515411377
    },
    {
        "class_name": "car",
        "height": 0.4555974006652832,
        "score": 0.4407155513763428,
        "width": 0.8605666756629944,
        "x": 0.7803468108177185,
        "y": 0.34807342290878296
    },
    {
        "class_name": "person",
        "height": 1.0,
        "score": 0.43984636664390564,
        "width": 0.5317587852478027,
        "x": 0.019111961126327515,
        "y": 0.0471099317073822
    }
]
```

The `class_name` property refers to the type of object detected within the chosen dataset (by default, we're using <a href="http://cocodataset.org" target="_blank">COCO dataset</a>)


## Table of Contents

- [Quickstart](#quickstart)
- [Prerequisites](#prerequisites)
- [Contributing](#contributing)
- [Contributors](#contributors)
- [Support](#support)
- [License](#license)

---

## Quickstart

 - Clone or download this repo onto your machine;
 - Open up a command line, and build the image:

 ```shell
docker build . --tag tf-object-detector
 ````

 - Have some patience, this may take a while... 
 - You should see something like this on your machine:
 ```shell
 Successfully built 
 Successfully tagged tf-object-detector:latest
 ```
 - Run a new container with the freshly built image:
 ```
 docker run -d -p 8080:8080 --name tf-object-detector tf-object-detector
```
 > Hint: if it doesn't work, check if you have the 8080 port available

 - If you open up your browser in <a href="http://localhost:8080" target="_blank">http://localhost:8080</a> you will see something like this:
 ```javascript
 {
    "about": "tf-object-detector v1.0.0",
    "now": "2020-03-30 10:00:00.00000",
    "tensorflow_model": "ssd_mobilenet_v1_coco_2017_11_17",
    "tensorflow_version": "1.15.2"
}
 ``` 
 - Now, you can simply open up the `docs/video.html` file on your preferred browser and click play on the video. Your newly created service will start processing each frame on the video! 

---

## Prerequisites

For this image to work, you only need <a href="https://docs.docker.com/install/" target="_blank">Docker installed on your machine or server</a>. That's all folks!

---

## Contributing

Any contributions to this project are more than welcome. Feel free to reach us and we will gladly include any improvements or ideas that you may have.
Please, fork this repository, make any changes and submit a Pull Request and we will get in touch!

## Contributors

| <a href="http://jdsantos.github.io" target="_blank">**Jorge Santos**</a> | <a href="https://github.com/leoneljdias" target="_blank">**Leonel Dias**</a> 
| :---: |:---:|
| [![jdsantos](https://avatars1.githubusercontent.com/u/1708961?v=3&s=50)](http://jdsantos.github.io)    | [![leoneljdias](https://avatars1.githubusercontent.com/u/4217810?v=3&s=50)](http://fvcproductions.com) |
| <a href="https://github.com/jdsantos" target="_blank">`github.com/jdsantos`</a> | <a href="https://github.com/leoneljdias" target="_blank">`github.com/leoneljdias`</a> 

## Support

The easiest way to seek support is by submiting an issue on this repo.
Also, reach out to us at one of the following places!

- Website at <a href="https:/triedeti.pt" target="_blank">`TriedeTI`</a>
- Twitter at <a href="https://twitter.com/TriedeTi" target="_blank">`@triedeti`</a>
- Facebook at <a href="https://facebook.com/triedeti" target="_blank">`@triedeti`</a>

---

## License

- **[MIT license](http://opensource.org/licenses/mit-license.php)**