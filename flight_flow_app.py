import sys
import os

# Set up paths
current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GUI_path = os.path.join(current_dir, "gui")
sys.path.append(GUI_path)

# Import necessary PyQt5 classes
from PyQt5.QtWidgets import QApplication

# Import your main window class, which should be the one that integrates Ui_flightFlow_main_window
from gui.mainwindow_functionalties import FlightFlowMainWindow  # Adjust this path if needed

if __name__ == "__main__":
    # Start the application
    app = QApplication(sys.argv)
    
    # Create an instance of FlightFlowMainWindow
    main_window = FlightFlowMainWindow()  # Ensure this is your main class integrating the UI
    main_window.showMaximized()  # Show the main window maximized
    
    # Run the application
    sys.exit(app.exec_())

