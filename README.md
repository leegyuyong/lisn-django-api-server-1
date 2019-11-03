[![LISN](https://user-images.githubusercontent.com/51017609/63237566-7cae2980-c27d-11e9-8a2f-6067a66f8c18.png)](https://li-sn.io)

## Table of Contents
- [Server Architecture](#server-architecture)
- [User API](#user-api)
- [Record API](#record-api)
- [API response status code](#api-response-status-code)

<br>

## Server Architecture
![Architecture](https://user-images.githubusercontent.com/24379083/63470541-e01b9f80-c4a7-11e9-92db-4b5cd5c524f0.png)

<br>

## User API

*  Sign-in, Sign-out, token 발급등 user와 관련된 API
*  OAuth 2.0 - Google

#### User table
| Name | Type | Description | 
| ------ | ------ |------ |
| id | integer | pk |
| name | char(100) | 사용자 이름 |
| email | char(320) | google mail 계정 |

#### API List
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

## Record API

*  Record 및 Note 작성에 대한 API

#### Note table
| Name | Type | Description | 
| ------ | ------ |------ |
| id | integer | pk |
| user | integer | fk, user id |
| title | char(200) | note 제목 |
| created_at | date/time | 생성 날짜 |
| updated_at | date/time | 수정 날짜 |
| content | text | 사용자가 작성한 텍스트 |
| is_trash | bool | 휴지통에 있는지 true / false |

#### Audio table
| Name | Type | Description | 
| ------ | ------ |------ |
| id | integer | pk |
| note | integer | fk, note id |
| user | integer | fk, user id |

#### Sentence table
| Name | Type | Description | 
| ------ | ------ |------ |
| id | integer | pk |
| index | integer | audio 안에서 순서 |
| audio | integer | fk, audio id |
| user | integer | fk, user id |
| started_at | integer | record 안에서 시작 시간 (밀리초단위) |
| ended_at | integer | record 안에서 끝 시간 (밀리초단위) |
| content | text | 문장 내용 |

#### API LIST
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

## API response status code

| Status | Description |
| ------ | ------ |
| 200 | 응답 성공 (POST 이외) |
| 201 | POST 요청으로 리소스 생성에 성공했을 경우 |
| 400 | 부적절한 요청 (존재하지 않는 API, 존재하지 않는 리소스, 다른 유저의 리소스에 접근, 리소스 생성/수정/삭제 실패, 기타등등) |
| 401 | 로그인하지 않은 유저가, 로그인했을 때 요청가능한 리소스를 요청하는 경우 |
| 405 | 요청한 리소스에 불가능한 Method일 경우 |
| 500 | 서버에 내부문제가 있는 경우 |