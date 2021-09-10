from src.Bookmark import Bookmark


class TocTxt:
    '''
    用于处理目录 txt 文件
    '''
    def __init__(self, text):
        self.__text = text

    def get_text(self):
        return self.__text

    @staticmethod
    def read_from_txt(txt_file):
        '''
        从 txt 文件中读取文本并创建 TocTxt 对象
        '''
        with open(txt_file, 'r', encoding='utf8') as f:
            text = f.read()
        return TocTxt(text)

    @staticmethod
    def read_from_pdf(pdf):
        '''
        从 pdf 中读取书签信息, 并输出为 TocTxt 对象
        - pdf -> fitz.Document 对象
        '''
        fitz_toc = pdf.getToC()    # fitz 的书签格式是列表
        text = ''
        for t in fitz_toc:
            # t = [depth, title, pagenum]
            text += (t[0] - 1) * '\t' + str(t[1]) + '\t' + str(t[2]) + '\n'
        return TocTxt(text)

    def get_bookmark_list(self):
        bookmark_list = []
        lines = self.__text.split('\n')    # 分行
        for line in lines:
            bookmark = Bookmark.parse_text(line)
            if bookmark is None:
                pass    # 忽略不包含书签信息的行
            else:
                bookmark_list.append(bookmark)
        return bookmark_list

    # def get_max_depth(self):
    #     bookmark_list = self.get_bookmark_list()
    #     max_depth = 0
    #     for bookmark in bookmark_list:
    #         if bookmark.depth > max_depth:
    #             max_depth = bookmark.depth
    #     return max_depth

    def write_to_pdf(self, pdf, collapse_level, offset=0,):
        '''
        把 TocTxt 中的书签信息写入 pdf 文件
        - pdf -> fitz.Document 对象
        - offset -> 偏移量
        - collapse_level -> pdf 中书签展开的层级
        '''
        bookmark_list = self.get_bookmark_list()
        fitz_toc = []   # fitz 格式的书签列表
        for bookmark in bookmark_list:
            bookmark.pagenum += offset
            fitz_toc.append(bookmark.as_list()) 
        pdf.setToC(fitz_toc, collapse=collapse_level)

    def check_mono(self):
        '''
        检查书签的单调性，并且返回逆序的书签
        '''
        bookmark_list = self.get_bookmark_list()
        num_bookmarks = len(bookmark_list)
        wrong_bookmarks = []
        for i in range(0, num_bookmarks-1):
            if bookmark_list[i].pagenum > bookmark_list[i+1].pagenum:
                wrong_bookmarks.append(bookmark_list[i])
        return wrong_bookmarks
        