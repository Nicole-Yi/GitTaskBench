
from stegano.lsb.lsb import reveal

# Define input and output file paths
input_image = "/data/data/agent_test_codebase/GitTaskBench/queries/Stegano_02/input/Stegano_02_input.png"
output_file = "/data/data/agent_test_codebase/GitTaskBench/eval_automation/output/Stegano_02/output"

# Reveal the hidden message
hidden_message = reveal(input_image)

# Save the message to a file
with open(output_file, "w") as f:
    f.write(hidden_message)
    print("Hidden message extracted and saved to", output_file)