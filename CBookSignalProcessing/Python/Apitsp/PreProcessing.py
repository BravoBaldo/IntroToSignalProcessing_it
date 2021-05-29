
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
    iC = -1
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


def getHrefTextitInfo(sTest, iStart, spectrum_image_list, fNotFound, LocalPath):
    if sTest.startswith('%'):
        return "", -1, -1
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
<<<<<<< .mine
    # Founded an href
    href_url = sTest[s1+lenStart:s2].strip()            # link
    pFrom = sTest[s1+lenStart+len(href_url)+lenEnd:]

    if pFrom.startswith("{\\includegraphics"):
        ImgPathX, img_name, strImgSizeX, qqX, iAX = getImageInfo(pFrom, 0)
        if iAX >= 0:
            img_name = get_image_data(LocalPath + ImgPathX, img_name, spectrum_image_list, fNotFound)
            if img_name.lower().endswith(".gif"):  # Tex require no gif
                img_name = img_name + '.png'
            return "{\\InsImageLink{1.0}{" + img_name + "}{" + href_url + "}", s1, iAX+s2+1

    if pFrom.startswith("{\\textit{"):              # Extract text from textit{
||||||| .r6
    urlA = sTest[s1+lenStart:s2].strip()
    # Piece = sTest[s1:]
    pFrom = sTest[s1+lenStart+len(urlA)+lenEnd:]
    # Remai = sTest[:s2]
    # strStart2 = "{\\textit{"
    # strEnd2 = "}}"
    # strPre = "\\textit{\\url{"
    # strPost =  "}}"
    if pFrom.startswith("{\\textit{"):
=======
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
>>>>>>> .r8
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
<<<<<<< .mine
        return strPre + href_url + strPost, s1, s4+lenEnd2
    # return "", s4, -1
||||||| .r6
        return strPre + urlA + strPost, s1, s4+lenEnd2
    return "", s4, -1
=======
        return strPre + href_url + strPost, s1, s4+lenEnd2
    #return "", s4, -1
>>>>>>> .r8

<<<<<<< .mine
    # aa1 = sTest[:s1]
    # aa2 = sTest[s4:]
||||||| .r6
=======
    aa1 = sTest[:s1]
    aa2 = sTest[s4:]
>>>>>>> .r8

    return sTest[s1:s4], s1, s4


def move_at_end(xx, strto_find, strto_move, to_replace='%'):
    if xx.find(strto_find) >= 0:
        if to_replace == '%':
            to_replace = strto_move
        xx = xx.replace(strto_move, "") + "\n" + to_replace
    return xx


<<<<<<< .mine
def insert_couple(images, captions=""):
    if len(images) == 0:
        return ""
    divis = "{:.2f}".format(.97/len(images))
    cmd = ""
    cmd += r"\begin{figure}" + "\n"
    cmd += r"    \centering" + "\n"
||||||| .r6
if __name__ == '__main__':
    print('Tool for automatic preprocessing of "A Pragmatic Introduction to Signal Processing"')
=======
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
>>>>>>> .r8

    for i in range(0, len(images)):
        png_img = images[i] + '.png' if images[i].lower().endswith(".gif") else images[i]

<<<<<<< .mine
        cmd += r"    \begin{minipage}{" + divis + r"\textwidth}" + "\n"
        cmd += r"        \centering" + "\n"
||||||| .r6
    LocalPath = "C:/BookSignalProcessing/20210423/Eng/"    # Path of .tex file
    filedicImages = "C:/BookSignalProcessing/xImagesDb.csv"
    FileName = 'IntroToSignalProcessing2021'
=======
    LocalPath = "C:/BookSignalProcessing/20210502/Ita/"    # Path of .tex file
    filedicImages = "C:/BookSignalProcessing/xImagesDb.csv"
    FileName = 'IntroToSignalProcessing2021'
