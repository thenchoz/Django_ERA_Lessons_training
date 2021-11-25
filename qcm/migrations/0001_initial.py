# Generated by Django 3.2.9 on 2021-11-18 19:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_text', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='QuestionsSet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('polymorphic_ctype', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_qcm.questionsset_set+', to='contenttypes.contenttype')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
        ),
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('questionsset_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='qcm.questionsset')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('qcm.questionsset',),
        ),
        migrations.CreateModel(
            name='QuestionsSubset',
            fields=[
                ('questionsset_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='qcm.questionsset')),
                ('parent_branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='qcm.branch')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('qcm.questionsset',),
        ),
        migrations.CreateModel(
            name='Choice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('choice_text', models.CharField(max_length=200)),
                ('is_true', models.BooleanField()),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='qcm.question')),
            ],
        ),
        migrations.CreateModel(
            name='Training',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('choice_order', models.CharField(max_length=250, null=True)),
                ('questions_answers', models.CharField(max_length=250, null=True)),
                ('training_date', models.DateTimeField(auto_now=True, verbose_name='Training date')),
                ('results', models.DecimalField(decimal_places=2, max_digits=5, null=True)),
                ('nb_questions', models.SmallIntegerField(default=30)),
                ('questions', models.ManyToManyField(to='qcm.Question')),
                ('questions_set', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='qcm.questionssubset')),
            ],
        ),
        migrations.AddField(
            model_name='question',
            name='questions_subset',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='qcm.questionssubset'),
        ),
    ]