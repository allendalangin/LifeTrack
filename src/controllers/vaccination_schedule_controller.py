from src.models.vaccination_schedule_model import VaccinationScheduleModel

class VaccinationScheduleController:
    def __init__(self):
        self.model = VaccinationScheduleModel()

    def fetch_schedules(self):
        """Fetch vaccination schedules from the model."""
        return self.model.fetch_schedules()