"""
Data Visualizations - Charts and Analytics
Creates beautiful charts for tea collection insights
"""

import matplotlib
matplotlib.use('TkAgg')  # Use Tkinter backend

import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from collections import Counter
from typing import List, Dict, Tuple, Optional
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))
from models import Tea, JournalEntry


class ChartGenerator:
    """Generates charts and visualizations for tea data"""
    
    def __init__(self, style: str = 'seaborn-v0_8-darkgrid'):
        """
        Initialize chart generator
        
        Args:
            style: Matplotlib style to use
        """
        # Try to use modern style, fall back to default
        try:
            plt.style.use(style)
        except:
            pass
    
    def create_category_distribution(
        self,
        teas: List[Tea],
        figsize: Tuple[int, int] = (8, 6)
    ) -> Figure:
        """
        Create pie chart of tea categories
        
        Args:
            teas: List of Tea objects
            figsize: Figure size (width, height)
            
        Returns:
            matplotlib Figure
        """
        # Count categories
        categories = [tea.category for tea in teas if tea.category]
        category_counts = Counter(categories)
        
        # Create figure
        fig = Figure(figsize=figsize)
        ax = fig.add_subplot(111)
        
        # Colors - tea-inspired
        colors = ['#689f38', '#5d4037', '#ff6f00', '#e0e0e0', '#9c27b0']
        
        # Create pie chart
        wedges, texts, autotexts = ax.pie(
            category_counts.values(),
            labels=category_counts.keys(),
            autopct='%1.1f%%',
            colors=colors,
            startangle=90
        )
        
        # Style text
        for text in texts:
            text.set_fontsize(11)
            text.set_weight('bold')
        
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontsize(10)
            autotext.set_weight('bold')
        
        ax.set_title('Tea Collection by Category', fontsize=14, weight='bold', pad=20)
        
        return fig
    
    def create_origin_distribution(
        self,
        teas: List[Tea],
        figsize: Tuple[int, int] = (10, 6),
        top_n: int = 10
    ) -> Figure:
        """
        Create bar chart of tea origins
        
        Args:
            teas: List of Tea objects
            figsize: Figure size
            top_n: Number of top countries to show
            
        Returns:
            matplotlib Figure
        """
        # Count origins
        origins = [tea.origin for tea in teas if tea.origin]
        origin_counts = Counter(origins).most_common(top_n)
        
        countries = [item[0] for item in origin_counts]
        counts = [item[1] for item in origin_counts]
        
        # Create figure
        fig = Figure(figsize=figsize)
        ax = fig.add_subplot(111)
        
        # Create bar chart
        colors = plt.cm.viridis(np.linspace(0.3, 0.9, len(countries)))
        bars = ax.barh(countries, counts, color=colors)
        
        # Add value labels
        for i, bar in enumerate(bars):
            width = bar.get_width()
            ax.text(
                width, bar.get_y() + bar.get_height()/2,
                f' {int(width)}',
                va='center', ha='left',
                fontsize=10, weight='bold'
            )
        
        ax.set_xlabel('Number of Teas', fontsize=11, weight='bold')
        ax.set_title(f'Top {top_n} Tea Origins', fontsize=14, weight='bold', pad=20)
        ax.grid(axis='x', alpha=0.3)
        
        fig.tight_layout()
        
        return fig
    
    def create_rating_distribution(
        self,
        entries: List[JournalEntry],
        figsize: Tuple[int, int] = (8, 6)
    ) -> Figure:
        """
        Create histogram of ratings
        
        Args:
            entries: List of JournalEntry objects
            figsize: Figure size
            
        Returns:
            matplotlib Figure
        """
        # Get ratings
        ratings = [entry.rating for entry in entries if entry.rating]
        
        if not ratings:
            # Empty figure if no ratings
            fig = Figure(figsize=figsize)
            ax = fig.add_subplot(111)
            ax.text(
                0.5, 0.5, 'No ratings yet',
                ha='center', va='center',
                fontsize=14, color='gray'
            )
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            ax.axis('off')
            return fig
        
        # Create figure
        fig = Figure(figsize=figsize)
        ax = fig.add_subplot(111)
        
        # Create histogram
        bins = [0.5, 1.5, 2.5, 3.5, 4.5, 5.5]
        counts, _, bars = ax.hist(
            ratings,
            bins=bins,
            color='#689f38',
            edgecolor='white',
            linewidth=1.5
        )
        
        # Add value labels on bars
        for count, bar in zip(counts, bars):
            height = bar.get_height()
            if height > 0:
                ax.text(
                    bar.get_x() + bar.get_width()/2, height,
                    f'{int(count)}',
                    ha='center', va='bottom',
                    fontsize=11, weight='bold'
                )
        
        ax.set_xlabel('Rating (Stars)', fontsize=11, weight='bold')
        ax.set_ylabel('Number of Reviews', fontsize=11, weight='bold')
        ax.set_title('Tea Rating Distribution', fontsize=14, weight='bold', pad=20)
        ax.set_xticks([1, 2, 3, 4, 5])
        ax.set_xticklabels(['⭐', '⭐⭐', '⭐⭐⭐', '⭐⭐⭐⭐', '⭐⭐⭐⭐⭐'])
        ax.grid(axis='y', alpha=0.3)
        
        # Show average rating
        avg_rating = sum(ratings) / len(ratings)
        ax.axvline(
            avg_rating, color='#ff6f00', linestyle='--',
            linewidth=2, label=f'Average: {avg_rating:.1f}★'
        )
        ax.legend(fontsize=10)
        
        fig.tight_layout()
        
        return fig
    
    def create_caffeine_comparison(
        self,
        teas: List[Tea],
        figsize: Tuple[int, int] = (8, 6)
    ) -> Figure:
        """
        Create bar chart of caffeine levels
        
        Args:
            teas: List of Tea objects
            figsize: Figure size
            
        Returns:
            matplotlib Figure
        """
        # Count caffeine levels
        caffeine_levels = [tea.caffeine_level for tea in teas if tea.caffeine_level]
        caffeine_counts = Counter(caffeine_levels)
        
        # Order: Very Low, Low, Medium, High, Very High
        order = ['Very Low', 'Low', 'Low to Medium', 'Medium', 'Medium to High', 'High', 'Very High']
        labels = []
        values = []
        
        for level in order:
            if level in caffeine_counts:
                labels.append(level)
                values.append(caffeine_counts[level])
        
        if not labels:
            # Empty figure
            fig = Figure(figsize=figsize)
            ax = fig.add_subplot(111)
            ax.text(
                0.5, 0.5, 'No caffeine data',
                ha='center', va='center',
                fontsize=14, color='gray'
            )
            ax.axis('off')
            return fig
        
        # Create figure
        fig = Figure(figsize=figsize)
        ax = fig.add_subplot(111)
        
        # Color gradient from light to dark
        colors = plt.cm.YlOrRd(np.linspace(0.3, 0.9, len(labels)))
        bars = ax.bar(range(len(labels)), values, color=colors, edgecolor='white', linewidth=1.5)
        
        # Add value labels
        for i, (bar, value) in enumerate(zip(bars, values)):
            height = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width()/2, height,
                f'{int(value)}',
                ha='center', va='bottom',
                fontsize=11, weight='bold'
            )
        
        ax.set_xticks(range(len(labels)))
        ax.set_xticklabels(labels, rotation=45, ha='right')
        ax.set_ylabel('Number of Teas', fontsize=11, weight='bold')
        ax.set_title('Caffeine Level Distribution', fontsize=14, weight='bold', pad=20)
        ax.grid(axis='y', alpha=0.3)
        
        fig.tight_layout()
        
        return fig
    
    def save_chart(self, fig: Figure, filename: str, dpi: int = 150):
        """
        Save chart to file
        
        Args:
            fig: matplotlib Figure
            filename: Output filename
            dpi: Resolution (dots per inch)
        """
        fig.savefig(filename, dpi=dpi, bbox_inches='tight')
        print(f"Chart saved to {filename}")


