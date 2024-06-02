# Project : Board Maestro

![image](https://github.com/Intel-Edge-AI-SW-Developers-2nd-Team-1/BoardMaestro/assets/45201672/e90b6e6d-8a09-447a-91f0-e5ab1a945a75)

* 칠판 앞이나 어디든지 수식을 쓰는 모션을 취할 때, 수식을 인식하여 계산해주는 시스템
  (In front of board and anywhere, when you do motion writing math symbol and number, this system detects and calculates them.)

* 실시간 영상처리로 얻은 자세에 대한 영상정보로부터 수식에 대한 결과를 계산하여 보여주는 것이 최종 목표
  (The goal is to calculate and display the results of the formula from the image information about the posture obtained through real-time image processing.)

![image](https://github.com/Intel-Edge-AI-SW-Developers-2nd-Team-1/BoardMaestro/assets/45201672/fab5ef30-e38c-4594-a05e-33f1936a6e40)

## High Level Design

![image](https://github.com/Intel-Edge-AI-SW-Developers-2nd-Team-1/BoardMaestro/assets/45201672/494c0bfb-a611-45c5-bb65-c5b25ff616ba)

## Sequence Diagram

![KakaoTalk_20240523_083606031](https://github.com/Intel-Edge-AI-SW-Developers-2nd-Team-1/BoardMaestro/assets/45201672/4daabf81-efdc-46d5-90ca-c339628ed18b)

![image](https://github.com/Intel-Edge-AI-SW-Developers-2nd-Team-1/BoardMaestro/assets/45201672/f4f47c24-42b5-4f66-a07b-541d6979ce80)

## Contributors

**-Release v2.0.1------------------------**

**yeongdaekim(roby238)**
- Project Leader
- Git Manager
- Expression Calculating
- Create Deliverables for Develop
- Release v2.0.1

**User3198352(User3198352)**
- Project Manager
- System Integration
- Hand Pose Estimaion
- Create Deliverables for Develop
- Release v2.0.1

**simpleis6est(simpleis6est)**
- Image Preprocessing
- Create Deliverables for Develop
- Release v2.0.1

**Park JaeByeong(pjb8051)**
- UI / Hardware
- Create Deliverables for Develop
  
**-Release v1.0.0-------------------------**

**Daniel(kcg0118)**
- AI Modeling(Training, Inference)
- Create Deliverables for Communication
  
**jungjaeJJ(jungjaeJJ)**
- AI Modeling(Dataset, Inference)
- Create Deliverables for Develop 

**----------------------------------------**

## Clone code

* Enter below code to run this project.

```shell
git clone https://github.com/Intel-Edge-AI-SW-Developers-2nd-Team-1/BoardMaestro.git
```

## Prerequite

* Create new python virtual environment for this project.

```shell
# Start directory
cd ./BoardMaestro

# Create virtual env.
python3 -m venv .board_maestro

# Activate virtual env.
source .board_maestro/bin/activate

# Install requirements.
pip install -r requirements.txt
```

## Steps to run

1. How to run with bash file
  * Just enter below code at root directory of project.

```shell
# Go to root directory of project.
cd ~/BoardMaestro
source .board_maestro/bin/activate

# Run bash command.
./run.sh
``` 

## Output

![image](https://github.com/Intel-Edge-AI-SW-Developers-2nd-Team-1/BoardMaestro/assets/45201672/a5e7a93b-81c3-41f2-ab5b-1b0817d9b022)
*cos(3) + sqrt(100) + 2 * 3

## PR rules

- Do PR with part, milestone, details PR.
  * Title :
  ```
  [<your part name>] refer from each milestone 
  ```
  * Description :
  ```
  details:
      1. task1
      2. task2
      3. task3
  ```
  
## Commit rules

- commit message: 
  ```
  git commit -m "[<title>] update code.abc"
  ```

