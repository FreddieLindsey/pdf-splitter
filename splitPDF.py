import copy
import math
import pyPdf
import sys

def split_pages2(src, dst):
  src_f = file(src, 'r+b')
  dst_f = file(dst, 'w+b')
 
  input = pyPdf.PdfFileReader(src_f)
  output = pyPdf.PdfFileWriter()
 
  for i in range(input.getNumPages()):
    p = input.getPage(i)
    q = copy.copy(p)
    q.mediaBox = copy.copy(p.mediaBox)
 
    x1, x2 = p.mediaBox.lowerLeft
    x3, x4 = p.mediaBox.upperRight
 
    x1, x2 = math.floor(x1), math.floor(x2)
    x3, x4 = math.floor(x3), math.floor(x4)
    x5, x6 = math.floor(x3/2), math.floor(x4/2)
 
    if x3 > x4:
      # Horizontal Orientation
      p.mediaBox.upperRight = (x5, x4)
      p.mediaBox.lowerLeft = (x1, x2)
      q.mediaBox.upperRight = (x3, x4)
      q.mediaBox.lowerLeft = (x5, x2)
    else:
      # Vertical Orientation
      p.mediaBox.upperRight = (x3, x4)
      p.mediaBox.lowerLeft = (x1, x6)
      q.mediaBox.upperRight = (x3, x6)
      q.mediaBox.lowerLeft = (x1, x2)
 
    output.addPage(p)
    output.addPage(q)
 
  output.write(dst_f)
  src_f.close()
  dst_f.close()
 
def split_pages4(src, dst):
  src_f = file(src, 'r+b')
  dst_f = file(dst, 'w+b')
 
  input = pyPdf.PdfFileReader(src_f)
  output = pyPdf.PdfFileWriter()
 
  for i in range(input.getNumPages()):
    p = input.getPage(i)
    q = copy.copy(p)
    r = copy.copy(p)
    s = copy.copy(p)
    q.mediaBox = copy.copy(p.mediaBox)
    r.mediaBox = copy.copy(p.mediaBox)
    s.mediaBox = copy.copy(p.mediaBox)
 
    x1, x2 = p.mediaBox.lowerLeft
    x3, x4 = p.mediaBox.upperRight
 
    x1, x2 = math.floor(x1), math.floor(x2)
    x3, x4 = math.floor(x3), math.floor(x4)
    x5, x6 = math.floor(x3/2), math.floor(x4/2)
 
    if x3 > x4:
      # Horizontal Orientation
      p.mediaBox.upperRight = (x5, x4)
      p.mediaBox.lowerLeft = (x1, x6)
      q.mediaBox.upperRight = (x3, x4)
      q.mediaBox.lowerLeft = (x5, x6)
      r.mediaBox.upperRight = (x5,x6)
      r.mediaBox.lowerLeft = (x1,x2)
      s.mediaBox.upperRight = (x3,x6)
      s.mediaBox.lowerLeft = (x5,x2)
    else:
      # Vertical Orientation
      p.mediaBox.upperRight = (x5,x6)
      p.mediaBox.lowerLeft = (x1,x4)
      q.mediaBox.upperRight = (x3,x6)
      q.mediaBox.lowerLeft = (x5,x4)
      r.mediaBox.upperRight = (x5,x2)
      r.mediaBox.lowerLeft = (x1,x6)
      s.mediaBox.upperRight = (x1,x4)
      s.mediaBox.lowerLeft = (x5,x6)
 
    output.addPage(p)
    output.addPage(q)
    output.addPage(r)
    output.addPage(s)
 
  output.write(dst_f)
  src_f.close()
  dst_f.close()
 
inputfile = sys.argv[1]
outputfile = sys.argv[2]
print 'Input file is "', inputfile, '"'
print 'Output file is "', outputfile, '"'
num = input("How many slides are there per page?\n")
if num == 2:
  split_pages2(inputfile, outputfile)
elif num == 4:
  split_pages4(inputfile, outputfile)
else:
  print "You gave an invalid number of pages. Try 2 or 4."
