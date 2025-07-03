from django.core.management.base import BaseCommand
from chatbot.vanna_integration import vn

class Command(BaseCommand):
    help = 'Train the Vanna AI model with university data'
    
    def handle(self, *args, **options):
        vn.train(ddl=open("schema.sql", encoding="utf-8").read())
        
        # [Add all your training examples and documentation]
        
        self.stdout.write(self.style.SUCCESS('Successfully trained Vanna model'))