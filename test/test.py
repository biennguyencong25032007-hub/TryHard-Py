for item in range:
    if item == 5:
        print("Found 5!")
    else:
        print("Not 5.")
        if item == 10:
            print("Found 10!")
            
from django.utils.translation import ugettext_lazy as _
fiwe = _("Hello, World!")
    