class DashboardGenerator:
    """Creates comprehensive dashboard with multiple charts"""
    
    def __init__(self):
        self.chart_gen = ChartGenerator()
    
    def create_overview_dashboard(
        self,
        teas: List[Tea],
        entries: List[JournalEntry],
        figsize: Tuple[int, int] = (16, 10)
    ) -> Figure:
        """
        Create overview dashboard with multiple charts
        
        Args:
            teas: List of Tea objects
            entries: List of JournalEntry objects
            figsize: Figure size
            
        Returns:
            matplotlib Figure with subplots
        """
        fig = Figure(figsize=figsize)
        
        # 2x2 grid of subplots
        gs = fig.add_gridspec(2, 2, hspace=0.3, wspace=0.3)
        
        # Top left: Category distribution
        ax1 = fig.add_subplot(gs[0, 0])
        self._add_category_pie(ax1, teas)
        
        # Top right: Origin distribution
        ax2 = fig.add_subplot(gs[0, 1])
        self._add_origin_bars(ax2, teas, top_n=5)
        
        # Bottom left: Rating distribution
        ax3 = fig.add_subplot(gs[1, 0])
        self._add_rating_histogram(ax3, entries)
        
        # Bottom right: Statistics text
        ax4 = fig.add_subplot(gs[1, 1])
        self._add_statistics_text(ax4, teas, entries)
        
        fig.suptitle('Tea Collection Dashboard', fontsize=18, weight='bold', y=0.98)
        
        return fig
    
    def _add_category_pie(self, ax, teas):
        """Add category pie chart to axis"""
        categories = [tea.category for tea in teas if tea.category]
        category_counts = Counter(categories)
        
        colors = ['#689f38', '#5d4037', '#ff6f00', '#e0e0e0', '#9c27b0']
        
        wedges, texts, autotexts = ax.pie(
            category_counts.values(),
            labels=category_counts.keys(),
            autopct='%1.1f%%',
            colors=colors,
            startangle=90
        )
        
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontsize(9)
            autotext.set_weight('bold')
        
        ax.set_title('By Category', fontsize=12, weight='bold')
    
    def _add_origin_bars(self, ax, teas, top_n=5):
        """Add origin bar chart to axis"""
        origins = [tea.origin for tea in teas if tea.origin]
        origin_counts = Counter(origins).most_common(top_n)
        
        countries = [item[0] for item in origin_counts]
        counts = [item[1] for item in origin_counts]
        
        colors = plt.cm.viridis(np.linspace(0.3, 0.9, len(countries)))
        bars = ax.barh(countries, counts, color=colors)
        
        for bar in bars:
            width = bar.get_width()
            ax.text(
                width, bar.get_y() + bar.get_height()/2,
                f' {int(width)}',
                va='center', ha='left',
                fontsize=9
            )
        
        ax.set_xlabel('Count', fontsize=10)
        ax.set_title('Top Origins', fontsize=12, weight='bold')
        ax.grid(axis='x', alpha=0.3)
    
    def _add_rating_histogram(self, ax, entries):
        """Add rating histogram to axis"""
        ratings = [entry.rating for entry in entries if entry.rating]
        
        if not ratings:
            ax.text(0.5, 0.5, 'No ratings yet', ha='center', va='center', fontsize=12, color='gray')
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            ax.axis('off')
            return
        
        bins = [0.5, 1.5, 2.5, 3.5, 4.5, 5.5]
        ax.hist(ratings, bins=bins, color='#689f38', edgecolor='white')
        
        ax.set_xlabel('Rating', fontsize=10)
        ax.set_ylabel('Count', fontsize=10)
        ax.set_title('Rating Distribution', fontsize=12, weight='bold')
        ax.set_xticks([1, 2, 3, 4, 5])
        ax.grid(axis='y', alpha=0.3)
        
        avg = sum(ratings) / len(ratings)
        ax.axvline(avg, color='#ff6f00', linestyle='--', linewidth=2)
    
    def _add_statistics_text(self, ax, teas, entries):
        """Add statistics text to axis"""
        ax.axis('off')
        
        # Calculate statistics
        total_teas = len(teas)
        total_entries = len(entries)
        
        avg_rating = 0
        if entries:
            ratings = [e.rating for e in entries if e.rating]
            avg_rating = sum(ratings) / len(ratings) if ratings else 0
        
        categories = len(set(tea.category for tea in teas if tea.category))
        countries = len(set(tea.origin for tea in teas if tea.origin))
        
        # Create statistics text
        stats_text = f"""
Collection Statistics
{'='*25}

Total Teas:      {total_teas:>6}
Journal Entries: {total_entries:>6}
Average Rating:  {avg_rating:>6.1f}★

Categories:      {categories:>6}
Countries:       {countries:>6}

{'='*25}
        """
        
        ax.text(
            0.1, 0.95, stats_text,
            fontsize=11,
            family='monospace',
            verticalalignment='top',
            transform=ax.transAxes
        )
        
        ax.set_title('Statistics', fontsize=12, weight='bold')


