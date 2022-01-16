from django.core.management.base import BaseCommand, CommandError
from radio.models import Radio
import yaml


class Command(BaseCommand):
    help = 'Create radio'

    def handle(self, *args, **options):
        with open('radio\management\commands\data.yaml',encoding='UTF-8') as f:
            radios = yaml.load_all(f, Loader=yaml.FullLoader)
            for radio in radios:
                try:
                    id = radio['id']
                    title = radio['title']
                    contents = radio['contents']

                    Radio_Post = Radio(id=id,title=title,contents=contents)
                    Radio_Post.save()

                    print(f'Successfully make Radio {title}')
                except Exception as e:
                    print(f'Error {e}')
