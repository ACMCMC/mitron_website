import xmltodict
import pprint

with open('REDACTED', encoding="utf8") as fd:
    doc = xmltodict.parse(fd.read())

doc_scan = doc['TEI']['text']['body']['entry']

lista_terms_spa = [entry['form']['orth'] for entry in doc_scan]

with open('REDACTED', encoding="utf8") as fd:
    doc = xmltodict.parse(fd.read())

doc_scan = doc['TEI']['text']['body']['entry']

lista_fin = [(entry['form']['orth'], entry['gramGrp']['pos'], entry['sense'] ) for entry in doc_scan]

for i in range(len(lista_fin)):
    if isinstance(lista_fin[i][2], list):
        flatten_list = [thing['cit']['quote'] for thing in lista_fin[i][2]]
    else:
        flatten_list = [lista_fin[i][2]['cit']['quote']]
    flat = [item for sublist in flatten_list for item in (sublist if isinstance(sublist, list) else [sublist])]
    lista_fin[i] = (lista_fin[i][0], lista_fin[i][1], flat)

lista_fin = list(filter(lambda x: any([True if y in lista_terms_spa else False for y in x[2]]), lista_fin))

print(lista_fin[0:10], len(lista_fin))
types_words_list = list(map(lambda x: x.upper(), set([elem[1] for elem in lista_fin])))
print(types_words_list)
print(len(max(types_words_list, key=len)))
print(max(lista_fin, key=(lambda x: len(x[2][0]))))

lista_fin = list(map(lambda x: (x[0], 'NOUN' if x[1] == 'n' else 'ADVERB' if x[1] == 'adv' else 'VERB' if x[1] == 'v' else 'ADJECTIVE' if x[1] == 'adj' else x[1].upper(), x[2]), lista_fin))


import psycopg2
conn = psycopg2.connect("REDACTED")

cur = conn.cursor()

for i in range(len(lista_fin)):
    cur.execute("INSERT INTO dictionary_word (mitronese_word, word_class, translation) VALUES (%s, %s, %s)", (lista_fin[i][0],lista_fin[i][1],lista_fin[i][2][0]))
    print(i)
conn.commit()
cur.close()
conn.close()