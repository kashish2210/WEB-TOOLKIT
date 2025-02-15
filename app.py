from flask import Flask, render_template, request, redirect, url_for, send_file
import os
from bs4 import BeautifulSoup
import lxml

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "static/uploads"

# Ensure upload folder exists
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)


@app.route("/")
def index():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Upload SVG</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            body {
                font-family: Arial, sans-serif;
                height: 100vh;
                overflow: hidden;
                display: flex;
                justify-content: center;
                align-items: center;
            }
            /* Fullscreen interactive iframe */
            .background-iframe {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                border: none;
                z-index: -1;
                pointer-events: auto; /* Allows interaction */
            }
            /* Centered Glassmorphic container */
            .content {
                position: relative;
                z-index: 1;
                text-align: center;
                color: white;
                backdrop-filter: blur(10px) saturate(150%);
                -webkit-backdrop-filter: blur(10px) saturate(150%);
                background: rgba(255, 255, 255, 0.15);
                border-radius: 15px;
                padding: 25px;
                width: 350px;
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
                border: 1px solid rgba(255, 255, 255, 0.3);
            }
            h1 {
                font-size: 24px;
                margin-bottom: 15px;
            }
            form {
                display: flex;
                flex-direction: column;
                align-items: center;
            }
            input[type="file"] {
                background: rgba(255, 255, 255, 0.2);
                padding: 10px;
                border-radius: 5px;
                border: none;
                color: white;
                width: 100%;
                cursor: pointer;
                margin-bottom: 15px;
            }
            /* Disable iframe interaction inside the form */
            .content {
                pointer-events: auto;
            }
            .button-86 {
            all: unset;
            width: 100px;
            height: 30px;
            font-size: 16px;
            background: transparent;
            border: none;
            position: relative;
            color: #f0f0f0;
            cursor: pointer;
            z-index: 1;
            padding: 10px 20px;
            display: flex;
            align-items: center;
            justify-content: center;
            white-space: nowrap;
            user-select: none;
            -webkit-user-select: none;
            touch-action: manipulation;
            }

            .button-86::after,
            .button-86::before {
            content: '';
            position: absolute;
            bottom: 0;
            right: 0;
            z-index: -99999;
            transition: all .4s;
            }

            .button-86::before {
            transform: translate(0%, 0%);
            width: 100%;
            height: 100%;
            background: #28282d;
            border-radius: 10px;
            }

            .button-86::after {
            transform: translate(10px, 10px);
            width: 35px;
            height: 35px;
            background: #ffffff15;
            backdrop-filter: blur(5px);
            -webkit-backdrop-filter: blur(5px);
            border-radius: 50px;
            }

            .button-86:hover::before {
            transform: translate(5%, 20%);
            width: 110%;
            height: 110%;
            }

            .button-86:hover::after {
            border-radius: 10px;
            transform: translate(0, 0);
            width: 100%;
            height: 100%;
            }

            .button-86:active::after {
            transition: 0s;
            transform: translate(0, 5%);
            }
        </style>
    </head>
    <body>
        <iframe class="background-iframe" 
            src="https://my.spline.design/glassmorphlandingpage-f5c91a2569477c6cd238562e487f4c47/" 
            frameborder="0">
        </iframe>
        
        <div class="content">
            <h1>Upload your SVG file</h1>
            <form action="/upload" method="post" enctype="multipart/form-data">
                <input type="file" name="file" accept=".svg">
                <button class="button-86" type="submit">Upload</button>
            </form>
            <br>
            <a href="https://www.svgrepo.com/" target="_blank" rel="noopener noreferrer">FOR SVG CLICK HERE</a>
        </div>
    </body>
    </html>
    """


@app.route("/upload", methods=["POST"])
def upload():
    if "file" not in request.files:
        return redirect(request.url)

    file = request.files["file"]
    if file.filename == "":
        return redirect(request.url)

    if file and file.filename.endswith(".svg"):
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(filepath)
        return redirect(url_for("preview", filename=file.filename))

    return redirect(request.url)


@app.route("/preview/<filename>")
def preview(filename):
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    with open(filepath, "r", encoding="utf-8") as f:
        svg_content = f.read()

    soup = BeautifulSoup(svg_content, "lxml-xml")
    for path in soup.find_all("path"):
        path["class"] = "path"
        path["stroke"] = "#e74c3c"
        path["stroke-width"] = "2"
        path["fill"] = "none"
        path["stroke-dasharray"] = "1000"
        path["stroke-dashoffset"] = "1000"

    preview_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>SVG Preview</title>
        <style>
            /* General Styling */
            body {{
                font-family: 'Poppins', sans-serif;
                background: #f4f4f4;
                text-align: center;
                overflow-x: hidden;
                margin: 0;
                padding: 0;
            }}

            /* Control Panel - Top Right */
            .controls-container {{
                position: fixed;
                top: 20px;
                right: 20px;
                z-index: 100;
                text-align: center;
                color: #333;
                backdrop-filter: blur(10px) saturate(150%);
                -webkit-backdrop-filter: blur(10px) saturate(150%);
                background: rgba(255, 255, 255, 0.2);
                border-radius: 12px;
                padding: 20px;
                width: 300px;
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
                border: 1px solid rgba(255, 255, 255, 0.3);
            }}

            .controls-container label {{
                display: block;
                margin: 10px 0;
                font-size: 14px;
                font-weight: 600;
                color: #333;
            }}

            .controls-container input[type="color"],
            .controls-container input[type="range"] {{
                margin-top: 5px;
                width: 80%;
                border-radius: 5px;
                border: none;
                padding: 5px;
            }}

            /* SVG Container */
            .svg-container {{
                height: 2000px;
                margin-top: 80px;
            }}

            svg {{
                position: fixed;
                margin: auto;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                width: 100% !important;
                height: auto;
                max-width: 500px;
                max-height: 340px;
            }}

            .path {{
                transition: stroke-dashoffset 0.2s ease-out;
            }}

            /* Download Button */
            .download-btn {{
                display: block;
                margin-top: 15px;
                background: #e74c3c;
                color: white;
                padding: 10px 15px;
                border: none;
                border-radius: 8px;
                cursor: pointer;
                width: 100%;
                font-size: 14px;
                font-weight: bold;
                transition: background 0.3s;
            }}

            .download-btn:hover {{
                background: #c0392b;
            }}

            /* Responsive Design */
            @media (max-width: 768px) {{
                .controls-container {{
                    width: 90%;
                    left: 50%;
                    transform: translateX(-50%);
                }}
            }}
        </style>
        <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
        <script>
            $(document).ready(function() {{
                var $dashOffset = $('.path').css('stroke-dashoffset');

                $(window).on('scroll', function() {{
                    var $percentageComplete = (($(window).scrollTop() / ($('html').height() - $(window).height())) * 100);
                    var $newUnit = parseInt($dashOffset, 10);
                    var $offsetUnit = $percentageComplete * ($newUnit / 100);
                    $('.path').css({{
                        'stroke-dashoffset': $newUnit - $offsetUnit,
                        'transition': 'stroke-dashoffset 0.2s ease-out'
                    }});
                }});

                $('#strokeColor').on('input', function() {{
                    $('.path').css('stroke', $(this).val());
                }});

                $('#bgColor').on('input', function() {{
                    $('body').css('background', $(this).val());
                }});

                $('#strokeWidth').on('input', function() {{
                    $('.path').css('stroke-width', $(this).val() + 'px');
                }});

                $('#exportForm').submit(function() {{
                    $('#exportStrokeColor').val($('#strokeColor').val());
                    $('#exportBgColor').val($('#bgColor').val());
                    $('#exportStrokeWidth').val($('#strokeWidth').val());
                }});
            }});
        </script>
    </head>
    <body>
        <div class="controls-container">
            <label>Stroke Color: <input type="color" id="strokeColor" value="#e74c3c"></label>
            <label>Background Color: <input type="color" id="bgColor" value="#f4f4f4"></label>
            <label>Stroke Width: <input type="range" id="strokeWidth" min="1" max="10" value="2"></label>
        </div>

        <div class="svg-container"></div>
        {str(soup)}
        <br>

        <form id="exportForm" action="/export" method="post">
            <input type="hidden" name="filename" value="{filename}">
            <input type="hidden" name="strokeColor" id="exportStrokeColor">
            <input type="hidden" name="bgColor" id="exportBgColor">
            <input type="hidden" name="strokeWidth" id="exportStrokeWidth">
            <button type="submit" class="download-btn">Download HTML Code</button>
        </form>
    </body>
    </html>
    """


    file_path = os.path.join(app.config["UPLOAD_FOLDER"], "export.html")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(preview_html)

    return preview_html


