from django.shortcuts import render
from django.http import JsonResponse
from django.utils.translation import gettext as _
from .vanna_integration import vn, run_query, validate_sql
from .models import QueryLog
import json

def index(request):
    return render(request, 'chatbot/index.html')

def ask_question(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            question = data.get('question')
            lang = data.get('lang', 'en')
            
            # Set up language context
            request.LANGUAGE_CODE = lang
            
            # Generate SQL
            sql = vn.generate_sql(question)
            
            if not validate_sql(sql):
                return JsonResponse({'error': _('The SQL might be invalid or unsafe to run.')})
            
            # Execute query
            results = run_query(sql)
            
            # Log the query
            QueryLog.objects.create(
                question=question,
                sql=sql,
                results=str(results),
                language=lang
            )
            
            return JsonResponse({
                'sql': sql,
                'results': results,
                'lang': lang
            })
            
        except Exception as e:
            return JsonResponse({'error': str(e)})
    
    return JsonResponse({'error': 'Invalid request method'})