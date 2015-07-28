from django.test import TestCase
from rango.models import Category
from django.core.urlresolvers import reverse
# Create your tests here.

#class CategoryMetodTests(TestCase):
#    def test_ensure_iews_are_positie(self):
#        cat = Category(name="test",views=-1,likes=0)
#        cat.save()
#        self.assertEqual((cat.views >=0), True) 
		
class IndexViewTests(TestCase):
    def test_index_view_with_no_categories(self):
        """ If no questions exist, an appropriate message should be displayed."""
        response=self.client.get(reverse('index'))
        self.assertEqual(response.status_code,200)
        self.assertContains(response,"There are no categories present.")
        self.assertQuerysetEqual(response.context['categories'],[])
    
    def test_index_view_with_categories(self):
        add_cat('test',1,1)
        add_cat('temp',1,1)

        response=self.client.get(reverse('index'))
        self.assertEqual(response.status_code,200)
        self.assertContains(response,'test')

        num_cats = len(response.context['categories'])
        self.assertEqual(num_cats,2)		
	 
def add_cat(name, views, likes):  #a helper function
    c=Category.objects.get_or_create(name=name)[0]
    c.views=views
    c.likes=likes
    c.save()
    return c
	
