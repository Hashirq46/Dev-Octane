# JobPortal.pk (Rozee.pk-style Job Board)

A complete, production-ready Django web application designed for the Pakistani job market featuring automated AI document extraction, multi-layered company verification, role-based dashboards, and private document storage.

---

## 1. Product Summary & Features

### For Candidates (Job Seekers)
- **AI-Powered CV Signup**: Candidates register by uploading their CV (PDF, DOCX, JPG, PNG).
- **Form Autofill & Verification**: An AI pipeline (Anthropic Claude API) parses the uploaded CV and prefills a comprehensive review form (personal details, headline, skills, experience years, education history formset, and work history formset).
- **Human-in-the-Loop Integrity**: Nothing is committed to the candidate's public profile until the candidate reviews, edits, and submits the form.
- **Profile Dashboard & Completeness Meter**: Real-time completeness calculation, resume download, application tracking, and profile editing (uploading a new CV triggers fresh AI extraction and review).
- **One-Click Apply**: Candidate applies with their verified profile and attached CV; duplicate applications for the same opening are prevented.

### For Recruiters (Employers)
- **Official Company Email Enforcement**: Public email providers (`@gmail.com`, `@yahoo.com`, `@hotmail.com`, etc.) are rejected at signup. Only valid organizational domains are allowed.
- **Company Verification Pipeline**:
  1. **Document Upload**: Recruiter uploads their mandatory FBR NTN certificate and optional SECP incorporation certificate.
  2. **AI Extraction**: Credentials (company name, NTN, CUIN, address, city) are automatically extracted into a draft.
  3. **Recruiter Review**: Recruiter verifies and submits the prefilled form.
  4. **Automated Sanity Flags**: Cross-referenced against the local FBR Active Taxpayer List (ATL) and checked for name/NTN inconsistencies.
  5. **Admin Approval**: Staff administrator conducts manual verification against official records (e.g. SECP eServices) and approves or rejects with custom feedback notes.
- **Verified Badge**: Approved recruiters receive a green **✔ Verified** badge on their company profile and job listings.
- **Safety Lockdown**: Editing company name, NTN, or CUIN after approval immediately resets verification status to `pending` and revokes the badge until re-evaluated.
- **Job & Applicant Management**: Post openings (verified recruiters only), edit details, close listings, view candidate CVs, and transition applicant statuses (`Applied`, `Shortlisted`, `Hired`, `Rejected`).

### Security, Privacy & Compliance
- **Private Document Storage**: Resumes and business certificates are stored in `private_media/` and are never exposed over public HTTP URLs.
- **Strict Access Control**: Downloads are strictly gated via permission-checked Django views returning `404 Not Found` for unauthorized requests to prevent enumeration.
- **File Validation**: Strict file type validation (`.pdf`, `.docx`, `.jpg`, `.jpeg`, `.png`), 5 MB size limit, and binary magic byte signature verification.
- **Brute-Force & Rate Limiting**: `django-axes` login protection with temporary lockouts and `django-ratelimit` on signups and confirmation requests.
- **Automated Data Lifecycle**: Management command `cleanup_drafts` safely deletes unsubmitted drafts and files older than 14 days.

---

## 2. Tech Stack

- **Backend**: Python 3.12+, Django 5.x
- **Database**: SQLite (local dev), PostgreSQL (production via `dj-database-url`)
- **Frontend**: Django Templates + Bootstrap 5 + Bootstrap Icons
- **AI Extraction**: Anthropic API (`claude-haiku-5-5` default) with Pydantic schema validation
- **Background Tasks**: Celery + Redis (optional, controlled via `PARSE_ASYNC` setting)
- **Key Libraries**: `anthropic`, `pydantic`, `python-docx`, `pandas`, `openpyxl`, `django-ratelimit`, `django-axes`, `python-dotenv`, `dj-database-url`, `Pillow`

---

## 3. Project Directory Structure

