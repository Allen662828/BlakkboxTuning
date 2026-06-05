from .delta_logic import BlakkboxDeltaLogic
from .safety_filters import SafetyFilters

class RefinementEngine:
    def __init__(self):
        self.delta_logic = BlakkboxDeltaLogic()
        self.safety = SafetyFilters()

    def refine_modified_values(self, changes):
        refined = []

        filtered_changes = self.safety.preserve_zero_groups(changes)

        for change in filtered_changes:
            delta = change.get('delta', 0)
            processed_delta = self.delta_logic.process_delta(delta)

            refined.append({
                'address': change.get('address'),
                'original': change.get('original'),
                'modified': change.get('modified'),
                'processed_delta': processed_delta
            })

        return refined
