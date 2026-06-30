from dotenv import load_dotenv
from anthropic import Anthropic
import json
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright
from datetime import datetime






data = {
    "name": "BHARATHISELVAN RAJENDRAN",
    "email": "rajendranbharathiselvan@gmail.com",
    "phone": "4036802431",
    "linkedin_url": "https://linkedin.com/in/bharathiselvan-rajendran",   # fill in slug
    "github_url": "https://github.com/bharathiselvan451",
    "summary": (
        "Recent graduate in Information Security looking to launch a career in Cloud engineering "
        "with a strong attention to security. Certified in AWS, proactive in exploring emerging "
        "tech and building solutions around it."
    ),

    # ── Education ──────────────────────────────────────────────────────────────
    "education": [
        {
            "degree": "Master of Engineering Information Systems Security",
            "institution": "Concordia University",
            "start_date": "Jan 2024",
            "end_date": "June 2025",
            "notes": [],
        },
        {
            "degree": "Bachelor of Engineering Computer Science",
            "institution": "Anna University",
            "start_date": "Aug 2019",
            "end_date": "May 2023",
            "notes": [],
        },
    ],

    # ── Work Experience ────────────────────────────────────────────────────────
    "work_experience": [
        {
            "title": "Intern",
            "company": "Cognizant",
            "start_date": "Feb 2023",
            "end_date": "Dec 2023",
            "bullets": [
                "Integrated GitHub webhooks with Jenkins to automatically trigger build pipelines on pull requests and merges.",
                "Enabled early detection of issues such as exposed secrets, state drifts, and policy non-compliance during the pilot run.",
                "Improved code quality and infrastructure reliability by enforcing automated validation and security checks in the pipeline.",
            ],
        },
    ],

    # ── Projects ───────────────────────────────────────────────────────────────
    "projects": [
        {
            "name": "EMBA log processor",
            "url": "https://github.com/bharathiselvan451/EMBA_log_processor",
            "bullets": [
                "Integrated National Vulnerability Database (NVD) feeds to enrich EMBA-generated logs, enhancing detection accuracy.",
                "Built an API-driven workflow using API Gateway to receive user-submitted log files, processed them via AWS Lambda, and returned results through automated email notifications.",
                "Optimized cost and performance by storing NVD data feeds in S3 and using hash-based comparison to pull only updated data from NIST.",
                "Provisioned the entire infrastructure using Infrastructure as Code (IaC) for repeatability and scalability.",
                "Utilized AWS Lambda, S3, and API Gateway to ensure secure, scalable compute, storage, and external access.",
            ],
        },
        {
            "name": "Bus Reservation app",
            "url": "https://github.com/bharathiselvan451/Bus-Reservation-app",
            "bullets": [
                "Developed the backend with Spring Boot to handle routing, seat reservations, and user interactions, ensuring a scalable architecture.",
                "Integrated a MySQL database to persist user data, trip details, and booking records, enabling reliable and consistent data storage.",
                "Implemented essential features such as trip creation, booking confirmation, and seat availability tracking.",
                "Styled the frontend using HTML, CSS, and JavaScript, and integrated it with the backend to deliver a smooth and responsive user experience.",
                "Followed clean code principles to promote maintainability and extensibility.",
            ],
        },
        {
            "name": "Bitwarden autobackup",
            "url": "https://github.com/bharathiselvan451/Bitwarden_autobackup_aws",
            "bullets": [
                "Implemented an EventBridge schedule to trigger an AWS Lambda function that launched an EC2 instance bootstrapped via user data to authenticate with Bitwarden and export credentials.",
                "Stored the exported credentials dump in S3, which automatically triggered another Lambda function to send an email notification and gracefully terminate the EC2 instance.",
                "Cost efficiency through temporary compute provisioning and controlled data flow.",
                "Provisioned the entire solution using Terraform, leveraging AWS services including EC2, Lambda, S3, and EventBridge.",
            ],
        },
    ],

    # ── Certifications ─────────────────────────────────────────────────────────
    "certifications": [
        {
            "name": "AWS Certified Solutions Architect SAA-C03",
            "valid_from": "Dec 2024",
            "valid_until": "Dec 2027",
            "url": "#",   # replace with real certificate URL
        },
        {
            "name": "Certified in Cybersecurity ISC2",
            "valid_from": "Jul 2024",
            "valid_until": "Jun 2027",
            "url": "#",   # replace with real certificate URL
        },
    ],

    # ── Skills ─────────────────────────────────────────────────────────────────
    "skills": [
        {"category": "Cloud",                "tools": ["IAM", "S3 buckets", "Lambda", "API Gateway", "EC2", "EventBridge", "DynamoDB"]},
        {"category": "Automation Tools",     "tools": ["Jenkins", "Terraform", "Docker"]},
        {"category": "Programming Languages","tools": ["Java", "Python", "Vanilla JavaScript", "HTML", "CSS"]},
        {"category": "Security Tools",       "tools": ["Wireshark", "Burp Suite"]},
        {"category": "Frameworks",           "tools": ["SpringBoot", "SpringMVC", "Spring JPA", "Mockito", "JUnit"]},
    ],
}



