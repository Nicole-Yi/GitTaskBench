import sys
sys.path.append('/data/data/agent_test_codebase/GitTaskBench/minimal_stegano')
from lsb import hide, reveal

input_image = '/data/data/agent_test_codebase/GitTaskBench/queries/Stegano_03/input/Stegano_03_input.png'
output_path = '/data/data/agent_test_codebase/GitTaskBench/eval_automation/output/Stegano_03/output.png'

secret = hide(input_image, "hidden_text")
secret.save(output_path)
print(f"Message embedded successfully in {output_path}")