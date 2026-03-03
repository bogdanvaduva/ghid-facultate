# app.py

from flask import Flask, render_template, request, jsonify, session
from ai_advisor import SpecializationAdvisor
from assessment import StudentAssessment
from specializations_data import specializations
import requests  # adaugă la începutul fișierului

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

advisor = SpecializationAdvisor(specializations)

@app.route('/')
def index():
    return render_template('index.html')

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

    # Get recommendations
    recommendations = advisor.assess_student_profile(data)

    # Get detailed info for top recommendations
    detailed_recs = []
    for spec_name, score in recommendations:
        spec_info = advisor.get_detailed_info(spec_name)
        spec_info['match_score'] = round(score * 100, 2)
        detailed_recs.append(spec_info)

    return jsonify({'recommendations': detailed_recs})

@app.route('/api/specializations/all', methods=['GET'])
def get_all_specializations():
    """Returnează toate specializările."""
    return jsonify(specializations)

@app.route('/api/specialization/<name>')
def get_specialization(name):
    spec = advisor.get_detailed_info(name)
    if spec:
        return jsonify(spec)
    return jsonify({'error': 'Specialization not found'}), 404

@app.route('/api/compare', methods=['POST'])
def compare():
    data = request.json
    specs = data.get('specializations', [])
    comparison = advisor.compare_specializations(specs)
    return jsonify({'comparison': comparison})

@app.route('/api/ask', methods=['POST'])
def ask_question():
    data = request.json
    question = data.get('question', '')
    answer = advisor.answer_question(question)
    return jsonify({'answer': answer})

# Funcție de căutare simplă în lista de specializări (fallback)
def simple_chat_answer(question, specializations):
    question_lower = question.lower()
    # Caută nume de specializări în întrebare
    for spec in specializations:
        if spec['name'].lower() in question_lower:
            return (f"**{spec['name']}** – {spec.get('domain', '')} la {spec.get('faculty', '')}, "
                    f"{spec.get('university', '')}. Credite: {spec.get('credits', '')}, "
                    f"Acreditare: {spec.get('accreditation', '')}, Forma: {spec.get('study_form', 'Zi')}.")
    # Cuvinte cheie generale
    if 'salariu' in question_lower or 'venit' in question_lower or 'câștig' in question_lower:
        return "Salariile variază în funcție de specializare și piața muncii. Îți recomand să consulți site-urile universităților pentru date actualizate."
    if 'carieră' in question_lower or 'job' in question_lower or 'loc de muncă' in question_lower:
        return "Majoritatea specializărilor oferă oportunități diverse. Poți vedea exemple în descrierile fiecărei specializări."
    if 'durata' in question_lower or 'ani' in question_lower:
        return "Majoritatea programelor de licență durează 3 sau 4 ani (180 sau 240 credite). Verifică fișa fiecărei specializări."
    # Răspuns default
    return (f"Am înțeles întrebarea: „{question}”. Îți pot oferi informații despre specializări, cariere, credite etc. "
            "Te rog să reformulezi sau să întrebi ceva mai specific.")

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message', '')

    # Încearcă să folosești LLaMA prin Ollama
    try:
        response = requests.post('http://localhost:11434/api/generate',
                                 json={
                                     'model': 'llama3.1',  # sau 'llama2', 'mistral' etc.
                                     'prompt': 'Ești un consilier academic pentru specializări universitare. Răspunde la următoarea întrebare pe baza cunoștințelor tale:' + user_message
                                 },
                                 # timeout=25  # timeout scurt pentru a nu bloca aplicația
                                 )
        if response.status_code == 200:
            answer = response.text
            return jsonify({'answer': answer})
        else:
            # Fallback la răspunsul simplu
            answer = simple_chat_answer(user_message, specializations)
            return jsonify({'answer': answer + " (notă: răspuns generat local, LLaMA indisponibil)"})
    except Exception as e:
        print(f"Eroare conexiune Ollama: {e}")
        answer = simple_chat_answer(user_message, specializations)
        return jsonify({'answer': answer + " (notă: eroare la citire răspuns LLaMA)"})

if __name__ == '__main__':
    app.run(debug=True)
