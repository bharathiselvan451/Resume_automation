"""
Render resume_template.html.j2 with Bharathiselvan's data.

Install dependency:
    pip install jinja2

Run:
    python render_resume.py          # outputs resume.html
"""

from jinja2 import Environment, FileSystemLoader

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
            "end_date": "July 2023",
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
         {
            "name": "",
            "url": "",
            "bullets": [
                
            ],
        },
        {
            "name": "",
            "url": "",
            "bullets": [
                
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


def render(template_path: str = "resume_template.html",
           output_path: str = "resume.html") -> None:
    env = Environment(loader=FileSystemLoader("."))
    template = env.get_template(template_path)
    html = template.render(**data)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Rendered → {output_path}")


if __name__ == "__main__":
    render()