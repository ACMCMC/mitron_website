from django.db import models

# Create your models here.


class OriginLanguage(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Word(models.Model):
    mitronese_word = models.CharField(max_length=30)
    spanish_word = models.CharField(max_length=30)
    WORD_CLASSES = [(word[2], word) for word in ["Nombre", "Pronombre", "Verbo",
                                                 "Adjetivo", "Adverbio", "Preposición", "Conjunción", "Interjección"]]
    word_class = models.CharField(max_length=1, choices=WORD_CLASSES)
    orig_language = models.ManyToManyField(OriginLanguage)

    def __str__(self):
        return self.mitronese_word + " -> " + self.spanish_word
