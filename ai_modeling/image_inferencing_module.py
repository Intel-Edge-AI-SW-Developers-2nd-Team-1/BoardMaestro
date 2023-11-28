import numpy as np
import openvino as ov
import json


class ImageInferencing:
    '''
    Class that find number from image

    Instance :
        self.compiled_model:        Openvino.Core
        self.data:                  json

    Method :
        __init__():                 None
        get_inferencing_result():   char
    '''

    def __init__(self, model_path, device_name, input_shape):
        '''
        ImageInferencing class init function

        :input:
        :model_path: model_path must include .xmp file
        :device_name: input 'CPU' or 'GPU'
        :input_shape: input_shape value must be same shape with input image shape
        '''
        # Step 1. Initialize OpenVINO Runtime Core
        core = ov.Core()

        # Step 2. Read a model
        model = core.read_model(f'{model_path}/openvino.xml')

        # Step 3. Set up input
        input_tensor = np.expand_dims(input_shape, 0)

        # Step 4. Apply preprocessing
        ppp = ov.preprocess.PrePostProcessor(model)
        ppp.input().tensor() \
            .set_shape(input_tensor.shape) \
            .set_element_type(ov.Type.u8) \
            .set_layout(ov.Layout('NHWC'))
        ppp.input().preprocess().resize(ov.preprocess.ResizeAlgorithm.RESIZE_LINEAR)
        ppp.input().model().set_layout(ov.Layout('NCHW'))
        ppp.output().tensor().set_element_type(ov.Type.f32)
        model = ppp.build()

        # Step 5. Loading model to the device
        self.compiled_model = core.compile_model(model, device_name)

        # Step 6. Loading json
        with open(f'{model_path}/label_schema.json') as f:
            self.data = json.load(f)

    def get_inferencing_result(self, frame, result_show_flag):
        '''
        get inferencing result from image

        input : inference image and result show flag
        output : inference result from pretrained model
        '''
        input_tensor = np.expand_dims(frame, 0)
        results = self.compiled_model.infer_new_request({0: input_tensor})
        results_array = next(iter(results.values()))

        # find max_value index
        max_value = 0
        max_index = 0
        for i in range(0, len(results_array[0]), 1):
            if results_array[0][i] > max_value:
                max_value = results_array[0][i]
                max_index = i

        # print result to visibly
        if result_show_flag is True:
            for i in range(0, len(results_array[0]), 1):
                label = str(self.data["all_labels"][str(i)]['name'])
                print(label + " : " + str(results_array[0][i]))

        return self.data["all_labels"][f'{max_index}']['name']