>>>>>>> .r8

        cmd += "        \\href{" + images[i] + "}{\\includegraphics[width=" + "1" + "\\linewidth]{" + png_img + "}}%\n"

<<<<<<< .mine
        # cmd += r"        \includegraphics[width=1\textwidth]{" + images[i] + "}\n"  # first figure itself
        if len(captions) > 0 and captions[1]:
            cmd += r"        \caption{" + captions[1] + "}\n"
        # cmd += r"    \end{minipage}\hfill" + "\n"
        cmd += r"    \end{minipage}" + "\n"

    cmd += r"\end{figure}" + "\n"
    return cmd


def get_image_data(image_path, image_name, spectrum_image_list, fNotFound):
    # global fNotFound
    # global spectrum_image_list
    if image_path.endswith("/word/media"):
        sFilePath = os.path.join(image_path, image_name)
        sFnd = searchFiles(spectrum_image_list, sFilePath)  # search original image in Spectrum
        if sFnd != '':
            image_name = os.path.basename(sFnd)
        elif fNotFound:
            fNotFound.write(sFilePath + "\n")
    return image_name


def main(tex_name_noext,
         tex_path,           # Path of .tex file
         image_path_list,     # list of paths where to search images
         db_filepath
    ):
    print('Tool for automatic preprocessing of "A Pragmatic Introduction to Signal Processing"')

    dicImages = readcsv(db_filepath)
    FileNotFound = os.path.join(tex_path, "ImagesNotFound.txt")
    if not tex_path.endswith("/"):
        tex_path = tex_path + "/"

    spectrum_image_list = []
||||||| .r6
    spectrum_image_list = []
=======
>>>>>>> .r8
    for path in image_path_list:
        spectrum_image_list += get_images_in_directory(path)  # All images in Spectrum

    TimeStart = time.time()
    FilePath = os.path.join(tex_path, tex_name_noext + ".tex")
    FileOut = os.path.join(tex_path, tex_name_noext + "_AUTO.tex")

    fNotFound = open(FileNotFound, "w")

<<<<<<< .mine
    images_to_remove = ["imgge5.png", "new.gif", "updated.gif", "imgge6.png"]
    images_sided = [["imgge11.png", "imgge12.png"],
                    ["imgge39.png", "imgge40.png"],
                    ["imgge45.png", "imgge46.png"],
                    ["ps1.png", "ps2.png"],
                    ["SingleFreq.png", "DeltaSpectrum.png", "WhiteNoiseSpectrum.png"],
                    ["SilenceBeforeSignal.png", "SilenceAfterSignal.png"],
                    ["SunspotSpectrumMode2.png", "SunspotSpectrumMode.png"],
                    ["imgge78.png", "PlotSegFreqSpectExample6b.png", "imgge80.png"],
                  # ["IntermittentSinusoidSTFT.png"],
                    ["IntermittentSinusoidPlotSegFreqSpect.png", "IntermittentSinusoidPlotSegFreqSpectLog.png"],
                    ["Integration2.gif", "Integration.gif"],
                  # ["10unsmoothed.png", "10smoothed.png"],
                    ["imgge113.png", "imgge114.png", "imgge115.png"],
                    ["SnPvs7percent1.png", "LogSnP_index_since1950logy.png"]
                    ]
    images_sided_first = []
    images_sided_last = []
    for block in images_sided:
        images_sided_first.extend(block[0:-1])
        images_sided_last.append(block[-1])


||||||| .r6
=======
    images_to_remove = ["image5.png", "new.gif", "updated.gif", "image6.png"]

>>>>>>> .r8
    fOut = open(FileOut, "w", encoding="utf8")
    f = open(FilePath, "r", encoding="utf8")
    for x in f:
        # print(f"{x.strip()}", end="")
        print(f"{x.strip()}")
        # -- Handle \href ---
        # -- Handle \href ---
        iA = 0
        while True:
            LurlA, LStart, iA = getHrefTextitInfo(x, iA, spectrum_image_list, fNotFound, tex_path)
            if iA >= 0:
                x = x[:LStart] + LurlA + x[iA:]
                iA = LStart + len(LurlA)
            else:
                break

