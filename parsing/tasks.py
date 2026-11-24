from django.conf import settings
from .models import ParsedDraft
from .schemas import CVData, CompanyDocData
from .extractor import extract

try:
    from celery import shared_task
except ImportError:
    def shared_task(f):
        f.delay = f
        return f


@shared_task
def parse_draft(draft_id):
    d = ParsedDraft.objects.get(pk=draft_id)
    cls = CVData if d.kind == 'cv' else CompanyDocData
    try:
        d.data = extract(d.file.path, cls).model_dump()
        d.state = 'ready'
    except Exception:
        d.state = 'failed'
    d.save()


def enqueue(draft_id):
    if settings.PARSE_ASYNC:
        parse_draft.delay(draft_id)
    else:
        parse_draft(draft_id)
