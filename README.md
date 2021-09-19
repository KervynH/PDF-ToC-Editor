# PDF ToC Editor

## 介绍

这是一个基于 PyMuPDF 包的用于处理 PDF 目录的命令行工具。

#### ToC 文件

**ToC 文件**是一种 txt 文件，用于给出 PDF 的书签信息（标题、缩进层级、页码）。其格式大致如下：
```
第一个书签  1
    子书签 1.1  1
        子书签 1.1.1    3
        子书签 1.1.2    7
    子书签 1.2  9
        子书签 1.2.1    10
    子书签 1.3  16
第二个书签  20
    子书签 2.1  25
        子书签 2.1.1    29
        子书签 2.1.2    35
    子书签 2.2  40
```
- 用 tab 或者四个空格表示缩进，用缩进来表示书签的层级
- 页码和书签标题之间用 tab 或者四个空格隔开

作为样例，项目仓库的 `test` 文件夹中的 `toc.txt` 文件就是《Linear_Algebra_Done_Right》这本书的 ToC 文件，`test` 文件夹中也提供了这本书的 PDF 用于测试。（注：这个 PDF 是由 Springer 免费发布的。）

## 安装方法

#### 安装

首先安装 python 依赖库：
```
pip install PyMuPDF click
```

然后在项目根目录中执行
```
pip install -e .
```

然后用
```
toc --help
```
来测试安装是否成功。如果出现了帮助信息就说明安装成功了。

#### 卸载和移动

项目安装好之后，如果文件夹的位置发生移动，那么需要重新执行安装步骤。

如果想要卸载，只需要在项目根目录中运行
```
pip uninstall pdf-toc-cli -y
```
不推荐直接删除项目文件夹，这样子并没有把 `toc` 命令从命令行中删除掉。

## 使用说明

#### 给 PDF 添加目录

```
toc add [PDF文件] [ToC文件] -o [输出文件名，默认覆盖原文件] -s [偏移量，默认为 0] -c [书签折叠层级，默认为 1]
```

- 偏移量 (offset) == PDF页码 - 电子书的实际页码
    - ToC 文件通常是通过 OCR 或者直接复制 PDF 电子书的目录部分而得到的，所以 ToC 文件中的页码通常会和 PDF 的页码有一个偏差，这时就可以通过偏移量参数来调整
    - 例如, `test` 文件夹中给出的 `toc.txt` 是 `Done_Right.pdf` 的 ToC 文件, 对应的 offset 应该是 17.
- 书签折叠层级：控制 PDF 文件打开时书签的展开状态
    - 折叠层级为 0：自动展开所有书签
    - 折叠层级为 n：折叠所有缩进层级大于或等于 n 的书签，其中 n 为正整数
    - 特别地，缩进层级为 1 时会自动折叠所有书签，这也是默认的设置

#### 调整书签折叠层级

```
toc collapse [PDF文件] -c [折叠层级，默认为 1]
```

#### 清除 PDF 的目录

```
toc clear [PDF文件] -o [输出文件名，默认覆盖原文件]
```

#### 检查书签页码是否是递增的

由于 ToC 文件通常通过 OCR 得到，所以有可能会有识别错误的页码。通过检查 PDF 文件的书签是否按照页码递增的顺序进行排列，可以在一定程度上帮助我们发现那些错误的书签。

通过下面的命令，可以检查书签页码是否是递增的：

```
toc check [PDF文件/ToC文件]
```

这个命令可以输出所有产生了逆序的书签标题和页码（产生逆序的意思是比前面某个书签的页码严格大）

#### 提取 PDF 中的目录并存为 ToC 文件

```
toc get [PDF文件] -o [输出的文件名，默认为 "[PDF文件名]-toc.txt"]
```

#### 批量偏移 PDF 书签页码

```
toc shift [PDF文件] [页码范围] -p [增加的页码数，默认为 1] -m [减少的页码数，默认为 0]
```

#### 获取帮助信息

在命令行中通过 `toc --help` 以及 `toc [COMMAND] --help` 可以获取帮助信息
