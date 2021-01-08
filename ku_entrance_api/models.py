from django.db import models
from django import forms

from django.conf import settings

# Create your models here.

class PayVerificationCode(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, to_field='username', on_delete=models.CASCADE)
    code = models.CharField(max_length=50, unique=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.code

    

class QstnSubject(models.Model):
    subject_name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.subject_name

    class Meta:
        verbose_name_plural = 'Subjects'



class QuestionManager(models.Manager):

    def fetch_next(self, question_id, answer, quiz_id):

        instance = Questions.objects.get(pk=question_id)

        level = instance.level

        quiz1 = Quiz.objects.get(id=quiz_id)

        if instance.answer == answer:

            if level == 1:
                quiz1.score += 11
                quiz1.save()
            elif level == 2:
                quiz1.score += 13
                quiz1.save()
            elif level == 3:
                quiz1.score += 15
                quiz1.save()
            elif level == 4:
                quiz1.score += 17
                quiz1.save()
            elif level == 5:
                quiz1.score += 19
                quiz1.save()


            if (level != 5):
                level += 1
        
        else:
            if (level != 1):
                level -= 1


        if instance.subject.subject_name == "Physics":

            if instance in quiz1.phys_question.all():
                return -1

            quiz1.phys_question.add(instance)
            
            quiz = Quiz.objects.filter(id=quiz_id).values('phys_question')
            print(quiz)

        elif instance.subject.subject_name == "Chemistry":

            if instance in quiz1.chem_question.all():
                return -1

            quiz1.chem_question.add(instance) 

            quiz = Quiz.objects.filter(id=quiz_id).values('chem_question')
            print(quiz)
        
        elif instance.subject.subject_name == "Mathematics":

            if instance in quiz1.math_question.all():
                return -1

            quiz1.math_question.add(instance)

            quiz = Quiz.objects.filter(id=quiz_id).values('math_question')
            print(quiz)

        
        return Questions.objects.exclude(id__in=quiz).filter(level=level, subject=instance.subject).order_by('?').first()



class Questions(models.Model):
    subject = models.ForeignKey(QstnSubject, on_delete=models.CASCADE)
    question = models.TextField(null=True, blank=True)
    level = models.IntegerField(default=1)

    option1 = models.TextField(null=True, blank=True)
    option2 = models.TextField(null=True, blank=True)
    option3 = models.TextField(null=True, blank=True)
    option4 = models.TextField(null=True, blank=True)
    
    choices = (
        ('a', option1),
        ('b', option2),
        ('c', option3),
        ('d', option4)
    )

    answer = models.CharField(max_length=2, choices=choices, null=True, blank=True)

    objects = QuestionManager()
    
    def __str__(self):
        return self.question



class Quiz(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='quiz', on_delete=models.CASCADE)
    quiz_name = models.CharField(max_length=75)
    activation_code = models.ForeignKey(PayVerificationCode, related_name='pay_code', on_delete=models.CASCADE)
    phys_question = models.ManyToManyField(Questions, related_name='phys', blank=True)
    chem_question = models.ManyToManyField(Questions, related_name='chem', blank=True)
    math_question = models.ManyToManyField(Questions, related_name='math', blank=True)
    score = models.IntegerField(default=0)

    def __str__(self):
        return self.quiz_name
