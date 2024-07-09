import numpy as np
#Funktion zum Winkel berechnen für BMI-Kategorie
def calculate_angle_for_bmi(sizes, labels, bmi_category):
    category_index = labels.index(bmi_category)
    start_angle = sum(sizes[:category_index]) / sum(sizes) * 360
    slice_angle = sizes[category_index] / sum(sizes) * 360
    return start_angle + slice_angle / 2

#Berchnen der Winkel und Label-Positionen
def calculate_angle_and_label_positions(sizes, labels):
        angles = []
        label_positions = []

        total = sum(sizes)
        cumulative_sizes = np.cumsum(sizes)
    
        for i in range(len(labels)):
            if i == 0:
                start_angle = 0
            else:
                start_angle = cumulative_sizes[i - 1] / total * 360
        
            slice_angle = sizes[i] / total * 360
            angle = start_angle + slice_angle / 2
            angles.append(angle)

        # Position für die Label-Beschriftung
            label_angle = start_angle + slice_angle / 2
            label_x = 0.7 * np.cos(np.radians(label_angle))  # Grobe Anpassung mit 0.7 um näher am Kreisrand zu sein
            label_y = 0.7 * np.sin(np.radians(label_angle))  
            label_positions.append((label_x, label_y))

        return angles, label_positions