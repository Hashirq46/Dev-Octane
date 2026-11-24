from pydantic import BaseModel


class Education(BaseModel):
    degree: str = ''
    institute: str = ''
    year: str = ''


class Experience(BaseModel):
    title: str = ''
    company: str = ''
    start: str = ''
    end: str = ''
    description: str = ''


class CVData(BaseModel):
    full_name: str = ''
    email: str = ''
    phone: str = ''
    city: str = ''
    headline: str = ''
    skills: list[str] = []
    experience_years: int = 0
    education: list[Education] = []
    experience: list[Experience] = []


class CompanyDocData(BaseModel):
    doc_type: str = ''  # 'ntn_certificate' or 'secp_certificate'
    company_name: str = ''
    ntn: str = ''
    cuin: str = ''
    address: str = ''
    city: str = ''
    incorporation_date: str = ''