load_dotenv()

client = Anthropic()
#model = "claude-haiku-4-5"
model = "claude-sonnet-4-6"

file_path = "Bharathiselvan Rajendran-cybersecurity-resume.md"
with open(file_path, "r", encoding="utf-8") as file:
    resume_cybersecurity = file.read()

file_path = "Bharathiselvan Rajendran-developer-resume.md"
with open(file_path, "r", encoding="utf-8") as file:
    resume_developer = file.read()

file_path = "Bharathiselvan-Rajendran-cloud-resume.md"
with open(file_path, "r", encoding="utf-8") as file:
    resume_cloud = file.read()

def add_user_message(messages, text):
    user_message = {"role": "user", "content": text}
    user_message_null = {"role": "user", "content": "continue"}

    assistant_message = {
            "role": "assistant",
            "content": "```json"
        }
    messages.append(user_message)
   # messages.append(assistant_message)
   # messages.append(user_message_null)

def chat(messages, system=None, temperature=1.0, stop_sequences=[]):
    params = {
        "model": model,
        "max_tokens": 2000,
        "messages": messages,
        "temperature": temperature,
        "stop_sequences": stop_sequences,
        "cache_control" :{"type": "ephemeral"}
    }

    if system:
        params["system"] = system

    message = client.messages.create(**params)
    clean_json = message.content[0].text.replace("```json", "").replace("```", "").strip()

    return(clean_json)

async def html_to_pdf():
    # Define absolute paths
    html_path = Path("resume.html").absolute().as_uri()
    timestamp_int = int(datetime.now().timestamp())
    pdf_path = f"Bharathisevan_Rajendran_{timestamp_int}.pdf"
    
    async with async_playwright() as p:
        # Launch headless browser
        browser = await p.chromium.launch()
        page = await browser.new_page()
        
        # Load local HTML file URI
        await page.goto(html_path, wait_until="load")
        
        # Save as PDF
        await page.pdf(
            path=pdf_path, 
            format="A4", 
            print_background=True
        )
        await browser.close()
    print(f"PDF successfully generated: {pdf_path}")
    return pdf_path

# Run the async loop
def render(template_path: str = "resume_template.html",
           output_path: str = "resume.html") -> None:
    env = Environment(loader=FileSystemLoader("."))
    template = env.get_template(template_path)
    html = template.render(**data)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Rendered → {output_path}")


def json_process(result):
    json_data = json.loads(result)
    data["work_experience"][0]["title"] = json_data[0]["work_experience"][0]["title"]
    data["work_experience"][0]["company"] = json_data[0]["work_experience"][0]["company"]
    data["work_experience"][0]["duration"] = json_data[0]["work_experience"][0]["duration"]
    data["work_experience"][0]["bullets"] = json_data[0]["work_experience"][0]["bullets"]
    for i in range(len(data["projects"])):
        data["projects"][i] = json_data[1]["projects"][i]
    render()

