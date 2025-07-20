import json
import os
from typing import List, Dict, Optional
from PySide6.QtWidgets import QFileDialog, QMessageBox
from datetime import datetime

class InvestmentFileManager:
    """Manager for saving and loading investments from files"""
    
    def __init__(self):
        self.default_extension = "json"
        self.file_filter = "Investment Files (*.json);;All Files (*)"
        
    def save_investments_to_file(self, parent_widget, investments_data: List[Dict], 
                                years: int, compound_freq: str, contrib_freq: str) -> bool:
        """
        Save investments to a JSON file
        
        Args:
            parent_widget: Parent widget for dialogs
            investments_data: List of investment data
            years: Years of growth
            compound_freq: Compound frequency
            contrib_freq: Contribution frequency
            
        Returns:
            bool: True if save successful, False otherwise
        """
        try:
            # Open dialog to choose save location
            file_path, _ = QFileDialog.getSaveFileName(
                parent_widget,
                "Save Investments",
                f"investments_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                self.file_filter
            )
            
            if not file_path:
                return False
                
            # Prepare data to save
            save_data = {
                "metadata": {
                    "version": "3.0",
                    "created_at": datetime.now().isoformat(),
                    "years": years,
                    "compound_frequency": compound_freq,
                    "contribution_frequency": contrib_freq
                },
                "investments": investments_data
            }
            
            # Save to file
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(save_data, f, indent=2, ensure_ascii=False)
                
            self._show_message(parent_widget, "Success", f"Investments saved to {os.path.basename(file_path)}")
            return True
            
        except Exception as e:
            self._show_error(parent_widget, "Save Error", f"Failed to save investments: {str(e)}")
            return False
    
    def load_investments_from_file(self, parent_widget) -> Optional[Dict]:
        """
        Load investments from a JSON file
        
        Args:
            parent_widget: Parent widget for dialogs
            
        Returns:
            Dict with loaded data or None if failed
        """
        try:
            # Open dialog to choose file to load
            file_path, _ = QFileDialog.getOpenFileName(
                parent_widget,
                "Load Investments",
                "",
                self.file_filter
            )
            
            if not file_path:
                return None
                
            # Load from file
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            # Validate file structure
            if not self._validate_file_structure(data):
                self._show_error(parent_widget, "Invalid File", 
                               "The selected file is not a valid investment file.")
                return None
                
            self._show_message(parent_widget, "Success", f"Investments loaded from {os.path.basename(file_path)}")
            return data
            
        except FileNotFoundError:
            self._show_error(parent_widget, "File Not Found", "The selected file was not found.")
        except json.JSONDecodeError:
            self._show_error(parent_widget, "Invalid File", "The selected file is not a valid JSON file.")
        except Exception as e:
            self._show_error(parent_widget, "Load Error", f"Failed to load investments: {str(e)}")
            
        return None
    
    def _validate_file_structure(self, data: Dict) -> bool:
        """Validate the structure of loaded file"""
        if not isinstance(data, dict):
            return False
            
        if 'metadata' not in data or 'investments' not in data:
            return False
            
        metadata = data['metadata']
        required_metadata = ['years', 'compound_frequency', 'contribution_frequency']
        
        if not all(key in metadata for key in required_metadata):
            return False
            
        if not isinstance(data['investments'], list):
            return False
            
        # Validate each investment
        for investment in data['investments']:
            if not isinstance(investment, dict):
                return False
                
            required_fields = ['ticker', 'rate', 'initial_deposit', 'contribution_amount']
            if not all(key in investment for key in required_fields):
                return False
                
        return True
    
    def _show_message(self, parent, title: str, message: str):
        """Show information message"""
        QMessageBox.information(parent, title, message)
        
    def _show_error(self, parent, title: str, message: str):
        """Show error message"""
        QMessageBox.critical(parent, title, message)
    
    def export_to_csv(self, parent_widget, investments_data: List[Dict], 
                      years: int, compound_freq: str, contrib_freq: str) -> bool:
        """
        Export investments to CSV format for Excel
        """
        try:
            import csv
            
            file_path, _ = QFileDialog.getSaveFileName(
                parent_widget,
                "Export to CSV",
                f"investments_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                "CSV Files (*.csv);;All Files (*)"
            )
            
            if not file_path:
                return False
                
            with open(file_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                
                # Write general information
                writer.writerow(["Investment Portfolio Export"])
                writer.writerow(["Export Date:", datetime.now().strftime('%Y-%m-%d %H:%M:%S')])
                writer.writerow(["Years of Growth:", years])
                writer.writerow(["Compound Frequency:", compound_freq])
                writer.writerow(["Contribution Frequency:", contrib_freq])
                writer.writerow([])  # Empty row
                
                # Write investment header
                writer.writerow([
                    "Ticker", "Annual Rate (%)", "Initial Deposit", 
                    "Contribution Amount", "Expected Final Value"
                ])
                
                # Write investment data
                for inv in investments_data:
                    # Calculate approximate final value
                    # (this is simplified, use your calculator for precise values)
                    rate = inv['rate'] / 100
                    initial = inv['initial_deposit']
                    contribution = inv['contribution_amount']
                    
                    # Simplified annual calculation
                    final_value = initial * ((1 + rate) ** years) + contribution * years * (1 + rate)
                    
                    writer.writerow([
                        inv['ticker'],
                        f"{inv['rate']:.2f}",
                        f"{initial:.2f}",
                        f"{contribution:.2f}",
                        f"{final_value:.2f}"
                    ])
                    
            self._show_message(parent_widget, "Success", f"Data exported to {os.path.basename(file_path)}")
            return True
            
        except Exception as e:
            self._show_error(parent_widget, "Export Error", f"Failed to export data: {str(e)}")
            return False