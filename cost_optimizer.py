# cost_optimizer.py

class LLMCostOptimizer:
    """
    Optimize LLM usage to reduce costs
    """

    def __init__(self, advisor):
        self.advisor = advisor
        self.query_count = 0
        self.cache = {}

    def get_recommendations_cached(self, student_profile: Dict) -> Dict:
        """
        Cache recommendations for similar profiles
        """
        # Create profile hash
        profile_hash = self._hash_profile(student_profile)

        if profile_hash in self.cache:
            print("Returning cached recommendation")
            return self.cache[profile_hash]

        # Get new recommendation
        recommendations = self.advisor.get_recommendations(student_profile)

        # Cache it
        self.cache[profile_hash] = recommendations

        return recommendations

    def _hash_profile(self, profile: Dict) -> str:
        """Create a hash of the student profile for caching"""
        import hashlib
        import json

        # Normalize profile
        normalized = {
            'skills': sorted(profile.get('skills', [])),
            'interests': sorted(profile.get('interests', [])),
            'personality': sorted(profile.get('personality_traits', [])),
            'careers': sorted(profile.get('desired_careers', []))
        }

        profile_str = json.dumps(normalized, sort_keys=True)
        return hashlib.md5(profile_str.encode()).hexdigest()

    def should_use_llm(self, query: str) -> bool:
        """
        Decide whether to use LLM based on query complexity
        """
        self.query_count += 1

        # Simple heuristics
        complex_keywords = ['compare', 'difference between', 'why', 'how', 'explain', 'advice']
        simple_keywords = ['salary', 'duration', 'prerequisites', 'courses']

        query_lower = query.lower()

        # Check for complex queries
        if any(keyword in query_lower for keyword in complex_keywords):
            return True

        # Check for simple queries
        if any(keyword in query_lower for keyword in simple_keywords):
            return False

        # Default: use ML for first few queries, then LLM for follow-ups
        return self.query_count > 3
