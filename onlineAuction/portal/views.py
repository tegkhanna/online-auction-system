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
from .forms import *

from django.contrib import messages



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
                messages.error(request,"You are not authorised.")
                return HttpResponseRedirect(reverse('portal:index'))
        except:
            pass

    def deleteUser(request, id):
        if isadmin(request):
            b = UserDetail.objects.get(pk=id)
            b.delete()
            messages.success(request, "User deleted successfully")
            return HttpResponseRedirect(reverse('portal:adminPage'))
        else:
            messages.error(request, "You are not authorised.")
            return HttpResponseRedirect(reverse('portal:index'))

    def banUser(request, id):
        if isadmin(request):
            if banned_user.objects.filter(userid=id).exists():
                pass
            else:
                ob = banned_user(userid=id)
                ob.save()
                messages.success(request, "User banned")
            return HttpResponseRedirect(reverse('portal:adminPage'))
        else:
            messages.error(request, "You are not authorised.")
            return HttpResponseRedirect(reverse('portal:index'))

class ArticleView(generic.TemplateView):
    template_name = 'portal/adminPageShowArticles.html'

    def get(self, request, id, *args, **kwargs):
        try:
            if isadmin(request):
                context = {'details': articlereg.objects.filter(userid=id)}
                return render(request, self.template_name, context)
            else:
                messages.error(request, "You are not authorised.")
                return HttpResponseRedirect(reverse('portal:index'))
        except:
            pass

    def deleteArticle(request, userid, id):
        if isadmin(request) or (('inSession' in request.session) and request.session['inSession'] == True):
            b = articlereg.objects.get(pk=id)
            if isadmin(request)==False and (b.timestart<timezone.now()):
                messages.error(request, "Ended or active bids cannot be deleted")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            else:
                try:
                    b.delete()
                    messages.success(request, "Article deleted")
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
                except:
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        else:
            messages.error(request, "You are not authorised.")
            return HttpResponseRedirect(reverse('portal:index'))



class ActiveBidView(generic.TemplateView):
    template_name = 'portal/activeArticles.html'

    def get(self, request, *args, **kwargs):
        try:
            if (('inSession' in request.session) and request.session['inSession'] == True) or isadmin(request):
                quer = UserDetail.objects.get(pk=request.session['userID'])
                articles = articlereg.objects.all()
                active_articles = []
                now = timezone.now()
                for a in articles:
                    endtime = a.timestart + timedelta(hours=1)
                    if now >= a.timestart and now < endtime:
                        active_articles.append(a.id)
                context = {'userName': quer.name, 'active': articlereg.objects.filter(id__in=active_articles)}
                return render(request, self.template_name, context)
            else:
                messages.error(request, "Login or signup to proceed.")
                return HttpResponseRedirect(reverse('portal:index'))
        except:
            pass



class RecentBidView(generic.TemplateView):
    template_name = 'portal/recentArticles.html'

    def get(self, request, *args, **kwargs):
        try:
            if (('inSession' in request.session) and request.session['inSession'] == True) or isadmin(request):
                quer = UserDetail.objects.get(pk=request.session['userID'])
                articles = articlereg.objects.all()
                recent_bids = []
                now = timezone.now()
                for a in articles:
                    if a.timestart < (now - timedelta(hours=1)) and a.timestart > (now - timedelta(days=1, hours=1)):
                        recent_bids.append(a.id)
                        a.status = "sold"
                        a.save()
                context = {'userName': quer.name, 'bid': bids.objects.filter(articleid__in=recent_bids)}
                return render(request, self.template_name, context)
            else:
                messages.error(request, "Login or signup to proceed.")
                return HttpResponseRedirect(reverse('portal:index'))
        except:
            pass



























