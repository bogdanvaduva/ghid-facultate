# assessment.py

class StudentAssessment:
    def __init__(self):
        self.responses = {
            'skills': [],
            'interests': [],
            'personality_traits': [],
            'desired_careers': [],
            'preferred_work_environment': [],
            'academic_strengths': []
        }

    def run_skills_assessment(self):
        """Interactive skills assessment"""
        print("\n=== Skills Assessment ===")
        skills_list = [
            "Programming", "Mathematics", "Writing", "Public Speaking",
            "Data Analysis", "Creative Design", "Problem Solving", "Leadership",
            "Foreign Languages", "Research", "Project Management", "Critical Thinking"
        ]

        print("Rate your proficiency in these skills (1-5):")
        for skill in skills_list:
            while True:
                try:
                    rating = int(input(f"{skill}: "))
                    if 1 <= rating <= 5:
                        if rating >= 4:  # Consider high proficiency as a skill
                            self.responses['skills'].append(skill)
                        break
                    else:
                        print("Please enter a number between 1 and 5")
                except ValueError:
                    print("Invalid input. Please enter a number.")

    def run_personality_quiz(self):
        """Quick personality assessment"""
        print("\n=== Personality Assessment ===")
        questions = [
            {
                "question": "Do you prefer working in teams or alone?",
                "options": ["Alone", "Small teams", "Large teams", "Mix of both"],
                "traits": {"Alone": "Independent", "Small teams": "Collaborative",
                           "Large teams": "Social", "Mix of both": "Flexible"}
            },
            {
                "question": "How do you approach problems?",
                "options": ["Step by step logically", "Creative/outside box",
                            "Research first", "Intuitively"],
                "traits": {"Step by step logically": "Analytical",
                           "Creative/outside box": "Innovative",
                           "Research first": "Methodical",
                           "Intuitively": "Intuitive"}
            }
        ]

        for q in questions:
            print(f"\n{q['question']}")
            for i, opt in enumerate(q['options'], 1):
                print(f"{i}. {opt}")

            choice = int(input("Choose (1-4): "))
            selected = q['options'][choice-1]
            self.responses['personality_traits'].append(q['traits'][selected])

    def run_career_goals(self):
        """Assess career aspirations"""
        print("\n=== Career Goals Assessment ===")
        careers = [
            "Software Engineer", "Data Scientist", "Business Analyst",
            "Doctor", "Lawyer", "Teacher", "Architect", "Marketing Manager",
            "Financial Analyst", "Entrepreneur", "Researcher", "Consultant"
        ]

        print("Select your top 3 career interests:")
        for i, career in enumerate(careers, 1):
            print(f"{i}. {career}")

        selected = []
        while len(selected) < 3:
            try:
                choice = int(input(f"Choose career #{len(selected)+1} (1-12): "))
                if 1 <= choice <= 12:
                    career = careers[choice-1]
                    if career not in selected:
                        selected.append(career)
                        self.responses['desired_careers'].append(career)
                    else:
                        print("Already selected. Choose another.")
                else:
                    print("Please enter a number between 1 and 12")
            except ValueError:
                print("Invalid input.")

    def get_full_profile(self):
        """Run all assessments and return complete profile"""
        self.run_skills_assessment()
        self.run_personality_quiz()
        self.run_career_goals()
        return self.responses