def generate_resume(message):


    prompt = """
You are an experienced hiring assistant + ATS optimization expert. Your task: I will give you a job description and three resumes. You will tailor the resume to perfectly match the job description. Rules:

1. Extract ALL relevant keywords from the job description:

* job title
* required skills
* preferred skills
* responsibilities
* tools / technologies
* soft skills
* domain keywords
* industry terms

1. Compare the job description with the candidate’s resume. For every required or relevant skill/keyword:

* If it already exists in the resume → rewrite & emphasize it
* If it exists but weak → strengthen, move higher, highlight impact
* If it's missing but the candidate has similar experience → add a truthful sentence
* If it’s not in the resume and can’t be assumed → DO NOT invent it

2. Reorganize the resume:

* Move the most relevant experience to the top
* Add a strong, tailored summary section at the beginning using job-description keywords
* Strengthen achievements using measurable impact when possible
* Make responsibilities match the job description phrasing (without copying word-for-word)

3. Keep formatting clean and ATS-friendly:

* No icons
* No tables
* No images
* Standard resume structure

4. Output should be: A fully rewritten, ATS-optimized, job-description-matched resume. Keep it concise, professional, and keyword-rich.

here are the candidate resume

"
f"Cloud-resume:\n\n{## **BHARATHISELVAN RAJENDRAN**


## rajendranbharathiselvan@gmail.com **Linkedin github** 4036802431


Recent graduate in Information Security looking to launch a career in Cloud engineering with a strong attention to security. Certified in AWS, proactive in exploring emerging tech and building solutions around it.


## **WORK EXPERIENCE**


**Software Engineer, Cognizant Feb 2023 - Dec 2023**


- Integrated GitHub webhooks with Jenkins to automatically trigger build pipelines on pull requests and merges.


- Enabled early detection of issues such as exposed secrets, state drifts, and policy non-compliance during the pilot run.


- Improved code quality and infrastructure reliability by enforcing automated validation and security checks in the pipeline.


## **PROJECTS**


- **EMBA log processor -** https://github.com/bharathiselvan451/EMBA_log_processor Integrated National Vulnerability Database (NVD) feeds to enrich EMBA-generated logs, enhancing detection accuracy.


  - Built an API-driven workflow using API Gateway to receive user-submitted log files, processed them via AWS Lambda, and returned results through automated email notifications.


  - Optimized cost and performance by storing NVD data feeds in S3 and using hash-based comparison to pull only updated data from NIST.


  - Provisioned the entire infrastructure using Infrastructure as Code (IaC) for repeatability and scalability. Utilized AWS Lambda, S3, and API Gateway to ensure secure, scalable compute, storage, and external access.


- **Bitwarden autobackup -** https://github.com/bharathiselvan451/Bitwarden_autobackup_aws Implemented an EventBridge schedule to trigger an AWS Lambda function that launched an EC2 instance bootstrapped via user data to authenticate with Bitwarden and export credentials.


  - Stored the exported credentials dump in S3, which automatically triggered another Lambda function to send an email notification and gracefully terminate the EC2 instance.


  - Cost efficiency through temporary compute provisioning and controlled data flow. Provisioned the entire solution using Terraform, leveraging AWS services including EC2, Lambda, S3, and EventBridge.


**Bus Reservation app -** https://github.com/bharathiselvan451/Bus-Reservation-app


- Developed the backend with Spring Boot to handle routing, seat reservations, and user interactions, ensuring a scalable architecture.


- Integrated a MySQL database to persist user data, trip details, and booking records, enabling reliable and consistent data storage.


- Implemented essential features such as trip creation, booking confirmation, and seat availability tracking. Styled the frontend using HTML, CSS, and JavaScript, and integrated it with the backend to deliver a smooth and responsive user experience.


Followed clean code principles to promote maintainability and extensibility.


J **enkins_security_pipeline -** https://github.com/bharathiselvan451/Jenkins_pipeline


Built a security pipeline for a simple springboot application by leveraging Jenkins


  - Performed Static code analysis and software component analysis on the application by integrating SonarQube and Dependency-check with the pipeline.


  - Packaged the application along with its dependencies as a Docker container in the final stage of the pipeline


- **Web application vulnerability assessment -** https://github.com/bharathiselvan451/INSE_6140 wordpress Applied a combination of static, dynamic, and software composition analysis using tools such as SonarQube, WPScan, Wordfence, Dependency-check, and OWASP ZAP.


  - Automated the assessment pipeline using Bash scripts and consolidated multi-tool results via Python for streamlined reporting.


  - Developed a code-level proof-of-concept exploit and implemented mitigation strategies for CVE-2022-21661 (SQL Injection in WordPress).


- **Android penetration testing -** https://github.com/bharathiselvan451/Android_pentesting INSE_6120 Performed static and dynamic security analysis on 15 Android apps targeting vulnerable user groups using MobSF, Burp Suite, and Android Studio.


- Identified major issues such as insecure cryptographic practices, excessive permissions, unencrypted data at rest, and replay attack vulnerabilities


- Highlighted critical flaws in real-world apps, including expired certificates and exposure of personal data.






## **EDUCATION**


|**EDUCATION**||||
|---|---|---|---|
|**Master of Engineering Information**|**Systems Security**|||
|Concordia University|||**Jan 2024 - June 2025**|
|**Bachelor of Engineering Computer Science**||||
|Anna University|||**Aug 2019 - May 2023**|
|**CERTIFICATIONS**||||
|**AWS Certified Solutions Architect SAA-C03 -**||<br>**Certificate**|**Dec 2024 - Dec 2027**|
|**Certified in Cybersecurity ISC2 -**|<br>**Certificate**||**Jul 2024 - Jun 2027**|
|**SKILLS**||||
|**Cloud**|**IAM, S3 buckets, Lambda, Api gateway, EC2, Eventbridge, DynamoDB**|||
|**Automation Tools**|||**Jenkins, Terraform, Docker**|
|**Programming languages**|||**Java, Python, Vanilla JavaScript, HTML, CSS**|
|**Security tools**|||**Wireshark, Burp Suite**|
|**Frameworks**||**SpringBoot, SpringMVC, Spring JPA, Mockito, Junit**||
}"
}"





}"

Generate an array of JSON objects, and only provide the required work experience and projects. do not give reccomendations about the job.

Example output:
```json
[
    "work_experience": [{   
        "title" : "name of the role"
        "company" : "name of the company"
        "duration" : "jan 2023 to dec 2023
        "bullets": "Description of work_experience",
    }],
    {
        "projects": [{
            "name": "name of the project",
            "url": "github url of the project",
            "bullets": [
                "bulleted points of the project"
            ],
        },
        ...additional
        ]
    }
]
```

"""+message+""

    messages = []
    add_user_message(messages, prompt)
    text = chat(messages)
    json_process(text)

