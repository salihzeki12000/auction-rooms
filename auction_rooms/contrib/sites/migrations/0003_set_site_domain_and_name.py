"""
To understand why this file is here, please read:

http://cookiecutter-django.readthedocs.io/en/latest/faq.html#why-is-there-a-django-contrib-sites-directory-in-cookiecutter-django
"""
from django.conf import settings
from django.db import migrations


def update_site_forward(apps, schema_editor):
    """Set site domain and name."""
    Site = apps.get_model('sites', 'Site')
    Site.objects.update_or_create(
        id=1,
        domain='auction_rooms.sonick.co.uk',
        name='Auction Rooms'
    )
    Site.objects.create(
        id=2,
        domain='localhost:8000',
        name='Auction Rooms Dev'
    )


def update_site_backward(apps, schema_editor):
    """Revert site domain and name to default."""
    Site = apps.get_model('sites', 'Site')
    Site.objects.update_or_create(
        id=1,
        defaults={
            'domain': 'example.com',
            'name': 'example.com'
        }
    )
    Site.objects.get(pk=1).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0002_alter_domain_unique'),
    ]

    operations = [
        migrations.RunPython(update_site_forward, update_site_backward),
    ]