if __name__ == '__main__':
    # Demo usage
    import tkinter as tk
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    
    # Create sample data
    sample_teas = [
        type('Tea', (), {'category': 'Green', 'origin': 'Japan', 'caffeine_level': 'Medium'})(),
        type('Tea', (), {'category': 'Green', 'origin': 'China', 'caffeine_level': 'Low'})(),
        type('Tea', (), {'category': 'Black', 'origin': 'India', 'caffeine_level': 'High'})(),
        type('Tea', (), {'category': 'Oolong', 'origin': 'China', 'caffeine_level': 'Medium'})(),
        type('Tea', (), {'category': 'Green', 'origin': 'Japan', 'caffeine_level': 'Medium'})(),
    ]
    
    sample_entries = [
        type('Entry', (), {'rating': 5})(),
        type('Entry', (), {'rating': 4})(),
        type('Entry', (), {'rating': 5})(),
        type('Entry', (), {'rating': 3})(),
    ]
    
    # Create window
    root = tk.Tk()
    root.title("Visualization Demo")
    root.geometry("800x600")
    
    # Create chart
    gen = ChartGenerator()
    fig = gen.create_category_distribution(sample_teas)
    
    # Embed in tkinter
    canvas = FigureCanvasTkAgg(fig, root)
    canvas.draw()
    canvas.get_tk_widget().pack(fill='both', expand=True)
    
    root.mainloop()
