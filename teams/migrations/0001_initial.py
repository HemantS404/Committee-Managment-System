# Generated by Django 4.1.3 on 2022-12-31 22:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('team_name', models.CharField(max_length=20)),
                ('Mentee', models.ManyToManyField(to='accounts.cocom')),
                ('Mentors', models.ManyToManyField(to='accounts.core')),
                ('belongs_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Committee', to='accounts.committee')),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_name', models.CharField(max_length=20)),
                ('description', models.CharField(max_length=200)),
                ('material', models.FileField(upload_to='Tasks/')),
                ('assigned_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Core', to='accounts.core')),
                ('team_assign', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Team', to='teams.team')),
            ],
        ),
        migrations.CreateModel(
            name='AssignedTo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('submitted', models.BooleanField(default=False)),
                ('comments', models.CharField(blank=True, max_length=200, null=True)),
                ('repo_link', models.URLField(blank=True, null=True)),
                ('upload', models.FileField(blank=True, null=True, upload_to='')),
                ('assgined_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assigned_to', to='accounts.cocom')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Task', to='teams.task')),
            ],
        ),
    ]