class IndexView(generic.TemplateView):
    template_name = 'portal/index.html'

    def get(self, request, *args, **kwargs):
        try:
            if 'userID' in request.session and request.session['userID'] != None:
                quer = UserDetail.objects.get(pk=request.session['userID'])
                arts = privateusers.objects.all()
                articles = []
                now = timezone.now()
                for art in arts:
                    endtime = art.article.timestart + timedelta(hours=1)
                    if now >= art.article.timestart and now < endtime:
                        if(art.user == quer):
                            articles.append(art.article)
                arts = articlereg.objects.filter(category = quer.interests)
                interest = []
                now = timezone.now()
                for art in arts:
                    endtime = art.timestart + timedelta(hours=1)
                    if now >= art.timestart and now < endtime:
                        interest.append(art)

                context = {'userName': quer.name, 'article': articles, 'interest':interest}
                return render(request, self.template_name, context)
            else:
                return HttpResponseRedirect(reverse("signup:LoginForm"))
        except UserDetail.DoesNotExist:
            return HttpResponseRedirect(reverse("signup:LoginForm"))


class RegForm(generic.edit.FormView):
    form_class = RegForm
    template_name = 'portal/articleForm.html'

    def get(self, request, *args, **kwargs):
        try:
            context = {'userName': UserDetail.objects.get(pk=request.session['userID']).name, 'form': self.form_class}
            return render(request, self.template_name, context)
        except:
            return HttpResponseRedirect(reverse('signup:index'))
    def post(self, request, *args, **kwargs):
        try:
            stat = None
            quer = UserDetail.objects.get(pk=request.session['userID'])
            try:
                time = dateparse.parse_datetime(request.POST['timestart'])
            except ValueError:
                messages.error(request,"Enter correct date time values")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

            now = datetime.now()
            deltaNow = timedelta(days=int(now.day), hours=int(now.hour), minutes=int(now.minute),
                                 seconds=int(now.second))
            try:
                delta = timedelta(days=int(time.day), hours=int(time.hour), minutes=int(time.minute),
                              seconds=int(time.second))
            except AttributeError:
                messages.error(request, "Enter correct date time values")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            timedif = (delta - deltaNow).seconds
            deltaHour = timedelta(seconds=3600)
            if (time < (now - timedelta(hours=1))):
                messages.error(request, "Enter correct date time.")
                return HttpResponseRedirect(reverse("portal:RegForm"))
            if(delta > deltaNow):
                stat = "inactive"
            elif(delta > deltaNow - deltaHour):
                stat = "active"
            try :
                request.POST['private'] == 'on'
                priv = True
            except:
                priv = False
            art = quer.articlereg_set.create(
                timestart=request.POST['timestart'], articlename=request.POST['articlename'],
                category=request.POST['category'], desc=request.POST['desc'],
                minbid=request.POST['minbid'], status = stat,
                private = priv)
            art.articleimage_set.create(image=request.FILES['image'])
            USERS = request.POST.getlist('Select_Users')
            if(priv) is True:
                for users in USERS:
                    art.privateusers_set.create(user = UserDetail.objects.get(name = str(users)))
            art.bids_set.create(userid=UserDetail.objects.get(pk=request.session['userID']),
                                highestbid=request.POST['minbid'])
            art.save()
            messages.success(request, "Article registered.")
            return HttpResponseRedirect(reverse("portal:userArticles"))
        except UserDetail.DoesNotExist:
            messages.error(request, "You are not authorised.")
            return HttpResponseRedirect(reverse("portal:index"))


