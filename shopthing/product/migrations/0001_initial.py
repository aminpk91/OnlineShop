# Generated by Django 3.2.7 on 2021-10-06 08:44

from django.db import migrations, models
import django.db.models.deletion
import product.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Brands',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Cat_attr',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attr_name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('cat_parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='child_cat', to='product.category')),
            ],
        ),
        migrations.CreateModel(
            name='Productbase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField(blank=True, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('previous_price', models.FloatField(default=0.0)),
                ('price', models.FloatField(default=0.0)),
                ('added_time', models.DateTimeField(auto_now_add=True)),
                ('qty', models.IntegerField(default=1)),
                ('rate', models.IntegerField(default=3)),
                ('brand', models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, to='product.brands')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='product.category')),
            ],
        ),
        migrations.CreateModel(
            name='ProductComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.CharField(default='????????????', max_length=255)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('body', models.TextField(null=True)),
                ('article', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comment', to='product.productbase')),
                ('reply_to', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='product.productcomment')),
            ],
        ),
        migrations.CreateModel(
            name='Product_attr',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attr', models.CharField(max_length=255)),
                ('cat_attr', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.cat_attr')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.productbase')),
            ],
        ),
        migrations.CreateModel(
            name='ImageProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to=product.models.model_image_directory_path)),
                ('default', models.BooleanField(default=False)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='img', to='product.productbase')),
            ],
        ),
        migrations.AddField(
            model_name='cat_attr',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.category'),
        ),
    ]
