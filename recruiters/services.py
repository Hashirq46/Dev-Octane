import re
from difflib import SequenceMatcher
from .models import ActiveTaxpayer


def normalize_ntn(value):
    return re.sub(r'[^0-9]', '', value or '')


def check_atl(ntn):
    n = normalize_ntn(ntn)
    if not n:
        return False
    # Check full digits or 7-digit root
    candidates = [n]
    if len(n) >= 7:
        candidates.append(n[:7])
    return ActiveTaxpayer.objects.filter(ntn__in=candidates).exists()


def merged_company_data(drafts):
    merged = {}
    for d in drafts:
        for k, v in (d.data or {}).items():
            if v and not merged.get(k):
                merged[k] = v
    return merged


def company_flags(typed, extracted):
    flags = []
    if extracted.get('ntn') and normalize_ntn(typed.get('ntn')) != normalize_ntn(extracted.get('ntn')):
        flags.append('NTN entered differs from NTN read from the certificate')

    if extracted.get('company_name'):
        ratio = SequenceMatcher(
            None,
            str(typed.get('company_name', '')).lower().strip(),
            str(extracted.get('company_name', '')).lower().strip()
        ).ratio()
        if ratio < 0.85:
            flags.append('Company name differs from the name on the certificate')

    if not check_atl(typed.get('ntn')):
        flags.append('NTN not found in imported Active Taxpayer List')

    if not typed.get('cuin'):
        flags.append('No CUIN provided (SECP check not possible)')

    return flags
