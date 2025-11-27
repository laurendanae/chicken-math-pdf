#!/usr/bin/env python3
"""
Flask API Server for Chicken Math PDF Generation
Deploy this to any server (Heroku, DigitalOcean, AWS, etc.)
"""

from flask import Flask, request, jsonify, send_file
from chicken_math_pdf_generator import generate_chicken_math_pdf
import os
import uuid
import tempfile
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "service": "Chicken Math PDF Generator API",
        "version": "1.0",
        "endpoints": {
            "/generate-pdf": "POST - Generate PDF report",
            "/health": "GET - Health check"
        }
    })

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy", "service": "chicken-math-pdf-api"})

@app.route('/generate-pdf', methods=['POST'])
def generate_pdf():
    """
    Generate a Chicken Math PDF report
    
    Expected JSON body:
    {
        "name": "John Doe",
        "current_flock": 6,
        "real_flock": 11,
        "yearly_eggs": 3146,
        "egg_revenue": 1573.00,
        "feed_cost": 756.00,
        "net_profit": 817.00,
        "funny_quote": "Your funny quote here...",
        "recommended_purchase": "Premium Package",
        "meme_image_url": null
    }
    """
    try:
        # Get data from request
        data = request.json
        
        # Validate required fields
        required_fields = ['name', 'current_flock', 'real_flock', 'yearly_eggs', 
                          'egg_revenue', 'feed_cost', 'net_profit', 'funny_quote']
        
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({
                "error": "Missing required fields",
                "missing": missing_fields
            }), 400
        
        # Generate unique filename in temp directory
        temp_dir = tempfile.gettempdir()
        filename = os.path.join(temp_dir, f"chicken_math_{uuid.uuid4()}.pdf")
        
        # Generate PDF
        generate_chicken_math_pdf(data, filename)
        
        # Send file and cleanup
        response = send_file(
            filename,
            as_attachment=True,
            download_name=f"Chicken_Math_Report_{data['name'].replace(' ', '_')}.pdf",
            mimetype='application/pdf'
        )
        
        # Schedule cleanup after sending
        @response.call_on_close
        def cleanup():
            try:
                if os.path.exists(filename):
                    os.remove(filename)
            except Exception as e:
                app.logger.error(f"Error cleaning up file: {e}")
        
        return response
        
    except Exception as e:
        app.logger.error(f"Error generating PDF: {str(e)}")
        return jsonify({
            "error": "Failed to generate PDF",
            "message": str(e)
        }), 500

@app.route('/generate-pdf-base64', methods=['POST'])
def generate_pdf_base64():
    """
    Generate PDF and return as base64 string (useful for some integrations)
    """
    try:
        import base64
        
        data = request.json
        
        # Generate PDF in temp location
        temp_dir = tempfile.gettempdir()
        filename = os.path.join(temp_dir, f"chicken_math_{uuid.uuid4()}.pdf")
        
        generate_chicken_math_pdf(data, filename)
        
        # Read and encode
        with open(filename, 'rb') as f:
            pdf_data = f.read()
            encoded = base64.b64encode(pdf_data).decode('utf-8')
        
        # Cleanup
        os.remove(filename)
        
        return jsonify({
            "success": True,
            "pdf_base64": encoded,
            "filename": f"Chicken_Math_Report_{data['name'].replace(' ', '_')}.pdf"
        })
        
    except Exception as e:
        app.logger.error(f"Error generating PDF: {str(e)}")
        return jsonify({
            "error": "Failed to generate PDF",
            "message": str(e)
        }), 500

if __name__ == '__main__':
    # Development server
    app.run(host='0.0.0.0', port=5000, debug=True)
