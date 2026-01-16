"""
Tests for models
"""

import pytest
from models import Tea, Blend, JournalEntry


class TestTeaModel:
    """Tests for Tea model"""
    
    def test_create_tea(self):
        """Test creating a tea"""
        tea = Tea(name="Sencha", category="Green")
        assert tea.name == "Sencha"
        assert tea.category == "Green"
    
    def test_tea_from_dict(self):
        """Test creating tea from dictionary"""
        data = {
            'tea_id': 1,
            'name': 'Sencha',
            'category': 'Green',
            'origin_country': 'Japan'
        }
        tea = Tea.from_dict(data)
        assert tea.tea_id == 1
        assert tea.name == 'Sencha'
        assert tea.category == 'Green'
        assert tea.origin_country == 'Japan'
    
    def test_tea_to_dict(self):
        """Test converting tea to dictionary"""
        tea = Tea(name="Sencha", category="Green")
        data = tea.to_dict()
        assert data['name'] == 'Sencha'
        assert data['category'] == 'Green'
    
    def test_tea_display_name(self):
        """Test tea display name"""
        tea = Tea(name="Sencha", origin_region="Shizuoka")
        assert tea.get_display_name() == "Sencha (Shizuoka)"
    
    def test_tea_temperature_display(self):
        """Test temperature display"""
        tea = Tea(brew_temp_c=80, brew_temp_f=176)
        assert tea.get_temperature_display() == "80°C / 176°F"


class TestBlendModel:
    """Tests for Blend model"""
    
    def test_create_blend(self):
        """Test creating a blend"""
        blend = Blend(blend_name="Earl Grey", category="Black")
        assert blend.blend_name == "Earl Grey"
        assert blend.category == "Black"
    
    def test_blend_from_dict(self):
        """Test creating blend from dictionary"""
        data = {
            'blend_id': 1,
            'blend_name': 'Earl Grey',
            'category': 'Black',
            'ingredients': 'Black tea, bergamot'
        }
        blend = Blend.from_dict(data)
        assert blend.blend_id == 1
        assert blend.blend_name == 'Earl Grey'


class TestJournalEntryModel:
    """Tests for JournalEntry model"""
    
    def test_create_entry(self):
        """Test creating journal entry"""
        entry = JournalEntry(
            tea_name="Sencha",
            date="2026-01-15",
            rating=5,
            notes="Excellent"
        )
        assert entry.tea_name == "Sencha"
        assert entry.rating == 5
    
    def test_rating_validation(self):
        """Test rating validation"""
        entry = JournalEntry(tea_name="Test", date="2026-01-15", rating=10)
        assert entry.rating == 5  # Should be clamped to 5
        
        entry = JournalEntry(tea_name="Test", date="2026-01-15", rating=-1)
        assert entry.rating == 1  # Should be clamped to 1
    
    def test_star_display(self):
        """Test star rating display"""
        entry = JournalEntry(tea_name="Test", date="2026-01-15", rating=3)
        assert entry.get_star_display() == "★★★☆☆"
