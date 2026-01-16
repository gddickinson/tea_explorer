"""
Recommendations Engine - Smart Tea Suggestions
Provides personalized tea recommendations based on various criteria
"""

from typing import List, Optional, Set, Dict
from collections import Counter
import re
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))
from models import Tea, JournalEntry


class RecommendationEngine:
    """
    Smart recommendation engine for tea suggestions
    Uses multiple strategies to find relevant teas
    """
    
    def __init__(self):
        """Initialize recommendation engine"""
        pass
    
    def get_similar_teas(
        self,
        tea: Tea,
        all_teas: List[Tea],
        max_results: int = 5
    ) -> List[Tea]:
        """
        Get teas similar to the given tea
        
        Args:
            tea: Reference tea
            all_teas: List of all teas to search
            max_results: Maximum number of recommendations
            
        Returns:
            List of similar Tea objects
        """
        scored_teas = []
        
        for candidate in all_teas:
            # Skip the tea itself
            if candidate.tea_id == tea.tea_id:
                continue
            
            score = self._calculate_similarity(tea, candidate)
            scored_teas.append((score, candidate))
        
        # Sort by score (descending) and return top results
        scored_teas.sort(reverse=True, key=lambda x: x[0])
        return [tea for score, tea in scored_teas[:max_results] if score > 0]
    
    def _calculate_similarity(self, tea1: Tea, tea2: Tea) -> float:
        """
        Calculate similarity score between two teas
        
        Args:
            tea1: First tea
            tea2: Second tea
            
        Returns:
            Similarity score (higher = more similar)
        """
        score = 0.0
        
        # Same category (strong match)
        if tea1.category and tea2.category and tea1.category == tea2.category:
            score += 3.0
        
        # Same origin country (medium match)
        if tea1.origin and tea2.origin and tea1.origin == tea2.origin:
            score += 2.0
        
        # Same region (weak match)
        if tea1.origin_region and tea2.origin_region and tea1.origin_region == tea2.origin_region:
            score += 1.0
        
        # Similar caffeine level (weak match)
        if tea1.caffeine_level and tea2.caffeine_level and tea1.caffeine_level == tea2.caffeine_level:
            score += 0.5
        
        # Similar flavor profile (text similarity)
        if tea1.flavor_profile and tea2.flavor_profile:
            flavor_sim = self._text_similarity(tea1.flavor_profile, tea2.flavor_profile)
            score += flavor_sim * 2.0
        
        # Similar processing method
        if tea1.processing_method and tea2.processing_method and tea1.processing_method == tea2.processing_method:
            score += 1.0
        
        return score
    
    def _text_similarity(self, text1: str, text2: str) -> float:
        """
        Calculate text similarity based on common words
        
        Args:
            text1: First text
            text2: Second text
            
        Returns:
            Similarity score between 0 and 1
        """
        # Convert to lowercase and split into words
        words1 = set(re.findall(r'\w+', text1.lower()))
        words2 = set(re.findall(r'\w+', text2.lower()))
        
        # Remove common stop words
        stop_words = {'a', 'an', 'the', 'and', 'or', 'but', 'with', 'of', 'in', 'to', 'for'}
        words1 = words1 - stop_words
        words2 = words2 - stop_words
        
        if not words1 or not words2:
            return 0.0
        
        # Calculate Jaccard similarity
        intersection = len(words1 & words2)
        union = len(words1 | words2)
        
        return intersection / union if union > 0 else 0.0
    
    def recommend_based_on_ratings(
        self,
        entries: List[JournalEntry],
        all_teas: List[Tea],
        min_rating: int = 4,
        max_results: int = 5
    ) -> List[Tea]:
        """
        Recommend teas based on highly rated entries
        
        Args:
            entries: List of journal entries
            all_teas: List of all teas
            min_rating: Minimum rating to consider
            max_results: Maximum recommendations
            
        Returns:
            List of recommended teas
        """
        # Get highly rated tea names
        highly_rated = set()
        for entry in entries:
            if entry.rating and entry.rating >= min_rating:
                highly_rated.add(entry.tea_name)
        
        if not highly_rated:
            return []
        
        # Find teas similar to highly rated ones
        recommendations = []
        tea_dict = {tea.name: tea for tea in all_teas}
        
        for tea_name in highly_rated:
            if tea_name in tea_dict:
                reference_tea = tea_dict[tea_name]
                similar = self.get_similar_teas(reference_tea, all_teas, max_results=3)
                recommendations.extend(similar)
        
        # Remove duplicates and limit results
        seen = set()
        unique_recommendations = []
        for tea in recommendations:
            if tea.name not in seen and tea.name not in highly_rated:
                seen.add(tea.name)
                unique_recommendations.append(tea)
                if len(unique_recommendations) >= max_results:
                    break
        
        return unique_recommendations
    
    def recommend_by_category(
        self,
        category: str,
        all_teas: List[Tea],
        max_results: int = 5
    ) -> List[Tea]:
        """
        Recommend teas from a specific category
        
        Args:
            category: Tea category
            all_teas: List of all teas
            max_results: Maximum recommendations
            
        Returns:
            List of recommended teas
        """
        category_teas = [
            tea for tea in all_teas
            if tea.category and tea.category.lower() == category.lower()
        ]
        
        return category_teas[:max_results]
    
    def recommend_by_origin(
        self,
        country: str,
        all_teas: List[Tea],
        max_results: int = 5
    ) -> List[Tea]:
        """
        Recommend teas from a specific origin
        
        Args:
            country: Origin country
            all_teas: List of all teas
            max_results: Maximum recommendations
            
        Returns:
            List of recommended teas
        """
        origin_teas = [
            tea for tea in all_teas
            if tea.origin and tea.origin.lower() == country.lower()
        ]
        
        return origin_teas[:max_results]
    
    def recommend_for_beginners(
        self,
        all_teas: List[Tea],
        max_results: int = 5
    ) -> List[Tea]:
        """
        Recommend teas suitable for beginners
        
        Looks for:
        - Common categories (Green, Black)
        - Mild/medium caffeine
        - Approachable flavor profiles
        
        Args:
            all_teas: List of all teas
            max_results: Maximum recommendations
            
        Returns:
            List of beginner-friendly teas
        """
        beginner_friendly = []
        
        for tea in all_teas:
            score = 0
            
            # Prefer common categories
            if tea.category in ['Green', 'Black', 'White']:
                score += 2
            
            # Prefer mild/medium caffeine
            if tea.caffeine_level in ['Low', 'Low to Medium', 'Medium']:
                score += 1
            
            # Prefer approachable flavors
            if tea.flavor_profile:
                friendly_words = ['sweet', 'mild', 'smooth', 'gentle', 'delicate']
                if any(word in tea.flavor_profile.lower() for word in friendly_words):
                    score += 1
            
            if score > 0:
                beginner_friendly.append((score, tea))
        
        # Sort by score and return top results
        beginner_friendly.sort(reverse=True, key=lambda x: x[0])
        return [tea for score, tea in beginner_friendly[:max_results]]
    
    def recommend_to_try_next(
        self,
        entries: List[JournalEntry],
        all_teas: List[Tea],
        max_results: int = 5
    ) -> List[Tea]:
        """
        Recommend new teas to try based on tasting history
        
        Args:
            entries: List of journal entries
            all_teas: List of all teas
            max_results: Maximum recommendations
            
        Returns:
            List of teas to try next
        """
        # Get teas already tried
        tried_teas = set(entry.tea_name for entry in entries)
        
        # Get categories and origins the user likes
        liked_categories = []
        liked_origins = []
        
        tea_dict = {tea.name: tea for tea in all_teas}
        
        for entry in entries:
            if entry.rating and entry.rating >= 4:
                if entry.tea_name in tea_dict:
                    tea = tea_dict[entry.tea_name]
                    if tea.category:
                        liked_categories.append(tea.category)
                    if tea.origin:
                        liked_origins.append(tea.origin)
        
        # Count preferences
        category_preferences = Counter(liked_categories).most_common(3)
        origin_preferences = Counter(liked_origins).most_common(3)
        
        # Score untried teas
        recommendations = []
        for tea in all_teas:
            if tea.name in tried_teas:
                continue
            
            score = 0
            
            # Bonus for matching preferred categories
            for category, count in category_preferences:
                if tea.category == category:
                    score += count * 2
            
            # Bonus for matching preferred origins
            for origin, count in origin_preferences:
                if tea.origin == origin:
                    score += count
            
            if score > 0:
                recommendations.append((score, tea))
        
        # Sort by score and return top results
        recommendations.sort(reverse=True, key=lambda x: x[0])
        return [tea for score, tea in recommendations[:max_results]]


