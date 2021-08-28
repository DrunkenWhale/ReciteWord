# ReciteWord  API


  
> 请以表单格式提交数据 (如果想用json也行 请和我说一下)

  
------------------------  
## 用户

### 获取验证码

- url : http://81.68.100.77:7777/auth/identify

- method: POST

| 参数名|参数类型  |说明    |
|------|------- |-------|
|mailbox| String| 用户邮箱 |

- 获取邮箱后 服务端会向用户发送邮件 用户需使用邮件中的验证码进行注册
- 验证码会在五分钟后过期
- 发送最好有间隔，当然，过于频繁的请求会被拒绝


#### 返回

| 参数名|参数类型  |说明    |
|------|------- |-------|
|status|boolean| 状态 1代表获取成功 0代表失败 |
|message|String| (响应的详细信息)|


返回示例

```json

{
     "status": 1,
     "message": "Succeed/InvalidArgument(请求参数错误)/FrequentSubmission(请求验证码过于频繁)",
     "data": {}
}

```

### 注册

  
- url : http://81.68.100.77:7777/auth/register 

- method: POST
    
#### 提交


| 参数名|参数类型  |说明    |
|------|------- |-------|
|mailbox| String   | 用户邮箱 |
|user_name|String  | 用户名(请不要太长)|
|password|String| 用户密码（也请不要太长）|
|education|int| 用户学习层次|
|identify_code|int| 用户输入的验证码|

- 0 小学
- 1 初中
- 2 高中
- 3 大学及以上

> 4个参数均不可为空

#### 返回

| 参数名|参数类型  |说明    |
|------|------- |-------|
|status|boolean| 状态 1代表注册成功 0代表失败 |
|message|String| (响应的详细信息)|



返回示例

```json

{
     "status": 1,
     "message": "Succeed/UserExist(用户已存在)/WrongIdentifyCode(验证码错误)/ExceedTimeLimit(验证码过期)/InvalidArgument(参数错误)",
     "data": {}
}

```  
  
-----------------------------------
  
### 登陆

- url : http://81.68.100.77:7777/auth

- method: POST

#### 提交


| 参数名|参数类型  |说明    |
|------|------- |-------|
|mailbox| String   | 用户邮箱 |
|password|String| 用户密码（请不要太长）|

> 同上 不可为空

#### 返回

| 参数名|参数类型  |说明    |
|------|------- |-------|
|status|boolean| 状态 1代表登陆成功 0代表失败 |
|message|String| (响应的详细信息)|
|token|String| 请在请求时将该参数置于请求头中|

返回示例

```json

{
     "status": 1,
     "message": "Succeed/InvalidArgument(请求参数错误)/PasswordWrong(用户邮箱与密码不匹配)",
     "token": "我是字符串~"
}

```



-----------------------------------
  
### 获取用户信息

- url : http://81.68.100.77:7777/auth

- method: GET

#### 提交

> 请携带token

| 参数名|参数类型  |说明    |
|------|------- |-------|
|这里| 不需要参数   | 有token就行 |




#### 返回

| 参数名|参数类型  |说明    |
|------|------- |-------|
|status|boolean| 状态 1代表获取成功 0代表失败 |
|message|String| (响应的详细信息)|
|data|对象|大概是要序列化？但是我真的没试过这个 不知道叫什么诶...|


返回示例

```json

{
     "status": 1,
     "message": "Succeed",
     "data": {
            "mailbox": "114514@1919810.com,",
            "name": "Pigeon",
            "education": 3,
            "learned_words_number": 7
        }
}

```



-----------------------------------
  
### 修改用户信息

- url : http://81.68.100.77:7777/auth

- method: PUT

#### 提交

- 请求时需要携带token

| 参数名|参数类型  |说明    |
|------|------- |-------|
|password|String| 用户密码(当前)|
|new_password|String| 用户密码(修改后)(可空置)|
|user_name|String| 用户名称(修改后)(可空置)|
|education|int| 用户的等级(用于调整单词难度)(可空置)|

#### 返回

