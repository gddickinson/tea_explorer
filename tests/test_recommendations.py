"""
Tests for the recommendation engine
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from models import Tea
from recommendations.engine import RecommendationEngine


@pytest.fixture
def engine():
    return RecommendationEngine()


@pytest.fixture
def sample_teas():
    return [
        Tea(tea_id=1, name="Sencha", category="Green", origin="Japan",
            caffeine_level="Medium", flavor_profile="Fresh, grassy, vegetal"),
        Tea(tea_id=2, name="Gyokuro", category="Green", origin="Japan",
            caffeine_level="High", flavor_profile="Sweet, umami, rich"),
        Tea(tea_id=3, name="Dragonwell", category="Green", origin="China",
            caffeine_level="Medium", flavor_profile="Nutty, sweet, chestnut"),
        Tea(tea_id=4, name="Earl Grey", category="Black", origin="Sri Lanka",
            caffeine_level="High", flavor_profile="Bergamot, citrus, malty"),
        Tea(tea_id=5, name="Assam", category="Black", origin="India",
            caffeine_level="High", flavor_profile="Malty, bold, brisk"),
    ]


class TestRecommendationEngine:
    """Tests for the RecommendationEngine class"""

    def test_engine_creation(self, engine):
        """Test engine can be created"""
        assert engine is not None

    def test_similar_teas_same_category(self, engine, sample_teas):
        """Test that similar teas returns teas from the same category"""
        sencha = sample_teas[0]  # Green tea
        similar = engine.get_similar_teas(sencha, sample_teas, max_results=3)
        # Should prefer green teas
        assert len(similar) > 0
        assert all(t.name != "Sencha" for t in similar)

    def test_similar_teas_excludes_self(self, engine, sample_teas):
        """Test that similar teas never includes the reference tea"""
        sencha = sample_teas[0]
        similar = engine.get_similar_teas(sencha, sample_teas, max_results=10)
        assert sencha not in similar

    def test_similar_teas_max_results(self, engine, sample_teas):
        """Test max_results limit is respected"""
        similar = engine.get_similar_teas(sample_teas[0], sample_teas, max_results=2)
        assert len(similar) <= 2

    def test_recommend_by_category(self, engine, sample_teas):
        """Test recommending teas by category"""
        greens = engine.recommend_by_category("Green", sample_teas, max_results=5)
        assert len(greens) == 3  # Sencha, Gyokuro, Dragonwell
        assert all(t.category == "Green" for t in greens)

    def test_recommend_by_category_case_insensitive(self, engine, sample_teas):
        """Test category matching is case insensitive"""
        greens = engine.recommend_by_category("green", sample_teas, max_results=5)
        assert len(greens) == 3

    def test_recommend_by_origin(self, engine, sample_teas):
        """Test recommending teas by origin"""
        japanese = engine.recommend_by_origin("Japan", sample_teas, max_results=5)
        assert len(japanese) == 2
        assert all(t.origin == "Japan" for t in japanese)

    def test_recommend_for_beginners(self, engine, sample_teas):
        """Test beginner recommendations"""
        recs = engine.recommend_for_beginners(sample_teas, max_results=5)
        assert len(recs) > 0
        # Should include common categories
        categories = {t.category for t in recs}
        assert categories.issubset({"Green", "Black", "White"})

    def test_text_similarity(self, engine):
        """Test text similarity calculation"""
        sim = engine._text_similarity("fresh grassy green", "fresh grassy vegetal")
        assert sim > 0
        sim_zero = engine._text_similarity("chocolate", "citrus bergamot")
        assert sim_zero == 0.0

    def test_text_similarity_empty(self, engine):
        """Test text similarity with empty strings"""
        assert engine._text_similarity("", "") == 0.0
        assert engine._text_similarity("tea", "") == 0.0