<<<<<<< .mine
        parallel_images = []
||||||| .r6
        images_to_remove = ["image5.png", "new.gif", "updated.gif"]

=======
        img_first_couple = ""
>>>>>>> .r8
        iA = 0
        while True:
            ImgPath, ImgName, strImgSize, qq, iA = getImageInfo(x, iA)

            if iA >= 0 and (not strImgSize.startswith("#")):
<<<<<<< .mine
                ImgName = get_image_data(tex_path+ImgPath, ImgName, spectrum_image_list, fNotFound)
||||||| .r6
=======
                ImgName = get_image_data(LocalPath+ImgPath, ImgName)
>>>>>>> .r8

                img_size = "0.5"
                img_inline = False
                img_Pos = 'l'       # r,R, l,L, i,I, o,O    The uppercase version allows the figure to float. The lowercase version means exactly here.

                if ImgName in dicImages:
                    img_size   = dicImages[ImgName].get('Size',   img_size) if dicImages[ImgName].get('Size', '') != '' else img_size
                    img_inline = dicImages[ImgName].get('InLine', '').lower() == 'n'  # if dicImages[ImgName].get('InLine', '') != '' else img_size
                    # before resolve next replacement block
                    img_Pos = 'l' if dicImages[ImgName].get('Position', 'l').lower() == 'l' else 'r'

<<<<<<< .mine
                # --- Side-By-Side images ---
                if ImgName in images_sided_first:    # First couple
||||||| .r6
                if ImgName in images_to_remove:
=======
                # --- Couples ---
                if ImgName in ["image10.png", "image38.png", "image44.png"]:    # First couple
>>>>>>> .r8
                    command = ""
<<<<<<< .mine
                    parallel_images.append(ImgName)     # this is a parallel image
                elif ImgName in images_sided_last:    # Last couple
                    parallel_images.append(ImgName)     # this is the last parallel image
                    command = insert_couple(parallel_images)
                    img_first_couple = ""       # Second image of a couple founded.
                    parallel_images.clear()

                # Images to remove
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
                elif ImgName == "FourierDivide.gif":
                    # command = "\\begin{center}$\\frac{a+ib}{c+id} = \\frac{ac+bd}{c^{2}+d^{2}} + i\\frac{bc-ad}{c^{2}+d^{2}}$\\end{center}\n\n"
                    command = r"\begin{equation}\mbox{\fontsize{17.28}{21.6}\selectfont\(\frac{a+ib}{c+id} = \frac{ac+bd}{c^{2}+d^{2}} + i\frac{bc-ad}{c^{2}+d^{2}}\)}\end{equation}" + "\n\n"
                elif ImgName == "delta.GIF":
                    command = "$\\Delta$"
||||||| .r6
=======
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
>>>>>>> .r8
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