| 参数名|参数类型  |说明    |
|------|------- |-------|
|status|boolean| 状态 1代表登陆成功 0代表失败 |
|message|String| (响应的详细信息)|
|data|None| 空的 但是只有两个不好看|

返回示例

```json

{
     "status": 1,
     "message": "Succeed",
     "data": {}
}

```



## 单词书

-----------------------------------
  
### 获取单词书的书名列表

- url : http://81.68.100.77:7777/book/dir

- method: GET

#### 提交

- 请求时需要携带token(Token放在headers里)

| 参数名|参数类型  |说明    |
|------|------- |-------|
|要     |    毛线|    参数|

#### 返回

| 参数名|参数类型  |说明    |
|------|------- |-------|
|status|boolean| 状态 1代表登陆成功 0代表失败 |
|message|String| (响应的详细信息)|
|data|List<String>| 其中包含了对应层级的书名|

ps:
 - 获取到的书籍名与用户的等级匹配

返回示例

```json

{
     "status": 1,
     "message": "Succeed",
     "data": [
        "设计模式",
        "HADOOP+SPARK大数据技术",
        "算法Algorithm(第三版)"
    ]
}

```


-----------------------------------
  
### 获取某本单词书的所有单词

- url : http://81.68.100.77:7777/book/word

- method: GET

#### 提交

- 请求时需要携带token(Token放在headers里)

| 参数名|参数类型  |说明   |
|------|------- |-------|
|  book|  String|    参数|

#### 返回

| 参数名|参数类型  |说明   |
|------|------- |-------|
|status|boolean| 状态 1代表登陆成功 0代表失败 |
|message|String| (响应的详细信息)|
|data|List<Object>| 对象列表|

ps:
 - 其中 每一个对象的属性都相同..
 
 (~~写了两天都搞不定它的格式和编码..难顶~~ )
  (为了确保数据完整,所以就没有对数据做什么太大调整,只去除了一点无用的属性)
  
 因为编码的问题 存数据库得扔掉大部分数据
 所以我直接读取文件返回数据
 这个接口返回的数据放在data中，*量挺大*
 响应也会比较久
 
返回示例

```json

{
     "status": 1,
     "message": "Succeed/InvalidArgument",
     "data": [
         {
            "content": {
                "phone": "ri'fju:z, ri:-",
                "phrase": {
                    "desc": "短语",
                    "phrases": [
                        {
                            "pCn": "城市垃圾",
                            "pContent": "municipal refuse"
                        },
                        {
                            "pCn": "拒绝做某事",
                            "pContent": "refuse to do"
                        },
                        {
                            "pCn": "垃圾处理；废物处理",
                            "pContent": "refuse treatment"
                        },
                        {
                            "pCn": "垃圾收集",
                            "pContent": "refuse collection"
                        },
                        {
                            "pCn": "废物处理",
                            "pContent": "refuse disposal"
                        },
                        {
                            "pCn": "煤矸石",
                            "pContent": "coal refuse"
                        },
                        {
                            "pCn": "n. 垃圾场",
                            "pContent": "refuse dump"
                        },
                        {
                            "pCn": "垃圾转运站；废物转运站",
                            "pContent": "refuse transfer station"
                        }
                    ]
                },
                "relWord": {
                    "desc": "同根",
                    "rels": [
                        {
                            "pos": "n",
                            "words": [
                                {
                                    "hwd": "refusal",
                                    "tran": "拒绝；优先取舍权；推却；取舍权"
                                }
                            ]
                        }
                    ]
                },
                "sentence": {
                    "desc": "例句",
                    "sentences": [
                        {
                            "sCn": "她叫他走，但他不肯。",
                            "sContent": "She asked him to leave, but he refused."
                        },
                        {
                            "sCn": "他愿意给那么多钱，我怎么可能拒绝呢？",
                            "sContent": "When he offered all that money, I could hardly refuse (= could not refuse ) , could I?"
                        }
                    ]
                },
                "trans": [
                    {
                        "descCn": "中释",
                        "descOther": "英释",
                        "pos": "v",
                        "tranCn": "拒绝",
                        "tranOther": "to say firmly that you will not do something that someone has asked you to do"
                    }
                ]
            },
            "headWord": "refuse",
            "wordId": "CET4luan_2_1",
            "wordRank": 1
        }
    ]
}

```


