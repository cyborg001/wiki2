from django.shortcuts import render
from django.http import  HttpResponseRedirect
from django.urls import reverse
import markdown2 as mk
import random
from .models import Procedimiento
from .forms import MyForm, NewPageForm


def index(request):
    '''si el metodo es POST y los datos son validos investiga si la wiki
        digitada existe, si existe nos redirecciona a ella, sino nos envia
        una lista con todas las wikis cuyo nombre contegan la substring
        digitada. por otro lado si el metodo es GET entonces nos envia a
        una lista con todas las wikis existentes'''

    form = MyForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            name = form.cleaned_data['Entry']
            entry = Procedimiento.objects.filter(title=name).first()
            if entry != None:
                return HttpResponseRedirect(reverse('wiki',args=(name,)))
            else:
                l = [e.serialize() for e in Procedimiento.objects.all() if e.title.lower().startswith(name.lower())]# if name in e.title.lower()]
                return render(request,'encyclopedia/index.html',{
                    'entries':l,
                    'form':MyForm()
                })

        else:
            return render(request,'encyclopedia/index.html',{
                'form':form
            })
    entries = Procedimiento.objects.all()
    
    entries = [procedimiento.serialize() for procedimiento in entries]
    return render(request,'encyclopedia/index.html',{
        "entries":entries,
        'form':MyForm(),
    })


def wiki(request,name):
    '''esta funcion que acepta request y a name como parametro se
        asegura de devolver la wiki en formato html para que pueda ser
        visualizada por los usuarios. si la wiki no existe devuelve
        un error diciendo que la wiki no fue encontrada'''
        
    form = MyForm()
    procedimiento = Procedimiento.objects.filter(title=name)
    print(procedimiento)
    if procedimiento.first() == None or procedimiento.first() == '':
        print('es nulo')
        return render(request, 'encyclopedia/wiki.html', {
            'entry':f'Error the {name} page was not found.',
            'name':'Error',
            'form':form,
        })
    entry = procedimiento.first() 
    title = entry.title.capitalize()
    contenido = mk.markdown(f'# {title} \n{entry.content}')
    return render(request, 'encyclopedia/wiki.html', {
        'entry':entry,
        'content':contenido,
        'form':form,
    })
def random_page(request):
    '''Esta funcion devuelve una wiki aleatoria de las existentes  '''
    l = [entry for entry in Procedimiento.objects.all()]
    num = random.randint(0,len(l)-1)
    entry = l[num]
    print(l[num].title)
    return HttpResponseRedirect(reverse('ency:wiki',args=(entry.title,)))

def new_page(request):
    '''Esta funcion nos permite crear nuestra propia wiki, llenando un titulo
        para el titulo de la pagina y un contenido en formato Markdown para que
        el creador pueda desarrollar contenido mucho mas facil y rapido
        aqui pueden ir a una pagina acerca de este formato:
        https://docs.github.com/en/github/writing-on-github/basic-writing-and-formatting-syntax'''

    form  = MyForm()
    newPageForm = NewPageForm(request.POST)
    if request.method == 'POST':
        if newPageForm.is_valid():
            title = newPageForm.cleaned_data['title']
            content = newPageForm.cleaned_data['content']
            if Procedimiento.objects.filter(title=title).first() != None:
                # print()
                return render(request, 'encyclopedia/new_page.html', {
                    'form':form,
                    'newPageForm':newPageForm,
                    'error':'Error the entry already exists!',
                })
            else:
                entry = Procedimiento.objects.create(title=title,content=content)
                entry.save()
                return HttpResponseRedirect(reverse('ency:wiki',args=(entry.title,)))

    return render(request, 'encyclopedia/new_page.html', {
        'form':form,
        'newPageForm':NewPageForm()
    })

def edit(request):
    '''Esta funcion nos permite editar una pagina visitada dandole al link
        "click hera for edit page" nos permite ir a una pagina para la ediccion
        de nuestra wiki'''

    form = MyForm()
    newPageForm = NewPageForm(request.POST)
    if request.method == 'POST':
        if newPageForm.is_valid():
            title = newPageForm.cleaned_data['title']
            content = newPageForm.cleaned_data['content']
            entry = Procedimiento.objects.get(title=title)
            entry.content = content
            entry.save()
            return HttpResponseRedirect(reverse('ency:wiki',args=(title,)))
    title = request.headers['Referer'].split('/')[-1]
    entry = Procedimiento.objects.get(title=title)
    request.POST ={'title':entry.title,'content':entry.content}
    return render(request, 'encyclopedia/edit.html', {
        'form': form,
        'newPageForm':NewPageForm(request.POST),
        'error':'',
    })
