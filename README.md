 
### Introduction
```
搜索目录下是否有相同的PNG或JPG图片资源，
比如App工程目录下检查是否有重复的资源图，可有效减小App安装包体积。
```

### Usage

```python
# 不带参数直接运行，在控制台中输入
python3 search_repeat_icons.py

# 带-p和-o参数运行，建议使用这种方法
python3 search_repeat_icons.py -p path -o outfile

# help模式
python3 search_repeat_icons.py -h
```

### Options
```
-p path  		icons根目录
-o outfile		输入结果文件，结果是dict，所以建议输出文件格式为json
```
