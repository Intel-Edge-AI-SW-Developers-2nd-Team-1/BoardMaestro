## Documentation
### Description
- The external modules use opencv and matplotlib.
```
    Class that help Image preprocessing and Camera real-time processing.
 
    Instance : 
        self.result_counter:                        int
        self.image_width:                           int
        self.image_height:                          int
        self.top_pad:                               int
        self.bottom_pad:                            int
        self.left_pad:                              int
        self.right_pad:                             int
        self.desired_width:                         int
        self.desired_height:                        int

    Method :
        __init__():                                 None
        get_current_calculate_distance():           None
        get_current_image():                        None
        get_current_roi():                          float
        get_current_resize():                       None
        get_current_padding():                      float

```

### Flow
- For example, let put the image below..

#### Pre-processing

![number](https://github.com/simpleis6est/BoardMaestro/assets/143490860/81e57962-b885-4917-8f4a-046e28a5e159)

1. To remove floating values, obtain the average coordinates of 5 nodes and draw a point.
2. To remove the messy part at the bottom, erase the three nodes behind and make a dot.
3. Before connecting the coordinates, find the distance between nodes of each captured point.
4. When connecting each point with a line, if the distance is more than a certain distance, it is recognized as a distant part and the two points are not connected.
5. Save the drawn graph.

- The image above was created in the same order as above.
- After that, image preprocessing begins.

#### First 
- We need to find a specific Roi to find the exact object.
- As a method, Roi is extracted using exhaustive search.
- Then it will appear like the image below.

![image](https://github.com/simpleis6est/BoardMaestro/assets/143490860/088206be-f3c4-4a8e-8f33-f5ff50dfa92e)

#### Second
- Problems occurred in the image pre-processing process for certain characters such as 1 or -, so we padded areas with specific roi.

- Result 1

![Result_1](https://github.com/simpleis6est/BoardMaestro/assets/143490860/d1dfed0e-a74d-40ac-84fc-53d4f4b4915a)

- However, because this padding task was different from the trained dataset, a different padding method was used. Since that method knows the height and width of a specific Roi, it takes the larger of the height and width as the reference point and pads it to the extent of the deficiency.
- Like the picture below

- Result -

![Result_7](https://github.com/simpleis6est/BoardMaestro/assets/143490860/99540634-eac9-4fc1-b4cf-befe39a39c4e)

#### Third
- For photos to be included in the AI model, we change them to a size that matches the model input data.
- Resize was performed to match the model input data (150,150,3).

#### Finally
- Finally we were able to obtain the image below.

-Result 2

![Result_1](https://github.com/simpleis6est/BoardMaestro/assets/143490860/66d9e32a-7f58-4cab-8e2c-6c9dc2c11518)

### Usage
- Example Code

```python
preprocessing = Preprocessing(desired_width, desired_height)
str2 = f'counter: {preprocessing.result_counter}'
# inferencing and make string
string_image = cv2.imread(f'./Result/Result_{preprocessing.result_counter - 1}.jpg')
string_buf.append(f'{infer.get_inferencing_result(string_image, False)}')
```
