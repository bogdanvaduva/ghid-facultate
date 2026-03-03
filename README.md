# ghid-facultate 🎓

**ghid-facultate** este un asistent inteligent web-based care ajută viitorii studenți să aleagă specializarea universitară potrivită, pe baza abilităților, intereselor și personalității lor. Aplicația utilizează o bază de date completă cu specializări din universitățile de stat și private din România (extrasă din HG 749/2009) și oferă recomandări personalizate, precum și un chatbot cu suport LLaMA (sau fallback local) pentru întrebări specifice.

## ✨ Funcționalități principale
- 📋 **Catalog complet** – Explorează toate specializările universitare acreditate din România.
- 🔍 **Recomandări personalizate** – Pe baza abilităților și intereselor tale, primești sugestii de specializări.
- 💬 **Chat inteligent** – Întreabă despre cariere, credite, forme de învățământ și perspective profesionale. Răspunsurile sunt generate local (fallback) sau prin LLaMA (dacă este configurat).
- ⚖️ **Comparare** – Compară două sau mai multe specializări pentru a face alegerea mai ușoară.
- 🏛️ **Date reale** – Specializările sunt preluate din HG 749/2009 și includ universități, facultăți, domenii, credite, acreditare și formă de învățământ.

## 🛠️ Tehnologii utilizate
- **Backend:** Python, Flask
- **Frontend:** HTML, CSS, JavaScript (vanilla)
- **Machine Learning / LLM:** LLaMA prin Ollama (opțional) + fallback bazat pe reguli
- **Extragere date:** PyMuPDF (pentru parsarea PDF-ului original)

## 🚀 Instalare și rulare
Configurare chat cu LLaMA (prin Ollama)
Pentru a beneficia de răspunsuri inteligente, poți integra modelul LLaMA folosind Ollama.

Instalare Ollama
Pe Linux/macOS:

bash
curl -fsSL https://ollama.com/install.sh | sh

Pe Windows:

Descarcă și rulează instalatorul de pe ollama.com.

Pornire Ollama
După instalare, Ollama rulează automat ca serviciu în fundal. Poți verifica cu:

bash
ollama serve
Descărcare model LLaMA 3
bash
ollama pull llama3
(Acest pas descarcă aproximativ 4.7 GB. Este necesar o singură dată.)

Verificare funcționare
Ollama va fi disponibil la adresa http://localhost:11434. Aplicația Flask va încerca automat să folosească acest endpoint pentru chat. Dacă Ollama nu rulează sau modelul lipsește, aplicația va folosi un fallback local (răspunsuri simple, pe baza cuvintelor cheie).

Pentru a testa manual dacă Ollama funcționează:

bash
curl http://localhost:11434/api/generate -d '{
  "model": "llama3",
  "prompt": "Care sunt specializările din domeniul ingineriei?",
  "stream": false
}'
Oprire Ollama (dacă este necesar)
bash

# Linux/macOS (dacă rulează ca serviciu)
sudo systemctl stop ollama

# Windows - din Managerul de servicii

### 1. Clonează repository-ul
```bash
git clone https://github.com/utilizator/ghid-facultate.git
cd ghid-facultate
