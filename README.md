# Project : Board Maestro

* 칠판 앞에서 수식을 쓰는 모션을 취할 때, 수식을 인식하여 계산해주는 시스템
* 실시간 영상처리로 얻은 자세에 대한 영상정보로부터 수식에 대한 결과를 계산하여 보여주는 것이 최종 목표  

## High Level Design
![image](https://github.com/roby238/BoardMaestro/assets/45201672/aaeefcd4-a364-4b70-9625-3cac775e5cc1)

## Sequence Diagram
![Whole Sequence Diagram drawio](https://github.com/roby238/BoardMaestro/assets/45201672/b28c0dff-38d2-4396-9cba-d74d72cf9517)

## Contributors

**yeongdaekim(roby238)**
- Project Leader
- Git Manager
- Expression Calculating
- Create Deliverables for Develop

**User3198352(User3198352)**
- Project Manager
- System Integration
- Hand Pose Estimaion
- Create Deliverables for Develop

**Daniel(kcg0118)**
- AI Modeling(Training, Inference)
- Create Deliverables for Communication
  
**simpleis6est(simpleis6est)**
- Image Preprocessing
- Create Deliverables for Develop

**Park JaeByeong(pjb8051)**
- UI / Hardware
- Create Deliverables for Develop 
  
**jungjaeJJ(jungjaeJJ)**
- AI Modeling(Dataset, Inference)
- Create Deliverables for Develop 

## Clone code

* Enter below code to run this project.

```shell
git clone https://github.com/Intel-Edge-AI-SW-Developers-2nd-Team-1/BoardMaestro.git
```

## Prerequite

* First, you should set OTX(Openvino Training Extensions). Install OTX dependency through below code.

```shell
sudo apt update
sudo apt-get install g++ freeglut3-dev build-essential libx11-dev libxmu-dev libxi-dev libglu1-mesa libglu1-mesa-dev gcc-multilib dkms mesa-utils
sudo apt upgrade
```

* Second, you need CUDA 11.7 version. Note, link below is for Ubuntu20.04. For other versions please refer CUDA Toolkit 11.7 Downloads.

```shell
cd ~/Downloads/
wget https://developer.download.nvidia.com/compute/cuda/11.7.0/local_installers/cuda_11.7.0_515.43.04_linux.run
sudo sh cuda_11.7.0_515.43.04_linux.run
```

* Third, create new python virtual environment for this project.

```shell
# Create virtual env.
python3 -m venv board_maestro

# Activate virtual env.
source board_maestro/bin/activate

# Install requirements.
pip install -r requirements.txt
```

## Steps to run

* (프로젝트 실행방법에 대해서 기술, 특별한 사용방법이 있다면 같이 기술)

```shell
cd ~/BoardMaestro
source .venv/bin/activate

cd /demo_test/
python demo.py
```

## Output

![./result.jpg](./result.jpg)

## PR rules
- part, milestone, details 포함하여 PR
  * Title :
  ```
  [<your part name>] 해당 milestone 참조
  ```
  * Description :
  ```
  details:
  
  1. 항목1
  2. 항목2
  3. 항목3
  ```
## Commit rules
- commit message: 
  ```
  git commit -m "updated code.abc by <your id>"
  ```

