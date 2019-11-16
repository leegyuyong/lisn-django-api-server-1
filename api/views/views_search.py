from log import log
import sys

from django.http import HttpResponse, JsonResponse, QueryDict
from django.conf import settings

from api.utils import remove_tag
from api.models import User, Note, Sentence, Share
from api.auth import auth_user_id, auth_note_id
from api.es_client.es_client import es

@auth_user_id
def search_by_title(request):
    user_id = int(request.GET.get('user_id'))
    query_word = request.GET.get('query')

    query = {'query':{'bool':{'must':[]}}}
    query['query']['bool']['must'].append({'match':{'title':query_word}})
    query['query']['bool']['must'].append({'term':{'user_id':user_id}})
    es_result = es.search(index='note', body=query)

    note_id_list = list()
    for note in es_result['hits']['hits']:
        note_id_list.append(int(note['_source']['note_id']))
    note_id_list = list(set(note_id_list))

    json_res = dict()
    json_res['notes'] = []

    user = User.objects.get(id=user_id)
    for note_id in note_id_list:
        note = Note.objects.get(id=note_id)
        full_content = remove_tag(note.content)
        summary = ''
        if len(full_content) > 40:
            summary = full_content[:40]
        else:
            summary = full_content
        
        color = 0
        if note.directory is None:
            color = -1
        else:
            color = note.directory.color

        is_shared = False
        share = Share.objects.filter(note_id=note.id)
        if share.exists():
            is_shared = True

        json_res['notes'].append({
            'user_email': user.email,
            'note_id': note.id,
            'title': note.title,
            'created_at': note.created_at,
            'updated_at': note.updated_at,
            'summary': summary,
            'color': color,
            'is_shared': is_shared,
            'num_of_share': len(share)
        })

    return JsonResponse(json_res, status=200)

@auth_user_id
def search_by_content(request):
    user_id = int(request.GET.get('user_id'))
    query_word = request.GET.get('query')

    query = {'query':{'bool':{'must':[]}}}
    query['query']['bool']['must'].append({'match':{'content':query_word}})
    query['query']['bool']['must'].append({'term':{'user_id':user_id}})
    es_result = es.search(index='note', body=query)

    note_id_list = list()
    for note in es_result['hits']['hits']:
        note_id_list.append(int(note['_source']['note_id']))
    note_id_list = list(set(note_id_list))

    json_res = dict()
    json_res['notes'] = []

    user = User.objects.get(id=user_id)
    for note_id in note_id_list:
        note = Note.objects.get(id=note_id)
        full_content = remove_tag(note.content)
        summary = ''
        if len(full_content) > 40:
            summary = full_content[:40]
        else:
            summary = full_content
        
        color = 0
        if note.directory is None:
            color = -1
        else:
            color = note.directory.color

        is_shared = False
        share = Share.objects.filter(note_id=note.id)
        if share.exists():
            is_shared = True

        json_res['notes'].append({
            'user_email': user.email,
            'note_id': note.id,
            'title': note.title,
            'created_at': note.created_at,
            'updated_at': note.updated_at,
            'summary': summary,
            'color': color,
            'is_shared': is_shared,
            'num_of_share': len(share)
        })

    return JsonResponse(json_res, status=200)

