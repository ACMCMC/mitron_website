from django.db import models

# Create your models here.


class OriginLanguage(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Word(models.Model):
    mitronese_word = models.CharField(max_length=40)
    translation = models.CharField(max_length=40)
    WORD_CLASSES = [(word.upper(), word) for word in ['AFFIX', 'NOUN', 'PROVERB', 'POSTPOSITION', 'VERB', 'ADJECTIVE', 'ARTICLE', 'PRONOUN', 'PREPOSITION', 'ADVERB', 'INTERJECTION', 'CONJUNCTION']]
    word_class = models.CharField(max_length=15, choices=WORD_CLASSES)
    orig_language = models.ManyToManyField(OriginLanguage)

    def __str__(self):
        return self.mitronese_word + " -> " + self.spanish_word
