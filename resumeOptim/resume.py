import yaml
import os
from openai import OpenAI
import re

# Initialize the OpenAI client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def read_yaml(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def get_ats_compliant_resume(latex_template, job_description):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are an ATS compliance expert. Your task is to update the Technical Skills section of a LaTeX resume to make it more relevant to a given job description, while maintaining the overall structure and formatting of the resume."},
            {"role": "user", "content": f"Here is the full LaTeX resume template:\n\n{latex_template}\n\nAnd here is the job description:\n\n{job_description}\n\nPlease update only the Technical Skills section to make it more ATS-compliant and relevant to the job description. Return the entire updated LaTeX resume."}
        ]
    )
    return response.choices[0].message.content

def main():
    yaml_data = read_yaml('/Users/kabir/Downloads/jobs/resumeOptim/jd.yaml')
    with open('/Users/kabir/Downloads/jobs/resumeOptim/resume_template.tex', 'r') as file:
        latex_template = file.read()

    output_folder = '/Users/kabir/Downloads/jobs/resumeOptim/resumes/August_19'
    os.makedirs(output_folder, exist_ok=True)

    for job in yaml_data['jobs']:
        job_name = job['name']
        job_description = job['description']

        updated_latex = get_ats_compliant_resume(latex_template, job_description)

        output_file = os.path.join(output_folder, f"Kabir_Jaiswal_{job_name}.tex")
        with open(output_file, 'w') as file:
            file.write(updated_latex)
        print(f"Created optimized LaTeX resume for {job_name}")

if __name__ == "__main__":
    main()