#result = generate_resume("""About The Role:
#Assist in the deployment and maintenance of cloud infrastructure. 
#nsure availability and reliability through resource provisioning, continuous monitoring, and proactive troubleshooting. 
#Manage backup and recovery processes to ensure data integrity and availability in case of failures or outages. 
#Support the deployment of cloud-based applications and services. 
#Adhere to best practices for application configuration including version control, environment management, and integration with existing systems. 
#Facilitate scaling and load balancing to handle variable demand and optimize resource usage. 
#Assist in implementing and maintaining security measures. 
#Protect cloud resources and data through effective access control, security auditing, and patch management. 
#Monitor and respond to security threats by staying informed on the latest vulnerabilities and implementing necessary updates and fixes. 
#Skill Requirements
#Cloud Platform Proficiency: A strong understanding in Azure and its services, including compute, storage, networking, and security. 
#Infrastructure as Code (IaC): Proficiency in IaC tools such as Bicep and ARM. 
#Scripting and Automation: Solid programming and scripting skills in languages like Python, Bash, or PowerShell to automate routine tasks and optimize cloud operations. 
#Networking Knowledge: Familiarity with cloud networking concepts, including virtual networks, subnets, load balancers, and VPNs, to design and maintain secure and efficient network architectures. 
#Security Best Practices: Understanding of cloud security principles, identity and access management (IAM), encryption, and the ability to implement and follow security best practices within cloud environments. 
#Monitoring and Troubleshooting: Proficiency in cloud monitoring and logging tools (e.g., CloudWatch, Azure Monitor) to proactively identify and troubleshoot issues, ensuring optimal performance and availability. 
#Familiarity with Azure OpenAI Service""")




















