## Documentation
### Description
- It does NOT require any external module.
    ```
    Class that hand pattern recognition

    Instance :
        self.x, self.y, self.z:         int
        self.nodes:                     string list
        self.angle:                     float
        self.flags:                     int
        self.ptrn:                      int
        self.check_frames_len:          int
        self.check_frames_idx:          int
        self.check_frames_ptrn_list:    int list
        self.mode_value:                int

    Method :
        __init__():                     None
        set_3d_position():              None
        get_3d_len():                   float
        get_angle_from_lens():          float
        get_node_angle():               float
        get_current_pattern():          int
        check_switch_pattern():         int
    ```

### Flow
- For example, let's think of recognizing a pattern like the picture below.

![KakaoTalk_20231127_130957018_01](https://github.com/Intel-Edge-AI-SW-Developers-2nd-Team-1/BoardMaestro/assets/143490860/af5237d1-1d09-471b-9f7f-def47a9f2a96)

#### First
- The node of the index finger in the image above is known through the MedieaPipe model, and the normalized coordinate values of each node are read.

#### Second
- When only the index finger is opened, grab the 3 nodes (MCP, PIP, TIP) on each finger. The middle angle of each node for the fingers except the index finger is formed below 160 to 180 degrees. It is recognized as a writing pattern.

![스크린샷 2023-11-27 131312](https://github.com/Intel-Edge-AI-SW-Developers-2nd-Team-1/BoardMaestro/assets/143490860/63344a26-ca14-45f3-8996-65e6947b3857)

- In the photo above, when fully unfolded, the starting finger MCP, PIP, and TIP are approximately between 160 and 180 degrees.

![스크린샷 2023-11-27 20-18-38](https://github.com/Intel-Edge-AI-SW-Developers-2nd-Team-1/BoardMaestro/assets/143490860/93252aeb-a97a-4835-bfa2-ac794cda94ed)

- In the photo above, when only the index finger is extended, the starting MCP, PIP, and TIP are approximately between 160 and 180 degrees. The rest of the fingers come out at an angle below them.

#### Third

- By creating four cases of the above pattern, stop mode, writing mode, enter mode, and erase mode can be implemented.

![스크린샷 2023-11-27 202427](https://github.com/Intel-Edge-AI-SW-Developers-2nd-Team-1/BoardMaestro/assets/143490860/2fc70166-0156-4aaf-a931-e97c66066c1e)

#### Finally
- After recognizing the pattern, the mode that matches the frame is returned by storing it in the buffer.
### Usage

