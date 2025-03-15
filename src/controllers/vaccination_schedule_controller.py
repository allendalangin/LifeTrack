from src.models.vaccination_schedule_model import VaccinationScheduleModel

class VaccinationScheduleController:
    def __init__(self):
        self.model = VaccinationScheduleModel()

    def fetch_schedules(self):
        """Fetch vaccination schedules from the model."""
        try:
            schedules = self.model.fetch_schedules()
            if not schedules:
                print("No vaccination schedules found.")
            return schedules
        except Exception as e:
            print(f"Error fetching schedules: {e}")
            return []