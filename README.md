<div align="center">
    <h1>Good Listener Project (SW Maestro)</h1>
    <h1>LISN</h1>
</div>

![LISN](https://user-images.githubusercontent.com/51017609/63237566-7cae2980-c27d-11e9-8a2f-6067a66f8c18.png)

<div align="center">
    <h3>
        <a href="https://li-sn.io">
            Website
        </a>
    </h3>
</div>

<br>

## Table of Contents
- [Structure](#Structure)
- [main](#main)
- [signin](#signin)
- [record](#record)
- [Run](#run)
- [Using](#using)

<br>

## Structure
- __main :__ 첫 화면
- __signin :__ 로그인에 관련된 모든 것 
- __record :__ 음성 노트에 관련된 모든 것

<br>

## main

### HTTP API
| Method | URI | Parameter | Return | Description |
| ------ | ------ |------ |------ |------ |
| GET | / |  | index.html | 처음 접속 시, main page 반환 |

<br>

## signin

*  로그인과 회원가입을 할 수 있는 페이지
*  OAuth 2.0 - Google을 사용

### DB - User table
| Name | Type | Description | 
| ------ | ------ |------ |
| id | integer | pk |
| name | char(100) | 사용자 이름 |
| email | char(320) | google mail 계정 |

### HTTP API
| Method | URI | Parameter | Return | Description |
| ------ | ------ |------ |------ |------ |
| POST | /v1/api/signin/oauth/google/user | data | return #1 | google이 전달해주는 id_token을 이용하여 user의 정보를 받아오고 db에 저장. 이후 jwt 토큰을 생성해 user의 cookie에 등록하고 request |
| DELETE | /v1/api/signin/token |  |  | session을 flush -> 등록된 토큰 제거 |

**return #1**

```
{
    redirect_url,
    user_id
}
```

<br>

## record

*  녹음과 관련된 페이지
*  사용자의 note 리스트 페이지 + 편집/녹음 페이*  

### DB - note table
| Name | Type | Description | 
| ------ | ------ |------ |
| id | integer | pk |
| user | integer | fk, user id |
| title | char(200) | note 제목 |
| created_at | date/time | 생성 날짜 |
| updated_at | date/time | 수정 날짜 |
| content | text | 사용자가 작성한 최종 회의록 |
| is_trash | bool | 휴지통에 있는지 true / false |

### DB - audio table
| Name | Type | Description | 
| ------ | ------ |------ |
| id | integer | pk |
| note | integer | fk, note id |
| user | integer | fk, user id |

### DB - sentence table
| Name | Type | Description | 
| ------ | ------ |------ |
| id | integer | pk |
| index | integer | audio 안에서 몇번째 문장인지 |
| audio | integer | fk, audio id |
| user | integer | fk, user id |
| started_at | integer | record 안에서 시작 시간(밀리초단위) |
| ended_at | integer | record 안에서 끝 시간(밀리초단위) |
| content | text | 실제 문장 내용 |

### HTTP API
| Method | URI | Parameter | Parameter Type | Return | Description |
| ------ | ------ |------ |------ |------ |------ |
| GET | /v1/api/record/list | user_id | query | return #1 | user의 note list 정보를 가져오는 api(trash 제외) |
| GET | /v1/api/record/note | note_id | query | return #2 | user의 한 개의 note에 대한 정보를 가져오는 api |
| POST | /v1/api/record/note | user_id | form | return #3 | 새로운 note를 생성하고 그 정보를 받아오는 api |
| PUT | /v1/api/record/note | note_id, title, content | form | return #4 | user가 작성한 title과 content를 저장하는 api |
| DELETE | /v1/api/record/note | note_id | form | return #5 | 특정 note를 삭제하는 api |
| POST | /v1/api/record/audio | note_id, FILE['audio_data'] | form | return #6 | 녹음파일 webm 형식으로 S3에 보내서 저장 |
| GET | /v1/api/record/audio | audio_id | query | return #7 | S3 audio data의 url을 변환하는 api(제한시간 : 호출 이후 1시간) |
| POST | /v1/api/record/sentence | index, audio_id, started_at, ended_at, content | form | return #8 | 문장 단위로 오디오를 split하고 저장 |
| PUT | /v1/api/record/trash/note | note_id | form | return #9 | 특정 note를 휴지통으로 보내는 api |
| GET | /v1/api/record/trash/note | user_id | form | like return #1 | user의 note list 정보를 가져오는 api(trash만) |

**return #1**

```
{
    user_id,
    notes:[
        {
            note_id,
            title,
            created_at,
            updated_at,
            summary [content 앞 20글자]
        }
    ]    
}
```
**return #2**
```
{
    note_id,
    title,
    content,
    audios:[
        {
            audio_id,
            sentences:[
                {
                    sentence_id,
                    started_at,
                    ended_at,
                    content
                }
            ]
        }
    ]
}
```
**return #3**
```
{
    note_id
}
```
**return #6**
```
{
    audio_id
}
```
**return #7**
```
{
    data_url
}
```
**return #8**
```
{
    sentence_id
}
```

<br>

## Run

```
$ pip install -r requirements.txt
$ python manage.py runserver
```

## Using
```
1. python3
2. Django 2.0
```