from pydantic import BaseSettings


class StreamConfig(BaseSettings):
    IMAGES_DIRECTORY = 'images/'


stream_config = StreamConfig()
