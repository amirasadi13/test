from multiprocessing import Process
from app.stream.stream_base import StreamThreading


def start_video_process(sources: list):
    processes = [Process(target=streaming, args=(sources[i],)) for i in range(len(sources))]
    for process in processes:
        process.start()


def streaming(src: dict):
    stream = StreamThreading(src=src['source_url'])
    stream.start()
    frame_index = 0
    while frame_index < stream.frames_count():
        grab, frame = stream.read()
        stream.write(frame=frame, dir_name=src['dir_name'], frame_index=frame_index)
        frame_index += 1
    stream.stop()

