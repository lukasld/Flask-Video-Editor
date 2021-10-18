# Runway Backend Engineer Challenge

### Context

At Runway, we're building web-based, interactive tools that enable creators of all kinds to incorporate machine learning models in their creative workflows. Most recently, we have started releasing a series of tools for video creation such as [Green Screen](https://runwayml.com/green-screen/) and [Sequel](https://runwayml.com/sequel/), with the aim of speeding up processes in video editing / VFX that have traditionally been time-consuming or required expensive equipment.

One big component of our product is a cloud export functionality, which allows processing videos remotely and applying transformations on them, from machine learning models to more traditional graphics effects.

### Goal

The goal of this exercise is to create a **Video Filter API** service that could be used in a hypothetical app where users can upload input videos, process them to add some simple effects to them, and export the results.

Specifically, the service should support the following effects:

* __Grayscale It!__: Turn every frame of the input video into grayscale.
* __Blur It!__: Apply Gaussian blur on each of the frames of the video.
* __Edge Detect It!__: Apply [Canny edge detection](https://en.wikipedia.org/wiki/Canny_edge_detector) on each of the frames of the video.

In addition, clients of the API should be able to perform the following actions:

* List all the available commands and input parameters associated with each command, if any.
* Upload a video to the service to be processed.
* Preview the results of a command and given parameters on a single frame of the video.
* Submit a video export with a command and input parameters.
* Track the progress of a video export.
* Download the final result of the export.

You can use any language or framework for the project. Please note that there's no need to build a super complex and deeply comprehensive solution. We're primarily interested in how you think about the problem and approach the challenge from an API design perspective.

**Bonus points for**:

* Adding a filter of your own choosing to the service!
* Automatically generating docs for your API with a framework like [Swagger](https://swagger.io/).

**You don't need to worry about**:

* Implementing the effects from scratch - you can use an existing implementation from an image processing library.
* Supporting a variety of video formats or related edge cases (e.g. very high resolutions). Supporting 720p video on a standard format (e.g. H.264 MP4) would be enough.
* Implementing any kind of authentication or authorization logic.

## Time-Frame

End of challenge: Sunday August 1st, 2021

## License

Please do not post this repo or make it public without Runway's consent.


## Lukas's Notes


### Requirements

- Make sure that you have pip installed `$ which pip`
- Python version `3.5+`
- `ffmpeg`

### Setup Guidlines

1. `$ cd` into the repository - `lukas-debiasi_engineering_challenge`
2. Create environment - through issuing `$ python3 -m venv venv`
3. Activate environment through:`$ source venv/bin/activate`
4. Install dependencies `$ pip install -r requirements.txt`
5. Create a shell `run.sh` script to set up the required environment variables
    - `$ touch run.sh` - to create run.sh
    - copy paste this into `run.sh`:
    
    ```
    #!/bin/sh

    . ./venv/bin/activate

    export FLASK_CONFIG='development'
    export FLASK_APP='video_api.py'
    export SECRET_KEY='asecretkey'

    export VIDEO_EXTENSION='.mp4'
    export IMG_EXTENSION='.png'
    export VIDEO_WIDTH=1280
    export VIDEO_HEIGHT=720

    export FLASK_DEBUG=1
    flask run --host=0.0.0.0 --port=5000
    ```
    
6. Change the permissions of `run.sh` to make it executable running the following command: `$ sudo chmod 750 run.sh`
7. Start the server and set the environment variables - through calling `$ . ./run.sh`

### Usage Examples:

I used curl to test the endpoints. <br>

#### Video Upload

* To upload a video issue:
    ```
    curl -X POST -H "Content-Type: multipart/form-data" \
    -F "file=@/<absolute>/<path>/<to>/<video>/<videoname>.mp4;Type=video/mp4" \
    -j -D "./cookie.txt" \
    "0.0.0.0:5000/videoApi/v1/upload/"
    ```
    This can take a little bit depending on your video length - youll get a response if successful

#### Frame Preview

* To preview a frame in the video issue:
    ```
    curl -X GET -H "Content-Type: application/json" \
    -b './cookie.txt' \
    -d '{"filter_params":{"type":""}}' \
    '0.0.0.0:5000/videoApi/v1/preview/<int: your frame of choice>/' > preview.png
    ```

* To preview a frame in the video - adding a filter - issue one of the following:

    * GAUSS
        ```
        curl -X GET -H "Content-Type: application/json" \
        -b './cookie.txt' \
        -d '{"filter_params":{"type":"gauss", "ksize_x":31, "ksize_y":31}}' \
        '0.0.0.0:5000/videoApi/v1/preview/5000/' > preview_gauss.png
        ```

    * CANNY
        ```
        curl -X GET -H "Content-Type: application/json" \
        -b './cookie.txt' \
        -d '{"filter_params":{"type":"canny", "thresh1":"10", "thresh2":200}}' \
        '0.0.0.0:5000/videoApi/v1/preview/2000/' > preview_canny.png
        ```

    * LAPLACIAN
        ```
        curl -X GET -H "Content-Type: application/json" \
        -b './cookie.txt' \
        -d '{"filter_params":{"type":"laplacian"}}' \
        '0.0.0.0:5000/videoApi/v1/preview/50000/' > preview_laplacian.png
        ```

    * GREYSCALE
        ```
        curl -X GET -H "Content-Type: application/json" \
        -b './cookie.txt' \
        -d '{"filter_params":{"type":"greyscale"}}' \
        '0.0.0.0:5000/videoApi/v1/preview/20000/' > preview_greyscale.png
        ```

#### Download

* To download the video with filters use the following:

    * GAUSS: <br> 
    `ksize_x` and `ksize_y` - need to be ODD numbers, `min_f` the start-frame where the filter should be applied and `max_f` is the end-frame where the filter should be applied.

        ```
        curl -X POST -H "Content-Type: application/json" \
        -b './cookie.txt' \
        -d '{"fps":"23.98", "filter_params":{"type":"gauss", "ksize_x":31, "ksize_y":31, "min_f":"200", "max_f": 10000}}' \
        '0.0.0.0:5000/videoApi/v1/download/' > download_gauss.mp4
        ```

    * CANNY: <br> 
    `thresh1` and `thresh2` - should be positive ints.
        ```
        curl -X POST -H "Content-Type: application/json" \
        -b './cookie.txt' \
        -d '{"fps":"23.98", "filter_params":{"type":"canny", "thresh1":100, "thresh2":200 }}' \
        '0.0.0.0:5000/videoApi/v1/download/' > download_canny.mp4
        ```

    * LAPLACIAN: <br> 
    `min_f` the start-frame where the filter should be applied and `max_f` is the end-frame where the filter should be applied.
        ```
        curl -X POST -H "Content-Type: application/json" \
        -b './cookie.txt' \
        -d '{"fps":"23.98", "filter_params":{"type":"laplacian", "min_f":"200", "max_f": 300}}' \
        '0.0.0.0:5000/videoApi/v1/download/' > download_laplacian.mp4
        ```

   * GREYSCALE:
        ```
        curl -X POST -H "Content-Type: application/json" \
        -b './cookie.txt' \
        -d '{"fps":"23.98", "filter_params":{"type":"greyscale", "min_f":"200", "max_f": 300}}' \
        '0.0.0.0:5000/videoApi/v1/download/' > download_greyscale.mp4
        ```

#### Status

During preview and download you can always check the progress:

    ```
    curl -X GET -H "Content-Type: application/json" \
    -b "./cookie.txt" \
    '0.0.0.0:5000/videoApi/v1/status/'
    ```

#### Help

For Help you can issue:

```
curl -X GET -H "Content-Type: application/json" \
-b './cookie.txt' \
'0.0.0.0:5000/videoApi/v1/help/'
```

For help on endpoints:

```
curl -X GET -H "Content-Type: application/json" \
-b './cookie.txt' \
'0.0.0.0:5000/videoApi/v1/help/<endpoints>/'
```

For help on filters:

```
curl -X GET -H "Content-Type: application/json" \
-b './cookie.txt' \
'0.0.0.0:5000/videoApi/v1/help/filters/<filtername>'
```

### Limitations and Todo's:

- Swagger
- The API is designed around accepting `.mp4` @ `720p`.
- I tried to cover most grounds and exceptions but might need a second pair of eyes.
- Automated Testing
- Developed and tested on Ubuntu 20.04.




