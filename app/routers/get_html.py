from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.dependencies.db import get_db
import json

router = APIRouter()

# Endpoint to get classification by ID and draw tables in HTML
@router.get("/api/v1/classification/html/{classification_id}", response_class=HTMLResponse, tags=['Classification'])
def get_classification_html(classification_id: str, db: Session = Depends(get_db)):
    # Search info in 'classification' using the ID
    classification_data = db.execute(text("SELECT result FROM classification WHERE id = :id"), {"id": classification_id}).fetchone()
    if not classification_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ID Not Found.")
    classification_result = json.loads(classification_data[0])
    # HTML
    html_content = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Classification Results</title>
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                margin: 0;
                padding: 0;
                background-color: #f7f7f7;
                color: #333;
            }}
            .container {{
                width: 90%;
                margin: auto;
                overflow: hidden;
            }}
            header {{
                background: #333;
                color: #fff;
                padding-top: 30px;
                min-height: 70px;
                border-bottom: #50b3a2 4px solid;
            }}
            header a {{
                color: #50b3a2;
                text-decoration: none;
                font-size: 18px;
            }}
            header ul {{
                padding: 0;
                list-style: none;
            }}
            header ul li {{
                float: left;
                display: inline;
                padding: 0 25px;
            }}
            header #branding {{
                float: left;
            }}
            header #branding h1 {{
                margin: 0;
                font-size: 24px;
            }}
            header nav {{
                float: right;
                margin-top: 15px;
            }}
            header .highlight, header .current a {{
                color: #e8491d;
                font-weight: bold;
            }}
            header a:hover {{
                color: #50b3a2;
                font-weight: bold;
            }}
            table {{
                width: 100%;
                margin-top: 20px;
                border-collapse: collapse;
            }}
            table, th, td {{
                border: 1px solid #eaeaea;
                padding: 10px;
                text-align: left;
            }}
            table tr:nth-child(even) {{
                background-color: #f9f9f9;
            }}
            table th {{
                padding-top: 15px;
                padding-bottom: 15px;
                background-color: #333;
                color: #fff;
            }}
        </style>
    </head>
    <body>
        <header>
            <div class="container">
                <div id="branding">
                    <h1>BD Name: <span class="highlight">{classification_result["database_name"]}</span></h1>
                </div>
                <nav>
                    <ul>
                        <li class="current"><a href="http://127.0.0.1:8000/api/v1/classification/html/{classification_id}">Classification</a></li>
                    </ul>
                </nav>
            </div>
        </header>
        <div class="container">
    """

    # for to tables and columns in HTML
    for table_name, columns in classification_result["tables"].items():
        html_content += f"<h2>{table_name}</h2>"
        html_content += """
            <table>
                <tr>
                    <th>Column Name</th>
                    <th>Clasificación</th>
                </tr>
        """
        for column in columns:
            html_content += f"""
                <tr>
                    <td>{column["column_name"]}</td>
                    <td>{column["classification"]}</td>
                </tr>
            """
        html_content += "</table>"

    html_content += """
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)