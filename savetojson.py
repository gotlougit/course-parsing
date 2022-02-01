import sys, json

def resetEntry():
    return {"course code": "", "course title": "", "prerequisites": "", "course type": "", "course learning objectives":"", "course content":"", "course outcomes":"", "credits":"", "books": ""}

def writeLines(lines, entry, key, start):
   
    i = start
    running = 1
    while running:
        for term in parsingTerms:
            try:
                x = term.replace(" ","")
                l = lines[i].lower()
                if (term in l or x in l):
                    running = 0
                    break
            except IndexError:
                return start - 1
        else:
            entry[key] += "\n" + processVal(lines[i])
            i+=1
    return i-1

def processVal(val):

    val = "".join(char for char in val if 0 < ord(char) < 128)
    val = val.strip()
    if val in ["-", "nil", "none"]:
        val = ""
    val = val.title()
    return val

def preprocess(line, term):
    
    if parsingTerms.index(term) >= 5:
        line = line.replace(term, "\n" + term + "\n")

    if "books" in line and "reference" not in line:
        line = line.replace("books","reference books")

    return line

def write2dict(lines, entry, lline, term, lineno):
    
    x = lline.partition(":")[-1]
    if not x:
        lline = lline.replace(term,"")
        lline = lline.replace(term.replace(" ",""),"")
    else:
        lline = x
    if (parsingTerms.index(term) >= 5):
        lineno = writeLines(lines, entry, term, lineno + 1)
        return lineno
    else:
        entry[term] = processVal(lline)
    return 0


fname = sys.argv[1]
parsingTerms = ["course code", "course title", "prerequisites", "credits", "course type", "course content", "course learning objectives",  "course outcomes", "books"]
entry = resetEntry()
outname = fname + ".json"
output = open(outname,"w")

with open(fname) as f:
    lines = list(f.readlines())

    lineno = 0
    iters = 1 
    nlines = []
    for l in lines:
        if l != "\n" or "---" not in l:
            l = l.lower()
            for term in parsingTerms:
                if term in l:
                    l = preprocess(l, term)
                else:
                    orig = term
                    term = term.replace(" ","")
                    if term in l:
                        l = preprocess(l, orig)
            nlines.append(l)
         
    lines = nlines
    n = len(lines) 
    while lineno < n:
        flag = 0
        lline = lines[lineno]
        for term in parsingTerms:
            if term in lline:
                flag = 1
                x = write2dict(lines, entry, lline, term, lineno)
                if x:
                    lineno = x
                    continue
            else:
                orig = term
                term = term.replace(" ","")
                if term in lline:
                    flag = 1
                    x = write2dict(lines, entry, lline, orig, lineno)
                    if x:
                        lineno = x
                        continue
        if not iters % 9:
            try:
                entry["credits"] = (entry["credits"].replace("0",""))[0]
            except IndexError:
                entry["credits"] = "0"
            output.write(json.dumps(entry, indent = 2))
            output.write("\n")
            entry = resetEntry()
            iters = 0

        lineno += 1
        iters += 1

output.close()