class EditArticle(generic.edit.FormView):
    form_class = EditRegForm
    template_name = 'portal/articleForm.html'

    def get(self, request, a_id, *args, **kwargs):
        data = articlereg.objects.get(pk=int(a_id))
        if data.timestart<timezone.now():
            messages.error(request,"Active or ended bids cannot be edited.")
            return HttpResponseRedirect(reverse('portal:userArticles'))
        else:
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
            stat = None
            quer = UserDetail.objects.get(pk=request.session['userID'])
            try :
                request.POST['private'] == 'on'
                priv = True
            except:
                priv = False

            art = quer.articlereg_set.get(pk=int(a_id))
            art.private = priv
            USERS = request.POST.getlist('Select_Users')
            if(priv) is True:
                for users in USERS:
                    art.privateusers_set.create(user = UserDetail.objects.get(name = str(users)))
            art.timestart = request.POST['timestart']
            art.articlename = request.POST['articlename']
            art.category = request.POST['category']
            art.desc = request.POST['desc']
            art.minbid = request.POST['minbid']
            img = art.articleimage_set.reverse()[0]
            img.image = request.FILES['image']
            # time check
            try:
                time = dateparse.parse_datetime(request.POST['timestart'])
            except ValueError:
                messages.error(request,"Enter correct date time values")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            now = datetime.now()
            deltaNow = timedelta(days=int(now.day), hours=int(now.hour), minutes=int(now.minute),
                                 seconds=int(now.second))
            try:
                delta = timedelta(days=int(time.day), hours=int(time.hour), minutes=int(time.minute),
                              seconds=int(time.second))
            except AttributeError:
                messages.error(request, "Enter correct date time values")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            deltaHour = timedelta(seconds=3600)
            timedif = (delta - deltaNow).seconds
            if (time < (now - timedelta(hours=1))):
                messages.error(request, "Enter correct date time.")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            if(delta > deltaNow):
                stat = "inactive"
            elif(delta > deltaNow - deltaHour):
                stat = "active"
            art.status = stat
            


            img.save()
            art.save()
            art.bids_set.reverse()[0].highestbid = art.minbid
            messages.success(request, "Article registered.")
            return HttpResponseRedirect(reverse("portal:userArticles"))
        except UserDetail.DoesNotExist:
            messages.error(request, "You are not authorised.")
            return HttpResponseRedirect(reverse("portal:index"))


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
        if articlereg.objects.filter(pk=a_id).exists()==False:
            messages.error(request,"Article not found")
            return HttpResponseRedirect(reverse("portal:index"))
        else:
            quer = UserDetail.objects.get(pk=request.session['userID'])
            if (quer.visa_set.count() == 0):
                return HttpResponseRedirect(reverse("signup:VisaForm"))
            art = articlereg.objects.get(pk=a_id)
            if(art.private == False or art.userid == quer):
                pass
            else:
                try:
                    art.privateusers_set.get(user = quer)
                    pass
                except privateusers.DoesNotExist:
                    messages.error(request, "You are not authorised for this article bid.")
                    return HttpResponseRedirect(reverse("portal:index"))
            context = {'bid': art.bids_set.reverse()[0], 'userName': quer.name, 'quer': quer,
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
    def sold(request, a_id):
        article = articlereg.objects.get(pk = a_id)
        article.status = "sold"
        article.save()
        return HttpResponseRedirect("/portal/activeArticles/BidPage/" + str(a_id))



class BidsSoldView(generic.TemplateView):
    template_name = 'portal/soldArticle.html'

    def get(self, request, *args, **kwargs):
        try:
            quer = UserDetail.objects.get(pk=request.session['userID'])
            articles = quer.articlereg_set.all()
            now = timezone.now()
            if (('inSession' in request.session) and request.session['inSession'] == True):
                sold_bids = []
                for a in articles:
                    if a.timestart < (now - timedelta(hours=1)) and a.timestart > (now - timedelta(days=1, hours=1)):
                        if(a.bids_set.reverse()[0].highestbid != a.minbid):
                            sold_bids.append(a.id)
                        a.status = "sold"
                        a.save()
                context = {'userName': quer.name, 'bid': bids.objects.filter(articleid__in=sold_bids)}
                return render(request, self.template_name, context)
            else:
                return HttpResponse("Login as user to proceed.")
        except UserDetail.DoesNotExist:
            pass



class BidsWonView(generic.TemplateView):
    template_name = 'portal/wonArticle.html'

    def get(self, request, *args, **kwargs):
        try:
            quer = UserDetail.objects.get(pk=request.session['userID'])
            articles = articlereg.objects.all()
            now = timezone.now()
            if (('inSession' in request.session) and request.session['inSession'] == True):
                won_bids = []
                for a in articles:
                    if a.timestart < (now - timedelta(hours=1)) and a.timestart > (now - timedelta(days=1, hours=1)):
                        if((a.bids_set.reverse()[0].highestbid != a.minbid) and (a.bids_set.reverse()[0].userid == quer) and (a.userid != quer)):
                            won_bids.append(a.id)
                        a.status = "sold"
                        a.save()
                context = {'userName': quer.name, 'bid': bids.objects.filter(articleid__in=won_bids)}
                return render(request, self.template_name, context)
            else:
                return HttpResponse("Login as user to proceed.")
        except UserDetail.DoesNotExist:
            return HttpResponseRedirect(reverse('signup:index'))
