## Dataset 구조
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

## Training 결과
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
|MobileNet-V3-large-1x|4|4|0.96199|0.1674|120|△
|MobileNet-V3-large-1x|4|6|0.97863|0.1714|180|
|MobileNet-V3-large-1x|8|4|0.9868|0.1671|60|
|MobileNet-V3-large-1x|8|6|0.9885|0.1677|90|△