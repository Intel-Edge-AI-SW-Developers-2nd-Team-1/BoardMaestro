## Documentation
### Description
- The external modules use mediapipe,numpy and opencv.
    ```
    init to use hand pose estimation
    :model_path: model_path must include .xml, .bin, .task, .json
    ```

### Flow
- For example, let's take the photo below, which is one frame from a camera, and insert it into the model.

![Alt text](KakaoTalk_20231127_130957018_03.jpg)
#### First 
- Load the Hand Pose estimation model.
#### Second
- The image of the photo in the example above is read. After that, model inference is performed.
#### Finally
- Outputs an inferencing image. In that case, the image below is output. It does this every frame. Proceed.

![Alt text](<스크린샷 2023-11-27 133212.png>)

### Usage
