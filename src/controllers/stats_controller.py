# src/controllers/stats_controller.py

import matplotlib.pyplot as plt
from io import BytesIO
import base64

class StatsController:
    def __init__(self, view, model):
        self.view = view
        self.model = model

    async def plot_data(self, data):
        """
        Plot data and return the image as a base64-encoded string.
        """
        plt.figure(figsize=(10, 6))
        plt.plot([p["x"] for p in data["data_points"]], 
                 [float(p["y"]) for p in data["data_points"]],
                 marker='o', linestyle='-')
        plt.title(data.get("table_title", "Statistics Graph"))
        plt.xlabel(data.get("x_axis_label", "X-Axis"))
        plt.ylabel(data.get("y_axis_label", "Y-Axis"))
        
        buf = BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight')
        buf.seek(0)
        return base64.b64encode(buf.getvalue()).decode('utf-8')