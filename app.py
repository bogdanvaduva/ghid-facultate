from flask import Flask, render_template, request, session, jsonify, Response
from chatbot import OllamaChatbot
import json
from ai_advisor import SpecializationAdvisor
from assessment import StudentAssessment
from specializations_data import specializations

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Required for session if you switch to per-user bots

advisor = SpecializationAdvisor(specializations)

def simple_chat_answer(question, specializations):
    # ... (unchanged, same as before) ...
    question_lower = question.lower()
    for spec in specializations:
        if spec['name'].lower() in question_lower:
            return (f"**{spec['name']}** – {spec.get('domain', '')} la {spec.get('faculty', '')}, "
                    f"{spec.get('university', '')}. Credite: {spec.get('credits', '')}, "
                    f"Acreditare: {spec.get('accreditation', '')}, Forma: {spec.get('study_form', 'Zi')}.")
    if 'salariu' in question_lower or 'venit' in question_lower or 'câștig' in question_lower:
        return "Salariile variază în funcție de specializare și piața muncii. Îți recomand să consulți site-urile universităților pentru date actualizate."
    if 'carieră' in question_lower or 'job' in question_lower or 'loc de muncă' in question_lower:
        return "Majoritatea specializărilor oferă oportunități diverse. Poți vedea exemple în descrierile fiecărei specializări."
    if 'durata' in question_lower or 'ani' in question_lower:
        return "Majoritatea programelor de licență durează 3 sau 4 ani (180 sau 240 credite). Verifică fișa fiecărei specializări."
    return (f"Am înțeles întrebarea: „{question}”. Îți pot oferi informații despre specializări, cariere, credite etc. "
            "Te rog să reformulezi sau să întrebi ceva mai specific.")

# Global chatbot instance (suitable for single‑user or personal use)
chatbot = OllamaChatbot(
    model="llama3.2",
    system_prompt="Ești un consilier academic." # Specializări disponibile:'" + ''.join([s['name'] for s in specializations])
)

@app.route('/')
def index():
    """Serve the chat interface."""
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    """
    Send a message and receive a streaming response (Server‑Sent Events).
    Expects JSON: {"message": "user input", "stream": true}
    """
    data = request.json
    message = data.get('message')
    stream = data.get('stream', True)

    if not message:
        return jsonify({'error': 'No message provided'}), 400

    def generate():
        try:
            for chunk in chatbot.chat(message, stream=stream):
                # Each chunk is sent as an SSE event
                yield f"data: {json.dumps({'chunk': chunk})}\n\n"
            # Signal end of stream
            yield f"data: {json.dumps({'done': True})}\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"

    return Response(generate(), mimetype='text/event-stream')

@app.route('/api/history', methods=['GET'])
def get_history():
    """Return the full conversation history."""
    return jsonify(chatbot.get_history())

@app.route('/api/clear', methods=['POST'])
def clear_history():
    """Clear conversation history (system prompt remains)."""
    chatbot.clear_history()
    return jsonify({'status': 'cleared'})

@app.route('/api/model', methods=['POST'])
def set_model():
    """Switch the active model."""
    data = request.json
    model = data.get('model')
    if not model:
        return jsonify({'error': 'No model specified'}), 400
    chatbot.set_model(model)
    return jsonify({'status': 'model set', 'model': model})

@app.route('/assessment')
def assessment():
    return render_template('assessment.html')

@app.route('/api/start-assessment', methods=['POST'])
def start_assessment():
    session['assessment'] = StudentAssessment()
    return jsonify({'status': 'started'})

@app.route('/api/submit-assessment', methods=['POST'])
def submit_assessment():
    data = request.json
    session['student_profile'] = data

    # Get recommendations (rule‑based)
    recommendations = advisor.assess_student_profile(data)

    detailed_recs = []
    for spec_name, score in recommendations:
        spec_info = advisor.get_detailed_info(spec_name)
        spec_info['match_score'] = round(score * 100, 2)
        detailed_recs.append(spec_info)

    return jsonify({'recommendations': detailed_recs})

@app.route('/api/specializations/all', methods=['GET'])
def get_all_specializations():
    return jsonify(specializations)

@app.route('/api/specialization/<name>')
def get_specialization(name):
    spec = advisor.get_detailed_info(name)
    if spec:
        return jsonify(spec)
    return jsonify({'error': 'Specialization not found'}), 404
if __name__ == '__main__':
    app.run(debug=True)
