import copy
import math
import pyPdf
import sys
import getopt
import os

def usage():
  print ("Usage: splitPDF.py [args]\n\n" + 
         "\t--- Short ---\n"
         "\t-i <input_file>\n" +
         "\n" +
         "\t--- Long  ---\n" +
         "\t--input <input_file>\n")

def request_info(pdfLoaded):
  pages = pdfLoaded.getNumPages()
  print ("There are " + str(pages) + " pages in your document.\n")
  num = input("How many slides are there per page?\n")
  if num > 2:
    numline = input("How many slides are there per line?\n")

  layouts = ["[1]: Left to right, then top to bottom.", \
             "[2]: Right to left, then top to bottom.", \
             "[3]: Top to bottom, then left to right.", \
             "[4]: Top to bottom, then right to left."
             ]

  print  ("Since the layout of PDFs varies according to how it has\n" + \
          "originally been written, I need to know what the layout is.\n")
  
  layoutValid = False
  count = 0
  while (not layoutValid and count < 3):
    count = count + 1
    print ("Please choose from the following options:\n" + \
          "[0]: None of the below.")

    for i in layouts:
      print i
  
    layout = (input("\nWhat number layout does your document match?\n"))
    if not (0 <= layout and layout <= 4):
      print "You have chosen an incompatible layout option. Try again.\n"
    else:
      layoutValid = True
  
  if (not layoutValid):
    print "You chose an incompatible layout option too many times. Exiting..."
    sys.exit(3)
  return num, numline, layout

def layoutRead(layout, lpage, sline, slides, input, output):
  # Left to right then top row to bottom row
  for p in range(input.getNumPages()):
    page = input.getPage(p)
    
    x1, x2 = page.mediaBox.upperLeft
    x3, x4 = page.mediaBox.lowerRight
  
    x1, x2 = math.floor(x1), math.floor(x2)
    x3, x4 = math.floor(x3), math.floor(x4)
    x5, x6 = math.floor((x3 - x1)/sline), math.floor((x4 - x2)/lpage)

    for slide in range(slides):
      q = copy.copy(page)
      q.mediaBox = copy.copy(page.mediaBox)

      if layout == 1:
        lalign = 1 + (slide % sline)
        talign = 1 + math.floor(slide / sline)
      elif layout == 2:
        lalign = sline - (slide % sline)
        talign = 1 + math.floor(slide / sline)
      elif layout == 3:
        lalign = 1 + math.floor(slide / lpage)
        talign = 1 + (slide % lpage)
      elif layout == 4:
        lalign = sline - math.floor(slide / lpage)
        talign = 1 + (slide % lpage)

      upperLeftx  = x1 + ((lalign - 1) * ((x3-x1) / sline))
      upperLefty  = x2 + ((talign - 1) * ((x4-x2) / lpage))
      lowerRightx = x1 + (lalign * ((x3-x1) / sline))
      lowerRighty = x2 + (talign * ((x4-x2) / lpage))

      # print (slide, lalign, talign, upperLeftx, upperLefty, lowerRightx, lowerRighty)

      q.mediaBox.upperLeft  = (upperLeftx , upperLefty )
      q.mediaBox.lowerRight = (lowerRightx, lowerRighty)
        
      output.addPage(q)

  return output

def split_pages(src, dst):
  src_f = file(src, 'r+b')
  dst_f = file(dst, 'w+b')
 
  input = pyPdf.PdfFileReader(src_f)
  output = pyPdf.PdfFileWriter()
  
  spage, sline, layout = request_info(input)
  lpage = spage / sline
  
  if not (spage % sline == 0):
    lpage = lpage + 1

  output = layoutRead(layout, lpage, sline, spage, input, output)
 
  output.write(dst_f)
  src_f.close()
  dst_f.close()

def main():
  try:
    opts, args = getopt.getopt(sys.argv[1:], "hi:", ["help", "input="])
  except getopt.error, msg:
    print msg
    usage()
    sys.exit(2)
 
  src = None
  for o, a in opts:
      if o in ("-i", "--input"):
        src = a
      elif o in ("-h", "--help"):
        usage()
        sys.exit()
      else:
        assert False, "unhandled option"

  if src == None:
    print ("\n--- Input file not set!---\n")
    usage()
    sys.exit()

  src_n, src_e = os.path.splitext(src)

  if src_e != ".pdf":
    print ("\n--- Input file not pdf!---\n")

  dst = src_n + "-changed.pdf"

  print ("\nProcessing the pdf called " + src_n + " into " + dst + "\n")

  split_pages(src,dst)

if __name__ == "__main__":
  main()
