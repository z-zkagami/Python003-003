# 学习笔记
### get()/getall()和extract()/extract_first()
前者是新版本的方法，前者取不到值则返回None，后者是老版本的方法，后者取不到则raise一个错误。官方推荐使用新方法。

scrapy.selector.unifield.SelectorList对象：

* getall() == extract()

* get() == extract_first()

scrapy.selector.unifield.Selector对象：

* getall() == extract()

* get() != extract_first()

对于SelectorList，getall()/extract()返回的是一个list，包含了多个string，get()/extract_first()返回一个string，是list中的第一个元素

对于Selector，并不能使用extract_first()

### middlewares添加流程
首先在middlewares文件中添加相应的class，添加完成后到setting.py中DOWNLOADER_MIDDLEWARES字段中按照格式添加`PROJECT_NAME.middlewares.CLASS_NAME`

### 遇到的问题
pipeline写入mysql的时候提示Keyerror，不清楚是哪里有问题求指点。