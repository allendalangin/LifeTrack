# src/controllers/infographics_controller.py
from src.models.infographics_model import InfographicsModel

class InfographicsController:
    def __init__(self, view):
        self.view = view
        self.model = InfographicsModel()

    async def load_infographics(self):
        """Load infographics and update the view."""
        infographics = self.model.get_infographics()
        self.view.update_infographics(infographics)