# Version.1
#### Dataset 구조
```
(.otx)$ ds_count ./splitted_dataset 14
./splitted_dataset:	157485
./splitted_dataset/val:	31497
./splitted_dataset/val/1:	5304
./splitted_dataset/val/2:	5229
./splitted_dataset/val/3:	2182
./splitted_dataset/val/4:	1480
./splitted_dataset/val/5:	709
./splitted_dataset/val/6:	623
./splitted_dataset/val/7:	581
./splitted_dataset/val/8:	614
./splitted_dataset/val/9:	748
./splitted_dataset/val/0:	1383
./splitted_dataset/val/+:	5022
./splitted_dataset/val/-:	6799
./splitted_dataset/val/*:	650
./splitted_dataset/val/÷:	173
./splitted_dataset/train:	125988
./splitted_dataset/train/1:	21216
./splitted_dataset/train/2:	20912
./splitted_dataset/train/3:	8727
./splitted_dataset/train/4:	5916
./splitted_dataset/train/5:	2836
./splitted_dataset/train/6:	2495
./splitted_dataset/train/7:	2328
./splitted_dataset/train/8:	2454
./splitted_dataset/train/9:	2989
./splitted_dataset/train/0:	5531
./splitted_dataset/train/+:	20090
./splitted_dataset/train/-:	27198
./splitted_dataset/train/*:	2601
./splitted_dataset/train/÷:	695
```
#### Training 결과
|Classification model|Batch size|epoch|Accuracy|infertime|시간|정상
|----|----|----|----|----|----|----|
|EfficientNet-V2-S|4|1|0.9804|0.3309|60|
|EfficientNet-B0|4|1|0.9713|0.1532|30|
|DeiT-Tiny|4|1|0.9594|0.2342|30|
|MobileNet-V3-large-1x|4|1|0.9506|0.1736|30|
|----|----|----|----|----|----|----|
|EfficientNet-V2-S|4|2|0.9800|0.3295|120|
|EfficientNet-B0|4|2|0.9794|0.1552|60|
|DeiT-Tiny|4|2|0.9621|0.2363|60|
|MobileNet-V3-large-1x|4|2|0.9621|0.2566|60|O
|----|----|----|----|----|----|----|
|EfficientNet-V2-S|8|1|0.9757|0.3416|30|
|EfficientNet-B0|8|1|0.9774|0.1565|15|
|DeiT-Tiny|8|1|0.9452|0.2349|15|
|MobileNet-V3-large-1x|8|1|0.9687|0.1708|15|
|----|----|----|----|----|----|----|
|EfficientNet-V2-S|8|2|0.9888|0.3452|60|△
|EfficientNet-B0|8|2|0.9880|0.1635|30|
|DeiT-Tiny|8|2|0.9709|0.2412|30|
|MobileNet-V3-large-1x|8|2|0.9743|0.1755|30|△
|----|----|----|----|----|----|----|
|EfficientNet-B0|8|4|0.9872|0.1550|60|
|----|----|----|----|----|----|----|
|MobileNet-V3-large-1x|4|4|0.9619|0.1674|120|△
|MobileNet-V3-large-1x|4|6|0.97863|0.1714|180|
|MobileNet-V3-large-1x|8|4|0.9868|0.1671|60|
|MobileNet-V3-large-1x|8|6|0.9885|0.1677|90|△
|MobileNet-V3-large-1x|8|8|0.9896|0.1742|120|
#### Details
```
20개의 클래스사용
15개 샘플이미지사용 5개의 상위모델선정
```
#### How to measure FPS
|Classification model|Batch size|epoch|Accuracy|infertime|시간|정상
|----|----|----|----|----|----|----|
|MobileNet-V3-large-1x|4|2|0.9621|0.2566|60|O
|EfficientNet-V2-S|8|2|0.9888|0.3452|60|△
|MobileNet-V3-large-1x|8|2|0.9743|0.1755|30|△
|MobileNet-V3-large-1x|4|4|0.9619|0.1674|120|△ 
|MobileNet-V3-large-1x|8|6|0.9885|0.1677|90|△
#### Why
```
Classification model : MobileNet-V3-large-1x
Batch size : 4
epoch : 2
infertime : 0.2566
5개의 상위모델중 다른 손글씨 데이터셋 사용하여 검증 
우수한 모델 선정
```
# Version.2
#### Dataset 구조
```
./splitted_dataset:	224519
./splitted_dataset/val:	44904
./splitted_dataset/val/0:	1383
./splitted_dataset/val/1:	5304
./splitted_dataset/val/2:	5228
./splitted_dataset/val/3:	2182
./splitted_dataset/val/4:	1480
./splitted_dataset/val/5:	709
./splitted_dataset/val/6:	623
./splitted_dataset/val/7:	582
./splitted_dataset/val/8:	613
./splitted_dataset/val/9:	747
./splitted_dataset/val/+:	5022
./splitted_dataset/val/-:	6799
./splitted_dataset/val/times:	650
./splitted_dataset/val/div:	174
./splitted_dataset/val/(:	2859
./splitted_dataset/val/):	2871
./splitted_dataset/val/{:	75
./splitted_dataset/val/}:	75
./splitted_dataset/val/[:	156
./splitted_dataset/val/]:	156
./splitted_dataset/val/sqrt:	1782
./splitted_dataset/val/log:	400
./splitted_dataset/val/sin:	859
./splitted_dataset/val/cos:	597
./splitted_dataset/val/tan:	490
./splitted_dataset/val/pi:	467
./splitted_dataset/val/=:	2621
--------------------------------------
./splitted_dataset/train:	179615
./splitted_dataset/train/0:	5531
./splitted_dataset/train/1:	21216
./splitted_dataset/train/2:	20913
./splitted_dataset/train/3:	8727
./splitted_dataset/train/4:	5916
./splitted_dataset/train/5:	2836
./splitted_dataset/train/6:	2495
./splitted_dataset/train/7:	2327
./splitted_dataset/train/8:	2455
./splitted_dataset/train/9:	2990
./splitted_dataset/train/+:	20090
./splitted_dataset/train/-:	27198
./splitted_dataset/train/times:	2601
./splitted_dataset/train/div:	694
./splitted_dataset/train/(:	11435
./splitted_dataset/train/):	11484
./splitted_dataset/train/{:	301
./splitted_dataset/train/}:	302
./splitted_dataset/train/[:	622
./splitted_dataset/train/]:	624
./splitted_dataset/train/sqrt:	7126
./splitted_dataset/train/log:	1601
./splitted_dataset/train/sin:	3434
./splitted_dataset/train/cos:	2389
./splitted_dataset/train/tan:	1960
./splitted_dataset/train/pi:	1865
./splitted_dataset/train/=:	10483
```
#### Why
```
Classification model : MobileNet-V3-large-1x
Batch size : 16
epoch : 10
infertime : 0.1677
우수한 모델 선정
```