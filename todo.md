
# Todos

- Basic Prototype
  - 사용자의 입력에 결과 출력
  - 커맨드라인 관련 질문만 답변
  - 프롬프트 엔지니어링(prompt template) 사용하여 결과 triming

- Advanced Steps
  - 옵션으로 apikey 설정받기.
  - llm이 작성한 cmd를 실제로 실행시키기
  - 질문 history 보여주기
  - 사용자 인터페이스: 추전 명령어 제안, 사용자가 선택하면 실행하기.
  - 사용자가 여러줄 입력할수 있도록

- 버그
  - 현재 OS, 및 shell이름을 얻어내서 그것에 맞는 command를 생성해야함.  
    sed -i 's/AAA/BBB/g' test.txt
  - execute한다면 stdout/stderr 를 출력해야함(현재는 subprocess에서 실행해서 출력할수 없음)
  - 모호한 질문에 대해서 추가 질의를 받아야함(chat model사용)

- Software Design 전략
  - 다양한 llm 사용가능한 소프트웨어 디자인
  - SOLID

- Testing 전략
  - 실제 예시 cmd를 예시 폴더나, 테스트용 파일에서 수행시켜서 원하는 결과를 만들었는지 평가.
  - 기본적으로 모든 UC에 대해서 모두 TC를 작성(새로 발견한 UC는 새로운 TC로)
  - Non-Deterministic 줄이기.

- 비용 절감 전략
  - 유사 질문에 대해서는 Caching
  - 커맨드라인 관련 질문이 아닌경우 <- 판단을 LLM사용하지 않기. 


# Use Cases

./recmd.py "hello.txt 이름의 파일을 생성 하고 해당 파일에 hello 문자열을 공백포함 20개 추가"
./recmd.py "hello.txt 파일에서 hello 문자열을 world로 치환하고 파일명을 world.txt로 변경"


./recmd.py "words.txt 파일에 무작위 문자열 20개를 추가. 한줄에 하나씩 추가. macOS zshell 기준"
./recmd.py "words.txt 의 각 line을 오름차순 정렬해서 저장"


./recmd.py "month 이름의 경로를 생성하고, 그 내부에 모든 월에 해당하는 경로를 생성"
