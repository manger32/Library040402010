# Generated by Django 4.2.3 on 2023-08-15 13:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_book_assigned_materials_library_entity_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='libraryentity',
            name='access_rights',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.authorize'),
        ),
    ]