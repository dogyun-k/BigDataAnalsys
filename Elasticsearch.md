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


## 실습 환경

- OS : Window 10
- Tool : VSCode
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

구조