@auth_user_id
def search_by_sentence(request):
    user_id = int(request.GET.get('user_id'))
    query_word = request.GET.get('query')

    query = {'query':{'bool':{'must':[]}}}
    query['query']['bool']['must'].append({'match':{'content':query_word}})
    query['query']['bool']['must'].append({'term':{'user_id':user_id}})
    es_result = es.search(index='sentence', body=query)

    note_id_list = list()
    for sentence in es_result['hits']['hits']:
        note_id_list.append(int(sentence['_source']['note_id']))
    note_id_list = list(set(note_id_list))
    
    json_res = dict()
    json_res['notes'] = []

    user = User.objects.get(id=user_id)
    for note_id in note_id_list:
        note = Note.objects.get(id=note_id)
        full_content = remove_tag(note.content)
        summary = ''
        if len(full_content) > 40:
            summary = full_content[:40]
        else:
            summary = full_content
        
        color = 0
        if note.directory is None:
            color = -1
        else:
            color = note.directory.color

        is_shared = False
        share = Share.objects.filter(note_id=note.id)
        if share.exists():
            is_shared = True

        json_res['notes'].append({
            'user_email': user.email,
            'note_id': note.id,
            'title': note.title,
            'created_at': note.created_at,
            'updated_at': note.updated_at,
            'summary': summary,
            'color': color,
            'is_shared': is_shared,
            'num_of_share': len(share)
        })

    return JsonResponse(json_res, status=200)

@auth_note_id
def search_by_note_sentence(request):
    note_id = int(request.GET.get('note_id'))
    query_word = request.GET.get('query')

    query = {'query':{'bool':{'must':[]}}}
    query['query']['bool']['must'].append({'match':{'content':query_word}})
    query['query']['bool']['must'].append({'term':{'note_id':note_id}})
    es_result = es.search(index='sentence', body=query)

    sentence_id_list = list()
    for sentence in es_result['hits']['hits']:
        sentence_id_list.append(int(sentence['_source']['sentence_id']))
    sentence_id_list = list(set(sentence_id_list))

    json_res = dict()
    json_res['sentences'] = []

    for sentence_id in sentence_id_list:
        sentence = Sentence.objects.get(id=sentence_id)
        
        json_res['sentences'].append({
            'sentence_id': sentence.id,
            'started_at': sentence.started_at,
            'ended_at': sentence.ended_at,
            'content': sentence.content
        })

    return JsonResponse(json_res, status=200)

def search_user(request):
    query_str = request.GET.get('query')
    query_word = query_str.split('@')[0]

    query = {'query':{'prefix':{}}}
    query['query']['prefix']['email'] = {'value':query_word}
    es_result = es.search(index='user', body=query)

    json_res = dict()
    json_res['users'] = []

    for user in es_result['hits']['hits']:
        user_id = int(user['_id'])
        user_name = user['_source']['name']
        user_email = user['_source']['email']
        user_picture_url = user['_source']['picture_url']
        
        if len(query_word) > 0:
            if query_word[0] != user_email[0]:
                continue
                
        json_res['users'].append({
            'user_id': user_id,
            'user_name': user_name,
            'user_email': user_email,
            'user_picture_url': user_picture_url
        })
        
        if len(json_res['users']) >= 5:
            break

    return JsonResponse(json_res, status=200)

@log
def api_search_title(request):
    try:
        if request.method == 'GET':
            return search_by_title(request)
        else:
            return HttpResponse(status=405)
    except:
        print("Unexpected error:", sys.exc_info()[0])
        return HttpResponse(status=400)

@log
def api_search_content(request):
    try:
        if request.method == 'GET':
            return search_by_content(request)
        else:
            return HttpResponse(status=405)
    except:
        print("Unexpected error:", sys.exc_info()[0])
        return HttpResponse(status=400)

@log
def api_search_sentence(request):
    try:
        if request.method == 'GET':
            return search_by_sentence(request)
        else:
            return HttpResponse(status=405)
    except:
        print("Unexpected error:", sys.exc_info()[0])
        return HttpResponse(status=400)

@log
def api_search_note_sentence(request):
    try:
        if request.method == 'GET':
            return search_by_note_sentence(request)
        else:
            return HttpResponse(status=405)
    except:
        print("Unexpected error:", sys.exc_info()[0])
        return HttpResponse(status=400)

@log
def api_search_user(request):
    try:
        if request.method == 'GET':
            return search_user(request)
        else:
            return HttpResponse(status=405)
    except:
        print("Unexpected error:", sys.exc_info()[0])
        return HttpResponse(status=400)