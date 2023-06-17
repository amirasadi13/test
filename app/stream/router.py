from fastapi import APIRouter, Depends
from starlette.background import BackgroundTasks

from .dependencies import start_video_process
from ..authentication.dependencies import valid_token

router = APIRouter()


@router.post("/stream-images/", response_model=dict)
def stream_images(background_tasks: BackgroundTasks, token: str = Depends(valid_token)):
    sources = [
        {
            'dir_name': 'test folder 1',
            'source_url': 'test.avi'
        }, {
            'dir_name': 'test folder 2',
            'source_url': 'test.avi'
        }, {
            'dir_name': 'test folder 3',
            'source_url': 'test.avi'
        }, {
            'dir_name': 'test folder 4',
            'source_url': 'test.avi'
        }
    ]
    background_tasks.add_task(start_video_process, sources)
    return {"message": "started streaming video"}
