import numpy
import pandas as pd
import json

class wer():
    def __init__(self):
        print "Predict WER model!"

    def predict(self, r, h):
        """
        This is a function that calculate the word error rate in ASR.
        Just provide the function with two strings
        model.predict('This is a boy','boy this is')
        """
        #build the matrix
        r = r.split()
        h = h.split()
        d = numpy.zeros((len(r)+1)*(len(h)+1), dtype=numpy.uint8).reshape((len(r)+1, len(h)+1))
        for i in range(len(r)+1):
            for j in range(len(h)+1):
                if i == 0: d[0][j] = j
                elif j == 0: d[i][0] = i
        for i in range(1,len(r)+1):
            for j in range(1, len(h)+1):
                if r[i-1] == h[j-1]:
                    d[i][j] = d[i-1][j-1]
                else:
                    substitute = d[i-1][j-1] + 1
                    insert = d[i][j-1] + 1
                    delete = d[i-1][j] + 1
                    d[i][j] = min(substitute, insert, delete)
        result = float(d[len(r)][len(h)]) / len(r) * 100
        result = str("%.2f" % result) + "%"

        #find out the manipulation steps
        x = len(r)
        y = len(h)
        list = []
        while True:
            if x == 0 and y == 0:
                break
            else:
                if d[x][y] == d[x-1][y-1] and r[x-1] == h[y-1]:
                    list.append("e")
                    x = x-1
                    y = y-1
                elif d[x][y] == d[x][y-1]+1:
                    list.append("i")
                    x = x
                    y = y-1
                elif d[x][y] == d[x-1][y-1]+1:
                    list.append("s")
                    x = x-1
                    y = y-1
                else:
                    list.append("d")
                    x = x-1
                    y = y
        list = list[::-1]

        #print the result in aligned way
        print "REF:",
        for i in range(len(list)):
            if list[i] == "i":
                count = 0
                for j in range(i):
                    if list[j] == "d":
                        count += 1;
                index = i - count
                print " "*(len(h[index])),
            elif list[i] == "s":
                count1 = 0
                for j in range(i):
                    if list[j] == "i":
                        count1 += 1;
                index1 = i - count1
                count2 = 0
                for j in range(i):
                    if list[j] == "d":
                        count2 += 1;
                index2 = i - count2
                if len(r[index1])<len(h[index2]):
                    print r[index1]+" "*(len(h[index2])-len(r[index1])),
                else:
                    print r[index1],
            else:
                count = 0
                for j in range(i):
                    if list[j] == "i":
                        count += 1;
                index = i - count
                print r[index],
        print
        print "HYP:",
        for i in range(len(list)):
            if list[i] == "d":
                count = 0
                for j in range(i):
                    if list[j] == "i":
                        count += 1;
                index = i - count
                print " "*(len(r[index])),
            elif list[i] == "s":
                count1 = 0
                for j in range(i):
                    if list[j] == "i":
                        count1 += 1;
                index1 = i - count1
                count2 = 0
                for j in range(i):
                    if list[j] == "d":
                        count2 += 1;
                index2 = i - count2
                if len(r[index1])>len(h[index2]):
                    print h[index2]+" "*(len(r[index1])-len(h[index2])),
                else:
                    print h[index2],
            else:
                count = 0
                for j in range(i):
                    if list[j] == "d":
                        count += 1;
                index = i - count
                print h[index],
        print
        print "EVA:",
        for i in range(len(list)):
            if list[i] == "d":
                count = 0
                for j in range(i):
                    if list[j] == "i":
                        count += 1;
                index = i - count
                print "D"+" "*(len(r[index])-1),
            elif list[i] == "i":
                count = 0
                for j in range(i):
                    if list[j] == "d":
                        count += 1;
                index = i - count
                print "I"+" "*(len(h[index])-1),
            elif list[i] == "s":
                count1 = 0
                for j in range(i):
                    if list[j] == "i":
                        count1 += 1;
                index1 = i - count1
                count2 = 0
                for j in range(i):
                    if list[j] == "d":
                        count2 += 1;
                index2 = i - count2
                if len(r[index1])>len(h[index2]):
                    print "S"+" "*(len(r[index1])-1),
                else:
                    print "S"+" "*(len(h[index2])-1),
            else:
                count = 0
                for j in range(i):
                    if list[j] == "i":
                        count += 1;
                index = i - count
                print " "*(len(r[index])),
        print
        print "WER: "+result
        return result

if __name__ == '__main__':
    wo = wer()
    # Reference text, Hypothesized text
    wo.predict('This is a boy','This is boy')
    data = pd.DataFrame.from_csv('./data/samplesall/results_enIN.csv')

    files =[]
    confidencesUS = []
    transcriptsUS = []
    confidencesIN = []
    transcriptsIN = []
    for index, row in data.iterrows():
        files.append(row['Files'])
        try:
            in_data = json.loads(row['Trans IN'])['results']
            confidence = []
            transcript = []
            for alter in in_data:
                confidence.append(alter['alternatives'][0]['confidence'])
                transcript.append(alter['alternatives'][0]['transcript'])
            confidence = sum(confidence) / len(confidence)
            transcript = ''.join(transcript)
            confidencesIN.append(confidence)
            transcriptsIN.append(transcript)
        except:
            confidencesIN.append('')
            transcriptsIN.append('')
        try:
            us_data = json.loads(row['Trans US'])['results']
            confidence = []
            transcript = []
            for alter in us_data:
                confidence.append(alter['alternatives'][0]['confidence'])
                transcript.append(alter['alternatives'][0]['transcript'])
            confidence = sum(confidence)/ len(confidence)
            transcript = ''.join(transcript)
            confidencesUS.append(confidence)
            transcriptsUS.append(transcript)
        except:
            confidencesUS.append('')
            transcriptsUS.append('')
    results = pd.DataFrame({
        'Files':files,
        'transcriptsUS':transcriptsUS,
        'transcriptsIN': transcriptsIN,
        'confidencesUS': confidencesUS,
        'confidencesIN': confidencesIN
    })
    results.to_csv('./results/google_ASR_Results.csv')


