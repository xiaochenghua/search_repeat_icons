
### Introduction
```html
遍历查找指定目录下重复的图标，导出结果到文件中。
```

### Usage

```python
# 不带参数直接运行，在控制台中输入
python3 search_repeat_icons.py

# 带-p和-e参数运行，建议使用这种方法
python3 search_repeat_icons.py -p iconPath -e exportFile

# help模式
python3 search_repeat_icons.py -h
```

### Options
```html
-p iconPath  		icon目录
-o exportFile		导出文件，建议文件格式为json
```

### Export file
```json
result.json
├── count	重复的图片次数
└── icons 	重复的图片数组信息
```

