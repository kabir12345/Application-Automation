# Application-Automation


### `resumeOptim/jd.yaml`
YAML file containing job descriptions used to tailor the resumes.

### `resumeOptim/resume_template.tex`
LaTeX template for the resume.

### `resumeOptim/resumes/`
Directory containing the generated LaTeX resumes for different job applications.

## Usage

1. **Set up the OpenAI API key:**
   Ensure you have the OpenAI API key set in your environment variables:
   ```bash
   export OPENAI_API_KEY='your-api-key'
   ```

2. **Prepare job descriptions:**
   Add job descriptions to the `jd.yaml` file in the following format:
   ```yaml
   jobs:
     - name: Job_Title
       description: Job description text here
   ```

3. **Run the script:**
   Execute the Python script to generate the tailored resumes:
   ```bash
   python resumeOptim/resume.py
   ```

4. **Check the output:**
   The generated resumes will be saved in the `resumeOptim/resumes/` directory, organized by date.

## LaTeX Resume Template
The LaTeX template includes sections for personal information, summary, technical skills, experience, projects, publications, and education. The script updates the Technical Skills section based on the job description provided.

Example LaTeX template: