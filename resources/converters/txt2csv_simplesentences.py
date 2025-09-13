import csv
import sys
import os

def txt_to_csv(input_file, output_file):
    # Open input and output files
    with open(input_file, 'r') as txt_file, open(output_file, 'w', newline='') as csv_file:
        # Create CSV writer
        csv_writer = csv.writer(csv_file)
        # Write header
        csv_writer.writerow(['index', 'sentence'])
        # Initialize index
        index = 0
        # Iterate over each line in the TXT file
        for line in txt_file:
            # Remove leading/trailing whitespace and newline characters
            sentence = line.strip()
            # Write index and sentence to CSV
            csv_writer.writerow([index, sentence])
            # Increment index
            index += 1

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
print(sys.path[0])

# File paths
input_file = os.path.join(sys.path[0], "converters", "data", "it_sentences.txt")
output_file = os.path.join(sys.path[0], "it", "simple_sentences.csv" )

# Convert TXT to CSV
txt_to_csv(input_file, output_file)

print("Converted {} to {}".format(input_file, output_file))
