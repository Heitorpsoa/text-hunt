import os
import time
from controller import stopwords

class Controller:
    index = {}
    documents = []

    def __init__(self):
        self.index = self.indexation()
        self.raw = self.getRawTexts()
        self.documents = self.getProcessedTexts()

    def getRawTexts(self):
        users = os.listdir('users')
        texts = []
        
        # Cada usuário
        for u in users:

            # Lista de arquivos de cada usuário (text1, text2, tags1, tags2... textn, tagsn)
            files = os.listdir('users/'+u)

            for i in range(int((len(files) + 1) / 2)):

                # Exemplo: users/user2/text3 
                textPath = os.path.join('users', u, "text"+str(i+1) + '.txt')
                tagsPath = os.path.join('users', u, "tags"+str(i+1) + '.txt')
            
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

    def processWord(self, word):
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

    def processText(self, text): 

        # Todas as palavras do texto
        words = text.split()
        processedWords = ""

        # Para cada palavra
        for word in words:

            # Limpa a palavra
            w = self.processWord(word)
            if w:
                processedWords += w + ' '
        return processedWords



    # Retorna os textos processados, objetivo é salvar posteriormente
    def getProcessedTexts(self):
        texts = self.getRawTexts()
        processed = []

        for t in texts:
            processed.append({
                'processed': self.processText(t['data']),
                'user': t['user'],
                'data': t['data'],
                'tags': t['tags']
            }) 
        return processed


    def indexation(self): 
        texts = self.getProcessedTexts()
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
                    
                # Se a palavra ainda não está indexada
                if w not in index:
                    index[w] = {'occurences': [], 'tagsWeight': {}}
                    index[w]['occurences'].append((i,j))
                else:
                    index[w]['occurences'].append((i,j))

                # Adicionando peso para as tags do texto atual
                tags = t['tags'].split('\n')


                for tag in tags:

                    # Se a tag já existe nos pesos
                    if tag in index[w]['tagsWeight']:
                        index[w]['tagsWeight'][tag] = index[w]['tagsWeight'][tag] + 1
                    else:
                        index[w]['tagsWeight'][tag] = 1
                
                j = j + len(w) + 1
            i = i + 1

        return index


    # Retorna um objeto de preview para aquela ocorrência
    def getOccurencePreview(self, documents, occurence):
        documentIndex, startIndex = occurence
        document =  documents[documentIndex]

        preview =  "..." + document['processed'][startIndex-20:startIndex+20] + "..."
        
        return {  
            "user": document['user'],
            "preview": preview,
            "index": documentIndex,
            "startIndex": startIndex,
        }

    def getOccurenceRelevance(self, index, term, tags, documents, occurence):
        try:
            documentIndex, startIndex = occurence
            document =  documents[documentIndex]

            tagsWeights = index[term]['tagsWeight']

            score = 0
            maximum = 0

            # Para cada um das tags weights: [money: 54, finnance: 22 ... ] 
            for tw in tagsWeights:
                # O potencial máximo  de relevância aumenta 
                maximum += tagsWeights[tw]
                
                # Para cada tag que o usuário tem interesse [money, terror]
                for tag in tags:

                    # Se a tag está contida nos pesos indexados
                    if tag in tw:
                        score += tagsWeights[tw]
            
            # Relevância relativa
            percent = (score / maximum) * 100
            return {
                "score": score,
                "wordScore": maximum,
                "percent": "{:.2f}".format(percent)
            }

        except Exception as e:
            print(e)
            return e

    def search(self, term, tags):
        documents = self.documents
        index = self.index

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
                    
                    ocuResult = self.getOccurencePreview(documents, occurence)
                    ocuResult['relevance'] = self.getOccurenceRelevance(index, term, tags, documents, occurence)
                    occurences.append(
                        ocuResult
                    )
        
        # Ordenando por relevância
        def sortFunc(el):
            return el['relevance']['score']
        occurences.sort(key=sortFunc, reverse=True)

        end = time.time()
        duration = end - start

        result = {
            "cont": cont,
            "duration": duration,
            "occurences": occurences,
        }
        return result

    def getText(self, docIndex):
        texts = self.getRawTexts()
        return texts[docIndex]

    def getAllTags(self):
        texts = self.getRawTexts()
        tags = []
        for tagArray in texts:
            for t in tagArray['tags'].split('\n'):
                tags.append(t)
                
        # Removendo duplicatas        
        tags = list(dict.fromkeys(tags))    
        return tags

