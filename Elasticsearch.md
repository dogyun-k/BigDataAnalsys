- [1. Elasticsearch?](#1-elasticsearch)
		- [용어정리](#용어정리)
- [2. Elasticsearch 시작하기](#2-elasticsearch-시작하기)
	- [1) 설치 및 실행](#1-설치-및-실행)
		- [실행 옵션](#실행-옵션)
		- [쉘스크립트를 사용해 데몬으로 실행하는 파일 만들기](#쉘스크립트를-사용해-데몬으로-실행하는-파일-만들기)
	- [2) Elasticsearch 환경설정](#2-elasticsearch-환경설정)
		- [환경설정방법](#환경설정방법)
- [3. Elasticsearch 시스템 구조](#3-elasticsearch-시스템-구조)
	- [1) 클러스터 구성](#1-클러스터-구성)
		- [하나의 서버에서 여러 클러스터 실행](#하나의-서버에서-여러-클러스터-실행)
		- [디스커버리(Discovery)](#디스커버리discovery)
	- [2) 인덱스와 샤드](#2-인덱스와-샤드)
		- [프라이머리샤드(Primary Shard)와 복제본(Replica)](#프라이머리샤드primary-shard와-복제본replica)
		- [샤드 개수 설정](#샤드-개수-설정)
	- [3) 마스터노드와 데이터노드](#3-마스터노드와-데이터노드)
		- [마스터노드(Master Node)](#마스터노드master-node)
		- [데이터노드(Data Node)](#데이터노드data-node)
		- [Split Brain](#split-brain)
- [4. Elasticsearch 데이터 처리](#4-elasticsearch-데이터-처리)
	- [1) REST API](#1-rest-api)
		- [REST API 설명](#rest-api-설명)
		- [유닉스 curl](#유닉스-curl)
		- [Kibana Dev Tools](#kibana-dev-tools)
	- [2) CRUD - 생성, 조회, 입력, 삭제](#2-crud---생성-조회-입력-삭제)
		- [입력(PUT)](#입력put)
		- [조회(GET)](#조회get)
		- [삭제(DELETE)](#삭제delete)
		- [수정(POST)](#수정post)
	- [3) 벌크 API - _bulk API](#3-벌크-api---_bulk-api)
		- [파일에 저장한 내용 실행](#파일에-저장한-내용-실행)
	- [4) 검색 API - _search API](#4-검색-api---_search-api)
		- [URI 검색](#uri-검색)
		- [데이터 본문(Data Body) 검색](#데이터-본문data-body-검색)
		- [멀티테넌시](#멀티테넌시)
- [5. 검색과 쿼리 - Query DSL](#5-검색과-쿼리---query-dsl)
	- [1) 풀 텍스트 쿼리 (Full Test Query)](#1-풀-텍스트-쿼리-full-test-query)
		- [match_all](#match_all)
		- [match](#match)
		- [match_phrase](#match_phrase)
		- [query_string](#query_string)
	- [2) Bool 복합 쿼리 - Bool Query](#2-bool-복합-쿼리---bool-query)
	- [3) 정확도 - Relevancy](#3-정확도---relevancy)
		- [스코어 (Score) 점수](#스코어-score-점수)
		- [TF (Term Frequency)](#tf-term-frequency)
		- [IDF (Inverse Document Frequency)](#idf-inverse-document-frequency)
		- [Field Length](#field-length)
	- [4) Bool: Should](#4-bool-should)
	- [5) 정확값 쿼리 - Exact Valu Query](#5-정확값-쿼리---exact-valu-query)
		- [bool: filter](#bool-filter)
		- [keyword](#keyword)
	- [6) 범위 쿼리 - Range Query](#6-범위-쿼리---range-query)
		- [range](#range)
		- [날짜 검색](#날짜-검색)
- [6. 데이터 색인과 텍스트 분석](#6-데이터-색인과-텍스트-분석)
	- [1) 역 인덱스 - Reverse Index](#1-역-인덱스---reverse-index)
	- [2) 텍스트 분석 - Text Analysis](#2-텍스트-분석---text-analysis)
	- [3) 애널라이저 - Analyser](#3-애널라이저---analyser)
		- [1. _analyze API](#1-_analyze-api)
		- [2. Term 쿼리](#2-term-쿼리)
		- [3. 사용자 정의 애널라이저 - Custom Analyze](#3-사용자-정의-애널라이저---custom-analyze)
		- [4. 텀 벡터 - Termvectors API](#4-텀-벡터---termvectors-api)
	- [4) 캐릭터 필터 - character Filter](#4-캐릭터-필터---character-filter)
		- [1. HTML Strip](#1-html-strip)
		- [2. Mapping](#2-mapping)
		- [3. Pattern Replace](#3-pattern-replace)
	- [5) 토크나이저 - Tokenizer](#5-토크나이저---tokenizer)
		- [1. Standard, Letter, Whitespace](#1-standard-letter-whitespace)
		- [2. UAX URL Email](#2-uax-url-email)
		- [3. Pattern](#3-pattern)
		- [4. Path hierarchy](#4-path-hierarchy)
	- [6) 토큰 필터 - Token Filter](#6-토큰-필터---token-filter)
		- [1. lowercase, uppercase](#1-lowercase-uppercase)
		- [2. stop](#2-stop)
		- [3. Synonym](#3-synonym)
		- [4. NGram, Edge NGram, Shingle](#4-ngram-edge-ngram-shingle)
		- [5. Unique](#5-unique)
	- [7) 형태소 분석 - Stemming](#7-형태소-분석---stemming)
		- [1. snowball](#1-snowball)
		- [2. nori - 한글 형태소 분석기](#2-nori---한글-형태소-분석기)
			- [nori 설치](#nori-설치)
- [7. 인덱스 설정과 매핑 - Settings & Mapping](#7-인덱스-설정과-매핑---settings--mapping)


## 실습 환경

- OS : Window 10
- Editor : VSCode
- Terminal : bash

# 1. Elasticsearch?

- 오픈소스
- 검색엔진
- 데이터 색인(Index)하여 저장. 데이터 입력을 검색엔진에서는 색인이라고 함.
- 검색, 집계. 결과는 Kibana로 전송하여 Kibana가 표출
- 모든 데이터는 JSON 포멧으로 전달되고 리턴됨. 따라서 변형필요. (CSV 등은 Logstash에서 변환 지원)
- REST API 지원. 모든 데이터 조회, 입력, 삭제를 http 프로토콜을 통해 Rest api로 처리.(GET, POST, PUT, DELETE)
    > REST API 참고 : https://meetup.toast.com/posts/92 


### 용어정리
- 색인 (indexing) : 데이터가 검색될 수 있는 구조로 변경하기 위해 원본 문서를 검색어 토큰들으로 변환하여 저장하는 일련의 과정
- 인덱스 (index, indices) : 색인 과정을 거친 **결과물**, 또는 색인된 데이터가 저장되는 **저장소**입니다. 또한 Elasticsearch에서 도큐먼트들의 논리적인 집합을 표현하는 단위
- 검색 (search) : 인덱스에 들어있는 검색어 토큰들을 포함하고 있는 문서를 찾아가는 과정
- 질의 (query) : 사용자가 원하는 문서를 찾거나 집계 결과를 출력하기 위해 검색 시 입력하는 **검색어 또는 검색 조건**

**용어를 확실히 이해하고 넘어가야 한다!**

# 2. Elasticsearch 시작하기

## 1) 설치 및 실행
> 설치 : https://www.elastic.co/kr/start

Window 기준 Window 버튼 누르면 Zip파일 다운받아짐. 압축푼다.

터미널에서 설치된 파일 디렉토리로 이동 후 실행파일 실행

```sh
$ cd elasticsearch-7.13.4/bin
$ ./elasticsearch.bat

[2021-07-22T09:54:34,874][INFO ][o.e.p.PluginsService     ] [DOGYUN-LABTOP] loggs-matrix-stats]
[2021-07-22T09:54:34,876][INFO ][o.e.p.PluginsService     ] [DOGYUN-LABTOP] lonalysis-common]
[2021-07-22T09:54:34,877][INFO ][o.e.p.PluginsService     ] [DOGYUN-LABTOP] loonstant-keyword]
.
.
.
```
- DOGYUN-LABTOP 이름으로 노드가 실행됨

실행 확인
```sh
$ curl http://localhost:9200

{
  "name" : "DOGYUN-LABTOP",
  "cluster_name" : "elasticsearch",
  "cluster_uuid" : "I23Zw70mSiyVYGVh061dJA",
  "version" : {
    "number" : "7.13.4",
    "build_flavor" : "default",
    "build_type" : "zip",
    "build_hash" : "c5f60e894ca0c61cdbae4f5a686d9f08bcefc942",
    "build_date" : "2021-07-14T18:33:36.673943207Z",
    "build_snapshot" : false,
    "lucene_version" : "8.8.2",
    "minimum_wire_compatibility_version" : "6.8.0",
    "minimum_index_compatibility_version" : "6.0.0-beta1"     
  },
  "tagline" : "You Know, for Search"
}
```


### 실행 옵션
- -d : 백그라운드 실행. 실행 로그는 logs 파일 내에서 확인가능. 백그라운드 실행을 종료하려면 `$ kill 38850` 명령어 사용(Linux)
- -p : 프로세스 ID를 파일로 저장. 아래 명령어는 es.pid 파일에 실행 프로세스 ID를 저장함.
    ```sh
    $ bin/elasticsearch.bat -p es.pid
    ```



### 쉘스크립트를 사용해 데몬으로 실행하는 파일 만들기

`start.sh`
```sh
./bin/elasticsearch.bat -d -p es.pid
```

`stop.sh`
```sh
kill `cat es.pid`
```

해당 파일들을 Elastic 홈 경로에 저장 후 실행하기 위해 권한 변경
```sh
$ chmod 755 start.sh stop.sh
```


## 2) Elasticsearch 환경설정

Elasticsearch는 각 노드별로 실행될 설정을 하여 **노드 역할을 나눌 수** 있다.

### 환경설정방법
1. config 경로 아래에 있는 파일 변경
    - jvm.options - Java 힙메모리 및 환경변수 
    - elasticsearch.yml - Elasticsearch 옵션 
    - log4j2.properties - 로그 관련 옵션 

2. 시작 명령으로 설정
    - -E <설정>


# 3. Elasticsearch 시스템 구조

## 1) 클러스터 구성

클러스터 이름을 설정하여 한 클러스터 내에 여러 노드 관리가능(설정파일에 `cluster.name`)

같은 클러스터의 노드끼리는 데이터통신 가능. 다른 클러스터의 노드끼리는 불가능

노드들은 두 개의 포트 개방
- 클라이언트 통신 http : 9200 ~ 9299
- 노드 간 통신 tcp : 9300 ~ 9399

1서버 1노드 국룰

### 하나의 서버에서 여러 클러스터 실행
설정파일을 수정해서 실행해도 되나 귀찮다.

실행옵션을 통해 여러 클러스터 실행한다.
```sh
$ ./bin/elasticsearch.bat -Ecluster.name=es-cluster-1 -Enode.name=node-1
$ ./bin/elasticsearch.bat -Ecluster.name=es-cluster-1 -Enode.name=node-2
$ ./bin/elasticsearch.bat -Ecluster.name=es-cluster-2 -Enode.name=node-3
```
- 클러스터1 - 노드1, 2
- 클러스터2 - 노드3

이렇게 하니 안된다.

설정파일을 일일이 수정해서 실행해주자...

- cluster.name: es-cluster-1~2
- node.name: node-1~3
- path.data: ./data/node-1~3
- path.logs: ./logs/node-1~3
- http.port: 9200 ~ 9202

설정 후 `./start.sh`로 실행 후 수정 반복.

클러스터에는 **마스터노드**가 존재

### 디스커버리(Discovery)
노드를 실행할 때 같은 서버, `discovery.seed_hosts:`에 설정된 네트워크 상의 다른 노드를 찾아서 하나의 클러스터로 바인딩 하는 과정

1. `discovery.seed_hosts:`에 있는 주소 순서대로 노드 유무 확인.
    - 있으면 `cluster.name`확인 
        - 일치 : 같은 클러스터로 바인딩 > 종료
        - 불일치 : 1로 돌아가 다음 주소 확인
    - 없으면 다음 주소 확인
2. 주소 끝날 때 까지 노드가 없으면
    - 스스로 새로운 클러스터 시작


## 2) 인덱스와 샤드

- 도큐먼트(Document) : 단일 데이터 단위
- 인덱스(Index) : 도큐먼트를 모아놓은 집합. 
- 샤드(Shard) : 인덱스를 나눈 것의 단위. 샤드는 루씬의 단일검색 인스턴스

### 프라이머리샤드(Primary Shard)와 복제본(Replica)

인덱스 생성 시

1. 디폴트로 인덱스는 1개의 샤드로 구성됨(6.x 이하에서는 5개)
2. 클러스터에 노드를 추가할 때 인덱스 샤드가 각 노드로 분산된다. 
3.  디폴트로 샤드복제본 1개 생성
4. 처음 생성된 샤드가 프라이머리샤드, 복제된게 복제본. 두 샤드는 반드시 다른 노드에 배치됨.(데이터 유실 방지)

- 데이터의 가용성과 무결성 유지!!
- 프라이머리 샤드가 유실 시 복제본이 프라이머리 샤드가 되고 복제본을 하나 생성함.

> 노드가 1개만 있는 경우 프라이머리 샤드만 존재하고 복제본은 생성되지 않습니다. Elasticsearch 는 아무리 작은 클러스터라도 데이터 가용성과 무결성을 위해 최소 3개의 노드로 구성 할 것을 권장하고 있습니다.


### 샤드 개수 설정

인덱스를 생성할 때 설정할 수 있다.

curl 명령을 통해 REST API로 샤드 5개, 복제본 1개, 이름 books인 인덱스 생성
```sh
$ curl -XPUT "http://localhost:9200/books" -H 'Content-Type: application/json' -d '
{
    "settings": {
        "number_of_shards": 5,
        "number_of_replicas": 1
    }
}'

{"acknowledged":true,"shards_acknowledged":true,"index":"books"}
```


## 3) 마스터노드와 데이터노드

### 마스터노드(Master Node)

클러스터는 마스터노드가 하나씩 존재하는데 이 노드는 클러스터 상태를 저장한다. 마스터노드가 없으면 클러스터는 동작하지 않음.

- 인덱스 메타데이터
- 샤드 위치 등.

`node.master:` 옵션값을 True로 하면 모든 노드가 마스터노드 후보로 되있어 마스터노드의 정보를 공유한다. 하지만 노드 수가 많아지면 정보 공유를 하는 양이 많아져 부담이 될 수 있어 마스터 후보노드를 정하며 해당 노드의 옵션 값만 True로 하고 다른 노드는 False로 설정한다.


### 데이터노드(Data Node)

실제 색인된 데이터를 저장하는 노드

`node.data:` 옵션을 False로 하면 데이터는 저장하지 않는 마스터노드로만 동작하도록 할 수 있다.

> 실제 운영 환경에서는 마스터 후보를 노드는 1개만 설정하면 안 되고 최소 3개 이상의 홀수개로 설정해야 합니다. 이유는 다음의 Split Brain 문제에서 설명합니다.

### Split Brain

마스터노드가 중지되면 클러스터가 동작하지 못 할 수 있다.

마스터노드가 2개라면 네트워크 단절이 일어나 동작하지 못 할 수 있고 이 때 데이터처리가 일어나고 나중에 복구됐을 때 클러스터 간 데이터 정합성에 문제가 있을 수 있다.

따라서 마스터노드를 포함한 후보노드까지 총 3개 이상의 홀수개로 설정해야한다.

# 4. Elasticsearch 데이터 처리

- 데이터 저장 형식으로 json 도큐먼트를 사용. 
- 쿼리와 클러스터 설정 등 모든 정보를 json 형태로 주고받음

## 1) REST API

**Elasticsearch는 RESTful한 시스템**
- 자원별 고유 URI로 접근 가능
- http 메소드 : GET, POST, PUT, DELETE 로 자원 처리

### REST API 설명
사용자 정보를 다루는 user.com 이라는 시스템이 있다고 가정하고 name=kim, age=38, gender=m 이라는 사용자 정보를 처리한다고 해 보겠습니다. REST를 지원하지 않는 시스템에서는 보통 다음과 같이 각 가능에 대한 개별 페이지로 접근하거나 명령을 매개변수로 처리합니다.

- RESTFul 하지 않은 시스템에서의 데이터 처리
    ```
    입력 : http://user.com/input.jsp?name=kim&age=38&gender=m
    조회 : http://user.com/get.jsp?name=kim
    삭제 : http://user.com/delete.jsp?name=kim
    ```

REST API를 지원하는 시스템은 kim 이라는 사용자에 대해 항상 단일 URL로 접근을 하고 PUT, GET, DELETE 같은 http 메서드로 데이터를 처리합니다

- RESTFul 한 시스템에서의 데이터 처리
    ```
    입력 : PUT http://user.com/kim -d {"name":"kim", "age":38, "gender":"m"}
    조회 : GET http://user.com/kim
    삭제 : DELETE http://user.com/kim
    ```
     
    - 하나의 URI로 처리함.

### 유닉스 curl

`curl` 명령어로 간편하게 REST API 사용 가능

```sh
$ curl -XGET http://localhost:9200

{
  "name" : "node-1",
  "cluster_name" : "es-cluster-1",
  "cluster_uuid" : "ulCKt5gOSiCIGEPuLAVD4Q",
  "version" : {
    "number" : "7.13.4",
    "build_flavor" : "default",
    "build_type" : "zip",
    "build_hash" : "c5f60e894ca0c61cdbae4f5a686d9f08bcefc942",
    "build_date" : "2021-07-14T18:33:36.673943207Z",
    "build_snapshot" : false,
    "lucene_version" : "8.8.2",
    "minimum_wire_compatibility_version" : "6.8.0",
    "minimum_index_compatibility_version" : "6.0.0-beta1"
  },
  "tagline" : "You Know, for Search"
}
```

- curl 명령을 이용해서 클러스터의 최상위 경로를 호출함
- 클러스터 상태 정보가 json형식으로 리턴됨.


### Kibana Dev Tools    

REST API를 이용하기 위해 포스트맨을 쓸 수도 있지만 kibana에서 elasticsearch에서 REST API를 간편하게 쓸 수 있는 Dev tools을 지원

**설치 및 실행**

- 설치
    > 설치 : https://www.elastic.co/kr/start

    Elasticsearch와 마찬가지로 zip 파일을 받아 압축풀기.

- 실행
    ```sh
    $ cd Kibana_PATH/bin/
    $ ./kibana.bat
    ```

- 웹브라우저에서 접속
    > http://localhost:5601

    좌측 3줄아이콘 클릭 후 밑으로 내리면 `Dev Tools`있음.

- 기타 설정
    `config/kibana.yml`에서 설정할 수 있다.


## 2) CRUD - 생성, 조회, 입력, 삭제

Elasticsearch의 도큐먼트는 각자 URI를 갖는다.

`http://<호스트>:<포트>/<인덱스>/_doc/<도큐먼트 id>`

```sh
$ curl -XPUT "http://localhost:9200/my_index/_doc/1" -H 'Content-Type: application/json' -d'
{
  "name": "Jongmin Kim",
  "message": "안녕하세요 Elasticsearch"
}'
```
- 간단하게 my_index 인덱스에 도큐먼트 id가 1인 데이터를 입력하는 예제


### 입력(PUT)

실습은 Kibana의 Dev tools에서 한다.

입력할 때는 **PUT 메소드** 사용
```json
PUT my_index/_doc/1
{
  "name":"Dogyun Kim",
  "message":"안녕하세요 Elasticsearch"
}
```
- Request

```json
{
  "_index" : "my_index",
  "_type" : "_doc",
  "_id" : "1",
  "_version" : 2,
  "result" : "updated",
  "_shards" : {
    "total" : 2,
    "successful" : 1,
    "failed" : 0
  },
  "_seq_no" : 1,
  "_primary_term" : 1
}
```
- Response
- "result"가 처음 요청 시에는 create로 됐다가 두 번 요청 시 "updated"로 리턴된다.
- 중복 입력 방지를 위해 요청 시 `PUT my_index/_create/1`로 하면 덮어쓰기를 방지할 수 있다.


### 조회(GET)

```json
GET my_index/_doc/1
```


### 삭제(DELETE)

도큐먼트 또는 인덱스 단위로 삭제 가능

```json
DELETE my_index/_doc/1
```
- 도큐먼트 삭제


```json
DELETE my_index
```
- 인덱스 삭제

### 수정(POST)

데이터 입력에도 사용 가능하다.

```json
POST my_index/_doc
{
  "name":"Dogyun Kim",
  "message":"안녕하세요 Elasticsearch"
}
```
- 도큐먼트 ID 없이 실행 시 랜덤 ID가 부여된다.

**원하는 필드만 수정하기**
```json
POST my_index/_update/1
{
  "doc": {
    "message": "안녕따리"
  }
}

GET my_index/_doc/1
```


## 3) 벌크 API - _bulk API

- 여러 명령을 한번에 수행하기 위해 벌크 API를 사용

- index, create, update, delete 수행 가능

> _bulk 의 명령문과 데이터문은 반드시 한 줄 안에 입력이 되어야 하며 줄바꿈을 허용하지 않음.


```json
POST _bulk
{"index":{"_index":"test", "_id":"1"}}
{"field":"value one"}
{"index":{"_index":"test", "_id":"2"}}
{"field":"value two"}
{"delete":{"_index":"test", "_id":"2"}}
{"create":{"_index":"test", "_id":"3"}}
{"field":"value three"}
{"update":{"_index":"test", "_id":"1"}}
{"doc":{"field":"value two"}}
```
- 명령문 예시. 
- 각 명령문의 결과는 items에 배열로 리턴됨.

벌크 동작은 따로 동작하는 것 보다 빠르다. 그래서 대용량 데이터 처리 시 벌크 명령을 통해 사용하는게 오버헤드가 적다.

Logstash, Beats는 데이터 입력 시 벌크 명령으로 수행함.


### 파일에 저장한 내용 실행

파일에 명령어 내용을 저장하고 `curl`명령어로 실행 가능.

bulk.json
```json
{"index":{"_index":"test","_id":"1"}}
{"field":"value one"}
{"index":{"_index":"test","_id":"2"}}
{"field":"value two"}
{"delete":{"_index":"test","_id":"2"}}
{"create":{"_index":"test","_id":"3"}}
{"field":"value three"}
{"update":{"_index":"test","_id":"1"}}
{"doc":{"field":"value two"}}
```

실행
```json
$ curl -XPOST "http://localhost:9200/_bulk" -H 'Content-Type: application/json' --data-binary @bulk.json
```
- `--data-binary` 옵션을 추가해서 실행
- 파일 이름 앞에는 `@`를 써야함


## 4) 검색 API - _search API

- 쿼리를 통한 검색기능이 짱이다.
- 검색은 인덱스 단위로 
- `GET 인덱스명/_serarch`

### URI 검색

- _search/뒤에 q 파라메터를 사용하여 검색가능


```json
GET test/_search?q=value
```
- test 인덱스에서 value 라는 값을 찾는 쿼리문

```json
{
  "took" : 16,
  "timed_out" : false,
  "_shards" : {
    "total" : 1,
    "successful" : 1,
    "skipped" : 0,
    "failed" : 0
  },
  "hits" : {
    "total" : {
      "value" : 2,
      "relation" : "eq"
    },
    "max_score" : 0.06453852,
    "hits" : [
      {
        "_index" : "test",
        "_type" : "_doc",
        "_id" : "3",
        "_score" : 0.06453852,
        "_source" : {
          "field" : "value three"
        }
      },
      {
        "_index" : "test",
        "_type" : "_doc",
        "_id" : "1",
        "_score" : 0.06453852,
        "_source" : {
          "field" : "value two"
        }
      }
    ]
  }
}
```

- `hits.total.value`에 보면 결과에 해당하는 문서 개수
- `hits` 리스트에는 정확도가 가장 높은 문서 10개까지 보여줌.
- `_score`는 Relevancy(랠러번시)라고 하는 정확도이다.


### 데이터 본문(Data Body) 검색

- 검색 쿼리를 본문에 입력하여 검색하는 방식
- Elastic의 QueryDSL과 json을 사용


간단하게 문법을 알아보기 위해 가장 많이 쓰이는 `match`를 사용해보쟈.
```json
GET test/_search
{
  "query": {
    "match": {
      "field": "value"
    }
  }
}
```
- "field" 필드에서 검색어 "value" 검색
- 쿼리 입력은 항상 "query" 지정자로 시작
- 그다음 쿼리 종류 선택, 여기서는 "match"
- 그다음 사용할 쿼리의 문법대로 명령어 입력. (쿼리마다 다름)
- match 명령어의 문법은 `<필드명>:<검색어>`

더 자세한 설명은 뒤에 함.

### 멀티테넌시

- 여러 개의 인덱스를 한꺼번에 묶어 검색할 수 있는 기능


1. 쉼표로 나열해서 검색
	```json
	GET logs-2018-01,2018-02,2018-03/_search
	```

2. 와일드카드 `*`를 이용해서 검색
	```json
	GET logs-2018-*/_search
	```

3. 모든 인덱스 검색
	```json
	GET _all/_search
	```

# 5. 검색과 쿼리 - Query DSL

- Elasticsearch는 검색어인 **Term**으로 분석 후 저장함.
- 풀 텍스트 검색 
- 검색을 위한 쿼리 기능. Query DSL (Domain Specific Language). **json 형식**으로!!


## 1) 풀 텍스트 쿼리 (Full Test Query)

- 정확도를 고려하여 검색결과 리턴!


명령어 실습을 위해 예제인덱스 my_index에 도큐먼트 5개를 생성 후 시작!

```json
POST my_index/_bulk
{"index":{"_id":1}}
{"message":"The quick brown fox"}
{"index":{"_id":2}}
{"message":"The quick brown fox jumps over the lazy dog"}
{"index":{"_id":3}}
{"message":"The quick brown fox jumps over the quick dog"}
{"index":{"_id":4}}
{"message":"Brown fox brown dog"}
{"index":{"_id":5}}
{"message":"Lazy jumping dog"}
```

```
The quick brown fox
The quick brown fox jumps over the lazy dog
The quick brown fox jumps over the quick dog
Brown fox brown dog
Lazy jumping dog
```

### match_all
```json
GET my_index/_search
{
  "query":{
    "match_all":{ }
  }
}
```
- 해당 인덱스의 모든 도큐먼트를 검색!


### match

기본적인 검색 명령!


```json
GET my_index/_search
{
  "query": {
	"match": {
      "message": "dog"
	}
  }
} 
```
- "dog" 이 포함된 도큐먼트 리턴!



```json
GET my_index/_search
{
  "query": {
	"match": {
      "message": "quick dog"
	}
  }
}
```
- "quick" or "dog" 이 포함된 도큐먼트 리턴!
- or 검색



```json
GET my_index/_search
{
  "query": {
	"match": {
      "message": "dog",
	  "operator": "and"
	}
  }
} 
```
- "operator"를 통해 and 검색 가능


### match_phrase

입력의 순서를 고려해서 입력어를 모두 포함하는 검색!

```json
GET my_index/_search
{
  "query": {
	"match_phrase": {
      "message": "quick dog"
	}
  }
}
```
- 검색 결과 "quick dog"이 정확하게 포함된 도큐먼트 리턴


```json
GET my_index/_search
{
  "query": {
    "match_phrase": {
      "message": {
        "query": "lazy dog",
        "slop": 1
      }
    }
  }
}
```
- `slop`을 통해 키워드 사이에 다른 단어 끼는 것 허용가능
- 예를들어 slop 값이 1이면 "lazy jumping dog"같이 사이에 낀 단어가 있어도 리턴
- 너무 큰 값은 정확도가 구려서 **1 이상은 비추**


### query_string

URI 검색을 하고싶을 때

```json
GET my_index/_search
{
  "query": {
    "query_string": {
      "default_field": "message",
      "query": "(jumping AND lazy) OR \"(quick dog)\""
    }
  }
}
```
- "jumping"과 "lazy"를 포함한 도큐먼트 또는 "quick dog"을 포함한 도큐먼트가 리턴




## 2) Bool 복합 쿼리 - Bool Query

여러 쿼리를 통해 검색하기 위함!

```json
GET <인덱스명>/_search
{
  "query": {
    "bool": {
      "must": [
        { <쿼리> }, ...
      ],
      "must_not": [
        { <쿼리> }, ...
      ],
      "should": [
        { <쿼리> }, ...
      ],
      "filter": [
        { <쿼리> }, ...
      ]
    }
  }
}
```
- must : 쿼리가 참인 도큐먼트들을 검색합니다. 
- must_not : 쿼리가 거짓인 도큐먼트들을 검색합니다. 
- should : 검색 결과 중 이 쿼리에 해당하는 도큐먼트의 점수를 높입니다. 
- filter : 쿼리가 참인 도큐먼트를 검색하지만 스코어를 계산하지 않습니다. must 보다 검색 속도가 빠르고 캐싱이 가능합니다.


```json
GET my_index/_search
{
  "query": {
    "bool": {
      "must": [
        {
          "match": {
            "message": "quick"
          }
        },
        {
          "match_phrase": {
            "message": "lazy dog"
          }
        }
      ]
    }
  }
}
```
- 단어 "quick"과 구문 "lazy dog"이 포함된 도큐먼트 리턴


```json
GET my_index/_search
{
  "query": {
    "bool": {
      "must_not": [
        {
          "match": {
            "message": "quick"
          }
        },
        {
          "match_phrase": {
            "message": "lazy dog"
          }
        }
      ]
    }
  }
}
```
- 단어 "quick"과 구문 "lazy dog"이 포함되지 않은 도큐먼트 리턴



## 3) 정확도 - Relevancy

- RDBMS와 달리 Elasticsearch는 정확도(**Relevancy**)가 있어 원하는 것과 가장 유사한 결과를 맨 먼저 보여줌!
- 언급할 때는 정확도보다 **랠러번시** 라고 읽는게 좋음


### 스코어 (Score) 점수

- BM25 알고리즘을 사용하여 검색결과가 조건에 얼마나 일치하는지 계산

### TF (Term Frequency)
구글에서 "쥬라기 공원" 이라는 검색어로 검색을 한다고 가정 해 보겠습니다. "쥬라기 공원"이라는 단어가 5번 들어 있는 웹 페이지 보다는 10번 들어있는 웹 페이지가 내가 보고싶어 하는 정보가 있는 페이지일 확률이 높을 것입니다. **도큐먼트 내에 검색된 텀(term)이 더 많을수록 점수가 높아지는 것을 Term Frequency** 라고 합니다.

### IDF (Inverse Document Frequency)
다시 구글에서 "쥬라기 공원" 이라는 검색어로 검색을 했을 때 "쥬라기" 또는 "공원" 중 어떤 단어든 포함하는 페이지들은 검색 결과에 나타날 수 있을 것입니다. 이 때 전체 검색 결과 중에 "쥬라기" 가 포함된 결과는 10개 "공원"이 포함된 결과는 100개 라고 가정한다면 흔한 단어인 "공원" 보다는 희소한 단어인 "쥬라기" 가 검색에 더 중요한 텀일 가능성이 높습니다. **검색한 텀을 포함하고 있는 도큐먼트 개수가 많을수록 그 텀의 자신의 점수가 감소하는 것을 Inverse Document Frequency** 라고 합니다.

### Field Length

검색조건을 포함한 문자열 길이에 따라 정확도가 달라진다. 문자열 길이가 긴 것보다(본문) 짧은 것(제목)에 있는 조건이 더 정확할 수 있다.

```json
GET my_index/_search
{
  "query": {
	"match": {
	  "message": "lazy"
	}
  }
}
```
- 조건으로 검색하면 짧은 도큐먼트의 랠러번시가 더 크다.



## 4) Bool: Should

- 검색 **Score를 조정**할 수 있다.

```json
GET my_index/_search
{
  "query": {
    "match": {
      "message": "fox"
    }
  }
}
```
- 먼저 "fox"가 포함된 도큐먼트 검색 후 결과를 보면

```json
{
  "took" : 0,
  "timed_out" : false,
  "_shards" : {
    "total" : 1,
    "successful" : 1,
    "skipped" : 0,
    "failed" : 0
  },
  "hits" : {
    "total" : {
      "value" : 4,
      "relation" : "eq"
    },
    "max_score" : 0.6063718,
    "hits" : [
      {
        "_index" : "my_index",
        "_type" : "_doc",
        "_id" : "1",
        "_score" : 0.6063718,
        "_source" : {
          "message" : "The quick brown fox"
        }
      },
      {
        "_index" : "my_index",
        "_type" : "_doc",
        "_id" : "4",
        "_score" : 0.6063718,
        "_source" : {
          "message" : "Brown fox brown dog"
        }
      },
      {
        "_index" : "my_index",
        "_type" : "_doc",
        "_id" : "2",
        "_score" : 0.4120614,
        "_source" : {
          "message" : "The quick brown fox jumps over the lazy dog"
        }
      },
      {
        "_index" : "my_index",
        "_type" : "_doc",
        "_id" : "3",
        "_score" : 0.4120614,
        "_source" : {
          "message" : "The quick brown fox jumps over the quick dog"
        }
      }
    ]
  }
}
```
- "lazy"가 포함된 결과의 스코어를 올리고 싶다면

```json
GET my_index/_search
{
  "query": {
    "bool": {
      "must": [
        {
          "match": {
            "message": "fox"
          }
        }
      ],
      "should": [
        {
          "match": {
            "message": "lazy"
          }
        }
      ]
    }
  }
}
```
- should로 "lazy" 검색 추가 후 실행!

```json
GET my_index/_search
{
  "took" : 13,
  "timed_out" : false,
  "_shards" : {
    "total" : 1,
    "successful" : 1,
    "skipped" : 0,
    "failed" : 0
  },
  "hits" : {
    "total" : {
      "value" : 4,
      "relation" : "eq"
    },
    "max_score" : 1.245081,
    "hits" : [
      {
        "_index" : "my_index",
        "_type" : "_doc",
        "_id" : "2",
        "_score" : 1.245081,
        "_source" : {
          "message" : "The quick brown fox jumps over the lazy dog"
        }
      },
      {
        "_index" : "my_index",
        "_type" : "_doc",
        "_id" : "1",
        "_score" : 0.6063718,
        "_source" : {
          "message" : "The quick brown fox"
        }
      },
      {
        "_index" : "my_index",
        "_type" : "_doc",
        "_id" : "4",
        "_score" : 0.6063718,
        "_source" : {
          "message" : "Brown fox brown dog"
        }
      },
      {
        "_index" : "my_index",
        "_type" : "_doc",
        "_id" : "3",
        "_score" : 0.4120614,
        "_source" : {
          "message" : "The quick brown fox jumps over the quick dog"
        }
      }
    ]
  }
}
```
- lazy가 포함된 도큐먼트의 스코어가 증가하여 상위로 올라감.


**should는 math_phrase와 찰떡임**

```json
GET my_index/_search
{
  "query": {
    "bool": {
      "must": [
        {
          "match": {
            "message": "lazy dog"
          }
        }
      ],
      "should": [
        {
          "match_phrase": {
            "message": "lazy dog"
          }
        }
      ]
    }
  }
}
```
- "lazy" or "dog"을 검색하면서 "lazy dog"에 가중치를 더해줌!

- 이렇게 같이 쓰면 장점 : 쇼핑몰 검색 시 "스키 장갑"을 검색 시 "스키"관련 용품도 좌라락 나오고 "장갑"관련 물건도 좌라락 나온다. 이 때 "스키 장갑"에 대한 것에 가중치를 주면 상위에 노출되게 할 수 있겠지. 여기서 `slop` 옵션에 1을 주면? "스키 보드 장갑", "스키 전용 장갑" 등 더 상세한 결과도 나올 수 있다!



## 5) 정확값 쿼리 - Exact Valu Query

- 풀 텍스트 검색과 달리 참/거짓만 판별하여 결과 리턴!

### bool: filter

- bool 쿼리의 filter 안에 쿼리를 사용하면 스코어에 영향 X
- 즉 검색 조건에는 넣지만 스코어에는 영향을 주지 않는 제어가 필요할 때 사용


```json
GET my_index/_search
{
  "query": {
    "bool": {
      "must": [
        {
          "match": {
            "message": "fox"
          }
        }
      ],
      "filter": [
        {
          "match": {
            "message": "quick"
          }
        }
      ]
    }
  }
}


GET my_index/_search
{
  "query": {
    "bool": {
      "must": [
        {
          "match": {
            "message": "fox"
          }
        },
        {
          "match": {
            "message": "quick"
          }
        }
      ]
    }
  }
}
```
- 두 쿼리를 실행했을 때 결과 스코어가 다르게 나온다.

```json
GET my_index/_search
{
  "query": {
    "bool": {
      "must": [
        {
          "match": {
            "message": "fox"
          }
        }
      ],
      "filter": [
        {
          "bool": {
            "must_not": {
              "match": {
                "message": "dog"
              }
            }
          }
        }
      ]
    }
  }
}
```
- "fox"는 포함하고 "dog"은 포함하지 않는 문서 검색
- filter 내부에서 must_not 과 같은 다른 bool 쿼리를 포함하려면 filter 내부에 bool 쿼리를 먼저 넣고 그 안에 다시 must_not 을 넣어야 함
- 스코어는 "fox"를 포함한 문서 검색 할 때와 같다. (dog은 있는 문서)


### keyword

- 문자열 데이터는 keyword형식으로 저장하여 정확값 검색 가능

```json
GET my_index/_search
{
  "query": {
    "bool": {
      "filter": [
        {
          "match": {
            "message.keyword": "Brown fox brown dog"
          }
        }
      ]
    }
  }
}
```
- 문자열, 공백, 대소문자까지 정확히 일치하는 문서 검색
- keyword 타입으로 저장된 필드는 스코어를 계산하지 않고 정확값의 일치 여부만을 따지기 때문에 스코어가 `"_score" : 0.0` 으로 나오게 됩니다. 스코어를 계산하지 않기 때문에 keyword 값을 검색 할 때는 filter 구문 안에!!


필터 안에 넣은 쿼리는 더 빠르게 실행되기 때문에, **스코어가 필요없는 쿼리는 필터로 실행하자!**


## 6) 범위 쿼리 - Range Query

- 숫자나 날짜 등을 범위로 검색가능!
- 스코어가 없다. (해당 조건의 참/거짓만 판별하면 되기 때문)

시작 전 예제 입력

```json
POST phones/_bulk
{"index":{"_id":1}}
{"model":"Samsung GalaxyS 5","price":475,"date":"2014-02-24"}
{"index":{"_id":2}}
{"model":"Samsung GalaxyS 6","price":795,"date":"2015-03-15"}
{"index":{"_id":3}}
{"model":"Samsung GalaxyS 7","price":859,"date":"2016-02-21"}
{"index":{"_id":4}}
{"model":"Samsung GalaxyS 8","price":959,"date":"2017-03-29"}
{"index":{"_id":5}}
{"model":"Samsung GalaxyS 9","price":1059,"date":"2018-02-25"}
```

### range

- 범위 검색을 할 때는 range로 한다.

`range: { <필드명> : { <파라메터> : <값> } }`

| 파라메터 |        설명        |
| :------: | :----------------: |
|   gte    |  이상 (같거나 큼)  |
|    gt    |     초과 (큼)      |
|   lte    | 이하 (같거나 작음) |
|    lt    |    미만 (작음)     |

```json
GET phones/_search
{
  "query": {
    "range": {
      "price": {
        "gte": 700,
        "lt": 900
      }
    }
  }
}
```
- 700 <= price < 900 검색하는 쿼리문


### 날짜 검색

- Elasticsearch에서 날짜는 **ISO8601형식**을 사용

```json
GET phones/_search
{
  "query": {
    "range": {
      "date": {
        "gt": "2016-01-01"
      }
    }
  }
}
```
- 2016년 1월 1일 이후 생산된 휴대폰 문서 리턴


`format`으로 쿼리의 포맷을 다르게 할 수 있다.

```json
GET phones/_search
{
  "query": {
    "range": {
      "date": {
        "gt": "31/12/2015",
        "lt": "2018",
        "format": "dd/MM/yyyy||yyyy"
      }
    }
  }
}
```


`now`
```json
GET phones/_search
{
  "query": {
    "range": {
      "date": {
        "gt": "2016-01-01||+6M",
        "lt": "now-365d"
      }
    }
  }
}
```
- date의 값이 2016년 1월 1일에서 6개월 후인 날 부터 오늘보다 365일 전인 날 사이의 데이터를 가져오는 쿼리


# 6. 데이터 색인과 텍스트 분석

- 검색을 위해 텍스트 데이터를 어떻게 처리하고 데이터를 색인 할 때 Elasticsearch에서 어떤 과정이 이루어지는지

## 1) 역 인덱스 - Reverse Index

- 텀(Term) : 문서 내에 포함된 키워드를 텀이라고 부른다.
- 역인덱스 구조 : 텀이 어떤 문서에 포함되어 있는지를 저장해놓은 것.

|  텀   |      ID(문서)       |
| :---: | :-----------------: |
| Hello |      doc1 doc2      |
|  The  |   doc2 doc4 doc5    |
|  man  |      doc1 doc4      |
|  is   | doc2 doc3 doc4 doc5 |
- 역인덱스 구조

| ID(문서) |     단어     |
| :------: | :----------: |
|   doc1   |  Hello man   |
|   doc2   | Hello The is |
|   doc3   |      is      |
|   doc4   |  The man is  |
|   doc5   |    The is    |
- 인덱스 구조


**검색이 빠르다!**



## 2) 텍스트 분석 - Text Analysis

- 텍스트를 저장하기 위해 그 전에 처리 과정을 거친다. (특수문자 제거, 공백제거, 대소문자 등등)
- 이 과정이 **텍스트 분석**
- 이를 수행하는 게 **애널라이저(분석기)**
- 애널라이저 구성과 과정
  
	```
	캐릭터 필터(0~3개) : 특정 문자를 대치하거나 제거 
			↓ 
	토크나이저(단 1개) : 문장에 속한 단어들을 텀 단위로 하나씩 분리 
			↓ 
	토큰 필터(0~n개) : 분리된 텀 들을 하나씩 가공
	```

- 특수문자 제거, 공백 제거, 대/소문자 변형, 불용어 제거, 형태소 변형(s, ~ing 등), 동의어 추가 등등..

> 자세한 사항 : https://esbook.kimjmin.net/06-text-analysis/6.2-text-analysis


## 3) 애널라이저 - Analyser
- Elasticsearch에는 애널라이저를 조합하고 그 동작을 자세히 확인할 수 있는 API 들이 있다.

### 1. _analyze API

- `_analyze` API로 분석된 문장 확인 가능!
- `tokenizer`는 하나만 가능. (단 1개 존재 위에 써놓음)
- `filter` 토큰필터는 배열로 설정

```json
GET _analyze
{
  "text": "The quick brown fox jumps over the lazy dog",
  "tokenizer": "whitespace",
  "filter": [
    "lowercase",
    "stop",
    "snowball"
  ]
}
```
- 결과를 보면 토크나이저, 토큰필터된 "jump"(s 필터링 됨), "lazi"(y가 i로)를 확인할 수 있다.
- 필터는 순서에 따라 적용되므로 순서가 중요.
- `lowercase` : 소문자로
- `stop` : 불용어 제거
- `snowball` : 형태소 변경


위에서 사용한 것 처럼 하나하나 필터와 토크나이저를 적용하여 애널라이저를 커스텀할 수 있고, Elasticsearch에 이미 존재하는 조합들을 사용할 수도 있다.

위의 애널라이저 옵션들은 Elasticsearch에서 `snowball`로 제공함

```json
GET _analyze
{
  "text": "The quick brown fox jumps over the lazy dog",
  "analyzer": "snowball"
}
```
- 위와 같은 결과

인덱스에 애널라이저를 설정해놓으면 검색 시 애널라이저 옵션을 거쳐 검색된다.

예를들면 설정 안하면 "jump"검색 시 "jumps"가 검색 안되지만 애널라이저 설정하면 검색됨

```json
PUT my_index2
{
  "mappings": {
    "properties": {
      "message": {
        "type": "text",
        "analyzer": "snowball"
      }
    }
  }
}
```
- my_index2 인덱스의 message 필드에 snowball 애널라이저 적용

```json
PUT my_index2/_doc/1
{
  "message": "The quick brown fox jumps over the lazy dog"
}
```
- 인덱스에 도큐먼트 입력

```json
GET my_index2/_search
{
  "query": {
    "match": {
      "message": "jumping"
    }
  }
}
```
- jumping으로 검색해도 jump로 필터링된 결과값이 나옴.
- 검색 메세지의 jumping은 jump로
- 도큐먼트의 jumps는 역인덱스에 jump로 저장되어 매칭됨.


### 2. Term 쿼리

- `match`보다 더 세심한 검색쿼리
- 애널라이저를 적용하지 않고 검색함
- jumps 검색 시 안나옴
- 정확히 jump를 검색해야 나옴! (역인덱스에는 jump로 저장되어 있기 때문!)

```json
GET my_index2/_search
{
  "query": {
	"message": "jumps"
  }
}
```
- 결과 안나옴.

------

- 텍스트 분석(Analysis) 과정은 검색에 사용되는 역 인덱스에만 관여 
- 원본 데이터는 변하지 않으므로 쿼리 결과의 _source 항목에는 항상 원본 데이터가 나옴

- Elasticsearch는 데이터를 실제로 검색에 사용되는 텀(Term) 으로 분석 과정을 거쳐 저장하기 때문에 검색 시 대소문자, 단수나 복수, 원형 여부와 상관 없이 검색이 가능합니다. 이러한 Elasticsearch의 특징을 풀 텍스트 검색(Full Text Search) 이라고 하며 한국어로 전문 검색 이라고도 합니다.

> 다양한 애널라이저, 캐릭터 필터, 토크나이저, 토큰필터는 공식문서 참조 : https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis-analyzers.html


### 3. 사용자 정의 애널라이저 - Custom Analyze

- 실제로는 주로 커스텀 애널라이저를 사용함.

- 사용자 정의 애널라이저는 인덱스 `settings`의 `"index": { "analysis": }`에서 설정함

```json
PUT my_index3
{
  "settings": {
    "index": {
      "analysis": {
        "analyzer": {
          "my_custom_analyzer": {
            "type": "custom",
            "tokenizer": "whitespace",
            "filter": [
              "lowercase",
              "stop",
              "snowball"
            ]
          }
        }
      }
    }
  }
}
```
- my_index3 인덱스의 settings 안에 my_custom_analyzer 생성
- `whitespace` 토큰크나이저 그리고 `lowercase`, `stop`, `snowball` 토큰필터를 사용하는 my_custom_analyzer 라는 이름의 애널라이저를 추가

```json
GET my_index3/_analyze
{
	"analyzer": "my_custom_analyzer",
  "text": [
	  "The quick brown fox jumps over the lazy dog"
  ]
}
```
- _analyzer API 로 my_index3 에서 my_custom_analyzer 사용


**사용자 정의 토큰필터**

우선 my_index3를 지운다.
```json
DELETE my_index3
```

```json
PUT my_index3
{
  "settings": {
    "index": {
      "analysis": {
        "analyzer": {
          "my_custom_analyzer": {
            "type": "custom",
            "tokenizer": "whitespace",
            "filter": [
              "lowercase",
              "my_stop_filter",
              "snowball"
            ]
          }
        },
        "filter": {
          "my_stop_filter": {
            "type": "stop",
            "stopwords": [
              "brown"
            ]
          }
        }
      }
    }
  }
}
```
- brown을 불용어로 설정하는 필터 커스텀

```json
GET my_index3/_analyze
{
  "analyzer": "my_custom_analyzer",
  "text": [
    "The quick brown fox jumps over the lazy dog"
  ]
}
```
- 실행해보면 brown이 불용어 처리되어 결과에 나타나지 않음.


### 4. 텀 벡터 - Termvectors API

-  색인된 도큐먼트의 역 인덱스의 내용을 확인할 때는 도큐먼트 별로 _termvectors API를이용해서 확인

```json
PUT my_index3/_doc/1
{
  "message": "The quick brown fox jumps over the lazy dog"
}

GET my_index3/_termvectors/1?fields=message
```
- my_index3/_doc/1 도큐먼트의 message 필드의 termvectors 확인



## 4) 캐릭터 필터 - character Filter

- 전처리 도구
- 전체 문장에서 특정 문자를 대치하거나 제거. 
- `char_filter` 항목에 배열로 입력하여 적용

### 1. HTML Strip

- 입력 텍스트가 HTML 텍스트인 경우 HTML 태그를 제거함.

```json
POST _analyze
{
  "tokenizer": "keyword",
  "char_filter": [
    "html_strip"
  ],
  "text": "<p>I&apos;m so <b>happy</b>!</p>"
}
```
- 결과는 <> 등의 태그 제거, HTML 문법 용어 해석하여 처리 됨.




### 2. Mapping

- 지정된 단어를 다른 단어로 치환
- 특수문자를 적용한 검색에 필수
- 실제로 제일 많이 쓰임

```json
POST coding/_bulk
{"index":{"_id":"1"}}
{"language":"Java"}
{"index":{"_id":"2"}}
{"language":"C"}
{"index":{"_id":"3"}}
{"language":"C++"}
```
- 예제를 위한 인덱스 생성

```json
GET coding/_search
{
  "query": {
    "match": {
      "language": "C++"
    }
  }
}
```
- C++로 검색했는데 결과는 C와 C++ 두 개의 도큐먼트가 나왔다.
- 애널라이저가 특수문자 +를 제거해버려서 이렇게 됨.
- 따라서 +를 다른 문자로 치환해주어야 한다.


`+` 문자를 `_plus_`로 치환하여 색인해보자!

```json
DELETE coding

PUT coding
{
  "settings": {
    "analysis": {
      "analyzer": {
        "coding_analyzer": {
          "char_filter": [
            "cpp_char_filter"
          ],
          "tokenizer": "whitespace",
          "filter": [ "lowercase", "stop", "snowball" ]
        }
      },
      "char_filter": {
        "cpp_char_filter": {
          "type": "mapping",
          "mappings": [ "+ => _plus_", "- => _minus_" ]
        }
      }
    }
  },
  "mappings": {
    "properties": {
      "language": {
        "type": "text",
        "analyzer": "coding_analyzer"
      }
    }
  }
}
```
- coding 인덱스에 mapping 캐릭터필터 설정.


```json
POST coding/_bulk
{"index":{"_id":"1"}}
{"language":"Java"}
{"index":{"_id":"2"}}
{"language":"C"}
{"index":{"_id":"3"}}
{"language":"C++"}

GET coding/_search
{
  "query": {
    "match": {
      "language": "C++"
    }
  }
}
```
- 다시 검색해보면 C++ 를 포함한 도큐먼트 하나만 검색됨!



### 3. Pattern Replace

- 정규식(Regular Expression)을 이용해서 좀더 복잡한 패턴들을 치환할 수 있는 캐릭터 필터
- 예를들면 카멜 표기법으로 된 것을 카멜마다 띄워서 각자의 텀으로 색인하는 등...
- HelloWorld => hello, world로 나눠서 색인

```json
PUT camel
{
  "settings": {
    "analysis": {
      "analyzer": {
        "camel_analyzer": {
          "char_filter": [
            "camel_filter"
          ],
          "tokenizer": "standard",
          "filter": [
            "lowercase"
          ]
        }
      },
      "char_filter": {
        "camel_filter": {
          "type": "pattern_replace",
          "pattern": "(?<=\\p{Lower})(?=\\p{Upper})",
          "replacement": " "
        }
      }
    }
  }
}
```
- camel 인덱스에 pattern_replace 캐릭터필터 설정


```json
GET camel/_analyze
{
  "analyzer": "camel_analyzer",
  "text": [
    "public void FooBazBar()"
  ]
}
```
- 결과는 Foo Baz Bar 하나씩 색인됨.


## 5) 토크나이저 - Tokenizer
- 문장에 속한 단어들을 텀 단위로 하나씩 분리
- 단 한개만 사용 가능


### 1. Standard, Letter, Whitespace
- 가장 많이 사용되는 것들

```json
GET _analyze
{
  "tokenizer": "standard",
  "text": "THE quick.brown_FOx jumped! @ 3.5 meters."
}

GET _analyze
{
  "tokenizer": "letter",
  "text": "THE quick.brown_FOx jumped! @ 3.5 meters."
}

GET _analyze
{
  "tokenizer": "whitespace",
  "text": "THE quick.brown_FOx jumped! @ 3.5 meters."
}
```
- `standard` : 특수문자 제거 및 공백 기준으로 색인. **젤 많이 쓰임**
- `letter` : 모든 공백, 숫자, 특수문자 기준으로 색인
- `whiterspace` : 공백 기준으로 색인

### 2. UAX URL Email

- 이메일 주소와 웹 URL 경로는 분리하지 않고 그대로 하나의 텀으로 저장
- `standard`로 할 경우 @같은 특수문자를 제거해버려서...

```json
GET _analyze
{
  "tokenizer": "uax_url_email",
  "text": "email address is my-name@email.com and website is https://www.elastic.co"
}
```


### 3. Pattern

- `/`, `|`, `,` 등 특수한 문자를 구분자로 사용하여 텀을 분리하고 싶은 경우 사용

```json
PUT pat_tokenizer
{
  "settings": {
    "analysis": {
      "tokenizer": {
        "my_pat_tokenizer": {
          "type": "pattern",
          "pattern": "/"
        }
      }
    }
  }
}

GET pat_tokenizer/_analyze
{
  "tokenizer": "my_pat_tokenizer",
  "text": "/usr/share/elasticsearch/bin"
}
```
- `/`를 구분자로 하는 토크나이저 생성 후 이걸로 분석
- 결과는 `/`로 나눠져서 색인됨.



### 4. Path hierarchy

- 파일 경로는 다르나 디렉토리 명이 같은 경우 혼돈을 줌
- 이때 경로별로 저장하는 토크나이저

```json
POST _analyze
{
  "tokenizer": "path_hierarchy",
  "text": "/usr/share/elasticsearch/bin"
}
```


## 6) 토큰 필터 - Token Filter

- 분리된 텀 들을 하나씩 가공

> 공식문서 토큰필터 : https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis-tokenfilters.html


### 1. lowercase, uppercase

```json
GET _analyze
{
  "filter": [ "lowercase" ],
  "text": [ "Harry Potter and the Philosopher's Stone" ]
}
```
- 그냥 필수로 쓰임


### 2. stop

- 불용어 제거하는 토큰필터


```json
PUT my_stop
{
  "settings": {
    "analysis": {
      "filter": {
        "my_stop_filter": {
          "type": "stop",
          "stopwords": [
            "in",
            "the",
            "days"
          ]
        }
      }
    }
  }
}

GET my_stop/_analyze
{
  "tokenizer": "whitespace",
  "filter": [
    "lowercase",
    "my_stop_filter"
  ],
  "text": [ "Around the World in Eighty Days" ]
}
```
- 불용어 커스텀


파일에 불용어를 저장해놓고 불러와서 쓸 수도 있다.

```sh
$ mkdir config/user_dic
$ vi my_stop_dic.txt

in
the
eighty
```
- 세 단어를 불용어로 입력
- 반드시 엔터로 구분

```json
PUT my_stop
{
  "settings": {
    "analysis": {
      "filter": {
        "my_stop_filter": {
          "type": "stop",
          "stopwords_path": "./user_dic/my_stop_dic.txt"
        }
      }
    }
  }
}

GET my_stop/_analyze
{
  "tokenizer": "whitespace",
  "filter": [
    "lowercase",
    "my_stop_filter"
  ],
  "text": [ "Around the World in Eighty Days" ]
}
```
- config 디렉토리를 기준으로 상대 경로를 지정
- 불용어로 지정되어 색인 안됨


기존에 사전 파일을 수정하면 인덱스를 새로고침 해줘야함
```json
POST <인덱스명>/_close
POST <인덱스명>/_open
```
- close 된 상태에서는 검색 불가능.

### 3. Synonym

- 동의어 설정하는 것 (AWS = Amazon = 아마존.. 등)

- `synonyms`에서 설정
- 파일을 만들어 설정

1. "A, B => C" : 왼쪽의 A, B 대신 오른쪽의 C 텀을 저장. A, B 로는 C 의 검색이 가능하지만 C 로는 A, B 가 검색안됨.
2. "A, B" : A, B 각 텀이 A 와 B 두개의 텀을 모두 저장. A 와 B 모두 서로의 검색어로 검색됨.

```json
PUT my_synonym
{
  "settings": {
    "analysis": {
      "analyzer": {
        "my_syn": {
          "tokenizer": "whitespace",
          "filter": [
            "lowercase",
            "syn_aws"
          ]
        }
      },
      "filter": {
        "syn_aws": {
          "type": "synonym",
          "synonyms": [
            "amazon => aws"
          ]
        }
      }
    }
  },
  "mappings": {
    "properties": {
      "message": {
        "type": "text",
        "analyzer": "my_syn"
      }
    }
  }
}
```
- "amazon => aws" 동의어를 지정하는 my_synonym 인덱스 생성

```json
PUT my_synonym/_doc/1
{ "message" : "Amazon Web Service" }
PUT my_synonym/_doc/2
{ "message" : "AWS" }


// term 쿼리로 aws 검색
GET my_synonym/_search
{
  "query": {
    "term": {
      "message": "aws"
    }
  }
}

// term 쿼리로 amazon 검색
GET my_synonym/_search
{
  "query": {
    "term": {
      "message": "amazon"
    }
  }
}

// match 쿼리로 amazon 검색
GET GET my_synonym/_search
{
  "query": {
    "match": {
      "message": "amazon"
    }
  }
}
```

```json
DELETE my_synonym

PUT my_synonym
{
  "settings": {
    "analysis": {
      "analyzer": {
        "my_syn": {
          "tokenizer": "whitespace",
          "filter": [
            "lowercase",
            "syn_aws"
          ]
        }
      },
      "filter": {
        "syn_aws": {
          "type": "synonym",
          "synonyms": [
            "amazon, aws"
          ]
        }
      }
    }
  },
  "mappings": {
    "properties": {
      "message": {
        "type": "text",
        "analyzer": "my_syn"
      }
    }
  }
}
```
- "amazon, aws" 동의어를 지정하는 my_synonym 인덱스 생성
- 이후 명령어를 입력해보자.

```json
```json
PUT my_synonym/_doc/1
{ "message" : "Amazon Web Service" }
PUT my_synonym/_doc/2
{ "message" : "AWS" }


// term 쿼리로 aws 검색
GET my_synonym/_search
{
  "query": {
    "term": {
      "message": "aws"
    }
  }
}

// term 쿼리로 amazon 검색
GET my_synonym/_search
{
  "query": {
    "term": {
      "message": "amazon"
    }
  }
}

// match 쿼리로 amazon 검색
GET GET my_synonym/_search
{
  "query": {
    "match": {
      "message": "amazon"
    }
  }
}
```

동음어가 많으면 쿼리로 관리하기 힘드므로 파일로 저장해둔다.

```sh
$ cd config/user_dic
$ vi my_syn_dic.txt

quick, fast
hop, jump
```

파일 생성 후 다시 실행

```json
DELETE my_synonym

PUT my_synonym
{
  "settings": {
    "analysis": {
      "analyzer": {
        "my_syn": {
          "tokenizer": "whitespace",
          "filter": [
            "lowercase",
            "syn_aws"
          ]
        }
      },
      "filter": {
        "syn_aws": {
          "type": "synonym",
          "synonyms_path": "user_dic/my_syn_dic.txt"
        }
      }
    }
  },
  "mappings": {
    "properties": {
      "message": {
        "type": "text",
        "analyzer": "my_syn"
      }
    }
  }
}
```
- 이후 동음어를 검색해본다.


```json
PUT my_synonym/_doc/1
{ "message": "Quick brown fox jump" }
PUT my_synonym/_doc/2
{ "message": "hop rabbit is fast" }

GET my_synonym/_search
{
  "query": {
    "bool": {
      "must": [
        {
          "term": {
            "message": "quick"
          }
        },
        {
          "term": {
            "message": "jump"
          }
        }
      ]
    }
  }
}
```
- quick과 jump로만 검색해도 hop, fast가 포함된 도큐먼트가 리턴된다.



### 4. NGram, Edge NGram, Shingle

**NGram : 텀 하나를 또 나눠서 저장하는 것.**
예를들면 Hour를 Ho, ou, ur 이렇게 나눠서 저걸로도 검색 가능하게 하는 것.

`"type": "nGram"`으로 설정

몇 글자로 나눌지는 `min_gram`, `max_gram`으로 설정가능 

```json
PUT my_ngram
{
  "settings": {
    "analysis": {
      "filter": {
        "my_ngram_f": {
          "type": "nGram",
          "min_gram": 2,
          "max_gram": 3
        }
      }
    }
  }
}

GET my_ngram/_analyze
{
  "tokenizer": "keyword",
  "filter": [
    "my_ngram_f"
  ],
  "text": "house"
}
```
- 예제



**Edge NGram : 텀 앞쪽부터 나눠서 저장하는 것**

예를들면 hour을 h, ho, hou, hour 이렇게 저장함

`"type": "edgeNGram"`로 설정

`min_gram`, `max_gram`으로 설정

```json
DELETE my_ngram

PUT my_ngram
{
  "settings": {
    "analysis": {
      "filter": {
        "my_ngram_f": {
          "type": "edgeNGram",
          "min_gram": 1,
          "max_gram": 3
        }
      }
    }
  }
}

GET my_ngram/_analyze
{
  "tokenizer": "keyword",
  "filter": [
    "my_ngram_f"
  ],
  "text": "house"
}
```
- 예제


**Shingle : 단어 단위로 구성하여 묶음**

예를들면 My name is dogyun을 My name, name is, is dogyun으로 나눠서 저장하는 것.

`"type": "shingle"`로 설정

`"min_shingle_size"`, `"max_shingle_size"`로 설정

```json
PUT my_shingle
{
  "settings": {
    "analysis": {
      "filter": {
        "my_shingle_f": {
          "type": "shingle",
          "min_shingle_size": 3,
          "max_shingle_size": 4
        }
      }
    }
  }
}

GET my_shingle/_analyze
{
  "tokenizer": "whitespace",
  "filter": [
    "my_shingle_f"
  ],
  "text": "this is my sweet home"
}
```
- 예제


> NGram, edgeNGram, Shingle은 자동 완성 기능을 구현하거나 프로그램 코드 안에서 문법이나 기능명을 검색하는 것과 같이 특수한 요구사항을 충족해야 하는 경우 유용


### 5. Unique

중복되는 텀 들은 하나만 저장하도록

예를들면 "white fox, white rabbit, white bear"은 white가 3번 저장되는데 이 중복을 없애줌.

```json
GET _analyze
{
  "tokenizer": "standard",
  "filter": [
    "lowercase",
    "unique"
  ],
  "text": [
    "white fox, white rabbit, white bear"
  ]
}
```

스코어 계산이 필요한 동작에서는 안 쓰는게 좋다.

왜? TF, IDF를 계산하는데 해당 단어의 빈도수가 필요하기 때문이다.


## 7) 형태소 분석 - Stemming

- 텀에 있는 단어들의 기본 형태인 어간을 추출하는 과정

### 1. snowball

- 대표적인 영어 형태소 분석기
- Elasticsearch에 있어서 그냥 쓰면됨.
- 위에서 써봤다.

### 2. nori - 한글 형태소 분석기

- 대표 한글 형태소분석기
- elasticsearch에 기본적으로 없어서 설치해야함


#### nori 설치
analysis-nori 플러그인을 설치해야 함

```sh
$ ./bin/elasticsearch-plugin.bat install analysis-nori 
```

```json
GET _analyze
{
  "tokenizer": "nori_tokenizer",
  "text": [
    "동해물과 백두산이"
  ]
}
```
- 간단 예제
- 잘 나눠진다. 쩌러

> 더 많은 정보 : https://esbook.kimjmin.net/06-text-analysis/6.7-stemming/6.7.2-nori

# 7. 인덱스 설정과 매핑 - Settings & Mapping

- 인덱스는 하나의 노드에만 있지 않음
- 샤드 단위로 쪼개져서 각 노드에 분산되어있다.
- 인덱스 단위에서의 설정해보기 
- 데이터 명세인 매핑 알아보기