<<<<<<< .mine
                # Position: Normal, AppendSpace, @End, Before
                # Image @SEPARATED
                if ImgName in ["Matlab.gif.png", "SmoothWidthTest.png", "iSignalSmoothAnimation.gif.png",
                               "DerivativeDemoMedium.png",
                                 "AnimatedDerivative.gif.png", "SharpenedOverlapDemo2.png", "imgge77.png"
                                 ]:           # Append Unbreakable-space
                    command = command + "\n~"

                # Image @END
                if ImgName in ["PerfectFit.png", "PeakDetectionSpreadsheet.png", "SmoothWidthTest.gif.png",
                               "724px-Spetrophotometer-en.svg.png",
                               # "imgge24.png",
                               "SegmentedSmoothDemo.png",
                               "s7s25s51.GIF.png",
                                "DeconvDemo3.gif.png",
                               # "ClickButtons.png",
                               "FourierFilterBandwidthOptimizationShape1.png",
                               ]:
                    x = x[:qq] + x[iA:] + "\n" + command + "~"   # Image at the end
                # Image @BEFORE
                elif ImgName in ["ClickButtons.png", "Octave.gif.png", "AnimatedDerivative.gif.png",
                                 "FunctionPrompt.gif.png",
                                 "CurveFitExponentialGaussian.png",
                                 "FittingAnimation.gif.png",
                                 "DemoADCNumericalNoise.png",
                                 "TestSignalAsymmetryTest.gif.png",
                                 "TestingOneTwoThree.png", "imgge57.png", "OriginalSignals.png",
                                 "imgge88.png", "iSignalSpectrumMode.gif.png",
                                 "SegExpDeconvPlotExample.png", "SSFexample3.png",
                                 "HeightAndAreaTest.png", "RectSNR3.png", "FourierFilterDemo.png",
                                 "EffectOfBroadening.png", "GeometricalHeightEqualization.png", "deconvolution.png",
                                 "LorentzianSelfDeconvDemo2spectrum.png", "imgge110.png",]:       # Before
                    # x = command + "\n\\noindent " + x[:qq] + x[iA:]
                    x = command + "~\n" + x[:qq] + x[iA:]
                # Image @HERE
                else:
                    x = x[:qq] + command + x[iA:]           # image in the same place

                iA = 0  # qq + len(command)
||||||| .r6
                x = x[:qq] + command + x[iA:]
                iA = qq + len(command)
=======
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
>>>>>>> .r8
            else:
                break

        to_rep = "\\texttt{\\textbf{amplitude*EXP(-1*((x-position)/(0.60056120439323*width))\\textasciicircum{}2)}}, "
        x = x.replace(to_rep, "\n\n" + "\\begin{center}" + to_rep + "\\end{center}")

        to_rep = "\\texttt{\\textbf{amplitude/(1+((x-position)/(0.5*width))\\textasciicircum{}2)}}."
        x = x.replace(to_rep, "\n\n" + "\\begin{center}" + to_rep + "\\end{center}" + "\n\n")

<<<<<<< .mine
||||||| .r6
        to_find = "\\index{Spreadsheets!Signal arithmetic}\\InsImage"
        to_move = "\\InsImageInline{0.5}{l}{PeakDetectionSpreadsheet.png}"
        x = move_at_end(x, to_find, to_move)

        to_find = "\\label{ref-0061}}"
        to_move = "\\InsImageInline{0.6}{l}{SmoothWidthTest.gif.png}"
        x = move_at_end(x, to_find, to_move)

        to_find = "\\InsImageInline{0.5}{l}{PerfectFit.png}"
        to_move = "\\InsImageInline{0.5}{l}{PerfectFit.png}"
        x = move_at_end(x, to_find, to_move)

        to_find = r"\InsImageInline{0.5}{l}{724px-Spetrophotometer-en.svg.png}"
        to_move = r"\InsImageInline{0.5}{l}{724px-Spetrophotometer-en.svg.png}"
        x = move_at_end(x, to_find, to_move)

        to_find = r"\InsImageInline{0.5}{l}{image23.png}"
        to_move = r"\InsImageInline{0.5}{l}{image23.png}"
        x = move_at_end(x, to_find, to_move)

        to_find = r"\InsImageInline{0.5}{l}{ClickButtons.png}"
        to_move = r"\InsImageInline{0.5}{l}{ClickButtons.png}"
        x = move_at_end(x, to_find, to_move)    # AAA: move_at_BEGIN

        # This is a QRCODE!!!!!
        to_find = r"\InsImageInline{0.5}{l}{image6.png}"
        to_move = r"\InsImageInline{0.5}{l}{image6.png}"
        to_repl = ""  # "\\qrcode[level=\\QRCodeQuality, height=2cm]{https://terpconnect.umd.edu/~toh/spectrum/functions.html}"
        x = move_at_end(x, to_find, to_move, to_repl)

