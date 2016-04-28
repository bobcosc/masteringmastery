from django.shortcuts import render
from data.models import Player, Champion
from django.views.generic import TemplateView

# Create your views here.
class IndexView (TemplateView):
    template_name = "index.html"
    
    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs) 

        #online = Player.objects.filter(lastStream__gte = datetime.now()- timedelta(minutes=15)).order_by('-sortPoints')

        #sortedData = sorted(data,key=lambda riotplayer: riotplayer.sortPoints, reverse=True )
        #context['summoners'] = online
        return context