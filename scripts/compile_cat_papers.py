import csv
import os
from pdb import set_trace as st
from audioop import reverse

class Paper():
    def __init__(self):
        self.title = 'cat'
        self.year = 1900
        self.paper = None
        self.project = None
        self.article = 'SIGGRAPH'
        self.teaser = 'tmp.png'
        self.authors = None
        self.author_urls = None
        self.imgurl = None

    def ParseCSV(self, line):
      line = str(line)
      line_proc = line.replace("'", '').replace('[', '').replace(']','').replace(', ', ',')
      items = line_proc.split(',')

#       for item in items:
#         print(item)
      [self.title, self.year, self.paper, self.project,self.article,ainfo] = items
      if self.project is not None:
        self.imgurl = self.project
      elif self.paper is not None:
        self.imgurl = self.paper
      else:
        print('ERROR: no paper/project')
#       st()
      self.year = int(float(self.year))
      self.title = self.title.replace('$', ',')
      author_records = ainfo.split(';')
      self.authors = []
      self.author_urls = []
      for author_r in author_records:
        pos_id = author_r.find('+')
        author = ''
        url = ''
        if pos_id > 0:
          author = author_r[:pos_id]
          url = author_r[pos_id+1:]
        else:
          author = author_r
#         print('add %s at %s' % (author, url))
        self.authors.append(author)
        self.author_urls.append(url)
      # get teaser name
      author_name = self.authors[0]
      last_name = author_name.split(' ')[-1]
      self.teaser = '%s%d.jpg' % (last_name, self.year)


    def __str__(self):
      tmp = '[Title]: %s\n' % self.title
      tmp += '[Year]: %d\n' % self.year
      tmp += '[Paper]: %s\n' % self.paper
      tmp += '[Project]: %s\n' % self.project
      tmp += 'In %s\n' % self.article
      tmp += '[Teaser]: %s\n' % self.teaser
      for i, (author, url) in enumerate(zip(self.authors, self.author_urls)):
        tmp += '[Author %d]: %s at %s\n' % (i, author, url)

      return tmp


#     def __lt__(self, other):
#       if self.year < other.year:
#         return True
#       elif self.year > other.year:
#         return False
#       else:
#         return self.article < other.article

    def WriteMD(self, md):
      paper_md = '<table> <tbody> <tr> <td align="left" width=250>\n'
      paper_md += '<a href="%s"><img src="teasers/%s"/></a></td>\n' % (self.imgurl, self.teaser)
      paper_md += '<td align="left" width=550>%s<br>\n' % self.title
      n_authors = len(self.authors)
      for i, (author, url) in enumerate(zip(self.authors, self.author_urls)):
        if i < n_authors-1:
          if url:
            paper_md += '<a href="%s">%s</a>, \n' % (url, author)
          else:
            paper_md += '%s, \n' % author
        else:
          if url:
            paper_md += '<a href="%s">%s</a><br>\n' % (url, author)
          else:
            paper_md += '%s\n' % author
      paper_md += 'In %s %d<br>\n' % (self.article, self.year)
      if self.paper:
        paper_md += '<a href="%s">[Paper]</a> \n' % self.paper
      if self.project:
        paper_md += '<a href="%s">[Project]</a> \n' % self.project
      paper_md += '</td></tr></tbody></table>\n\n\n'
      md += paper_md
      return md


def ReadPapers(csv_file):
  papers = []
  with open(csv_file, 'rb') as cfile:
    csv_data = csv.reader(cfile)
    next(csv_data)

    for i, row in enumerate(csv_data):
      paper = Paper()
      paper.ParseCSV(row)
      print(paper.title)

      papers.append(paper)
  return papers

def WriteMD(papers, header_file=None, end_file=None):
  md = ''  # load header and end
  if header_file and os.path.exists(header_file):
    with open(header_file, 'r') as hfile:
      md = hfile.read()

  md += '\n\n\n'
  for paper in papers:
    md = paper.WriteMD(md)
  md += '\n\n\n'

  if end_file and os.path.exists(end_file):
    with open(end_file, 'r') as efile:
      md += efile.raed()

  return md


if __name__ == '__main__':
  WORK_DIR = '../data/'
  header_file = os.path.join(WORK_DIR, 'header.md')
  end_file = os.path.join(WORK_DIR, 'end.md')
  csv_file = os.path.join(WORK_DIR, 'reference.csv')#./usr/local/google/home/junyanz/Projects/CatPapers/reference.csv'
  out_file = os.path.join(WORK_DIR, 'output.md')

  papers = ReadPapers(csv_file=csv_file)
  papers.sort(key=lambda p: p.title)
  papers.sort(key=lambda p: (p.year, p.article), reverse=True)


  with open(out_file, 'w') as f:
    md_content = WriteMD(papers, header_file, end_file)
    f.write(md_content)
  # parse headers