=======

>>>>>>> .r8
        to_rep = "\\texttt{\\textbf{SQRT(2)*(}} \\textbf{RAND}\\texttt{\\textbf{()-}}\\textbf{RAND}\\texttt{\\textbf{()+}}\\textbf{RAND}\\texttt{\\textbf{()-}}\\textbf{RAND}\\texttt{\\textbf{()+}}\\textbf{RAND}\\texttt{\\textbf{()-}}\\textbf{RAND}\\texttt{\\textbf{())}}"
        x = x.replace(to_rep, "\n\n" + "\\begin{center}" + to_rep + "\\end{center}" + "\n\n")

<<<<<<< .mine
        to_rep = r"\fbox{\begin{minipage}[t]{0.8\textwidth}\end{minipage}}"
        x = x.replace(to_rep, "")
||||||| .r6
        x = x.replace(r"{Matlab.gif.png}\href{", "{Matlab.gif.png}" + "\n~\\href{")
        x = x.replace(r"{SmoothWidthTest.png}\href{", "{SmoothWidthTest.png}" + "\n~\\href{")
        x = x.replace(r"{iSignalSmoothAnimation.gif.png}\href{", "{iSignalSmoothAnimation.gif.png}" + "\n~\\href{")
        x = x.replace(r"{DerivativeDemoMedium.png}\href{", "{DerivativeDemoMedium.png}" + "\n~\\href{")
        x = x.replace("\\textsuperscript{\\InsImageInline{0.5}{l}{FourierDivide.gif.png}}", "\\InsImageInline{0.5}{l}{FourierDivide.gif.png}")
=======
>>>>>>> .r8

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

<<<<<<< .mine
        # Proposal: change k1, k2, k3 and k4 with number as pedix (K\textsubscript{1})
        # x = x.replace(" k1", " K\\textsubscript{1}")
        # x = x.replace(" k2", " K\\textsubscript{2}")
        # x = x.replace(" k3", " K\\textsubscript{3}")
        # x = x.replace(" k4", " K\\textsubscript{4}")
||||||| .r6
=======
        # Proposal: change k1, k2, k3 and k4 with number as pedix (K\textsubscript{1})
        x = x.replace(" k1", " K\textsubscript{1}")
        x = x.replace(" k2", " K\textsubscript{2}")
        x = x.replace(" k3", " K\textsubscript{3}")
        x = x.replace(" k4", " K\textsubscript{4}")
>>>>>>> .r8

        # To check again... and to remove
        if x.find(r"\subsection{") >= 0:
            x = x.replace(r".html\#Octave", r".html")

        fOut.write(x)
    f.close()
    fOut.close()
    fNotFound.close()

    TimeEnd = time.time()
<<<<<<< .mine
    print(f"\n\nDuration: {TimeEnd - TimeStart}")


if __name__ == '__main__':
    # SPECTRUM path and other images already converted in png
    '''Images MUST be found ONLY in these paths otherwise put in "ImagesNotFound.txt"
        This is due the repeatibility of images names
     '''
    main(
        'IntroToSignalProcessing2021',
        "C:/BookSignalProcessing/20210529/Ita/",
        ["F:/Dati/OmegaT/A Pragmatic Introduction to Signal Processing/Org/20210529/SPECTRUM/",
         "F:/Dati/OmegaT/A Pragmatic Introduction to Signal Processing/Org/GifPngImages",
         # "C:/BookSignalProcessing/20210529/Ita/IntroToSignalProcessing2021.docx.tmp/word/media"
         ],
        "C:/BookSignalProcessing/xImagesDb.csv"
    )||||||| .r6
    print(f"Duration: {TimeEnd - TimeStart}")
=======
    print(f"\n\nDuration: {TimeEnd - TimeStart}")
>>>>>>> .r8
