### 소개

* 부동산 실거래가 데이터를 스크랩하는 파이선 스크립트입니다.
* 아파트 전세/매매, 오피스텔 전세/매매
* 월단위로 수집합니다.

### config.ini

프로젝트 ROOT에 아래와 같이 `config.ini`을 추가

```ini
[DATA]
ROOT = ./data/scrap

[OPEN_DATA]
ServiceKey = 45
Host = http://openapi.molit.go.kr:8081/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/

[SERVICE_KEYS]
Service_Key1 = <service_key>
Service_Key2 = <service_key>

[OPEN_DATA_URLS]
Apt-Trade = http://openapi.molit.go.kr:8081/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcAptTrade
Apt-Rent = http://openapi.molit.go.kr:8081/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcAptRent
```

### 실행

```sh
python app.py --url_type [apt-trade|apt-rent] --service_key Service_Key1
```

### 스크랩 데이터 확인

```
├── preprocessed
│   └── apt-trade
│       └── 11110
│           ├── 202109.csv
│           ├── 202110.csv
│           ├── 202111.csv
│           ├── 202112.csv
│           ├── 202201.csv
│           └── 202202.csv
└── raw
    └── apt-trade
        └── 11110
            ├── 202109.csv
            ├── 202110.csv
            ├── 202111.csv
            ├── 202112.csv
            ├── 202201.csv
            └── 202202.csv
```

### Contact

* 제가 개인 연구의 목적으로 사용하고 있습니다. 혹시 문제나 개선점이 있으면 개선은 언제든 환영입니다.
* 에러 관련은 direcision@gmail.com으로 보내주세요.
