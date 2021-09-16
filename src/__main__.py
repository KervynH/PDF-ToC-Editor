import os
import fitz
import click
from src.TocTxt import TocTxt


@click.group()
def main():
    pass


def save_safely(pdf, output_file):
    '''
    fitz.save() 在覆盖已有文件时可能会有奇怪的问题，所以自己写了一个可以安全保存的函数
    - pdf -> fitz.Document() 对象
    - output_file -> 要保存的文件名
    '''
    if pdf.name == output_file:
        # 引入一个替身文件 ghost，避免文件冲突的问题
        for i in range(100000000):
            # 确保 ghost 的文件名是不存在的
            ghost = output_file[:-4] + '-ghost-%d.pdf' % i
            if not os.path.exists(ghost):
                break
        pdf.save(ghost)
        pdf.close()
        # 然后再用 ghost 文件替换掉 output_file
        if os.path.exists(output_file):
            os.remove(output_file)
        os.rename(ghost, output_file)
    else:
        pdf.save(output_file)
        pdf.close()


@main.command()
@click.argument('pdf_file', type=click.Path(exists=True))
@click.argument('toc_file', type=click.Path(exists=True))
@click.option('--offset', '-s', default=0, help='offset == pdf pagenum - actual book pagenum; offset should be non-negative; default=0.')
@click.option('--output', '-o', help='custom the output filename; by default, the output file will cover the input file.')
@click.option('--collapse_level', '-c', default=1, help='collapse_level = n means collapsing all bookmarks whose level >= n; and collapse_level = 0 means expanding all bookmarks; default=1.')
def add(pdf_file, toc_file, offset=0, output=None, collapse_level=1):
    '''
    Add bookmarks to a PDF file.
    '''
    if output is None:
        output = pdf_file
    pdf = fitz.open(pdf_file)
    toc_txt = TocTxt.read_from_txt(toc_file)
    toc_txt.write_to_pdf(pdf, collapse_level, offset)
    save_safely(pdf, output)


@main.command()
@click.argument('pdf_file', type=click.Path(exists=True))
@click.option('--output', '-o', help='custom the output filename; by default, the output file will cover the input file.')
def clear(pdf_file, output):
    '''
    Delete all bookmarks in a PDF file.
    '''
    if output is None:
        output = pdf_file
    pdf = fitz.open(pdf_file)
    pdf.setToC([])
    save_safely(pdf, output)


@main.command()
@click.argument('pdf_file', type=click.Path(exists=True))
@click.option('--output', '-o', help='custom the output txt filename; by default, the output filename will be [input-pdf]-ToC.txt.')
def get(pdf_file, output):
    '''
    Get bookmarks in a PDF file and save them as a ToC file.
    '''
    if output is None:
        output = pdf_file[:-4] + '-ToC.txt'
    pdf = fitz.open(pdf_file)
    toc_txt = TocTxt.read_from_pdf(pdf)
    with open(output, 'w', encoding='utf8') as f:
        f.write(toc_txt.get_text())


@main.command()
@click.argument("pdf_file", type=click.Path(exists=True))
@click.option("--page_range", '-r', default='1-')
@click.option('--plus', '-p', default=1, help='the number to be plus to the pagenums, default=1')
@click.option('--minus', '-m', default=0, help='the number to be minus from the pagenums, default=0.')
def shift(pdf_file, page_range, plus=1, minus=0):
    '''
    Shift bookmarks within a given page range, i.e. plus or minus their pagenums simultaneously by a number. This will be quite useful if some pages (usually blank pages) in an e-book PDF is missing.

    - PAGE_RANGE: given by format like '2-40'; or use '20-' to mean from page 20 to the end of the PDF. 
    '''
    pdf = fitz.open(pdf_file)
    offset = plus - minus
    try:
        start, end = page_range.strip().split('-')
        start = int(start)
        if end != '':
            end = int(end)
        else:
            end = pdf.page_count
    except:
        click.echo("PAGE_RANGE format is not correct! Type \"toc shift --help\" for more info.")
    toc_txt = TocTxt.read_from_pdf(pdf)
    bookmark_list = toc_txt.get_bookmark_list()
    new_text = ''
    for bookmark in bookmark_list:
        if start <= bookmark.pagenum <= end:
            bookmark.pagenum += offset
        new_text += bookmark.as_text() + "\n"
    new_toc_txt = TocTxt(new_text)
    new_toc_txt.write_to_pdf(pdf, collapse_level=1)
    save_safely(pdf, pdf_file)


@main.command()
@click.argument('file', type=click.Path(exists=True))
def check(file):
    '''
    Check whether bookmark pagenum is increasing.

    - FILE: .pdf file or toc file (.txt)
    '''
    if file.strip().endswith(".txt"):
        toc_txt = TocTxt.read_from_txt(file)
    elif file.strip().endswith('.pdf'):
        pdf = fitz.open(file)
        toc_txt = TocTxt.read_from_pdf(pdf)
    else:
        click.echo('Error! The input file should be .pdf or .txt!')

    wrong_bookmarks = toc_txt.check_mono()
    if wrong_bookmarks == []:
        click.echo('All bookmarks are arranged in the order of increasing pagenum!')
    else:
        click.echo('The following bookmarks might be wrong, because their pagenum are strictly greater than some latter bookmark.')
        for bookmark in wrong_bookmarks:
            click.echo(click.style('  ' + str(bookmark), fg='red'))


@main.command()
@click.argument('pdf_file', type=click.Path(exists=True))
@click.option('--collapse_level', '-c', help='collapse_level = n means collapsing all bookmarks whose level >= n; and collapse_level = 0 means expanding all bookmarks; by default, collapse_level = 1.')
def collapse(pdf_file, collapse_level):
    '''
    Modify collapse level of the bookmarks.
    '''
    pdf = fitz.open(pdf_file)
    toc_txt = TocTxt.read_from_pdf(pdf)
    toc_txt.write_to_pdf(pdf, collapse_level)
    save_safely(pdf, pdf_file)


if __name__ == '__main__':
    main()