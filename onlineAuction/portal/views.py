from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.urls import reverse
from django.views import generic
from django.utils import timezone, dateparse
# Create your views here.
from datetime import datetime, timedelta
from signup.models import UserDetail
from portal.models import articlereg

from portal.models import banned_user


def isadmin(request):
    if 'adminSession' in request.session:
        if request.session['adminSession'] == True:
            return True
        else:
            return False
    else:
        return False


class AdminIndexView(generic.TemplateView):
    template_name = 'portal/adminPage.html'

    def get(self, request, *args, **kwargs):
        try:
            if isadmin(request):
                context = {'details': UserDetail.objects.all()}
                return render(request, self.template_name, context)
            else:
                return HttpResponse("Login as admin to proceed.")
        except:
            pass

    def deleteUser(request, id):
        if isadmin(request):
            b = UserDetail.objects.get(pk=id)
            b.delete()
            return HttpResponseRedirect(reverse('portal:adminPage'))
        else:
            return HttpResponse("Login as admin to proceed.")

    def banUser(request, id):
        if isadmin(request):
            if banned_user.objects.filter(userid=id).exists():
                pass
            else:
                ob = banned_user(userid=id)
                ob.save()
            return HttpResponseRedirect(reverse('portal:adminPage'))
        else:
            return HttpResponse("Login as admin to proceed.")

class ArticleView(generic.TemplateView):
    template_name = 'portal/adminPageShowArticles.html'

    def get(self, request, id, *args, **kwargs):
        try:
            if isadmin(request):
                context = {'details': articlereg.objects.filter(userid=id)}
                return render(request, self.template_name, context)
            else:
                return HttpResponse("Login as admin to proceed.")
        except:
            pass

    def deleteArticle(request, userid, id):
        if isadmin(request) or (('inSession' in request.session) and request.session['inSession'] == True):
            b = articlereg.objects.get(pk=id)
            b.delete()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            return HttpResponse("Login as admin to proceed.")



class ActiveBidView(generic.TemplateView):
    template_name = 'portal/activeArticles.html'

    def get(self, request, *args, **kwargs):
        try:
            if (('inSession' in request.session) and request.session['inSession'] == True):
                quer = UserDetail.objects.get(pk=request.session['userID'])
                articles = articlereg.objects.all()
                active_articles = []
                now = timezone.now()
                for a in articles:
                    endtime = a.timestart + timedelta(hours=1)
                    if now >= a.timestart and now < endtime:
                        active_articles.append(a.id)
                context = {'userName': quer.name, 'active': articlereg.objects.filter(id__in=active_articles)}
                template_name = 'portal/activeArticles.html'
                return render(request, template_name, context)
            else:
                return HttpResponse("Login as user to proceed.")
        except:
            pass



class RecentBidView(generic.TemplateView):
    template_name = 'portal/activeArticles.html'

    def get(self, request, *args, **kwargs):
        try:
            if (('inSession' in request.session) and request.session['inSession'] == True):
                quer = UserDetail.objects.get(pk=request.session['userID'])
                articles = articlereg.objects.all()
                recent_bids = []
                now = timezone.now()
                for a in articles:
                    if a.timestart < (now - timedelta(hours=1)) and a.timestart > (now - timedelta(days=1, hours=1)):
                        recent_bids.append(a.id)
                context = {'userName': quer.name, 'bid': bids.objects.filter(articleid__in=recent_bids)}
                template_name = 'portal/recentArticles.html'
                return render(request, template_name, context)
            else:
                return HttpResponse("Login as user to proceed.")
        except:
            pass


from .forms import *


class IndexView(generic.TemplateView):
    template_name = 'portal/index.html'

    def get(self, request, *args, **kwargs):
        try:
            if 'userID' in request.session and request.session['userID'] != None:
                context = {'userName': UserDetail.objects.get(pk=request.session['userID']).name}
                return render(request, self.template_name, context)
            else:
                return HttpResponseRedirect(reverse("signup:LoginForm"))

        except UserDetail.DoesNotExist:
            return HttpResponseRedirect(reverse("signup:LoginForm"))


