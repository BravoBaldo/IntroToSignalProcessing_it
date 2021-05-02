
# import re
import os
import filecmp
import glob
import time
import csv

# Globals
spectrum_image_list = []
#fNotFound           = None

def csv_search(lst, field_name):
    idx = lst.index(field_name) if field_name in lst else 99
    return idx


def get_images_info(filename):
    d = {line.split()[0]: line.split()[1:] for line in open(filename)}
    return d


def readcsv(filepathname):
    maindict = {}
    line_count = 0
    with open(filepathname) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')  # , delimiter=' ', quotechar='|'
        header = []
        for row in csv_reader:
            if line_count == 0:
                header = row
            else:
                locdict = {}
                for c in range(1, len(row)):
                    print(f"{c}:{header[c]}:{row[c]}, ", end="")
                    locdict[header[c]] = row[c]
                maindict[row[0]] = locdict
                print("")
            line_count = line_count + 1
    return maindict


# Search a copy of a file
def get_original(org_file_path, dest_path):
    if filecmp.cmp(org_file_path, dest_path):
        return dest_path  # Founded a copy in the original folder
    return ""


# Returns all images in a directory
def get_images_in_directory(images_path):
    matches = [".jpg", ".png", ".gif", "jpeg"]
    dest_list = glob.glob(os.path.join(images_path, "*.*"))  # Lists all path
    list_dest_images = []
    for s in dest_list:
        if any(xx in s.lower() for xx in matches):
            list_dest_images.append(s)
    return list_dest_images


# Search the original file of a copy
def searchFiles(DestList, FileToSearch):
    for strng in DestList:
        sSub = get_original(FileToSearch, strng)
        if sSub != "":
            return sSub
    return ""


def SearchFromTo2(sTest, iiA, sStart, sEnd):
    iB = iC = -1
    iB = sTest.find(sStart, iiA)
    if iB >= 0:
        iC = sTest.find(sEnd, iB)
    return iB, iC


def getImageInfo(sTest, iStart):
    strStart = '\\includegraphics[width='
    strEnd = '\\textwidth]'
    strEnd2 = '}'
    lenStart = len(strStart)
    lenEnd = len(strEnd)
    s1, s2 = SearchFromTo2(sTest, iStart, strStart, strEnd)
    if s1 < 0 or s2 < 0:
        return "", "", "", s1, -1
    s3 = sTest.find(strEnd2, s2+lenEnd+1)

    # a0 = sTest[:s1]
    # aa = sTest[s1:s1+lenStart]
    strImagSize = sTest[s1+lenStart:s2]
    a2 = sTest[s2+lenEnd+1:s3]
    # a3 = sTest[s3+1:]
    # a4 = os.path.basename(a2)
    ImagPath, ImagName = os.path.split(a2)
    return ImagPath, ImagName, strImagSize, s1, s3+1


def getHrefTextitInfo(sTest, iStart):
    global LocalPath
    if sTest.startswith('%'):
        return "", -1, -1
    strStart = "\\href{"
    strEnd = "}"
    lenStart = len(strStart)
    lenEnd = len(strEnd)
    s1, s2 = SearchFromTo2(sTest, iStart, strStart, strEnd)
    if s1 < 0 or s2 < 0:
        return "", s1, -1
    # Founded an href
    href_url = sTest[s1+lenStart:s2].strip()            # link
    pFrom = sTest[s1+lenStart+len(href_url)+lenEnd:]

    if pFrom.startswith("{\\includegraphics"):
        ImgPathX, img_name, strImgSizeX, qqX, iAX = getImageInfo(pFrom, 0)
        if iAX >= 0:
            img_name = get_image_data(LocalPath + ImgPathX, img_name)
            if img_name.lower().endswith(".gif"):  # Tex require no gif
                img_name = img_name + '.png'
            return "{\\InsImageLink{1.0}{" + img_name + "}{" + href_url + "}", s1, iAX+s2+1

    if pFrom.startswith("{\\textit{"):              # Extract text from textit{
        strStart2 = "{\\textit{"
        strEnd2 = "}}"
        strPre = "\\textit{\\url{"
        strPost = "}}"
    else:
        strStart2 = "{"
        strEnd2 = "}"
        strPre = "\\url{"
        strPost = "}"

    lenStart2 = len(strStart2)
    lenEnd2 = len(strEnd2)

    s3, s4 = SearchFromTo2(sTest, s2, strStart2, strEnd2)
    if s3 < 0 or s4 < 0:
        return "", s3, -1
    href_txt = sTest[s3+lenStart2:s4].strip()       # Text Body

    if href_url.endswith("\\%20"):
        href_url = href_url[:-4]

    if href_txt == "":
        return "", s1, s4+lenEnd2

    if href_url == href_txt:    # href_txt == "" then change in url
        # repla = sTest[:s1]
        # replb = "\\textit{\\url{" + href_url + "}}"
        # replc = sTest[s4 + lenEnd2:]
        return strPre + href_url + strPost, s1, s4+lenEnd2
    #return "", s4, -1

    aa1 = sTest[:s1]
    aa2 = sTest[s4:]

    return sTest[s1:s4], s1, s4


