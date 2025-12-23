"""
Modern Physics Notes Evaluator Web App - SOTA 2024 Edition

Features:
- Modern responsive UI with real-time evaluation
- Multi-modal document analysis (PDF with diagrams)
- Interactive feedback and learning recommendations
- Progress tracking and analytics
- RESTful API for programmatic access
"""

import os
import json
import tempfile
from pathlib import Path
from datetime import datetime
from flask import Flask, request, jsonify, render_template, send_from_directory, Response
from werkzeug.utils import secure_filename
import logging
import base64
from io import BytesIO
from PIL import Image
import plotly.graph_objects as go
import plotly.utils

from modern_physics_evaluator import ModernPhysicsEvaluator, PhysicsConcept, ConfidenceLevel

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['SECRET_KEY'] = 'physics-evaluator-secret-key-2024'

# Ensure upload directory exists
Path(app.config['UPLOAD_FOLDER']).mkdir(exist_ok=True)

# Initialize the modern evaluator
evaluator = ModernPhysicsEvaluator()

@app.route('/')
def index():
    """Modern responsive web interface"""
    return render_template('modern_index.html')

@app.route('/api/evaluate-statement', methods=['POST'])
def evaluate_statement():
    """API endpoint for evaluating individual statements"""
    try:
        data = request.get_json()
        statement = data.get('statement', '').strip()
        context = data.get('context', '')

        if not statement:
            return jsonify({'error': 'No statement provided'}), 400

        result = evaluator.evaluate_statement(statement, context)

        # Convert result to JSON-serializable format
        response = {
            'statement': statement,
            'is_correct': result.is_correct,
            'confidence': result.confidence.value,
            'physics_concept': result.physics_concept.value,
            'statement_type': result.statement_type.value,
            'misconception_type': result.misconception_type,
            'mathematical_correctness': result.mathematical_correctness,
            'equation_analysis': result.equation_analysis,
            'feedback': result.feedback,
            'suggestions': result.suggestions,
            'related_concepts': result.related_concepts,
            'difficulty_level': result.difficulty_level,
            'learning_objectives': result.learning_objectives
        }

        return jsonify(response)

    except Exception as e:
        logger.error(f"Error evaluating statement: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/evaluate-document', methods=['POST'])
def evaluate_document():
    """API endpoint for evaluating entire documents"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400

        # Validate file type
        allowed_extensions = {'.pdf', '.txt', '.md'}
        file_ext = Path(file.filename).suffix.lower()
        if file_ext not in allowed_extensions:
            return jsonify({'error': 'Unsupported file type. Use PDF, TXT, or MD'}), 400

        # Save file temporarily
        filename = secure_filename(file.filename)
        temp_path = Path(app.config['UPLOAD_FOLDER']) / f"{datetime.now().isoformat()}_{filename}"
        file.save(temp_path)

        try:
            # Evaluate document
            if file_ext == '.pdf':
                results = evaluator.evaluate_document(str(temp_path))
            else:
                # Handle text files
                with open(temp_path, 'r', encoding='utf-8') as f:
                    text = f.read()
                statements = evaluator._split_into_statements(text)
                statement_results = []

                for stmt in statements[:20]:  # Limit for performance
                    if len(stmt.strip()) > 10:
                        result = evaluator.evaluate_statement(stmt, text)
                        statement_results.append({
                            'statement': stmt,
                            'evaluation': {
                                'is_correct': result.is_correct,
                                'confidence': result.confidence.value,
                                'physics_concept': result.physics_concept.value,
                                'feedback': result.feedback
                            }
                        })

                results = {
                    'document_summary': {
                        'total_statements': len(statement_results),
                        'correct_percentage': sum(1 for r in statement_results if r['evaluation']['is_correct']) / len(statement_results) * 100 if statement_results else 0,
                        'dominant_concept': 'mixed',
                        'average_confidence': 'medium'
                    },
                    'statement_evaluations': statement_results,
                    'recommendations': ['Document analysis complete']
                }

            return jsonify(results)

        finally:
            # Clean up temporary file
            if temp_path.exists():
                temp_path.unlink()

    except Exception as e:
        logger.error(f"Error evaluating document: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/analytics', methods=['GET'])
def get_analytics():
    """Get analytics data for visualization"""
    try:
        # This would typically fetch from a database
        # For now, return sample analytics
        analytics = {
            'concept_distribution': {
                'mechanics': 35,
                'electromagnetism': 25,
                'thermodynamics': 15,
                'quantum_mechanics': 10,
                'optics': 8,
                'other': 7
            },
            'confidence_trends': {
                'high': 60,
                'medium': 30,
                'low': 10
            },
            'common_misconceptions': [
                {'type': 'factual_inaccuracy', 'count': 45},
                {'type': 'mathematical_error', 'count': 32},
                {'type': 'conceptual_misunderstanding', 'count': 28}
            ]
        }

        return jsonify(analytics)

    except Exception as e:
        logger.error(f"Error fetching analytics: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/progress', methods=['GET'])
def get_progress():
    """Get learning progress data"""
    try:
        # Sample progress data
        progress = {
            'overall_score': 78,
            'concepts_mastered': ['mechanics', 'basic_electromagnetism'],
            'areas_for_improvement': ['quantum_mechanics', 'thermodynamics'],
            'recent_activity': [
                {'date': '2024-12-23', 'statements_evaluated': 15, 'accuracy': 82},
                {'date': '2024-12-22', 'statements_evaluated': 8, 'accuracy': 75},
                {'date': '2024-12-21', 'statements_evaluated': 12, 'accuracy': 80}
            ]
        }

        return jsonify(progress)

    except Exception as e:
        logger.error(f"Error fetching progress: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/export-results', methods=['POST'])
def export_results():
    """Export evaluation results"""
    try:
        data = request.get_json()
        results = data.get('results', [])
        format_type = data.get('format', 'json')

        if format_type == 'json':
            response_data = json.dumps(results, indent=2)
            return Response(
                response_data,
                mimetype='application/json',
                headers={'Content-Disposition': 'attachment; filename=physics_evaluation_results.json'}
            )
        elif format_type == 'csv':
            # Convert to CSV format
            import csv
            from io import StringIO

            output = StringIO()
            writer = csv.writer(output)

            # Write header
            writer.writerow(['Statement', 'Is Correct', 'Confidence', 'Concept', 'Feedback'])

            # Write data
            for result in results:
                writer.writerow([
                    result.get('statement', ''),
                    result.get('is_correct', ''),
                    result.get('confidence', ''),
                    result.get('physics_concept', ''),
                    result.get('feedback', '')
                ])

            csv_data = output.getvalue()
            output.close()

            return Response(
                csv_data,
                mimetype='text/csv',
                headers={'Content-Disposition': 'attachment; filename=physics_evaluation_results.csv'}
            )

        return jsonify({'error': 'Unsupported export format'}), 400

    except Exception as e:
        logger.error(f"Error exporting results: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '2.0.0-SOTA'
    })

# Static file serving
@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    debug = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'

    logger.info(f"Starting Modern Physics Evaluator on port {port}")
    logger.info("Features: Multi-modal analysis, RAG, Fine-grained classification, LLM feedback")

    app.run(host='0.0.0.0', port=port, debug=debug)