if __name__ == '__main__':
    # Demo usage
    print("Recommendation Engine Demo")
    print("=" * 50)
    
    # Create sample teas
    teas = [
        type('Tea', (), {
            'tea_id': 1, 'name': 'Sencha', 'category': 'Green',
            'origin': 'Japan', 'origin_region': 'Shizuoka',
            'caffeine_level': 'Medium', 'flavor_profile': 'Fresh, grassy',
            'processing_method': 'Steamed'
        })(),
        type('Tea', (), {
            'tea_id': 2, 'name': 'Gyokuro', 'category': 'Green',
            'origin': 'Japan', 'origin_region': 'Uji',
            'caffeine_level': 'High', 'flavor_profile': 'Sweet, umami',
            'processing_method': 'Shade-grown'
        })(),
        type('Tea', (), {
            'tea_id': 3, 'name': 'Dragonwell', 'category': 'Green',
            'origin': 'China', 'origin_region': 'Zhejiang',
            'caffeine_level': 'Medium', 'flavor_profile': 'Nutty, sweet',
            'processing_method': 'Pan-fired'
        })(),
    ]
    
    # Test recommendations
    engine = RecommendationEngine()
    
    # Similar to Sencha
    similar = engine.get_similar_teas(teas[0], teas, max_results=2)
    print(f"\nSimilar to {teas[0].name}:")
    for tea in similar:
        print(f"  - {tea.name} ({tea.category}, {tea.origin})")
    
    # Beginner recommendations
    beginners = engine.recommend_for_beginners(teas, max_results=2)
    print(f"\nFor beginners:")
    for tea in beginners:
        print(f"  - {tea.name} ({tea.category})")
