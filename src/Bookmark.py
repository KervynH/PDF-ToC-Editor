import re


class Bookmark:
    '''
    用于处理单个书签的信息

    核心属性: depth, title, pagenum
    '''
    def __init__(self, depth, title, pagenum):
        '''
        depth: 书签缩进层级, 可以是 1,2,3 ...
        title: 书签标题
        pagenum: 书签所在的页码
        '''
        self.depth = depth
        self.title = title
        self.pagenum = pagenum

    def __str__(self):
        return str(self.as_list())

    def __repr__(self):
        return str(self.as_list())

    @staticmethod
    def parse_text(text):
        '''
        功能: 从一行文本创建 Bookmark 对象
        输入: text: 目录txt中的一行文本
        输出: 对应的 Bookmark 对象; 如果这一行文本不包含书签信息, 就返回 None
        '''
        # 确定缩进层次
        text = text.replace('    ', '\t')    # 把四个空格转换成tab, 便于计数
        m = re.match(r'^\t*', text)    # 匹配开头的制表符
        if m is None:
            depth = 0
        else:
            start, end = m.span()
            depth = end - start + 1

        # 确定页码和书签标题
        text = text[end:].rstrip()    # 把开头的tab和结尾的换行符和空格删掉
        lst = text.split()
        if lst == []:
            return None   # 这时书签标题是空字符串, 直接返回 None
        else:
            s = lst[-1]
            # 匹配每行末尾的页码, 它可以是负整数
            if re.match(r'-?\d+', s) is None:
                return None    # 没有指定页码, 直接忽略
            else:
                page = int(s)
                title = text[:-len(s)].strip()
                return Bookmark(depth, title, page)

    def as_list(self):
        '''
        fitz 是用列表表示一个书签的, 这个方法就返回 Bookmark 对象对应的列表格式
        '''
        return [self.depth, self.title, self.pagenum]

    def as_text(self):
        '''
        用文本格式表示书签
        '''
        return (self.depth - 1) * '\t' + self.title + '\t' + str(self.pagenum)
