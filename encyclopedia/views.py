import http
from http.client import REQUEST_ENTITY_TOO_LARGE
from django.shortcuts import render
from django.http import  HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views import generic
import markdown2 as mk
import random
from .models import Procedimiento
from .forms import MyForm, NewPageForm
from django.views.generic.edit import FormView
from django.contrib.auth import logout, authenticate, login

def buscar(request):
    name = request.POST['procedimiento']
    procedimientos = Procedimiento.objects.all()
    lista = []
    print(name)
    for n in procedimientos:

        if name == n.title:
            print(n.pk)
            return HttpResponseRedirect(reverse('ency:wiki',args=(n.pk,)))
        else:
            if name in n.title:
                lista.append(n)
    if lista != []:
        return render(request,'encyclopedia/index.html',{"procedimiento_list":lista})
    else:
        return HttpResponseRedirect(reverse('ency:index'))
    pass

def loggout(request):
    logout(request)
    return HttpResponseRedirect(reverse('ency:index'))

def loggin(request):
    if request.method == 'POST':
        print('espost')
        previa = request.POST['fprevia']
        
        page = previa.split(request.headers['Origin'])[-1]
        username = request.POST['fusername']
        password = request.POST['fpassword']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page.
            # return render(request, previa)
            print(page)
            if page != '/' and page != '/edit':
                return HttpResponseRedirect(reverse(f'ency:wiki',args=(int(page[1:]),)))
            else:
                return HttpResponseRedirect(reverse('ency:index'))
            
        else:
            
            print('distinto')
            context = {'username':username,
                        'error': 'Usuario o contraseña incorrecta!',
                        "previa":previa}
            return render(request,'encyclopedia/login.html',context)
            
    print(request.headers['Referer'])
    
    return render(request, 'encyclopedia/login.html',{'previa':request.headers['Referer']})

class IndexView(generic.ListView):
    template_name = 'encyclopedia/index.html'
    context_object_name = 'procedimiento_list'
    
    def get_queryset(self):
        return Procedimiento.objects.all()



class WikiView(generic.DetailView):
    model = Procedimiento
    template_name = 'encyclopedia/wiki.html'
   
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        title = context['object'].title
        content = context['object'].content
        pre_text = mk.markdown(f'# {title} \n{content}')
        context['pre_text'] = pre_text
        return context

def random_page(request):
    '''Esta funcion devuelve una wiki aleatoria de las existentes  '''
    l = [entry for entry in Procedimiento.objects.all()]
    num = random.randint(0,len(l)-1)
    entry = l[num]
    # print(l[num].pk)
    return HttpResponseRedirect(reverse('ency:wiki',args=(entry.pk,)))

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
                    # 'form':form,  
                    'newPageForm':newPageForm,
                    'error':'Error the entry already exists!',
                })
            else:
                entry = Procedimiento.objects.create(title=title,content=content)
                entry.save()
                return HttpResponseRedirect(reverse('ency:wiki',args=(entry.pk,)))

    return render(request, 'encyclopedia/new_page.html', {
        # 'form':form,
        'newPageForm':NewPageForm()
    })

def edit(request,pk):
    '''Esta funcion nos permite editar una pagina visitada dandole al link
        "click hera for edit page" nos permite ir a una pagina para la ediccion
        de nuestra wiki'''
    print(pk)
    form = MyForm()
    newPageForm = NewPageForm(request.POST)
    if request.method == 'POST':
        if newPageForm.is_valid():
            title = newPageForm.cleaned_data['title']
            content = newPageForm.cleaned_data['content']
            entry = Procedimiento.objects.get(title=title)
            entry.content = content
            entry.save()
            return HttpResponseRedirect(reverse('ency:wiki',args=(pk,)))
    
    # title = request.headers['Referer'].split('/')[-1]
    entry = Procedimiento.objects.get(pk=pk)
    request.POST ={'title':entry.title,'content':entry.content, 'pk':entry.pk}
    return render(request, 'encyclopedia/edit.html', {
        'form': form,
        'newPageForm':NewPageForm(request.POST),
        'error':'',
        'pk':pk,
    })

class ProcedimientoDeleteView(generic.DeleteView):
    model = Procedimiento
    success_url = reverse_lazy('ency:index')
