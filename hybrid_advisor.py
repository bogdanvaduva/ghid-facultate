# hybrid_advisor.py

class HybridSpecializationAdvisor:
    """
    Combines traditional ML with LLM capabilities for optimal performance
    """

    def __init__(self, specializations_data: List[Dict], use_llm: bool = True, api_key: str = None):
        self.specializations = specializations_data
        self.use_llm = use_llm

        # Traditional ML advisor (fast, reliable)
        self.ml_advisor = SpecializationAdvisor(specializations_data)

        # LLM advisor (smart, conversational)
        if use_llm and api_key:
            self.llm_advisor = LLMSpecializationAdvisor(api_key, specializations_data)
        else:
            self.llm_advisor = None

    def get_recommendations(self, student_profile: Dict) -> Dict:
        """
        Get recommendations using hybrid approach:
        - Use ML for initial filtering (fast)
        - Use LLM for deep reasoning (smart)
        """
        # Step 1: Get ML-based scores (fast)
        ml_scores = self.ml_advisor.assess_student_profile(student_profile)

        # Get top 5 from ML
        top_ml_specs = [spec for spec, score in ml_scores[:5]]

        # Step 2: If LLM is available, get detailed analysis
        if self.llm_advisor and self.use_llm:
            # Add ML scores to student profile
            enriched_profile = student_profile.copy()
            enriched_profile['ml_top_picks'] = top_ml_specs

            # Get LLM-enhanced recommendations
            llm_recommendations = self.llm_advisor.get_personalized_recommendations(enriched_profile)

            # Merge ML scores with LLM insights
            for rec in llm_recommendations.get('recommendations', []):
                # Find ML score
                ml_score = dict(ml_scores).get(rec['name'], 0)
                rec['ml_match_score'] = ml_score

            return llm_recommendations

        # Step 3: Fallback to ML-only recommendations
        else:
            detailed_recs = []
            for spec_name, score in ml_scores[:5]:
                spec_info = self.ml_advisor.get_detailed_info(spec_name)
                spec_info['match_score'] = round(score * 100, 2)
                detailed_recs.append(spec_info)

            return {
                'recommendations': detailed_recs,
                'overall_advice': "Based on your profile analysis, here are your best matches.",
                'next_steps': ["Research these specializations", "Talk to current students", "Try introductory courses"]
            }

    def chat(self, message: str, context: Dict = None) -> str:
        """
        Intelligent chat that uses LLM for complex queries,
        but falls back to rule-based for simple ones
        """
        message_lower = message.lower()

        # Simple queries - handle with rule-based (faster, cheaper)
        if any(word in message_lower for word in ['salary', 'earn', 'pay']):
            return self._handle_salary_query(message, context)
        elif any(word in message_lower for word in ['duration', 'long', 'years']):
            return self._handle_duration_query(message, context)

        # Complex queries - use LLM
        if self.llm_advisor and self.use_llm:
            return self.llm_advisor.chat_advisor(message)
        else:
            return self.ml_advisor.answer_question(message)

    def _handle_salary_query(self, message: str, context: Dict = None) -> str:
        """Handle salary-related queries with rule-based logic"""
        # Extract specialization from message or context
        spec_name = self._extract_specialization(message)
        if spec_name:
            spec = self.ml_advisor.get_detailed_info(spec_name)
            if spec:
                return f"💼 {spec['name']} graduates typically earn {spec['average_salary']}. Entry-level positions start around ${spec.get('entry_salary', 'competitive')}."

        return "I can help with salary information! Which specialization are you interested in?"

    def _extract_specialization(self, message: str) -> str:
        """Extract specialization name from message"""
        for spec in self.specializations:
            if spec['name'].lower() in message.lower():
                return spec['name']
        return None
