# demo-pay

신용카드 결제 시스템

## 설치

먼저 `make venv` 명령어로 파이썬 가상환경을 설치합니다. 

```sh
$ make venv
source venv/bin/activate

Once activated, you can use the install target to install dependencies:

make install
```

다음으로 `make install` 타겟으로 의존성 패키지들을 설치합니다.

```sh
$ make install
```

## 테스트

pytest를 이용한 테스트는 다음 명령어로 실행합니다.

```sh
$ make test
```

## 린트

pylint는 다음과 같이 실행합니다. (시간관계상 다 잡지 못했습니다)

```sh
$ make lint
```

## 빌드

```sh
$ make build
```

## 설명

### 입력

CLI 전용 프로그램이라고 가정하고, 확장성을 위해 [`click`](https://github.com/pallets/click) 기반으로 아래 두 가지 방식의 파일 입력을 처리하였습니다.

#### argument 입력
```
$ pay input.txt
```

#### stdin 입력
```
$ pay < input.txt
```

이상, 위 두 가지 방식의 파일 입력을 위한 파이썬 코드는 다음과 같습니다.

```python
@click.argument("payloads", type=click.File("rb"), default="-")
```

### 출력

다음과 같이 로그를 사용하여 입력의 읽고 처리하는 것들을 나타내었습니다.

```
$ pay < input.txt
2019-08-31 20:26:15,563 - cli.py(12) - DEBUG: input: <_io.BufferedReader name='<stdin>'>
2019-08-31 20:26:15,563 - events.py(74) - DEBUG: AddEvent(kind='Add', name='Jane', params=[4111111111111111, 1000])
2019-08-31 20:26:15,563 - manager.py(24) - INFO: adding - Jane, 4111111111111111, $1000
2019-08-31 20:26:15,563 - manager.py(29) - INFO: added - Jane: $0                                                                                                                                                                                                               2019-08-31 20:26:15,563 - events.py(74) - DEBUG: AddEvent(kind='Add', name='Evan', params=[5454545454545454, 3000])
2019-08-31 20:26:15,563 - manager.py(24) - INFO: adding - Evan, 5454545454545454, $3000
2019-08-31 20:26:15,563 - manager.py(29) - INFO: added - Evan: $0
2019-08-31 20:26:15,563 - events.py(74) - DEBUG: AddEvent(kind='Add', name='Daniel', params=[1234567890123456, 2000])
2019-08-31 20:26:15,563 - manager.py(24) - INFO: adding - Daniel, 1234567890123456, $2000
2019-08-31 20:26:15,563 - creditcard.py(19) - WARNING: Invalid card number: 1234567890123456
2019-08-31 20:26:15,563 - manager.py(29) - INFO: added - Daniel: $0
2019-08-31 20:26:15,563 - events.py(82) - DEBUG: ChargeEvent(kind='Charge', name='Jane', params=[500])
2019-08-31 20:26:15,564 - manager.py(44) - INFO: charging - Jane: $500
2019-08-31 20:26:15,564 - manager.py(49) - INFO: charged - Jane: $500
2019-08-31 20:26:15,564 - events.py(82) - DEBUG: ChargeEvent(kind='Charge', name='Jane', params=[800])
2019-08-31 20:26:15,564 - manager.py(44) - INFO: charging - Jane: $800
2019-08-31 20:26:15,564 - creditcard.py(35) - WARNING: Charging $800 to balance $500 is exceeded the limit: $1000
2019-08-31 20:26:15,564 - events.py(82) - DEBUG: ChargeEvent(kind='Charge', name='Evan', params=[7])
2019-08-31 20:26:15,564 - manager.py(44) - INFO: charging - Evan: $7
2019-08-31 20:26:15,564 - manager.py(49) - INFO: charged - Evan: $7
2019-08-31 20:26:15,564 - events.py(90) - DEBUG: CreditEvent(kind='Credit', name='Evan', params=[100])
2019-08-31 20:26:15,564 - manager.py(60) - INFO: crediting - Evan: $100
2019-08-31 20:26:15,564 - manager.py(66) - INFO: creditied- Evan: $-93
2019-08-31 20:26:15,564 - events.py(90) - DEBUG: CreditEvent(kind='Credit', name='Daniel', params=[200])
2019-08-31 20:26:15,564 - manager.py(60) - INFO: crediting - Daniel: $200
2019-08-31 20:26:15,564 - creditcard.py(45) - WARNING: Invalid card number: 1234567890123456
2019-08-31 20:26:15,564 - cli.py(20) - DEBUG: output: Jane: $500
Evan: $-93
Daniel: error
```

## 주요 클래스

```sh
$ tree pay -L 1
pay
├── __init__.py
├── cli.py
├── creditcard.py
├── events.py
├── logging.py
├── manager.py
├── utils.py
└── version.py

1 directory, 8 files
```

- `cli.py`: 파일의 입력을 담당합니다.
- `events.py`: 부모 이벤트와 자식 이벤트를 정의합니다. 자식 이벤트들은 부모 클래스 `Event`에 정의된 `handle` 메소드를 오버라이딩하여, 해당 이벤트를 처리합니다. 부모 클래스의 `set_manager` 메소드를 통해 실제 이벤트 로직을 처리하는 이벤트 매니저를 지정할 수 있습니다.
- `manager.py`: 소위 DBManager와 유사한 역할을 합니다. 싱글레톤이며, `CreditCard` 클래스의 인스턴스들을 관리합니다.
- `creditcardd.py`: 신용카드의 기본 엔티티 로직들을 구현합니다.
- `logging.py`: 로깅을 담당합니다. 실제 로그 설정은 `logging.ini` 파일에 저장됩니다. 입출력 처리 과정을 보여주기 위해 사용되었습니다.
- `utils.py`: 유틸리티 성격의 클래스와 메소드들을 정의합니다. 여기에서는 `Singleton` 클래스만 정의하고 있습니다.