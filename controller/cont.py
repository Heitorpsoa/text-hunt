import os
import time
from controller import stopwords


def getRawTexts():
    users = os.listdir('users')
    texts = []
    
    # Cada usuário
    for u in users:

        # Lista de arquivos de cada usuário (text1, text2, tags1, tags2... textn, tagsn)
        files = os.listdir('users/'+u)
        for i in range(int((len(files) + 1) / 2)):

            # Exemplo: users/user2/text3 
            textPath = os.path.join('users', u, "text"+str(i+1))
            tagsPath = os.path.join('users', u, "tags"+str(i+1))

            text = open(textPath, "r")
            tags = open(tagsPath, "r")

            text = text.read()
            tags = tags.read()


            texts.append({
                "user": u,
                "data": text,
                "tags": tags
            })

    
    return texts

def processWord(word):
    processedWord = word.lower()

    #Tirando pontuação grudada na palavra
    processedWord = processedWord.replace(',', '')
    processedWord = processedWord.replace('.', '')
    processedWord = processedWord.replace('“', '')
    processedWord = processedWord.replace('"', '')

    #Substituição Semântica
    if processedWord.isnumeric():
        processedWord = "number " + processedWord
    if "%" in processedWord:
        processedWord = "percent " + processedWord
    if "$" in processedWord:
        processedWord = "money " + processedWord 

    # Retorna backspace para apagar o espaço adicionado
    if processedWord in stopwords.words:
        return False
    return processedWord

def processText(text): 
    words = text.split()
    processedWords = ""
    for word in words:
        w = processWord(word)
        if w:
            processedWords += w + ' '
    return processedWords



# Retorna os textos processados, objetivo é salvar posteriormente
def getProcessedTexts():
    texts = getRawTexts()
    processed = []
    for t in texts:
        processed.append({
            'processed': processText(t['data']),
            'user': t['user'],
            'data': t['data'],
            'tags': t['tags']
        }) 
    return processed


def indexation(): 
    texts = getProcessedTexts()
    index = {}

    # Índice do documento
    i = 0
    for t in texts:
        words = t['processed'].split(' ')
        
        # Índice da palavra
        j = 0
        for w in words:
            
            # Palavras Vazias exisitiam e não bugavam o sistema :O
            if w == '':
                continue
            if w not in index:
                index[w] = {'occurences': [], 'tagsWeight': {}}
                index[w]['occurences'].append((i,j))
            else:
                index[w]['occurences'].append((i,j))

            # Adicionando peso para as tags do texto atual
            tags = t['tags'].split('\n')
            for tag in tags:
                if tag in index[w]['tagsWeight']:
                    index[w]['tagsWeight'][tag] = index[w]['tagsWeight'][tag] + 1
                else:
                    index[w]['tagsWeight'][tag] = 1

            j = j + len(w) + 1
        i = i + 1

    return index


def getOccurencePreview(index, documents, occurence):
    documentIndex, startIndex = occurence
    document =  documents[documentIndex]
    
    preview =  "..." + document['processed'][startIndex-20:startIndex+20] + "..."
    return {"user": document['user'], "preview": preview, "index": documentIndex, "startIndex": startIndex} 

def search(term):
    documents = getProcessedTexts()
    index = indexation()

    # Indexação não conta para o tempo de pesquisa
    start = time.time()
    cont = 0
    occurences = []

    for key in index:

        # Se achou o termo 
        if key == term:

            # Para cada ocorrencia do termo em todos os documentos
            for occurence in index[key]['occurences']:
                cont = cont + 1
                occurences.append(
                    getOccurencePreview(index, documents, occurence)
                )

    end = time.time()
    duration = end - start

    result = {
        "cont": cont,
        "duration": duration,
        "occurences": occurences
    }
    return result

def getText(docIndex):
    texts = getRawTexts()
    return texts[docIndex]

def getAllTags():
    texts = getRawTexts()
    tags = []
    for tagArray in texts:
        for t in tagArray['tags'].split('\n'):
            tags.append(t)
            
    # Removendo duplicatas        
    tags = list(dict.fromkeys(tags))    
    return tags