import re

@app.route("/export", methods=["POST"])
def export():
    filename = request.form.get("filename", "export.html")
    stroke_color = request.form.get("strokeColor", "#e74c3c")
    bg_color = request.form.get("bgColor", "#f4f4f4")
    stroke_width = request.form.get("strokeWidth", "2")  # Ensure it's a string

    file_path = os.path.join(app.config["UPLOAD_FOLDER"], "export.html")

    with open(file_path, "r", encoding="utf-8") as f:
        export_html = f.read()

    soup = BeautifulSoup(export_html, "html.parser")
    
    # Remove unnecessary UI elements before export
    if soup.find(class_="controls-container"):
        soup.find(class_="controls-container").decompose()
    if soup.find(id="exportForm"):
        soup.find(id="exportForm").decompose()

    export_html = soup.prettify()

    # Update colors
    export_html = export_html.replace("#e74c3c", stroke_color)
    export_html = export_html.replace("#f4f4f4", bg_color)

    # Check if stroke-width exists in inline styles
    if 'stroke-width' in export_html:
        export_html = re.sub(r"stroke-width:\s*\d+px;", f"stroke-width: {stroke_width}px;", export_html)
    else:
        # If `stroke-width` is missing, add it manually to all path elements
        export_html = export_html.replace("<path", f"<path style='stroke-width: {stroke_width}px;'")

    modified_export_path = os.path.join(
        app.config["UPLOAD_FOLDER"], "SVG[ks].html"
    )
    with open(modified_export_path, "w", encoding="utf-8") as f:
        f.write(export_html)

    return send_file(modified_export_path, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
