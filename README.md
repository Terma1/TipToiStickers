# TipToiStickers
Code that will help you create your own interactive stickers for your tiptoy pen
## Installation
Clone the repository to your local machine:
```python
git clone https://github.com/Terma1/TipToiStickers.git
```
Navigate to the project directory:
```bash
cd your-repository
```
Install the required dependencies:
```bash
pip install -r requirements.txt
```
## Usage
Please open the file "TextToSpeech.py" and write your access key and secret access key(you can find it at AWS user cabinet)before using the code
1) Run main.py
2) Your output is: output.pdf(in project folder) which you should print(please use dpi=1200) and file with .gme type in "tttool" folder, which should be moved to the pen

## What does each part of the project do?
main.py  - activates all parts of the project //
GUI.py - is responsible for the graphical interface where users enter text. At the output, it generates a document with circles and a file (json type) with the coordinates of each circle and the corresponding text
TextToSpeech.py - Reads text from a json file and generates audio using amazon polly
OIDmaker.py - Using audio files, it generates a .yaml file which is then converted into a final .gme file. Also generates .png files with dots
MatrixMaker.py - Since the original dotted .png files are too small, this code creates a matrix of each .png image, which is ideal for our circles
SortedPNG.py - Since there are extra .png files that will not overlap our circles, this program removes them and sorts the remaining .png files by name
PdfToPng.py - converts a document with circles into a .png type for further merging with .png files with dots. Also increases file quality and dpi
Merging.py  - using coordinates from the .json file, overlays each .png file with dotes on the document with circles, and at the end converts the final document into PDF

## Contact
if you have questions or find bugs, please let me know
tsireshkaby@gmail.com
