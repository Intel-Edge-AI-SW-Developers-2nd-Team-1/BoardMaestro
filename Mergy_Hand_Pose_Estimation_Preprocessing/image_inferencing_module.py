import numpy as np
import openvino as ov
import json


class ImageInferencing:
    def __init__(self, model_path, device_name, input_shape):
        '''
        ImageInferencing class init function
        :model_path: model_path must include .xmp file
        :device_name: input 'CPU' or 'GPU'
        :input_shape: input_shape value must be same shape with input image shape
        '''
        # Step 1. Initialize OpenVINO Runtime Core
        core = ov.Core()

        # Step 2. Read a model
        model = core.read_model(f'{model_path}/openvino.xml')
        print(1)

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
        print(2)

        # Step 5. Loading model to the device
        self.compiled_model = core.compile_model(model)
        print(3)

        # Step 6. Loading json
        with open(f'{model_path}/label_schema.json') as f:
            self.data = json.load(f)

    def get_inferencing_result(self, frame):
        '''get inferencing result from image'''
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

        return self.data["all_labels"][f'{max_index}']['name']
