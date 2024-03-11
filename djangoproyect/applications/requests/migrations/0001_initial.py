# Generated by Django 4.2.11 on 2024-03-11 00:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Involved',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=320)),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Requests',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('document', models.CharField(max_length=255)),
                ('applicant', models.CharField(max_length=100)),
                ('manager', models.CharField(max_length=100)),
                ('initial_date', models.DateField()),
                ('final_date', models.DateField()),
                ('past_days', models.IntegerField()),
                ('status', models.CharField(max_length=20)),
                ('beneficiary', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='beneficiario', to='requests.involved')),
                ('final_approver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='aprobador_final', to='requests.involved')),
                ('reviewer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='revisor', to='requests.involved')),
            ],
        ),
        migrations.CreateModel(
            name='Traceability',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('involved', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='requests.involved')),
                ('request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='requests.requests')),
            ],
        ),
    ]
