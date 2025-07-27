"""
Visualization module for LTE signal metrics
Generates graphs and charts for signal quality analysis
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import logging
from pathlib import Path
from config import VIZ_CONFIG, SIGNAL_THRESHOLDS

# Set style for better looking plots
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

class SignalVisualizer:
    """Handles visualization of LTE signal metrics"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Create output directory for plots
        Path('plots').mkdir(exist_ok=True)
        
        # Set figure size and DPI
        plt.rcParams['figure.figsize'] = VIZ_CONFIG['figure_size']
        plt.rcParams['figure.dpi'] = VIZ_CONFIG['dpi']
    
    def plot_signal_timeline(self, csv_file: str, hours: int = 24, save_plot: bool = True) -> str:
        """Plot signal metrics over time"""
        try:
            # Read data
            df = pd.read_csv(csv_file)
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            
            # Filter by time range
            cutoff_time = datetime.now() - timedelta(hours=hours)
            recent_data = df[df['timestamp'] >= cutoff_time]
            
            if recent_data.empty:
                self.logger.warning("No data available for timeline plot")
                return ""
            
            # Create subplots
            fig, axes = plt.subplots(2, 2, figsize=(15, 10))
            fig.suptitle(f'LTE Signal Metrics Timeline (Last {hours} Hours)', fontsize=16)
            
            # Plot RSRP
            axes[0, 0].plot(recent_data['timestamp'], recent_data['rsrp'], 'b-', alpha=0.7)
            axes[0, 0].set_title('RSRP Over Time')
            axes[0, 0].set_ylabel('RSRP (dBm)')
            axes[0, 0].grid(True, alpha=0.3)
            
            # Plot RSRQ
            axes[0, 1].plot(recent_data['timestamp'], recent_data['rsrq'], 'g-', alpha=0.7)
            axes[0, 1].set_title('RSRQ Over Time')
            axes[0, 1].set_ylabel('RSRQ (dB)')
            axes[0, 1].grid(True, alpha=0.3)
            
            # Plot SINR
            axes[1, 0].plot(recent_data['timestamp'], recent_data['sinr'], 'r-', alpha=0.7)
            axes[1, 0].set_title('SINR Over Time')
            axes[1, 0].set_ylabel('SINR (dB)')
            axes[1, 0].grid(True, alpha=0.3)
            
            # Plot Bandwidth Score
            axes[1, 1].plot(recent_data['timestamp'], recent_data['bandwidth_score'], 'purple', alpha=0.7)
            axes[1, 1].set_title('Bandwidth Score Over Time')
            axes[1, 1].set_ylabel('Bandwidth Score')
            axes[1, 1].grid(True, alpha=0.3)
            
            # Rotate x-axis labels for better readability
            for ax in axes.flat:
                ax.tick_params(axis='x', rotation=45)
            
            plt.tight_layout()
            
            if save_plot:
                filename = f"plots/signal_timeline_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                plt.savefig(filename, dpi=VIZ_CONFIG['dpi'], bbox_inches='tight')
                self.logger.info(f"Timeline plot saved to {filename}")
                return filename
            
            plt.show()
            return ""
            
        except Exception as e:
            self.logger.error(f"Error creating timeline plot: {e}")
            return ""
    
    def plot_band_comparison(self, csv_file: str, save_plot: bool = True) -> str:
        """Create comparison plots for different LTE bands"""
        try:
            # Read data
            df = pd.read_csv(csv_file)
            
            if df.empty:
                self.logger.warning("No data available for band comparison")
                return ""
            
            # Create figure with subplots
            fig, axes = plt.subplots(2, 2, figsize=(16, 12))
            fig.suptitle('LTE Band Performance Comparison', fontsize=16)
            
            # Box plot for RSRP by band
            sns.boxplot(data=df, x='band', y='rsrp', ax=axes[0, 0])
            axes[0, 0].set_title('RSRP Distribution by Band')
            axes[0, 0].set_ylabel('RSRP (dBm)')
            axes[0, 0].tick_params(axis='x', rotation=45)
            
            # Box plot for SINR by band
            sns.boxplot(data=df, x='band', y='sinr', ax=axes[0, 1])
            axes[0, 1].set_title('SINR Distribution by Band')
            axes[0, 1].set_ylabel('SINR (dB)')
            axes[0, 1].tick_params(axis='x', rotation=45)
            
            # Violin plot for bandwidth score
            sns.violinplot(data=df, x='band', y='bandwidth_score', ax=axes[1, 0])
            axes[1, 0].set_title('Bandwidth Score Distribution by Band')
            axes[1, 0].set_ylabel('Bandwidth Score')
            axes[1, 0].tick_params(axis='x', rotation=45)
            
            # Signal quality distribution
            quality_counts = df.groupby(['band', 'signal_quality']).size().unstack(fill_value=0)
            quality_counts.plot(kind='bar', ax=axes[1, 1], stacked=True)
            axes[1, 1].set_title('Signal Quality Distribution by Band')
            axes[1, 1].set_ylabel('Count')
            axes[1, 1].tick_params(axis='x', rotation=45)
            axes[1, 1].legend(title='Quality')
            
            plt.tight_layout()
            
            if save_plot:
                filename = f"plots/band_comparison_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                plt.savefig(filename, dpi=VIZ_CONFIG['dpi'], bbox_inches='tight')
                self.logger.info(f"Band comparison plot saved to {filename}")
                return filename
            
            plt.show()
            return ""
            
        except Exception as e:
            self.logger.error(f"Error creating band comparison plot: {e}")
            return ""
    
    def plot_heatmap(self, csv_file: str, save_plot: bool = True) -> str:
        """Create a heatmap showing signal quality across bands and time"""
        try:
            # Read data
            df = pd.read_csv(csv_file)
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            
            if df.empty:
                self.logger.warning("No data available for heatmap")
                return ""
            
            # Create pivot table for heatmap
            # Group by hour and band, calculate average bandwidth score
            df['hour'] = df['timestamp'].dt.hour
            pivot_data = df.pivot_table(
                values='bandwidth_score',
                index='hour',
                columns='band',
                aggfunc='mean'
            )
            
            # Create heatmap
            plt.figure(figsize=(12, 8))
            sns.heatmap(
                pivot_data,
                annot=True,
                fmt='.2f',
                cmap='RdYlGn',
                center=0.5,
                cbar_kws={'label': 'Average Bandwidth Score'}
            )
            plt.title('Signal Quality Heatmap: Band vs Hour of Day')
            plt.xlabel('LTE Band')
            plt.ylabel('Hour of Day')
            
            if save_plot:
                filename = f"plots/signal_heatmap_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                plt.savefig(filename, dpi=VIZ_CONFIG['dpi'], bbox_inches='tight')
                self.logger.info(f"Heatmap saved to {filename}")
                return filename
            
            plt.show()
            return ""
            
        except Exception as e:
            self.logger.error(f"Error creating heatmap: {e}")
            return ""
    
    def plot_performance_summary(self, csv_file: str, save_plot: bool = True) -> str:
        """Create a comprehensive performance summary dashboard"""
        try:
            # Read data
            df = pd.read_csv(csv_file)
            
            if df.empty:
                self.logger.warning("No data available for performance summary")
                return ""
            
            # Calculate summary statistics
            band_stats = df.groupby('band').agg({
                'rsrp': ['mean', 'std'],
                'sinr': ['mean', 'std'],
                'bandwidth_score': ['mean', 'std'],
                'signal_quality': lambda x: x.value_counts().index[0]
            }).round(2)
            
            # Create dashboard
            fig, axes = plt.subplots(2, 3, figsize=(18, 12))
            fig.suptitle('LTE Performance Dashboard', fontsize=16)
            
            # 1. Average RSRP by band
            rsrp_means = band_stats[('rsrp', 'mean')]
            axes[0, 0].bar(rsrp_means.index, rsrp_means.values, color='skyblue')
            axes[0, 0].set_title('Average RSRP by Band')
            axes[0, 0].set_ylabel('RSRP (dBm)')
            axes[0, 0].tick_params(axis='x', rotation=45)
            
            # 2. Average SINR by band
            sinr_means = band_stats[('sinr', 'mean')]
            axes[0, 1].bar(sinr_means.index, sinr_means.values, color='lightgreen')
            axes[0, 1].set_title('Average SINR by Band')
            axes[0, 1].set_ylabel('SINR (dB)')
            axes[0, 1].tick_params(axis='x', rotation=45)
            
            # 3. Average bandwidth score by band
            bw_means = band_stats[('bandwidth_score', 'mean')]
            axes[0, 2].bar(bw_means.index, bw_means.values, color='orange')
            axes[0, 2].set_title('Average Bandwidth Score by Band')
            axes[0, 2].set_ylabel('Bandwidth Score')
            axes[0, 2].tick_params(axis='x', rotation=45)
            
            # 4. Signal quality distribution
            quality_dist = df['signal_quality'].value_counts()
            axes[1, 0].pie(quality_dist.values, labels=quality_dist.index, autopct='%1.1f%%')
            axes[1, 0].set_title('Overall Signal Quality Distribution')
            
            # 5. Best performing band
            best_band = bw_means.idxmax()
            best_band_data = df[df['band'] == best_band]
            axes[1, 1].hist(best_band_data['bandwidth_score'], bins=20, alpha=0.7, color='gold')
            axes[1, 1].set_title(f'Bandwidth Score Distribution\n(Best Band: {best_band})')
            axes[1, 1].set_xlabel('Bandwidth Score')
            
            # 6. Time series of best band
            if not best_band_data.empty:
                best_band_data['timestamp'] = pd.to_datetime(best_band_data['timestamp'])
                axes[1, 2].plot(best_band_data['timestamp'], best_band_data['bandwidth_score'], 'g-', alpha=0.7)
                axes[1, 2].set_title(f'Bandwidth Score Timeline\n(Best Band: {best_band})')
                axes[1, 2].set_ylabel('Bandwidth Score')
                axes[1, 2].tick_params(axis='x', rotation=45)
            
            plt.tight_layout()
            
            if save_plot:
                filename = f"plots/performance_dashboard_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                plt.savefig(filename, dpi=VIZ_CONFIG['dpi'], bbox_inches='tight')
                self.logger.info(f"Performance dashboard saved to {filename}")
                return filename
            
            plt.show()
            return ""
            
        except Exception as e:
            self.logger.error(f"Error creating performance summary: {e}")
            return ""
    
    def create_animated_plot(self, csv_file: str, duration_seconds: int = 60) -> str:
        """Create an animated plot showing real-time signal changes"""
        try:
            from matplotlib.animation import FuncAnimation
            
            # Read data
            df = pd.read_csv(csv_file)
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            
            if df.empty:
                self.logger.warning("No data available for animated plot")
                return ""
            
            # Create figure
            fig, ax = plt.subplots(figsize=(12, 8))
            
            def animate(frame):
                ax.clear()
                
                # Get data up to current frame
                end_time = df['timestamp'].min() + timedelta(seconds=frame * 10)
                current_data = df[df['timestamp'] <= end_time]
                
                if not current_data.empty:
                    # Plot bandwidth score over time
                    ax.plot(current_data['timestamp'], current_data['bandwidth_score'], 'b-', alpha=0.7)
                    ax.set_title(f'Real-time Bandwidth Score (Frame {frame})')
                    ax.set_ylabel('Bandwidth Score')
                    ax.set_xlabel('Time')
                    ax.grid(True, alpha=0.3)
                    ax.set_ylim(0, 1)
                
                return ax,
            
            # Create animation
            anim = FuncAnimation(
                fig, animate, frames=duration_seconds//10,
                interval=100, blit=False, repeat=False
            )
            
            # Save animation
            filename = f"plots/animated_signal_{datetime.now().strftime('%Y%m%d_%H%M%S')}.gif"
            anim.save(filename, writer='pillow', fps=10)
            self.logger.info(f"Animated plot saved to {filename}")
            
            return filename
            
        except Exception as e:
            self.logger.error(f"Error creating animated plot: {e}")
            return ""
    
    def generate_report(self, csv_file: str, output_dir: str = "reports") -> str:
        """Generate a comprehensive PDF report with all visualizations"""
        try:
            from reportlab.lib.pagesizes import letter
            from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.lib.units import inch
            
            # Create output directory
            Path(output_dir).mkdir(exist_ok=True)
            
            # Generate all plots
            timeline_plot = self.plot_signal_timeline(csv_file, save_plot=True)
            band_plot = self.plot_band_comparison(csv_file, save_plot=True)
            heatmap_plot = self.plot_heatmap(csv_file, save_plot=True)
            dashboard_plot = self.plot_performance_summary(csv_file, save_plot=True)
            
            # Create PDF report
            report_file = f"{output_dir}/lte_analysis_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            doc = SimpleDocTemplate(report_file, pagesize=letter)
            styles = getSampleStyleSheet()
            story = []
            
            # Title
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=24,
                spaceAfter=30,
                alignment=1  # Center alignment
            )
            story.append(Paragraph("LTE Signal Analysis Report", title_style))
            story.append(Spacer(1, 12))
            
            # Summary
            story.append(Paragraph("Executive Summary", styles['Heading2']))
            story.append(Paragraph(
                "This report provides a comprehensive analysis of LTE signal performance across different frequency bands. "
                "The analysis includes signal strength metrics (RSRP, RSRQ, SINR) and bandwidth efficiency scores.",
                styles['Normal']
            ))
            story.append(Spacer(1, 12))
            
            # Add plots to report
            if timeline_plot:
                story.append(Paragraph("Signal Timeline Analysis", styles['Heading2']))
                story.append(Image(timeline_plot, width=6*inch, height=4*inch))
                story.append(Spacer(1, 12))
            
            if band_plot:
                story.append(Paragraph("Band Performance Comparison", styles['Heading2']))
                story.append(Image(band_plot, width=6*inch, height=4*inch))
                story.append(Spacer(1, 12))
            
            if heatmap_plot:
                story.append(Paragraph("Signal Quality Heatmap", styles['Heading2']))
                story.append(Image(heatmap_plot, width=6*inch, height=4*inch))
                story.append(Spacer(1, 12))
            
            if dashboard_plot:
                story.append(Paragraph("Performance Dashboard", styles['Heading2']))
                story.append(Image(dashboard_plot, width=6*inch, height=4*inch))
                story.append(Spacer(1, 12))
            
            # Build PDF
            doc.build(story)
            self.logger.info(f"Report generated: {report_file}")
            
            return report_file
            
        except Exception as e:
            self.logger.error(f"Error generating report: {e}")
            return "" 