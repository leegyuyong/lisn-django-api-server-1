[![LISN](https://user-images.githubusercontent.com/51017609/63237566-7cae2980-c27d-11e9-8a2f-6067a66f8c18.png)](https://lisn.ai)

## Architecture
![Architecture](https://user-images.githubusercontent.com/24379083/69012865-b21dfc80-09bd-11ea-82e8-2ee40d095c55.png)

## API Authorization

-   HTTP Request 헤더의 'Authorization' key에 Access Token을 value로 첨부한다.
-   value는 '{type} {access token}' 형식을 따라야한다.
- ex) **Bearer xmp98-cb35.potn6jz.zorj15gmb**

## Database Table List

**User Table**

|Name  |Type   |Description |
|------|-------|------------|
|id    |integer|pk          |
|name  |char(100)|사용자 이름      |
|email |char(320)|google email 계정|
|picture_url|char(320)|사용자 프로필 이미지 url (구글 서버에 저장된)|
|language|char(100)|시스템 전체 언어 (디폴트 'ko-KR')|
|language_stt|char(100)|STT 설정 언어 (디폴트 'ko-KR')|

**Directory Table**

|Name  |Type   |Description |
|------|-------|------------|
|id    |integer|pk          |
|user  |integer|fk, user id |
|name  |char(100)|디렉토리 이름     |
|color |integer|디렉토리 색깔 (디폴트 0 → 회색)|

**Note Table**

|Name  |Type   |Description |
|------|-------|------------|
|id    |integer|pk, audio file 이름으로 사용 (id.webm)|
|user  |integer|fk, user id |
|directory|integer(NULL)|fk, directory id|
|title |char(200)|note 제목     |
|created_at|date/time|생성 날짜       |
|updated_at|date/time|수정 날짜       |
|deleted_at|date/time|삭제 날짜       |
|content|text   |사용자가 작성한 최종 회의록|
|is_trash|bool   |휴지통에 있는지 true / false|
|edit_user|integer(NULL)|편집 중인 user id|

**Audio Table**

|Name  |Type   |Description |
|------|-------|------------|
|id    |integer|pk          |
|note  |integer|fk, note id |
|user  |integer|user id     |
|length|integer|오디오 길이 (초단위)|

**Sentence Table**

|Name  |Type   |Description |
|------|-------|------------|
|id    |integer|pk          |
|index |integer|note 안에서 몇번째 문장인지|
|audio |integer|fk, audio_id|
|user  |integer|fk, user_id |
|started_at|integer|record 안에서 시작 시간 (밀리초단위)|
|ended_at|integer|record 안에서 시작 시간 (밀리초단위)|
|content|text   |실제 문장 내용    |

**Share Table**

|Name  |Type   |Description |
|------|-------|------------|
|id    |integer|pk          |
|note  |integer|fk, note id |
|user  |integer|fk, user id |

## API List

|Index|Method|URI                      |Parameter                                     |Parameter Type|AccessToken|Description                                               |
|-----|------|-------------------------|----------------------------------------------|--------------|-----------|----------------------------------------------------------|
|1    |POST  |/api/token/google        |google_token                                  |form          |           |google token을 이용해서 가입/로그인 → 자체 jwt 토큰 반환                  |
|2    |GET   |/api/profile             |user_id                                       |query         |needed     |user의 이름, 이메일, 프로필 사진 url을 반환                             |
|3    |DELETE|/api/profile             |user_id                                       |form          |needed     |회원 탈퇴                                                     |
|4    |GET   |/api/profile/usage       |user_id                                       |query         |needed     |유저 노트 개수, 오디오 사용량(초 단위), 공유한 노트수, 공유받은 노트수 반환             |
|5    |PUT   |/api/profile/language    |user_id, language                             |form          |needed     |시스템 언어 변경 (디폴트 'ko-KR')                                   |
|6    |PUT   |/api/profile/language/stt|user_id, language                             |form          |needed     |STT 언어 변경 (디폴트 'ko-KR')                                   |
|7    |GET   |/api/profile/language    |user_id                                       |query         |needed     |시스템 언어 반환                                                 |
|8    |GET   |/api/profile/language/stt|user_id                                       |query         |needed     |STT 언어 반환                                                 |
|9    |GET   |/api/list/note/all       |user_id                                       |query         |needed     |user의 모든 note list 반환 (trash 제외)                          |
|10   |GET   |/api/list/note           |directory_id                                  |query         |needed     |user의 특정 directory의 note list 반환 (trash 제외)               |
|11   |GET   |/api/list/note/trash     |user_id                                       |query         |needed     |user의 trash 안의 note list 반환                               |
|12   |GET   |/api/list/note/shared    |user_id                                       |query         |needed     |user에게 공유된 다른사람의 note list 반환 (trash 제외)                  |
|13   |GET   |/api/list/directory      |user_id                                       |query         |needed     |user의 directory list 반환                                   |
|14   |GET   |/api/list/user/shared    |note_id                                       |query         |needed     |현재 note를 공유하고 있는 user list 반환 (주인 포함)                     |
|15   |POST  |/api/directory           |user_id                                       |form          |needed     |directory 추가                                              |
|16   |PUT   |/api/directory           |directory_id, name                            |form          |needed     |directory 이름 변경                                           |
|17   |DELETE|/api/directory           |directory_id                                  |form          |needed     |directory 삭제 / directory만 삭제                              |
|18   |PUT   |/api/directory/color     |directory_id, color                           |form          |needed     |directory 색깔 변경 (0 이상 정수 사용하고 싶은 범위)                      |
|19   |PUT   |/api/directory/trash     |directory_id                                  |form          |needed     |directory 안의 모든 note들 trash로 (directory → NULL)           |
|20   |POST  |/api/note                |user_id                                       |form          |needed     |새로운 note 생성                                               |
|21   |GET   |/api/note                |note_id                                       |query         |needed     |note의 info 가져오기                                           |
|22   |PUT   |/api/note                |note_id, title, content                       |form          |needed     |title, content, started_at, ended_at 등의 note info를 저장     |
|23   |DELETE|/api/note                |note_id                                       |form          |needed     |note 영구삭제                                                 |
|24   |POST  |/api/note/audio          |note_id, length, FILE['audio_data']           |form          |needed     |녹음된 audio data를 s3에 저장                                    |
|25   |GET   |/api/note/audio          |audio_id                                      |query         |needed     |audio data의 s3 url 반환 (접근 제한시간 → 1시간)                     |
|26   |PUT   |/api/note/directory      |note_id, directory_id                         |form          |needed     |note를 해당 directory로 이동                                    |
|27   |DELETE|/api/note/directory      |note_id                                       |form          |needed     |directory → NULL, 소속된 디렉토리를 제거하고 all note에만 포함되도록         |
|28   |PUT   |/api/note/trash          |note_id                                       |form          |needed     |note를 trash로 (directory → NULL)                           |
|29   |DELETE|/api/note/trash          |note_id                                       |form          |needed     |trash의 note를 복구 (directory → NULL)                        |
|30   |POST  |/api/note/shared         |note_id, email                                |form          |needed     |내 note를 email(상대방)에게 공유                                   |
|31   |DELETE|/api/note/shared         |note_id, user_id                              |form          |needed     |내가(user_id) 공유받은 노트를 공유 취소                                |
|32   |DELETE|/api/note/shared/master  |note_id, user_id                              |form          |needed     |내가 공유한 노트(note_id)를 상대방(user_id)에게서 공유 취소                 |
|33   |POST  |/api/note/sentence       |index, audio_id, started_at, ended_at, content|form          |needed     |sentence info를 저장                                         |
|34   |GET   |/api/note/sentence       |sentence_id                                   |query         |needed     |sentence info를 반환                                         |
|35   |PUT   |/api/note/sentence       |sentence_id, content                          |form          |needed     |sentence content를 수정                                      |
|36   |DELETE|/api/note/sentence       |sentence_id                                   |form          |needed     |sentence 삭제                                               |
|37   |PUT   |/api/note/edited         |user_id, note_id                              |form          |needed     |note를 편집 상태로 변경                                           |
|38   |DELETE|/api/note/edited         |user_id, note_id                              |form          |needed     |note를 다시 편집이 아닌 상태로 변경                                    |
|39   |GET   |/api/note/edited         |note_id                                       |query         |needed     |현재 누가 편집중인지 반환 (없으면 edit_user_id = 'None')                |
|40   |GET   |/api/search/title        |user_id, query                                |query         |needed     |title안에 해당 word가 포함된 note들 리스트 반환                         |
|41   |GET   |/api/search/content      |user_id, query                                |query         |needed     |content안에 해당 word가 포함된 note들 리스트 반환                       |
|42   |GET   |/api/search/sentence     |user_id, query                                |query         |needed     |sentence안에 해당 word가 포함된 note들 리스트 반환                      |
|43   |GET   |/api/search/note/sentence|note_id, query                                |query         |needed     |note 안에서 word가 들어간 sentence 검색                            |
|44   |GET   |/api/search/user         |query                                         |query         |           |query 문자열로 시작하는 유저 검색 (최대5개)                              |
|45   |POST  |/api/contact             |user_id, title, content                       |form          |needed     |유저의 문의사항을 서버에 file로 저장, lisnhelp@gmail.com 으로 같은내용의 메일도 보냄|

**return #1**
```
{
	user_id,
	access_token
}
```
**return #2**
```
{
	user_name,
	user_email,
	user_picture_url,
	user_language,
	user_language_stt
}
```
**return #3, 5, 6, 16, 17, 18, 19, 22, 23, 26, 27, 28, 29, 30, 31, 32, 35, 36, 37, 38, 45**
```
{
}
```
**return #4**
```
{
	user_numb_of_notes,
	user_audio_usage,
	user_num_of_shared,
	user_num_of_sharing
}
```
**return #7**
```
{
	user_language
}
```
**return #8**
```
{
	user_language_stt
}
```
**return #9, 10, 12, 40, 41, 42**
```
{
	notes:
		[
			{
				user_email,
				note_id,
				title,
				created_at,
				updated_at,
				summary,
				color,
				is_shared,
				num_of_share
			}
		]
}
```
**return #11**
```
{
	notes:
		[
			{
				user_email,
				note_id,
				title,
				created_at,
				updated_at,
				deleted_at,
				summary,
				color,
				is_shared,
				num_of_share
			}
		]
}
```
**return #13**
```
{
	directories:
		[
			{
				directory_id,
				name,
				color
			}
		]
}
```
**return #14**
```
{
	users:
		[
			user_id,
			user_name,
			user_email,
			user_picture_url,
			is_master
		]
}
```
**return #15**
```
{
	directory_id
}
```
**return #20**
```
{
	note_id
}
```
**return #21**
```
{
	user_id,
	note_id,
    directory_id,
	title,
	content,
	created_at,
	updated_at,
	audios:
		[
			{
				audio_id,
				sentences:
					[
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
**return #24**
```
{
	audio_id
}
```
**return #25**
```
{
	audio_url
}
```
**return #33**
```
{
	sentence_id
}
```
**return #34**
```
{
	audio_id,
	index,
	started_at,
	ended_at,
	content
}
```
**return #39**
```
{
	edit_user_id,
	edit_user_name,
	edit_user_email
}
```
**return #43**
```
{
	sentences:
		[
			{
				sentence_id,
				started_at,
				ended_at,
				content
			}
		]
}
```
**return #44**
```
{
	users:
		[
			{
				user_id,
				user_name,
				user_email,
				user_picture_url
			}
		]
}
```

## API response status code

| Status | Description |
| ------ | ------ |
| 200 | 응답 성공 (201 이외) |
| 201 | POST 요청으로 리소스 생성에 성공했을 경우 |
| 400 | 부적절한 요청 (존재하지 않는 API, 존재하지 않는 리소스, 다른 유저의 리소스에 접근, 리소스 생성/수정/삭제 실패, 기타등등) |
| 401 | 로그인하지 않은 유저가, 로그인했을 때 요청가능한 리소스를 요청하는 경우 |
| 405 | 요청한 리소스에 불가능한 Method일 경우 |
| 500 | 서버에 내부문제가 있는 경우 |