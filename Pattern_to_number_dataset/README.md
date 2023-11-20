### 정리
- 11.17 일 정리
- Pose -> MidiaPipe 을 이용해서 좌표값 추출
- Pose -> Handwritting  을 인식을 위해서 오른쪽 손목 좌표 엑셀값으로 저장
- 숫자 및 Handwritting 을 하는 도중에 쓰레기값(다른 좌표)가 있어서 키보드 인터럽트로 숫자 '0'을 쓰는 그림
- 숫자 인식을 하는 pretraining 모델에 midia pipe 를 통해서 나온 숫자 그림을 넣어서 인식을 할수있는지 확인
- 키보드 인터럽트 보완점으로 motion detection program 을 이용해서 오른쪽 손목 왼쪽 손목의 길이가 8 미만일 경우 토글 방식으로 인터럽트 발생
- 보완할 점
- 각 pretraining 모델에 들어갈 다양한 그림을 넣어서 잘 그려지는지 확인
- 인터럽트 방식을 조금 더 편안한 방식으로 구현하는 법 생각해보기 


- 11.18 일 정리
- 정확한 숫자를 그리기위해 이미지 전처리방식으로 각 좌표의 chunk size을 정해서 (ex:5) 그의 평균값만 점찍게하여서 숫자를 그리게했다.
- 6, 9 인식이 잘 안되므로 추가적인 이미지 전처러 방식이 필요함.
- 위의 이유로 알고리즘 개발
- Fps을 늘리기위해(노드를 많이 찍기위해-정확도증가) 미디어파이프 인퍼런싱 하는 방식 CPU -> GPU 전환 방식 찾음
```
BaseOptions = mp.tasks.BaseOptions
base_options = python.BaseOptions(model_asset_path=model_path, delegate=BaseOptions.Delegate.GPU)
options = vision.PoseLandmarkerOptions(
    base_options=base_options,
    output_segmentation_masks=True)
detector = vision.PoseLandmarker.create_from_options(options)

```
- 보완할 점 여전히 6, 9 이런거는 인식문제 개선이 필요함을 느낌
- 원할한 작업을 위해 모델 학습된 PC에 SSH 로 파일을 전송
- 인식을 위해 선두께 3 -> 10 으로 상향 조정

