## Documentation
### Description
- The external modules use mediapipe,numpy and opencv.
    ```
    init to use hand pose estimation
    :model_path: model_path must include .xml, .bin, .task, .json
    ```

### Flow
- For example, let's take the photo below, which is one frame from a camera, and insert it into the model.

![KakaoTalk_20231127_130957018_03](https://github.com/Intel-Edge-AI-SW-Developers-2nd-Team-1/BoardMaestro/assets/143490860/71279fda-ccfa-49fb-a185-640f487e4db5)

#### First 
- Load the Hand Pose estimation model.
#### Second
- The image of the photo in the example above is read. After that, model inference is performed.
#### Finally
- Outputs an inferencing image. In that case, the image below is output. It does this every frame. Proceed.

![스크린샷 2023-11-27 133212](https://github.com/Intel-Edge-AI-SW-Developers-2nd-Team-1/BoardMaestro/assets/143490860/037dbf88-bb16-4b67-b310-446b71374c09)

### Usage
