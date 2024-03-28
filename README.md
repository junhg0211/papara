# 파파라 프로그래밍 언어

## 표준

### 변수 선언

변수는 `를` 격과 `선언` 키워드로 제작한다.

```
가 를 정수 로 선언.
```

선언하면서 값을 대입하려면 `로/으로` 격을 사용한다.

```
가 를 0 인 정수 으로 선언.
가 를 0 으로 선언.
```

### 변수 대입

변수에 값을 대입할 때에는 `에`, `를` 격과 `대입` 키워드를 사용한다.

```
가 에 3 을 대입.
```

### 함수 호출

함수는 함수 이름에 **격**을 통해 호출한다.

```
f.
```

```
밥 을 먹기.
"Hello, world!" 를 출력.
```

### 연산자

```
2 나누기 3 을 출력.
```

```
3 더하기 7 을 출력.
```

```
가 를 3 더하기 7 로 선언.

나 를 정수 로 선언.
나 에 3 빼기 7 대입.
```

- 논리연산

논리곱은 `이고`, `그리고`, `이면서`,
논리합은 `이거나`, `또는`으로 표현한다.

```
참 이고 거짓
거짓 이고 참
3 은 7 보다 큼 이거나 나 는 7 보다 크거나_같음 을 출력.
```

- 비트연산

```
100 을 2 번 왼쪽시프트
100 을 2 번 오른쪽시프트
```

### 제어문

#### 분기제어 (if)

조건에 따른 분기 제어는 `만약`, `이면` 키워드와 들여쓰기로 수행한다.

```
만약 3 보다 7 이 큼 이면
    "안녕, 세상!!" 출력.
```

`else if`는 `,`와 `이면`, `하기`키워드로 수행한다.
`else`는 `아니면`, `하기` 키워드로 수행한다.

```
만약 성적 이 90 보다 큼 이면
    "수"를 출력,
성적 이 80 보다 큼 이면
    "우" 를 출력,
아니면
    "가" 를 출력.
하기.
```

#### 조건 반복 (while)

조건 반복문은 `인 동안`, `하기` 키워드로 작성한다.

```
번호 가 10 보다 작음 인 동안
    번호 를 출력.
    번호 에 번호 더하기 1 대입.
하기.
```

#### 순회 반복 (for)

순회 반복문은 `각`, `하여`, `하기` 키워드로 작성한다.

```
각 이름들 을 이름 으로 하여
    이름 을 출력.
하기.
```

#### break & continue

break문은 `그만하기`, continue문은 `넘어가기` 키워드로 작성한다.

```
정수 번호 를 0 으로 선언.
번호 가 10 보다 작음 인동안
    만약 번호 나머지 3 이 0 과 같음 이면
        넘어가기.
    하기.

    만약 번호 가 8 과 같음 이면
        그만하기.
    하기.

    번호 를 출력.
하기.
```

### 함수

함수는 `... 를 ... 로 받고`, `하는 함수`를 활용하여 만든다.

```
삼 을
    3 을 반환
하는 함수 로 선언.
```

```
짝수임 을 정수 가 를 받고
    가 나머지 2 가 0 과 같음 을 반환.
하는 함수 로 선언.
```

```
ㅎ 을 정수 가 를 를 로, 정수 나 를 에 로 받고
    가 곱하기 123 더하기 나 를 반환.
하는 함수 로 선언.

3 에 7 을 ㅎ 을 출력.
```

```
로그 를 이름 을 를_이름으로 로, 내용 을 을 로 받고
    이름 을 출력.
    내용 을 출력.
하는 함수 로 선언.

"스치" 를 이름으로 "안녕하세요" 를 로그.
```

### 구조체

구조체는 `의 묶음`을 사용하여 만든다.

```
학생 을
    정수 학번, 문자열 이름, 실수 평점
의 묶음 으로 선언.

스치 를
    학번 이 123, "스치" 가 이름, 4.5 가 평점
인 학생 으로 선언.
```

#### 메소드

```
학생 에 먹기 를 음식 을 를 로 받고
    자신 의 이름 을 출력.
    "은/는 " 을 출력.
    음식 을 출력.
    "을/를 먹었다.\줄" 를 출력.
하는 함수 로 만들기.

스치 를 학번 이 123, "스치" 가 이름, 4.5 가 평점 인 학생 으로 선언.
밥 을 "햄버거" 로 선언.

스치 가 밥 을 먹기.
```

### 열거형

```
시간대 를
    아침, 점심, 저녁, 밤
의 항목 으로 선언.

지금 을 아침 인 시간대 로 선언.
```

### 주석

<s>주석은 괄호를 사용한다.</s>

```
"안녕, 세상!" 을 출력. ("안녕, 세상!"이 출력된다.)
```

### 리스트

```
숫자들 을
    1, 2, 3, 4, 5
인 정수 의 목록 으로 선언.

숫자들 의 1 번째 항목. (첫번째 항목인 1이 반환된다.)
숫자들 에 6 을 추가.
숫자들 에서 6 을 제거.

숫자들 에 6 을 푸시.
숫자들 에서 팝.
```

### 문자열

```
(concatenation)
"안녕, " 과 "세상!" 을 결합 을 출력.

메시지 를 "안녕, 세상!" 으로 선언.

메시지 의 1 번째 문자. ('안')
메시지 의 1 부터 3 까지 내용. ("안녕")
```

#### 이스케이프 문자

- `\줄`: `'\n'`
- `\탭`: `'\t'`
- `\끝`: `'\0'`
- `\알`: `'\a'`
- `\앞`: `'\r'`
- `\\`: `'\\'`
- `\"`: `'\"'`
