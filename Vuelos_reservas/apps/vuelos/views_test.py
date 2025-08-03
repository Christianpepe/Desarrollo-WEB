from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
import io
import sys

@staff_member_required
def run_scheduler_test(request):
    old_stdout = sys.stdout
    sys.stdout = mystdout = io.StringIO()
    try:
        import Vuelos_reservas.tests.test_scheduler as test_scheduler
        if hasattr(test_scheduler, 'main'):
            test_scheduler.main()
        else:
            exec(open(test_scheduler.__file__).read())
    except Exception as e:
        print(f"Error: {e}")
    sys.stdout = old_stdout
    output = mystdout.getvalue()
    return HttpResponse(f"<pre>{output}</pre>")
