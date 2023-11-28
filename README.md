# Project : Board Maestro

* 칠판 앞이나 어디든지 수식을 쓰는 모션을 취할 때, 수식을 인식하여 계산해주는 시스템
  (In front of board and anywhere, when you do motion writing math symbol and number, this system detects and calculates them.)

* 실시간 영상처리로 얻은 자세에 대한 영상정보로부터 수식에 대한 결과를 계산하여 보여주는 것이 최종 목표
  (The goal is to calculate and display the results of the formula from the image information about the posture obtained through real-time image processing.)

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

* Create new python virtual environment for this project.

```shell
# Create virtual env.
python3 -m venv board_maestro

# Activate virtual env.
source board_maestro/bin/activate

# Install requirements.
pip install -r requirements.txt
```

## Steps to run

1. How to run with python file.
  * Change directory to 'BoardMaestro/'.
  * Activate virtual environment created previously and go to 'demo_test/'.
  * Run demo.py file.

```shell
# Go to root directory of project.
cd ~/BoardMaestro
source board_maestro/bin/activate

# Run demo.py file.
cd /demo_test/
python demo.py
```

2. How to run with bash file
  * Just enter below code at root directory of project.

```shell
# Go to root directory of project.
cd ~/BoardMaestro
source board_maestro/bin/activate

# Run bash command.
./run.sh
``` 

## Output

![image](https://github.com/Intel-Edge-AI-SW-Developers-2nd-Team-1/BoardMaestro/assets/45201672/4d8622ed-c117-4ec8-8002-05e1e885c265)

## PR rules
- Do PR with part, milestone, details PR.
  * Title :
  ```
  [<your part name>] refered from each milestone 
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
  git commit -m "updated code.abc by <your id>" -s <signing id>
  ```

