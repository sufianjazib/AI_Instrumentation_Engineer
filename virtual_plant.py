import math

class VirtualPlant:
    def __init__(self):
        self.tick_count = 0
        self.fault = "NO_FAULT"

    def set_fault(self, fault_name):
        self.fault = fault_name

    def tick(self):
        self.tick_count += 1
        base_p = 8.0 + math.sin(self.tick_count * 0.2) * 0.3
        pt101 = base_p
        pt102 = base_p
        ma101 = 4.0 + (pt101 / 16.0) * 16.0
        v_cmd = 60.0
        v_fb = 60.0
        air = 6.0

        if self.fault == "PT101_DRIFT":
            pt101 += 4.5
            ma101 = 4.0 + (pt101 / 16.0) * 16.0
        elif self.fault == "LOOP_FAULT":
            ma101 = 3.6
        elif self.fault == "VALVE_FAULT":
            v_fb = 35.0
        elif self.fault == "LOW_AIR":
            air = 3.2
            v_fb = 42.0

        return {
            "pt101_pv": pt101, "pt102_pv": pt102, "pt101_ma": ma101,
            "level": 60.0, "temp": 85.0, "flow": 175.0,
            "valve_cmd": v_cmd, "valve_fb": v_fb, "air_pressure": air
        }
