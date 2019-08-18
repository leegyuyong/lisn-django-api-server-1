Good Listener Project (SW Maestro)
=====================

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
<br>
<br>


# API를 이용한 클라이언트 시나리오(초본)

---

### 브라우저에 "www.li-sn.io"를 치면

1. GET '/' 으로 index.html 전달받음

---


<br>
## main page

### 'Sign in' 버튼 or 'Sign up' 버튼을 누르면

1. GET '/signin'으로 signin.html 전달받고 Redirect (이때 vue.js는 싱글페이지 방식이므로 어떻게할지 고민)

---


<br>
## sign-in page

### 'Continue with Google Account' 버튼을 누르면

1. 'Social Account' DB에 저장, User DB에도 저장됨 (username, email, first_name, last_name)
2. 결과적으로 GET '/record/mylist/' {user_id} 으로 mylist.html을 전달받고 Redirect

---


<br>
## my-list page

### Sign in 이후

1. GET '/record/mylist' {user_id} 으로 mylist.html을 전달받고 Redirect 해야되는데
2. 이때 mylist.html을 db 참조해서 rendering (vue.js / django template 어떤걸 사용해서 할지 고민)
3. rendering 할때 각 note들의 note_id를 html tag property로 지정

### 이미 생성된 Note를 클릭하면

1. GET '/record/note' {note_id} 으로 note.html을 전달받고 Redirect
2. GET '/record/note/data' {note_id} 으로 왼쪽 text와 오른쪽 record 관련 정보, word 관련 정보 받아오기
3. 받아온 data를 이용해서 왼쪽 markdown editor 초기화 및 rendering
4. 받아온 data를 이용해서 오른쪽 word들 초기화 및 rendering

### 'Create Note' 버튼을 누르면

1. POST '/record/note'으로 새로운 note를 데이터베이스에 생성하고 note_id를 전달받음
2. 전달받은 note_id를 가지고 위의 '이미 생성된 note를 클릭하면' 1번부터 똑같이 수행

### 특정 Note의 'Delete' 버튼을 누르면

1. DELETE '/record/note' {note_id}으로 해당 note 데이터베이스에서 삭제
2. UI 갱신

---

<br>

## record-note page

### 'Save' 버튼을 누르면

1. PUT '/record/note' {note_id}으로 왼쪽 text를 데이터베이스에 갱신
2. 오른쪽 STT결과들은 녹음시에 자동으로 데이터베이스에 저장 됨 (애초에 따로 수정불가)

### 'Record' 버튼을 누르면

1. 현재 note의 마지막 record index 번호 확인 (처음이면 0)
2. 일정 시간단위로 record index를 1씩 증가시키며 API 호출
3. 즉, POST '/record/audio' {note_id, record_index}으로 녹음데이터(blob/webm) 전송

### 'Stop' 버튼을 누르면

1. 현재까지 녹음데이터를 전송
2. 주기적인 API 호출을 중단

### STT결과 뷰어에서 특정 Word를 누르면

1. 해당 word부터 다음 word로 반복하면서 API 호출
2. 첫번째 word의 index를 확인하여 GET '/record/audio/word' {note_id, record_index, word_index}으로 잘린 audio file 받아서 재생
3. 두번째 word부터는 word가 포함된 record index가 이전 word의 record index와 같은지 확인
4. if 같으면, UI 처리만 하고 넘어감 (단어 주변 블록색이 바뀌면서 재생되고 있는게 보이도록)
5. else 다르면, GET '/record/audio' {note_id, record_index}으로 전체 audio file 받아서 재생하고 넘어감
6. 'audio stop' 버튼을 누를 때까지 위와같이 반복