def move_at_end(xx, strto_find, strto_move, to_replace='%'):
    if xx.find(strto_find) >= 0:
        if to_replace == '%':
            to_replace = strto_move
        xx = xx.replace(strto_move, "") + "\n" + to_replace
    return xx


def insert_couple(ImgL, ImgR, CaptL = "", CaptR = ""):
    cmd = ""
    cmd += r"\begin{figure}" + "\n"
    cmd += r"    \centering" + "\n"
    cmd += r"    \begin{minipage}{0.5\textwidth}" + "\n"
    cmd += r"        \centering" + "\n"
    cmd += r"        \includegraphics[width=1\textwidth]{" + ImgL + "}\n"  # first figure itself
    if CaptL:
        cmd += r"        \caption{" + CaptL + "}\n"
    cmd += r"    \end{minipage}\hfill" + "\n"
    cmd += r"    \begin{minipage}{0.5\textwidth}" + "\n"
    cmd += r"        \centering" + "\n"
    cmd += r"        \includegraphics[width=1\textwidth]{" + ImgR + "}\n"  # second figure itself
    if CaptR:
        cmd += r"        \caption{" + CaptR + "}" + "\n"
    cmd += r"    \end{minipage}" + "\n"
    cmd += r"\end{figure}" + "\n"
    return cmd

def get_image_data(image_path, image_name):
    global fNotFound
    if image_path.endswith("/word/media"):
        sFilePath = os.path.join(image_path, image_name)
        sFnd      = searchFiles(spectrum_image_list, sFilePath)  # search original image in Spectrum
        if sFnd != '':
            image_name = os.path.basename(sFnd)
        else:
            fNotFound.write(sFilePath + "\n")
    return image_name


