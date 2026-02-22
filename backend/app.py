from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from services.enrichment import enrich_company_from_url
from db import init_db, SessionLocal, Company
from uuid import uuid4

app = FastAPI()

@app.on_event("startup")
def on_startup():
    init_db()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://vc-search.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class EnrichRequest(BaseModel):
    url: str

class EnrichResponse(BaseModel):
    summary: str
    whatTheyDo: list[str]
    keywords: list[str]
    signals: list[str]
    sources: list[str]
    enrichedAt: str

class CreateCompanyRequest(BaseModel):
    name: str
    website: str
    industry: str
    stage: str
    location: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/enrich-company", response_model=EnrichResponse)
def enrich_company(req: EnrichRequest):
    return enrich_company_from_url(req.url)


@app.post("/companies")
def create_company(req: CreateCompanyRequest):
    db = SessionLocal()
    try:
        company = Company(
            id=str(uuid4()),
            name=req.name,
            website=req.website,
            industry=req.industry,
            stage=req.stage,
            location=req.location,
        )
        db.add(company)
        db.commit()
        db.refresh(company)
        return company
    finally:
        db.close()


@app.get("/companies")
def list_companies():
    db = SessionLocal()
    try:
        return db.query(Company).all()
    finally:
        db.close()


@app.get("/companies/{company_id}")
def get_company(company_id: str):
    db = SessionLocal()
    try:
        company = db.query(Company).filter(Company.id == company_id).first()
        if not company:
            raise HTTPException(status_code=404, detail="Company not found")
        return company
    finally:
        db.close()