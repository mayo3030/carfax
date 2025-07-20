from flask import Blueprint, render_template, request, jsonify
import subprocess
import os
import sys
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')

@main_bp.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    })

@main_bp.route('/api/vin', methods=['POST'])
def submit_vin():
    """Handle VIN submission and launch CARFAX"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        vin = data.get('vin', '').strip().upper()
        
        if not vin:
            return jsonify({"error": "VIN is required"}), 400
        
        # Validate VIN format
        if len(vin) != 17:
            return jsonify({"error": "VIN must be exactly 17 characters"}), 400
        
        logger.info(f"Received VIN request: {vin}")
        
        # Path to the CARFAX launcher script
        script_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), 
            'scripts', 
            'carfax_launcher.py'
        )
        
        if not os.path.exists(script_path):
            logger.error(f"CARFAX launcher script not found at: {script_path}")
            return jsonify({"error": "CARFAX launcher script not found"}), 500
        
        # Launch the CARFAX script with VIN
        try:
            result = subprocess.run([
                sys.executable, 
                script_path, 
                vin
            ], capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                logger.info(f"Successfully launched CARFAX for VIN: {vin}")
                return jsonify({
                    "success": True,
                    "message": f"CARFAX launched successfully for VIN: {vin}",
                    "vin": vin,
                    "timestamp": datetime.now().isoformat()
                })
            else:
                logger.error(f"Error launching CARFAX: {result.stderr}")
                return jsonify({
                    "error": f"Failed to launch CARFAX: {result.stderr}"
                }), 500
                
        except subprocess.TimeoutExpired:
            logger.warning(f"Timeout launching CARFAX for VIN: {vin}")
            return jsonify({
                "error": "Timeout launching CARFAX"
            }), 500
        except Exception as e:
            logger.error(f"Exception launching CARFAX: {e}")
            return jsonify({
                "error": f"Exception launching CARFAX: {str(e)}"
            }), 500
            
    except Exception as e:
        logger.error(f"Error in submit_vin: {e}")
        return jsonify({"error": f"Server error: {str(e)}"}), 500

@main_bp.route('/api/vin/validate', methods=['POST'])
def validate_vin():
    """Validate VIN format"""
    try:
        data = request.get_json()
        vin = data.get('vin', '').strip().upper()
        
        if not vin:
            return jsonify({"valid": False, "error": "VIN is required"})
        
        if len(vin) != 17:
            return jsonify({"valid": False, "error": "VIN must be exactly 17 characters"})
        
        # Check for invalid characters
        invalid_chars = ['I', 'O', 'Q']
        for char in invalid_chars:
            if char in vin:
                return jsonify({"valid": False, "error": f"VIN cannot contain: {char}"})
        
        return jsonify({"valid": True, "vin": vin})
        
    except Exception as e:
        logger.error(f"Error validating VIN: {e}")
        return jsonify({"valid": False, "error": "Validation error"}), 500 