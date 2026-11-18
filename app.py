"""
Module: app.py
FastAPI Web Server phục vụ giao diện trực quan và các API file cho AI Analytics Agent
"""
import os
import base64
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from pydantic import BaseModel
from core.agent import EnterpriseAnalyticsAgent
from core.edtech_agent import EdTechInquiryAgent

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "db", "enterprise_dw.sqlite")
DATA_DIR = os.path.join(BASE_DIR, "data")

app = FastAPI(title="Enterprise AI Analytics Agent - BI Demo")

agent = EnterpriseAnalyticsAgent(db_path=DB_PATH)
edtech_agent = EdTechInquiryAgent(data_dir=DATA_DIR)

class EdTechInquiryRequest(BaseModel):
    inquiry_text: str
    sender_name: str = "Khách hàng"
    sender_email: str = "contact@school.edu.vn"
    organization: str = "Trường Đại học"

class QueryRequest(BaseModel):
    query: str
    role: str = "Manager_Region_North"

class ApprovalRequest(BaseModel):
    approval_id: str
    decision: str

class FeedbackRequest(BaseModel):
    query: str
    feedback_type: str
    comment: str = ""

class FileUploadPayload(BaseModel):
    filename: str
    content_base64: str

@app.get("/", response_class=HTMLResponse)
async def serve_index(request: Request):
    index_path = os.path.join(BASE_DIR, "index.html")
    if not os.path.exists(index_path):
        index_path = os.path.join(BASE_DIR, "templates", "index.html")
    with open(index_path, "r", encoding="utf-8") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)

@app.get("/bi", response_class=HTMLResponse)
async def serve_bi_dashboard(request: Request):
    bi_path = os.path.join(BASE_DIR, "templates", "bi_dashboard.html")
    if os.path.exists(bi_path):
        with open(bi_path, "r", encoding="utf-8") as f:
            html_content = f.read()
        return HTMLResponse(content=html_content)
    return HTMLResponse(content="<h1>BI Dashboard</h1>")

@app.post("/api/edtech/process")
async def process_edtech_inquiry(req: EdTechInquiryRequest):
    try:
        res = edtech_agent.process_inquiry(
            inquiry_text=req.inquiry_text,
            sender_name=req.sender_name,
            sender_email=req.sender_email,
            org=req.organization
        )
        return JSONResponse(content={"status": "success", "data": res})
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e)})

@app.post("/api/analyze")
async def analyze_query(req: QueryRequest):
    try:
        result = agent.execute(user_query=req.query, user_role=req.role)
        return JSONResponse(content={"status": "success", "data": result})
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e)})

@app.post("/api/upload")
async def upload_file(payload: FileUploadPayload):
    try:
        content = base64.b64decode(payload.content_base64)
        res = agent.ingest_uploaded_file(payload.filename, content)
        return JSONResponse(content=res)
    except Exception as e:
        return JSONResponse(status_code=400, content={"status": "error", "message": str(e)})

@app.get("/api/export/excel")
async def export_excel():
    try:
        filepath = agent.export_excel()
        filename = os.path.basename(filepath)
        return FileResponse(
            filepath,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            filename=filename
        )
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e)})

@app.get("/api/export/csv")
async def export_csv():
    try:
        filepath = agent.export_csv()
        filename = os.path.basename(filepath)
        return FileResponse(
            filepath,
            media_type="text/csv",
            filename=filename
        )
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e)})

@app.post("/api/approval")
async def resolve_approval(req: ApprovalRequest):
    success = agent.hitl_manager.resolve_approval(req.approval_id, req.decision)
    return JSONResponse(content={"status": "success" if success else "error"})

@app.post("/api/feedback")
async def save_feedback(req: FeedbackRequest):
    success = agent.hitl_manager.record_feedback(req.query, req.feedback_type, req.comment)
    return JSONResponse(content={"status": "success" if success else "error"})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=False)
