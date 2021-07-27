## 개발환경
- OS : Window 10
- Editor : VSCode
- Terminal : bash
- Java 16


# 1. Logstash?

- 실시간 파이프라이닝 기능을 갖춘 오픈 소스 데이터 수집 엔진
- 다른 소스의 데이터를 동적으로 통합하고 선택한 대상으로 데이터를 **정규화**할 수 있다.


# 2. 설치 및 실행

설치

> https://www.elastic.co/kr/downloads/logstash

Zip 파일 다운받고 압축풀기

실행

```sh
$ cd logstash-7.13.4
$ .\bin\logstash.bat -e "input { stdin {} } output { stdout {} }"

.
.
[main] Pipeline started
Pipelines running
```

실행이 된 것을 확인했으면 아무거나 입력 후 엔터

```
Hello! 입력 후 엔터
{
       "message" => "hello\r",
    "@timestamp" => 2021-07-27T01:37:15.488Z,
      "@version" => "1",
          "host" => "dogyun-labtop"
}
```

종료
```
Ctrl + C
```


> 왜 bash에서는 실행이 안 될까...
> 
> Powershell에서 실행함..

# 3. 예제

Apache web logs를 인풋으로 예제 진행

## 예제파일 다운

> https://download.elastic.co/demos/logstash/gettingstarted/logstash-tutorial.log.gz

압축풀기

```sh
$ gunzip logstash-tutorial.log.gz
```
- bash에서 실행

내용 확인

```sh
$ cat logstash-tutorial.log
```


## Filebeat 설치 및 설정

Logstash에 데이터 보내기 전에 **Filebeat**(전처리 오픈소스)로 데이터 재구성 해줘야함.

> https://www.elastic.co/kr/downloads/beats/filebeat

Zip 파일 다운받고 압축풀기

`filebeat.yml` 열기
```sh
$ vi filebeat.yml
```

Filebeat inputs에 인풋파일 설정

```yaml
filebeat.inputs:
- type: log
  enabled: true
	path:
		- c:\ELK Stack\logstash-tutorial.log
```
- 경로는 절대경로로 하자.


아웃풋을 Logstash로 보내기 위한 설정

```yaml
output.logstash:
	hosts: ["localhost:5044"]
```
- Filebeat는 포트 5044 사용
- 주석만 지워주면 된다.
- 다른 아웃풋 설정 되있는건 모두 주석처리!

실행해보기

```sh
$ ./filebeat -e -c filebeat.yml -d "publish"
```

## Logstash 설정

Logstash Home 디렉토리에 파이프라인 설정 파일 생성
```sh
$ vi first-pipeline.conf
```


파이프라인 기본 틀

```
input {
}
# The filter part of this file is commented out to indicate that it is
# optional.
# filter {
#
# }
output {
}
```
- 만든 파일에 붙여넣고 시작!

Beats input 플러그인
```yaml
  beats {
    port => "5044"
  }
```

Logstash 실행 결과 출력을 위한 것
```yaml
  stdout { codec => rubydebug }
```


옵션이 잘 설정됐나 확인
```sh
$ ./bin/logstash.bat -f first-pipeline.conf --config.test_and_exit

.
.
Config Validation Result: OK.
```

잘 됐으면 실행해보기
```sh
$ ./bin/logstash.bat -f first-pipeline.conf --config.reload.automatic

.
.
Starting server on port: 5044
```
- automatic실행 : 설정파일 바꿔도 알아서 적용된다.

> 실행하면 `[WARN ][logstash.config.source.multilocal] Ignoring the 'pipelines.yml' file because modules or command line options are specified`이 뜬다. 
>
> 이유 : 현재 `pipeline.yml`은 멀티파이프라인 실행을 위한건데 되는데 우리가 설정한 conf파일은 싱글 파이프라인을 위한 설정이라서 그럼.

이제 다시 filebeats를 실행하면 logstash로 log가 전송된다.
```sh
$ ./filebeat -e -c filebeat.yml -d "publish"
```

**Filebeat로부터 log를 읽는 파이프라인 실행 완료**

## grok filter plugin

웹 로그 필터링하는 플러그인을 써서 깔끔하게 받아오기

Apache log를 위한 `%{COMBINEDAPACHELOG}` grok pattern 사용

`first-pipeline.yml`필터에 추가
```yaml
filter {
  grok {
    match => { "message" => "%{COMBINEDAPACHELOG}"}
  }
}
```

저장. 

Logstash는 자동 리로드, filebeat의 registry 제거해야함

```sh
$ rm -r data/registry
```

다시 filebeat 실행
```sh
$ ./filebeat -e -c filebeat.yml -d "publish"
```
- JSON형태로 받아왔다.


더 많은 정보를 위해 플러그인을 더 추가해볼 수 있다.

`geoip` 플러그인을 추가해서 주소 내 IP주소를 파싱해 이걸로 위치정보를 얻어보자.

필터에 플러그인 추가
```yaml
filter {
  geoip {
    source => "clientip"
  }
}
```

다시 실행
```sh
$ rm -r data/registry
$ ./filebeat -e -c filebeat.yml -d "publish"
```

결과에서 `geoip` 정보를 확인할 수 있다.
```yaml
"geoip" => {
  "country_name" => "China",
  "continent_code" => "AS",
  "country_code3" => "CN",
  "latitude" => 39.9288,
  "country_code2" => "CN",
  "timezone" => "Asia/Shanghai",
  "region_name" => "Beijing",
  "city_name" => "Beijing",
  "location" => {
  "lon" => 116.3889,
  "lat" => 39.9288
  },
  "longitude" => 116.3889,
  "ip" => "218.30.103.62",
  "region_code" => "BJ"
}
```


## Elasticsearch로 데이터 보내기

`first-pipeline.conf`에 output 추가

```yaml
output {
  elasticsearch {
    hosts => ["localhost:9200"]
  }
}
```
- 해당 설정으로 Logstash는 Elasticsearch 연결을 위해 http protocol을 사용함


실행

1. Elasticsearch
2. Logstash
3. filebeat

하면 filebeat에서 데이터 입력받고 logstash에서 전처리 후 최종적으로 elasticsearch에 색인하는 logstash 파이프라인이 구성되었다.

테스트

```sh
$ curl 'localhost:9200/_cat/indices?v'
```

인덱스 확인 후 오늘 날짜로 만들어진 인덱스명 확인 후

```sh
$ curl -XGET 'localhost:9200/logstash-<파일명>/_search?pretty&q=response=200'
```

검색해본다.

Elasticsearch에 색인된 logs를 확인할 수 있다.


**끗.**

