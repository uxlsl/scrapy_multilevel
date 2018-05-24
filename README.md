## scrapy多级爬取例子!


### 原理



```

item = {'url':'http://127.0.0.1:5000/get?num=1',
  'extra':[
  {'url': 'http://127.0.0.1:5000/get?num=2'},
  {'url': 'http://127.0.0.1:5000/get?num=3', 'extra': [
    {'url': 'http://127.0.0.1:5000/get?num=5',
      'extra': [{'url':'http://127.0.0.1:5000/get?num=6'}]}]},
      {'url': 'http://127.0.0.1:5000/get?num=4'},
  ]}



def walk(lst, levels):
    if lst:
        i = lst.pop(0)
        yield i['url']
        levels[0] += 1
        yield from walk(i.get('extra'), levels)
        levels[0] -= 1
        yield from walk(lst, levels)

```

使用yield 进行跟踪 爬取的url

### 安装环境

```

virtualenv .venv -p python3.6
pip install -r requirements.txt

```

### 实验步骤

```


#1
FLASK_APP=server.py flask run
#2
scrapy crawl z


```

结果

{'body': '123564'}