if __name__ == '__main__':
    global fNotFound
    print('Tool for automatic preprocessing of "A Pragmatic Introduction to Signal Processing"')

    # SPECTRUM path and other images already converted in png
    SpectrumPath = ["F:/Dati/OmegaT/A Pragmatic Introduction to Signal Processing/Org/20210413/SPECTRUM/",
                    "F:/Dati/OmegaT/A Pragmatic Introduction to Signal Processing/Org/GifPngImages/NotFound"
                    ]

    LocalPath = "C:/BookSignalProcessing/20210502/Ita/"    # Path of .tex file
    filedicImages = "C:/BookSignalProcessing/xImagesDb.csv"
    FileName = 'IntroToSignalProcessing2021'

    dicImages = readcsv(filedicImages)
    FileNotFound = os.path.join(LocalPath, "ImagesNotFound.txt")
    if not LocalPath.endswith("/"):
        LocalPath = LocalPath + "/"

    for path in SpectrumPath:
        spectrum_image_list += get_images_in_directory(path)  # All images in Spectrum

    TimeStart = time.time()
    FilePath = os.path.join(LocalPath, FileName + ".tex")
    FileOut = os.path.join(LocalPath, FileName + "_AUTO.tex")

    fNotFound = open(FileNotFound, "w")

    images_to_remove = ["image5.png", "new.gif", "updated.gif", "image6.png"]

    fOut = open(FileOut, "w", encoding="utf8")
    f = open(FilePath, "r", encoding="utf8")
    for x in f:
        print(f"{x.strip()}", end="")

        # -- Handle \href ---
        iA = 0
        while True:
            LurlA, LStart, iA = getHrefTextitInfo(x, iA)
            if iA >= 0:
                x = x[:LStart] + LurlA + x[iA:]
                iA = LStart + len(LurlA)
            else:
                break

        img_first_couple = ""
        iA = 0
        while True:
            ImgPath, ImgName, strImgSize, qq, iA = getImageInfo(x, iA)
            if iA >= 0 and (not strImgSize.startswith("#")):
                ImgName = get_image_data(LocalPath+ImgPath, ImgName)

                img_size = "0.5"
                img_inline = False
                img_Pos = 'l'       # r,R, l,L, i,I, o,O    The uppercase version allows the figure to float. The lowercase version means exactly here.

                if ImgName in dicImages:
                    img_size   = dicImages[ImgName].get('Size',   img_size) if dicImages[ImgName].get('Size', '') != '' else img_size
                    img_inline = dicImages[ImgName].get('InLine', '').lower() == 'n'  # if dicImages[ImgName].get('InLine', '') != '' else img_size
                    # before resolve next replacement block
                    img_Pos = 'l' if dicImages[ImgName].get('Position', 'l').lower() == 'l' else 'r'

                # --- Couples ---
                if ImgName in ["image10.png", "image38.png", "image44.png"]:    # First couple
                    command = ""
                    img_first_couple = ImgName   # the next image will be the second of a couple
                elif img_first_couple:
                    command = insert_couple(img_first_couple, ImgName)
                    img_first_couple = ""       # Second image of a couple founded.
                #elif ImgName == "image11.png":    # First couple
                #    command = insert_couple("image10.png", ImgName )
                #elif ImgName == "image39.png":
                #    command = insert_couple("image38.png", ImgName )
                #elif ImgName == "image45.png":
                #    command = insert_couple("image44.png", ImgName )

                elif ImgName in images_to_remove:
                    command = ""

                # Equations
                elif ImgName == "Equation1.GIF":
                    command = r"\begin{center}$S_{j} = \frac{Y_{j-1} + Y_{j} + Y_{j+1}}{3}$\end{center}"
                elif ImgName == "Equation2.GIF":
                    command = "\n\n" + r"\begin{center}$S_{j} = \frac{Y_{j-2} + 2Y_{j-1} + 3Y_{j} + 2Y_{j+1} + Y_{j+2}}{9}$\end{center}" + "\n\n"
                elif ImgName == "DerivEquation1.GIF":
                    command = r"${Y_{j}}' = \frac{Y_{j+1} - Y_{j}}{X_{j+1} - X_{j}} = \frac{Y_{j+1} - Y_{j}}{\Delta X}\:\:\:\:\:\:\:\:\:\:{X_{j}}' = \frac{X_{j+1} - X_{j}}{2}$" + "\n\n"
                elif ImgName == "DerivEquation2.GIF":
                    command = "${Y_{j}}' = \\frac{Y_{j+1} - Y_{j-1}}{2 \\Delta X}\\:\\:\\:\\:\\:\\:\\:{X_{j}}' = X_{j}$\n\n"
                elif ImgName == "DerivEquation3.GIF":
                    command = "${Y_{j}}'' = \\frac{Y_{j+1} - 2Y_{j} + Y_{j-1}}{\\Delta X^{2}}\\:\\:\\:\\:\\:\\:\\:{X_{j}}' = X_{j}$\n\n"
                elif ImgName == "delta.GIF":
                    command = "$\\Delta$"
                else:
                    # Invert images
                    if ImgName == "s7s25s51.GIF":
                        ImgName = "s72551.GIF"
                    elif ImgName == "s72551.GIF":
                        ImgName = "s7s25s51.GIF"

                    if ImgName.lower().endswith(".gif"):  # Tex require no gif
                        ImgName = ImgName + '.png'

                    command = '\\InsImageInline{' + img_size + '}{' + img_Pos + '}{' + ImgName + '}'
                    if img_inline:
                        command = '\\InsImage{' + img_size + '}{' + ImgName + '}'

                # Position: Normal, AppendSpace, @End, Before
                if ImgName in ["Matlab.gif.png", "SmoothWidthTest.png", "iSignalSmoothAnimation.gif.png",
                               "DerivativeDemoMedium.png",
                                 "AnimatedDerivative.gif.png"   # also at the end
                                 ]:           # Append Unbreakable-space
                    command = command + "\n~"

                if ImgName in ["PerfectFit.png", "PeakDetectionSpreadsheet.png", "SmoothWidthTest.gif.png",
                               "724px-Spetrophotometer-en.svg.png",
                               # "image23.png",
                               "SegmentedSmoothDemo.png",
                               "s7s25s51.GIF.png",
                               # "ClickButtons.png"
                               ]:
                    x = x[:qq] + x[iA:] + "\n" + command    # Image at the end
                elif ImgName in ["ClickButtons.png", "Octave.gif.png", "AnimatedDerivative.gif.png",
                                 "FunctionPrompt.gif.png",
                                 "CurveFitExponentialGaussian.png",
                                 "FittingAnimation.gif.png",
                                 "DemoADCNumericalNoise.png",
                                 "TestSignalAsymmetryTest.gif.png",
                                 "TestingOneTwoThree.png"]:       # Before
                    x = command + "\n" + x[:qq] + x[iA:]
                else:
                    x = x[:qq] + command + x[iA:]           # image in the same place
                iA = qq + len(command)
            else:
                break

        to_rep = "\\texttt{\\textbf{amplitude*EXP(-1*((x-position)/(0.60056120439323*width))\\textasciicircum{}2)}}, "
        x = x.replace(to_rep, "\n\n" + "\\begin{center}" + to_rep + "\\end{center}")

        to_rep = "\\texttt{\\textbf{amplitude/(1+((x-position)/(0.5*width))\\textasciicircum{}2)}}."
        x = x.replace(to_rep, "\n\n" + "\\begin{center}" + to_rep + "\\end{center}" + "\n\n")


        to_rep = "\\texttt{\\textbf{SQRT(2)*(}} \\textbf{RAND}\\texttt{\\textbf{()-}}\\textbf{RAND}\\texttt{\\textbf{()+}}\\textbf{RAND}\\texttt{\\textbf{()-}}\\textbf{RAND}\\texttt{\\textbf{()+}}\\textbf{RAND}\\texttt{\\textbf{()-}}\\textbf{RAND}\\texttt{\\textbf{())}}"
        x = x.replace(to_rep, "\n\n" + "\\begin{center}" + to_rep + "\\end{center}" + "\n\n")


        x = x.replace(r"\textbf{A})\textsuperscript{\privateuse{}\privateuse{}}\textbf{A}", r"\textbf{A})\textsuperscript{${-}$1}\textbf{A}")
        x = x.replace("\\textbf{C} = \\textbf{Ɛ}\\textsuperscript{\\privateuse{}\\privateuse{}}\\textbf{A}", "\\textbf{C} = \\textbf{Ɛ}\\textsuperscript{${-}$1}\\textbf{A}")
        x = x.replace("\\textbf{M} = (\\textbf{A}\\textsuperscript{T}\\textbf{A})\\textsuperscript{\\privateuse{}\\privateuse{}}\\textbf{A}\textsuperscript{T}\textbf{C}", r"\textbf{M} = (\textbf{A}\textsuperscript{T}\textbf{A})\textsuperscript{${-}$1}\textbf{A}\textsuperscript{T}\textbf{C}")
        x = x.replace(r"{square root of pi}\privateuse{}\privateuse{}", r"{square root of pi}, ")
        x = x.replace(r"\href{http://www.mathworks.com/matlabcentral/fileexchange/authors/62607}{Diederick}", r"~\href{http://www.mathworks.com/matlabcentral/fileexchange/authors/62607}{Diederick}")

        if False:
            # -- Start Table 'Area'
            x = x.replace(r"\texttt{\textcolor{color-6}{max halfwidth Area}}\index{Area}",
                          r"\begin{table}[h]\centering\begin{tabular}{rrr}\hline" + "\n" +
                          r"\multicolumn{1}{c}{{\color{color-6} \textbf{max}}} & " + "\n" +
                          r"\multicolumn{1}{c}{{\color{color-6} \textbf{halfwidth}}} & " + "\n" +
                          r"\multicolumn{1}{c}{{\color{color-6} \textbf{Area}}} \\ \hline" + "\n"
                          )
            x = x.replace(r"\texttt{1 1.6662 1.7725}", r"1       & 1.6662 & 1.7725 \\")
            x = x.replace(r"\texttt{0.78442 2.1327 1.7725}",
                          r"0.78442 & 2.1327 & 1.7725 " + "\n" +
                          r"\end{tabular}\end{table}\index{Area}" + "\n"
                          )
            # -- End Table 'Area'

        # Proposal: change k1, k2, k3 and k4 with number as pedix (K\textsubscript{1})
        x = x.replace(" k1", " K\textsubscript{1}")
        x = x.replace(" k2", " K\textsubscript{2}")
        x = x.replace(" k3", " K\textsubscript{3}")
        x = x.replace(" k4", " K\textsubscript{4}")

        # To check again... and to remove
        if x.find(r"\subsection{") >= 0:
            x = x.replace(r".html\#Octave", r".html")

        fOut.write(x)
    f.close()
    fOut.close()
    fNotFound.close()

    TimeEnd = time.time()
    print(f"\n\nDuration: {TimeEnd - TimeStart}")