class RegForm(generic.edit.FormView):
    form_class = RegForm
    template_name = 'portal/articleForm.html'

    def get(self, request, *args, **kwargs):
        context = {'userName': UserDetail.objects.get(pk=request.session['userID']).name, 'form': self.form_class}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        try:
            quer = UserDetail.objects.get(pk=request.session['userID'])
            time = dateparse.parse_datetime(request.POST['timestart'])
            now = datetime.now()
            deltaNow = timedelta(days=int(now.day), hours=int(now.hour), minutes=int(now.minute),
                                 seconds=int(now.second))
            delta = timedelta(days=int(time.day), hours=int(time.hour), minutes=int(time.minute),
                              seconds=int(time.second))
            timedif = (delta - deltaNow).seconds
            deltaHour = timedelta(seconds=3600)
            if (delta < deltaNow - deltaHour):
                return HttpResponse("ENTER CORRECT DATE TIME")
            art = quer.articlereg_set.create(
                timestart=request.POST['timestart'], articlename=request.POST['articlename'],
                category=request.POST['category'], desc=request.POST['desc'],
                minbid=request.POST['minbid'])
            art.articleimage_set.create(image=request.FILES['image'])
            art.bids_set.create(userid=UserDetail.objects.get(pk=request.session['userID']),
                                highestbid=request.POST['minbid'])
            return HttpResponseRedirect(reverse("portal:userArticles"))
        except UserDetail.DoesNotExist:
            return HttpResponse("Article NOT Registered.")


class EditArticle(generic.edit.FormView):
    form_class = EditRegForm
    template_name = 'portal/articleForm.html'

    def get(self, request, a_id, *args, **kwargs):
        data = articlereg.objects.get(pk=int(a_id))
        form = self.form_class(initial={'timestart': data.timestart,
                                        'articlename': data.articlename,
                                        'category': data.category,
                                        'desc': data.desc,
                                        'minbid': data.minbid,
                                        })

        context = {'userName': UserDetail.objects.get(pk=request.session['userID']).name,
                   'form': form}
        return render(request, self.template_name, context)

    def post(self, request, a_id, *args, **kwargs):
        try:
            quer = UserDetail.objects.get(pk=request.session['userID'])
            art = quer.articlereg_set.get(pk=int(a_id))
            art.timestart = request.POST['timestart']
            art.articlename = request.POST['articlename']
            art.category = request.POST['category']
            art.desc = request.POST['desc']
            art.minbid = request.POST['minbid']
            img = art.articleimage_set.reverse()[0]
            img.image = request.FILES['image']
            # time check
            time = dateparse.parse_datetime(request.POST['timestart'])
            now = datetime.now()
            deltaNow = timedelta(days=int(now.day), hours=int(now.hour), minutes=int(now.minute),
                                 seconds=int(now.second))
            delta = timedelta(days=int(time.day), hours=int(time.hour), minutes=int(time.minute),
                              seconds=int(time.second))
            deltaHour = timedelta(seconds=3600)
            timedif = (delta - deltaNow).seconds
            if (delta < deltaNow - deltaHour):
                return HttpResponse("ENTER CORRECT DATE TIME")
            img.save()
            art.save()
            art.bids_set.reverse()[0].highestbid = art.minbid
            return HttpResponseRedirect(reverse("portal:userArticles"))
        except UserDetail.DoesNotExist:
            return HttpResponse("Article NOT Registered.")


class UserShowArticles(generic.TemplateView):
    template_name = 'portal/usershowarticle.html'

    def get(self, request, *args, **kwargs):
        quer = UserDetail.objects.get(pk=request.session['userID'])
        context = {'details': articlereg.objects.filter(userid=quer), 'userName': quer.name}
        return render(request, self.template_name, context)


class Bid(generic.edit.FormView):
    form_class = BidPrice
    template_name = 'portal/BidArticle.html'

    def get(self, request, a_id, *args, **kwargs):
        quer = UserDetail.objects.get(pk=request.session['userID'])
        if (quer.visa_set.count() == 0):
            return HttpResponseRedirect(reverse("signup:VisaForm"))
        context = {'bid': articlereg.objects.get(pk=a_id).bids_set.reverse()[0], 'userName': quer.name, 'quer': quer,
                   'form': self.form_class}
        return render(request, self.template_name, context)

    def post(self, request, a_id, *args, **kwargs):
        bid = articlereg.objects.get(pk=a_id).bids_set.reverse()[0]
        if (bid.highestbid < float(request.POST['highestbid'])):
            bid.highestbid = float(request.POST['highestbid'])
            bid.userid = UserDetail.objects.get(pk=request.session['userID'])
            bid.save()
            return HttpResponseRedirect("/portal/activeArticles/BidPage/" + str(a_id))
        else:
            pass


