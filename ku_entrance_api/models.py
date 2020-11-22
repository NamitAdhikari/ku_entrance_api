from django.db import models
from django import forms
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager

# Create your models here.

class UserProfileManager(BaseUserManager):

    def create_user(self, username, name, password=None):

        if not username:
            raise ValueError('Username not provided')

        user = self.model(username=username, name=name)

        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_superuser(self, username, name, password):

        user = self.create_user(username, name, password)

        user.is_superuser = True
        user.is_staff = True

        user.save(using=self._db)
        return user


class UserProfile(AbstractBaseUser, PermissionsMixin):

    username = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['name',]

    objects = UserProfileManager()

    def __str__(self):
        return self.username



class QstnSubject(models.Model):
    subject_name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.subject_name




class QuestionManager(models.Manager):

    def fetch_next(self, obj, answer, quiz_id):

        instance = Questions.objects.get(pk=obj)

        level = instance.level

        if instance.answer == answer:
            if (level != 5):
                level += 1
        
        else:
            if (level != 1):
                level -= 1

        quiz1 = Quiz.objects.get(id=quiz_id)

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
    user = models.ForeignKey(UserProfile, related_name='quiz', on_delete=models.CASCADE)
    quiz_name = models.CharField(max_length=50)
    phys_question = models.ManyToManyField(Questions, related_name='phys', blank=True)
    chem_question = models.ManyToManyField(Questions, related_name='chem',blank=True)
    math_question = models.ManyToManyField(Questions, related_name='math',blank=True)
    score = models.IntegerField(default=0)


    def __str__(self):
        return self.quiz_name