-----------------------------------
  
### 获取某个用户所有的单词书

- url : http://81.68.100.77:7777/book/

- method: GET

#### 提交

- 请求时需要携带token(Token放在headers里)

| 参数名|参数类型  |说明    |
|------|------- |-------|
|要     |    毛线|    参数|

#### 返回

| 参数名|参数类型  |说明    |
|------|------- |-------|
|status|boolean| 状态 1代表登陆成功 0代表失败 |
|message|String| (响应的详细信息)|
|data|List<String>| 其中包含了该用户拥有的所有书的书名|


返回示例

```json

{
    "data": [
        "CET4_2"
    ],
    "message": "Succeed/InvalidArgument(书名错误/参数错误)",
    "status": 0
}

```

-----------------------------------
  
### 为某一用户添加一本单词书

- url : http://81.68.100.77:7777/book

- method: POST

#### 提交

- 请求时需要携带token(Token放在headers里)

| 参数名|参数类型  |说明    |
|------|------- |-------|
|book  |   String|    书名(从之前的`/book/dir`可以获得)|

#### 返回

| 参数名|参数类型  |说明    |
|------|------- |-------|
|status|boolean| 状态 1代表登陆成功 0代表失败 |
|message|String| (响应的详细信息)|
|data|null| 无|


返回示例

```json

{
     "status": 1,
     "message": "Succeed/InvalidArgument",
     "data": {}
}

```


-----------------------------------
  
### 获得某一用户最新添加的单词书的名字

- url : http://81.68.100.77:7777/book/recent

- method: GET

#### 提交

- 请求时需要携带token(Token放在headers里)

| 参数名|参数类型  |说明    |
|------|------- |-------|
|----?--|?-----|--?------|

#### 返回

| 参数名|参数类型  |说明    |
|------|------- |-------|
|status|boolean| 状态 1代表登陆成功 0代表失败 |
|message|String| (响应的详细信息)|
|data|String| 最新添加的那本书 |


返回示例

```json

{
     "status": 1,
     "message": "Succeed/InvalidArgument",
     "data": "我是书名"
}

```




## 单词

-----------------------------------
  
### 为某一用户更新学习记录

- url : http://81.68.100.77:7777/word

- method: POST

#### 提交

- 请求时需要携带token(Token放在headers里)

| 参数名|参数类型  |说明    |
|------|------- |-------|
|book  |  String|书名(从之前的`/book/dir`可以获得)|
|size|int |该用户这本书的单词学习数量|
    

#### 返回

| 参数名|参数类型  |说明    |
|------|------- |-------|
|status|boolean| 状态 1代表登陆成功 0代表失败 |
|message|String| (响应的详细信息)|
|data|null | null|


返回示例

```json

{
     "status": 1,
     "message": "Succeed/InvalidArgument",
     "data": {}
}

```



-----------------------------------
  
### 获得某一用户的学习记录

- url : http://81.68.100.77:7777/word/

- method: GET

#### 提交

- 请求时需要携带token(Token放在headers里)

| 参数名|参数类型  |说明    |
|------|------- |-------|
|book  |  String|书名(从之前的`/book/dir`可以获得)|
|all|int |缺省或为0情况下默认需要book参数 获取该用户某一单词书的学习记录,为1的情况下不需要book参数 会返回用户所有的学习记录|


#### 返回

| 参数名|参数类型  |说明    |
|------|------- |-------|
|status|boolean| 状态 1代表登陆成功 0代表失败 |
|message|String| (响应的详细信息)|
|data|Map<String,?>| 学习记录 |


返回示例

```json
{
     "status": 1,
     "message": "Succeed/InvalidArgument",
     "data": {
          "sum": 114514, 
          "record": {
                 "奇怪的书": 1919810,
                 "比上面还奇怪的书": 222, 
           }   
      }
}

```

- "sum" 对应的是已学习的单词数量的总和
- "record" 中的键值对为 "某本书的书名"："该用户在这本书上学了多少单词 "