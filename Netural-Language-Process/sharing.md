# 语音识别API调研

开始准备用讯飞的API，可是讯飞的网站怎么也登不上去，就换成了效果相近的百度语音识别API

## 百度语音识别API

百度语音识别API除了Android和ios端提供离线语音识别API，其余的平台皆为在线的方式提供服务

### 简介
>百度语音识别通过 REST API 的方式给开发者提供一个通用的 HTTP 接口。   
>上传需要完整的录音文件，录音文件时长不超过60s。  
 
### 语种
>普通话、英语、粤语、四川话  
  
### 语音格式
>格式支持：pcm（不压缩）、wav（不压缩，pcm编码）、amr（压缩格式）。  
>原始 PCM 的录音参数必须符合 8k/16k 采样率、16bit 位深、单声道，  
>支持的格式有：pcm（不压缩）、wav（不压缩，pcm编码）、amr（压缩格式）。  
>推荐pcm 采样率 ：16000 固定值。 编码：16bit 位深的单声道。  

注：百度服务端会将非pcm格式，转为pcm格式，因此使用wav、amr会有额外的转换耗时。

### 调用方式（以Python为例）

#### ASR REST API

[REST API 文档](http://ai.baidu.com/docs#/ASR-API/top)

示例代码  

```python
import sys
import json
import time

IS_PY3 = sys.version_info.major == 3

if IS_PY3:
    from urllib.request import urlopen
    from urllib.request import Request
    from urllib.error import URLError
    from urllib.parse import urlencode
    timer = time.perf_counter
else:
    import urllib2
    from urllib2 import urlopen
    from urllib2 import Request
    from urllib2 import URLError
    from urllib import urlencode
    if sys.platform == "win32":
        timer = time.clock
    else:
        # On most other platforms the best timer is time.time()
        timer = time.time

API_KEY = '4E1BG9lTnlSeIf1NQFlrSq6h'
SECRET_KEY = '544ca4657ba8002e3dea3ac2f5fdd241'

# 需要识别的文件
AUDIO_FILE = './pcm/16k.pcm' # 只支持 pcm/wav/amr
# 文件格式
FORMAT = AUDIO_FILE[-3:];  # 文件后缀只支持 pcm/wav/amr

# 根据文档填写PID，选择语言及识别模型
DEV_PID = 1536;  # 1537 表示识别普通话，使用输入法模型。1536表示识别普通话，使用搜索模型

CUID = '123456PYTHON';
# 采样率
RATE = 16000;  # 固定值

ASR_URL = 'http://vop.baidu.com/server_api'


class DemoError(Exception):
    pass

"""  TOKEN start """

TOKEN_URL = 'http://openapi.baidu.com/oauth/2.0/token'
SCOPE = 'audio_voice_assistant_get'  # 有此scope表示有asr能力，没有请在网页里勾选


def fetch_token():
    params = {'grant_type': 'client_credentials',
              'client_id': API_KEY,
              'client_secret': SECRET_KEY}
    post_data = urlencode(params)
    if (IS_PY3):
        post_data = post_data.encode('utf-8')
    req = Request(TOKEN_URL, post_data)
    try:
        f = urlopen(req)
        result_str = f.read()
    except URLError as err:
        print('token http response http code : ' + str(err.code))
        result_str = err.read()
    if (IS_PY3):
        result_str = result_str.decode()

    print(result_str)
    result = json.loads(result_str)
    print(result)
    if ('access_token' in result.keys() and 'scope' in result.keys()):
        if not SCOPE in result['scope'].split(' '):
            raise DemoError('scope is not correct')
        print('SUCCESS WITH TOKEN: %s ; EXPIRES IN SECONDS: %s' % (result['access_token'], result['expires_in']))
        return result['access_token']
    else:
        raise DemoError('MAYBE API_KEY or SECRET_KEY not correct: access_token or scope not found in token response')


"""  TOKEN end """

if __name__ == '__main__':
    token = fetch_token()

    """
    httpHandler = urllib2.HTTPHandler(debuglevel=1)
    opener = urllib2.build_opener(httpHandler)
    urllib2.install_opener(opener)
    """

    speech_data = []
    with open(AUDIO_FILE, 'rb') as speech_file:
        speech_data = speech_file.read()
    length = len(speech_data)
    if length == 0:
        raise DemoError('file %s length read 0 bytes' % AUDIO_FILE)

    params = {'cuid': CUID, 'token': token, 'dev_pid': DEV_PID}
    params_query = urlencode(params);

    headers = {
        'Content-Type': 'audio/' + FORMAT + '; rate=' + str(RATE),
        'Content-Length': length
    }

    # print post_data
    req = Request(ASR_URL + "?" + params_query, speech_data, headers)
    try:
        begin =timer()
        f = urlopen(req)
        result_str = f.read()
        print ("Request time cost %f" %(timer() - begin))
    except  URLError as err:
        print('asr http response http code : ' + str(err.code))
        result_str = err.read()

    if (IS_PY3):
        result_str = str(result_str, 'utf-8')
    print(result_str)
    with open("result.txt", "w") as of:
        of.write(result_str)

```
#### Python SDK

[Python SDK文档](http://ai.baidu.com/docs#/ASR-Online-Python-SDK/top)  

首先安装Python SDK

```shell
pip install baidu-aip
```

登陆[百度云控制台](https://console.bce.baidu.com/?_=1540537657438&fromai=1#/aip/overview)   
创建一个应用，然后获得AppID、APIKey、SecretKey（这些调用目前都是免费的），然后输入   
```python
from aip import AipSpeech

""" 你的 APPID AK SK """
""" 都为字符串 """
APP_ID = '你的 App ID'
API_KEY = '你的 Api Key'
SECRET_KEY = '你的 Secret Key'

client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
```
随后直接调用函数就ok了  
```python
# 读取文件
def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

# 识别本地文件
client.asr(get_file_content('文件名'), 'pcm', 16000, {
    'dev_pid': 1536,
})
```

    

## 关于文件格式转换  

有一个文件格式转换的小工具叫ffmpeg（[官网地址](http://ffmpeg.org/)）   
调用方法：   

wav 文件转 16k 16bits 位深的单声道pcm文件   
```s
ffmpeg -y  -i 16k.wav  -acodec pcm_s16le -f s16le -ac 1 -ar 16000 16k.pcm 
```  
44100 采样率 单声道 16bts pcm 文件转 16000采样率 16bits 位深的单声道pcm文件   
```s
ffmpeg -y -f s16le -ac 1 -ar 44100 -i test44.pcm  -acodec pcm_s16le -f s16le -ac 1 -ar 16000 16k.pcm 
```   
mp3 文件转 16K 16bits 位深的单声道 pcm文件   
```s
ffmpeg -y  -i aidemo.mp3  -acodec pcm_s16le -f s16le -ac 1 -ar 16000 16k.pcm 

// -acodec pcm_s16le pcm_s16le 16bits 编码器 
// -f s16le 保存为16bits pcm格式
// -ac 1 单声道
//  -ar 16000  16000采样率
```  