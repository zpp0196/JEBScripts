# JebScripts

## JEB3DeobscureClass.py

与上一代 [JEB2DeobscureClass.py](https://github.com/S3cuRiTy-Er1C/JebScripts/blob/master/JEB2DeobscureClass.py) 的区别：

* 支持 `.source "*.kt"`
* 过滤 `.source "ProGuard"` 和 `.source "SourceFile"`
* 解决同一包名下 `.source` 属性重复导致类名重复而无法交叉引用的问题