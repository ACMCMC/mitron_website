import xmltodict

with open('REDACTED', encoding="utf8") as fd:
    doc = xmltodict.parse(fd.read())

lista_terms_spa = [entry['form']['orth'] for entry in doc['TEI']['text']['body']['entry']] #This is the list of the terms in spanish, it is trivial because we only have to get a certain key for every element. We will only use this list to filter which elemts from the REAL dictionary we want to keep, as it contains 4000 entries rather than the 10000 of the real dictionary.

with open('REDACTED', encoding="utf8") as fd:
    doc = xmltodict.parse(fd.read())

doc_scan = doc['TEI']['text']['body']['entry'] #This dictionary contains the real entries we are going to keep

lista_fin = [(entry['form']['orth'], entry['gramGrp']['pos'], entry['sense'] ) for entry in doc_scan] #This list will be the one we'll keep. It's a list of tuples of 3 elements: (mitroneseWord, wordType, [translation, ...]). The third one is a list of translations.

for i in range(len(lista_fin)): #Let's process the translations
    if isinstance(lista_fin[i][2], list): #The translations are a list of Dictionaries
        list_to_flatten = [thing['cit']['quote'] for thing in lista_fin[i][2]]
    else:
        list_to_flatten = [lista_fin[i][2]['cit']['quote']] #The translations are contained in only one Dictionary
    flattened_list = [item for sublist in list_to_flatten for item in (sublist if isinstance(sublist, list) else [sublist])] #Sometimes the list of translations contains sublists, so we flatten it
    lista_fin[i] = (lista_fin[i][0], lista_fin[i][1], flattened_list) #Reasign the tranlations element to the processed one

lista_fin = list(filter(lambda x: any([True if y in lista_terms_spa else False for y in x[2]]), lista_fin)) #Only keep the entries in the bigger dictionary that match the list we  got at first

print(lista_fin[0:10], len(lista_fin))
types_words_list = list(map(lambda x: x.upper(), set([elem[1] for elem in lista_fin]))) #A list of the diffent wordTypes there are in the filtered list
print(types_words_list)
print(len(max(types_words_list, key=len)))
print(max(lista_fin, key=(lambda x: len(x[2][0]))))

lista_fin = list(map(lambda x: (x[0], 'NOUN' if x[1] == 'n' else 'ADVERB' if x[1] == 'adv' else 'VERB' if x[1] == 'v' else 'ADJECTIVE' if x[1] == 'adj' else x[1].upper(), x[2]), lista_fin)) #Adjust the wordType entries to the types the DB asks


import psycopg2 #Upload the list to the DB
conn = psycopg2.connect("REDACTED")

cur = conn.cursor()

for i in range(len(lista_fin)):
    cur.execute("INSERT INTO dictionary_word (mitronese_word, word_class, translation) VALUES (%s, %s, %s)", (lista_fin[i][0],lista_fin[i][1],lista_fin[i][2][0]))
    print(i)
conn.commit()
cur.close()
conn.close()