```
jobportal/
├── accounts/               # Custom User model, signup forms, validators, email confirmation, login
├── candidates/             # CandidateProfile, Education, WorkExperience, CV review flow, dashboard
├── recruiters/             # RecruiterVerification, ActiveTaxpayer, company review, services, admin actions
│   └── management/commands/import_atl.py
├── jobs/                   # Job and Application models, search filters, apply flow, applicant management
├── parsing/                # ParsedDraft model, Pydantic schemas, extractor, Celery/sync tasks, protected downloads
│   └── management/commands/cleanup_drafts.py
├── jobportal/              # Project configuration (settings.py, urls.py, celery.py, wsgi.py)
├── templates/              # Base template and app-specific responsive templates
├── private_media/          # Private filesystem storage (drafts, resumes, certificates)
├── requirements.txt        # Pinned project dependencies
├── .env.example            # Environment variables template
└── db.sqlite3              # Local development database
```

---

## 4. Setup Instructions

### 1. Prerequisites
Ensure Python 3.12+ is installed on your machine.

### 2. Clone and Setup Virtual Environment
```bash
# Create virtual environment
python -m venv .venv

# Activate on Windows (PowerShell):
.\.venv\Scripts\Activate.ps1
# On Linux/macOS:
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```
Ensure your `.env` contains the required settings:
```ini
SECRET_KEY=your-secure-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,testserver
DATABASE_URL=sqlite:///db.sqlite3
ANTHROPIC_API_KEY=your-anthropic-api-key
PARSER_MODEL=claude-haiku-5-5
PARSE_ASYNC=False
CELERY_BROKER_URL=redis://localhost:6379/0
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
DEFAULT_FROM_EMAIL=noreply@example.com
```

### 5. Run Database Migrations
```bash
python manage.py migrate
```

### 6. Create Superuser (Admin)
```bash
python manage.py createsuperuser
```
Follow the prompts to enter an email (used as username) and password.

### 7. Import FBR Active Taxpayer List (ATL)
Download the latest ATL Excel or CSV file from FBR and import it:
```bash
python manage.py import_atl path/to/atl_file.xlsx
```
*The command dynamically detects NTN and taxpayer name columns case-insensitively and updates existing entries.*

### 8. Run the Development Server
```bash
python manage.py runserver
```
Visit `http://127.0.0.1:8000/` in your browser.

### 9. (Optional) Run Background Celery Worker
If running asynchronous parsing (`PARSE_ASYNC=True` in `.env`):
```bash
# Ensure Redis is running, then:
celery -A jobportal worker -l info
```

### 10. Run Draft Cleanup Command
To prune unsubmitted drafts and files older than 14 days:
```bash
python manage.py cleanup_drafts
```

---

## 5. Running the Automated Test Suite

The test suite covers all 12 core requirements specified in the project build specification:
1. Recruiter signup free email rejection (`@gmail.com`) and company domain acceptance with inactive activation state.
2. Email activation tokens (valid & invalid).
3. Candidate signup with CV and file magic signature validation.
4. Parsing task with mocked Anthropic extractor (success and failure modes).
5. CV review GET prefill and POST profile creation with Education/Experience formsets.
6. Multi-tenant draft access isolation (404 on other user's draft).
7. Permission barriers on job posting (unverified redirect vs. approved access).
8. Automatic reset to `pending` upon editing approved company credentials.
9. Automated sanity flag detection (`company_flags` for name, NTN, and ATL discrepancies).
10. Application constraints (prevention of duplicate applications and cross-recruiter isolation).
11. Secure resume download access control (owner, staff, hiring recruiter allowed; 404 for all others).
12. Verified badge appearance logic.

Execute the test suite:
```bash
python manage.py test
```
All 17 tests will run and pass.

---

## 6. Verification and Admin Checklist

When reviewing recruiter verifications in Django Admin (`/admin/recruiters/recruiterverification/`):
1. **SECP CUIN Lookup**: Open [eservices.secp.gov.pk](https://eservices.secp.gov.pk) and search the 7-digit CUIN to confirm legal entity title.
2. **Document Consistency**: Inspect the uploaded NTN certificate and SECP incorporation certificate using the protected download links.
3. **Domain Verification**: Verify that the recruiter's email domain matches the company's domain/organization.
4. **Sanity Flags**: Check the automated flags generated by the system (e.g. NTN not found in ATL, fuzzy name discrepancy).
5. **Decision**: Select **Approve selected** or **Reject selected** (with custom notes). Automated email alerts notify the recruiter immediately.
