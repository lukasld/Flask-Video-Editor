import os
from flask import Flask, request, redirect, \
                  url_for, session, jsonify, send_from_directory, make_response, send_file

from . import api
from . import utils
from .. import VIDEO_UPLOAD_PATH, FRAMES_UPLOAD_PATH, IMG_EXTENSION, VIDEO_EXTENSION, CACHE

from . VideoProcessing import Frame, VideoUploader, VideoDownloader, Filter
from . decorators import parameter_check, url_arg_check, metadata_check
from . errors import InvalidAPIUsage



@api.route('/upload/', methods=['POST'])
@parameter_check(does_return=False, req_c_type='multipart/form-data')
@metadata_check(does_return=False, req_type='video/mp4')
def upload_video():
    """
        uploads the video
    """

    byteStream = request.files['file']
    vu = VideoUploader()
    vu.upload_from_bytestream(byteStream)

    session['s_id'] = vu.id
    f_c = utils.framecount_from_vid_id(vu.id)
    session['video_frame_count'] = f_c
    session['is_uploaded'] = True

    return jsonify({'status' : '201',
                    'message' : 'video uploaded!'}), 201



@api.route('/preview/', defaults={'frame_idx':1}, methods=['GET'])
@api.route('/preview/<frame_idx>/', methods=['GET', 'POST'])
@parameter_check(does_return=False, req_c_type='application/json')
@url_arg_check(does_return=True, req_type=int, arg='frame_idx', session=session)
def preview_thumbnail(frame_idx):
    """
        Preview a frame by index, given filter parameters
    """
    if session.get('is_uploaded'):
        data = request.get_json()
        filter_params = data['filter_params']
        session['filter_params'] = filter_params
        frame = Frame(session['s_id'])
        frame_i = frame.get_by_idx(frame_idx)
        filter_frame = Filter(frame_i).run_func(filter_params)
        frame.f_save(filter_frame, session['s_id'])

        return send_from_directory(directory=f'{FRAMES_UPLOAD_PATH}',
                         path=f'{session["s_id"]}{IMG_EXTENSION}',
                         as_attachment=True), 200

    raise InvalidAPIUsage('Invalid usage: please upload a video first')



@api.route('/download/', methods=['POST'])
@parameter_check(does_return=True, req_c_type='application/json', session=session)
def download_video(vid_range):
    """
        Download a video given filter parameters
    """

    if session.get('is_uploaded'):
        data = request.get_json()
        fps = data['fps']
        filter_params = data['filter_params']
        frame_count = session['video_frame_count']
        vd = VideoDownloader(fps, vid_range)
        filter_vid = vd.download(session['s_id'], frame_count, filter_params)

        session['is_downloaded'] = True
        return send_from_directory(directory=f'{VIDEO_UPLOAD_PATH}',
                             path=f'{filter_vid}{VIDEO_EXTENSION}',
                             as_attachment=True), 200

    raise InvalidAPIUsage('Invalid usage: please upload a video first')


@api.route('/status/', methods=['GET'])
@parameter_check(req_c_type='application/json')
def status():
    """
        The progress of the user, uploaded, download / frames
    """

    resp = {}
    try:
        if session['is_uploaded']:
            resp["upload"] = "done"
        if CACHE.get(f"{session['s_id']}_d"):
            d_status = CACHE.get(f"{session['s_id']}_d")
            resp["downloaded_frames"] = f'{d_status}/{session["video_frame_count"]}'
        if session["is_downloaded"]:
            resp["is_downloaded"] = True
    except KeyError:
        pass
    return jsonify({"status" : resp}), 200
