### Flask Video Api

A simple Flask-Video-Api that allows for uploading videos, previewing keyframes, adding filters and downloading the edited video.
Build in Flask and Python

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
