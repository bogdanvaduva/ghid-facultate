# ai_advisor.py

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import json

class SpecializationAdvisor:
    def __init__(self, specializations_data):
        self.specializations = specializations_data
        self.vectorizer = TfidfVectorizer()
        self.specialization_vectors = self._create_vectors()

    def _create_vectors(self):
        """Create TF-IDF vectors for specializations based on descriptions and skills"""
        texts = []
        for spec in self.specializations:
            # Combine relevant fields for matching
            combined_text =  f"{spec['name']}" # f"{spec['description']} {' '.join(spec['key_skills'])} {' '.join(spec['career_paths'])}"
            texts.append(combined_text)

        return self.vectorizer.fit_transform(texts)

    def assess_student_profile(self, student_responses):
        """
        Analyze student's interests, skills, and preferences
        """
        profile_score = {}

        # Calculate compatibility scores for each specialization
        for spec in self.specializations:
            score = self._calculate_compatibility(spec, student_responses)
            profile_score[spec['name']] = score

        # Sort by score
        recommendations = sorted(profile_score.items(), key=lambda x: x[1], reverse=True)
        return recommendations[:5]  # Top 5 recommendations

    def _calculate_compatibility(self, specialization, student_profile):
        """
        Calculate how well a specialization matches a student's profile
        """
        score = 0

        # Skill match (40% weight)
        student_skills = set(student_profile.get('skills', []))
        spec_skills = set(specialization['key_skills'])
        skill_match = len(student_skills.intersection(spec_skills)) / len(spec_skills)
        score += skill_match * 0.4

        # Personality match (30% weight)
        student_traits = set(student_profile.get('personality_traits', []))
        spec_traits = set(specialization['personality_traits'])
        trait_match = len(student_traits.intersection(spec_traits)) / len(spec_traits) if spec_traits else 0
        score += trait_match * 0.3

        # Career goals alignment (30% weight)
        student_careers = set(student_profile.get('desired_careers', []))
        spec_careers = set(specialization['career_paths'])
        career_match = len(student_careers.intersection(spec_careers)) / len(spec_careers) if spec_careers else 0
        score += career_match * 0.3

        return score

    def get_detailed_info(self, specialization_name):
        """Get detailed information about a specific specialization"""
        for spec in self.specializations:
            if spec['name'].lower() == specialization_name.lower():
                return spec
        return None

    def compare_specializations(self, spec_names):
        """Compare multiple specializations side by side"""
        comparisons = []
        for name in spec_names:
            spec = self.get_detailed_info(name)
            if spec:
                comparisons.append(spec)
        return comparisons

    def answer_question(self, question, context=None):
        """
        Simple Q&A functionality about specializations
        """
        question = question.lower()

        # Common question patterns
        if "salary" in question or "earn" in question:
            for spec in self.specializations:
                if spec['name'].lower() in question:
                    return f"{spec['name']} average salary: {spec['average_salary']}"

        elif "career" in question or "job" in question:
            for spec in self.specializations:
                if spec['name'].lower() in question:
                    return f"Career paths for {spec['name']}: {', '.join(spec['career_paths'])}"

        elif "difficulty" in question or "hard" in question:
            for spec in self.specializations:
                if spec['name'].lower() in question:
                    return f"{spec['name']} difficulty level: {spec['difficulty_level']}"

        return "I can help with information about specializations, careers, salaries, and requirements. Please be more specific."
