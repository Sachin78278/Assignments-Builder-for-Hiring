import streamlit as st
import os
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv
from google import genai
from google.genai import types
from fpdf import FPDF
import re

# ==========================================
# 1. MANUAL SKILLS LIBRARY (EDIT HERE)
# ==========================================

SKILLS_LIBRARY = {
    "AI Engineer Intern": [
        "Python", "PyTorch", "TensorFlow", "Large Language Models (LLMs)", "LangChain", 
        "Hugging Face", "Vector Databases", "RAG Architecture", "OpenAI API", "Prompt Engineering", 
        "Fine-tuning Models", "FastAPI", "Docker", "NLP", "Computer Vision", "Git/GitHub", "MLOps", 
        "Model Quantization", "Pandas", "NumPy", "Scikit-Learn", "API Integration", "Neural Networks", 
        "Data Scraping", "GPU Optimization"
    ],
    "Narrative Design & Presentation Storytelling Intern": [
        "Visual Storytelling", "Copywriting", "Presentation Design", "Narrative Arcs", "Storyboarding", 
        "Brand Voice Alignment", "Script Writing", "Creative Direction", "Audience Psychology", "Data Visualization", 
        "Content Strategy", "Editorial Planning", "Public Speaking Prep", "Graphic Continuity", "UX Writing", 
        "Messaging Frameworks", "Pitch Deck Creation", "Emotional Hook Design", "Micro-copy", "Brand Storytelling", 
        "Slide Hierarchy", "Creative Briefing", "Grammar Excellence", "AI Art Generation", "Proofreading"
    ],
    "HR Intern": [
        "Talent Acquisition", "Technical Recruiting", "Sourcing", "Candidate Screening", "Onboarding", 
        "HR Operations", "Employee Engagement", "Interview Coordination", "JD Drafting", "ATS Systems", 
        "Documentation", "Payroll Basics", "Conflict Resolution", "Communication Skills", "Performance Management", 
        "Employer Branding", "HR Analytics", "Compliance & Ethics", "Stakeholder Management", "Google Workspace", 
        "Organizational Culture", "Diversity & Inclusion", "Candidate Experience", "Time Management", "Policy Drafting"
    ],
    "Founders Office Intern": [
        "Strategic Planning", "Project Management", "Market Research", "Data Analysis", "Investor Relations", 
        "Financial Modeling", "Competitor Intelligence", "Business Operations", "Stakeholder Communication", 
        "Executive Summaries", "GTM Strategy", "Problem Solving", "Agile Methodology", "Workflow Optimization", 
        "CRM Management", "Public Relations", "Business Development", "Risk Assessment", "Coordination", 
        "Crisis Management", "Growth Hacking", "Decision Making", "Note Taking", "Schedule Management", "Resource Allocation"
    ],
    "Graphic Designer Intern": [
        "Adobe Photoshop", "Adobe Illustrator", "Figma", "Canva", "UI Design Principles", "Typography", 
        "Color Theory", "Layout Design", "Brand Identity", "Motion Graphics", "Vector Illustration", 
        "Social Media Creatives", "Logo Design", "Print Media", "Photo Retouching", "Prototyping", 
        "Design Systems", "Infographic Design", "Visual Communication", "UX Design Basics", "Creative Ideation", 
        "Asset Management", "Design Thinking", "Moodboarding", "Ad Creative Strategy"
    ],
    "Curriculum Development Intern": [
        "Instructional Design", "Pedagogical Theory", "Lesson Planning", "LMS Management", "Blooms Taxonomy", 
        "Assessment Design", "Content Mapping", "K-12 Standards", "Educational Psychology", "Gamification", 
        "E-learning Development", "Curriculum Auditing", "Subject Matter Research", "Educational Scripting", 
        "Active Learning", "Learning Objectives", "Teacher Support", "Quality Control", "Worksheet Design", 
        "Interdisciplinary Integration", "EdTech Tools", "Student Personas", "Feedback Loops", "UX for Learning", "Storytelling"
    ],
    "Subject Matter Expert Intern (STEM) - English": [
        "Grammar & Syntax", "Literary Analysis", "Vocabulary Development", "Phonetics", "Creative Writing", 
        "Academic Writing", "IELTS/SAT Prep", "Reading Comprehension", "Curriculum Mapping", "ESL Methodologies", 
        "Etymology", "Content Editing", "Poetry Analysis", "Rhetorical Devices", "Linguistic Assessment", 
        "Plagiarism Checking", "Script Writing", "English Literature", "Sentence Transformation", "Proofreading", 
        "Digital Content", "Educational Research", "Interactive Learning", "Question Banks", "Public Speaking Pedagogy"
    ],
    "Subject Matter Expert Intern (STEM) - Maths": [
        "Algebra", "Calculus", "Geometry", "Trigonometry", "Statistics", "Number Theory", "Maths Curriculum", 
        "JEE/NEET Coaching", "Logical Reasoning", "Data Interpretation", "Vedic Maths", "Math Modeling", 
        "Symbolic Logic", "Problem-Solving", "LaTeX Typing", "Solution Writing", "Pedagogy of Maths", 
        "Coordinate Geometry", "Linear Algebra", "Mental Math", "Math Manipulatives", "Desmos", 
        "Question Framing", "Error Analysis", "Abstract Algebra"
    ],
    "Subject Matter Expert Intern (STEM) - Social Science": [
        "History", "Geography", "Political Science", "Economics", "Civics", "Sociology", "Current Affairs", 
        "Research Methodology", "Map Pointing", "Critical Thinking", "Environmental Studies", "Heritage Education", 
        "Civil Services Prep", "Case Study Development", "Social Theory", "Data Analysis", "Comparative Government", 
        "Demographics", "Political Geography", "Historiography", "Debate Moderation", "Source Analysis", 
        "Policy Analysis", "Educational Content", "Cultural Studies"
    ],
    "Subject Matter Expert Intern (STEM) - Science": [
        "Physics Concepts", "Chemistry Lab Techniques", "Biological Systems", "Scientific Method", "K-12 Science", 
        "STEM Pedagogy", "Scientific Literacy", "Experiment Design", "Data Observation", "Lab Safety", 
        "Environmental Science", "Astronomy", "Material Science", "Anatomy", "Periodic Table", "Newtonian Mechanics", 
        "Scientific Writing", "Diagram Illustration", "Scientific Inquiry", "Inorganic Chemistry", "Botany", 
        "Microscopy", "Thermodynamics", "Organic Synthesis", "Science Communication"
    ],
    "Academic Research Intern": [
        "Literature Review", "Qualitative Research", "Quantitative Analysis", "SPSS/R", "APA/MLA Styles", 
        "Academic Writing", "Data Collection", "Secondary Research", "Hypothesis Testing", "Grant Writing", 
        "Peer-Review Process", "Research Ethics", "Data Cleaning", "Survey Design", "Archival Research", 
        "Case Studies", "Abstract Drafting", "Zotero/Mendeley", "Academic Integrity", "Journal Databases", 
        "Critical Analysis", "Thematic Coding", "Fieldwork", "Report Formatting", "Presentation of Findings"
    ],
    "Competency Mapping Intern": [
        "Skill Gap Analysis", "Job Analysis", "Competency Frameworks", "Behavioral Indicators", "Performance Metrics", 
        "Psychometric Testing", "Organizational Development", "Assessment Centers", "Role Profiling", "L&D", 
        "Talent Management", "Succession Planning", "HR Audit", "Survey Administration", "Data Categorization", 
        "Stakeholder Interviews", "SOPs", "Employee Life Cycle", "Needs Analysis", "KPI Definition", "Instructional Design", 
        "Soft Skills Evaluation", "Analytical Thinking", "Process Mapping", "Curriculum Alignment"
    ],
    "Frontend Developer Intern": [
        "HTML5", "CSS3", "JavaScript (ES6+)", "React.js", "Vue.js", "Tailwind CSS", "Bootstrap", "Responsive Design", 
        "DOM Manipulation", "State Management", "Git", "Browser Debugging", "Performance Optimization", 
        "API Consumption", "Next.js", "SASS/SCSS", "Frontend Architecture", "Unit Testing", "Cross-Browser", 
        "UI/UX Implementation", "Package Managers", "TypeScript", "Vite", "PWA Basics", "Component Design"
    ],
    "Backend Developer Intern": [
        "Node.js", "Express.js", "Python (Django/Flask)", "PostgreSQL", "MongoDB", "RESTful APIs", "SQL Queries", 
        "Schema Design", "Authentication (JWT)", "Server-side Logic", "Microservices", "Docker", "Caching", 
        "AWS/Azure", "Webhooks", "Data Validation", "Middleware", "Async Programming", "Error Handling", 
        "API Documentation", "System Design", "Encryption", "Message Queues", "Serverless", "TDD"
    ],
    "UI /UX Development Intern": [
        "Figma", "Adobe XD", "User Research", "Wireframing", "Prototyping", "Interaction Design", 
        "Visual Hierarchy", "User Personas", "Usability Testing", "Information Architecture", "Design Systems", 
        "Typography", "Color Theory", "Accessibility (WCAG)", "Heuristic Evaluation", "Handoff", "Affinity Mapping", 
        "Journey Maps", "Micro-interactions", "Auto Layout", "Iconography", "Responsive Layouts", "Moodboards", 
        "Atomic Design", "Iterative Design"
    ],
    "School Partnership Intern": [
        "B2B Networking", "Educational Sales", "Pitching to Principals", "Proposal Drafting", "Relationship Management", 
        "Lead Qualification", "Coordination", "CRM Entry", "Market Penetration", "Territory Management", 
        "Public Speaking", "Negotiation", "Event Coordination", "Stakeholder Engagement", "Product Demos", 
        "Brand Representation", "Closing Deals", "Follow-up Strategies", "Client Retention", "Competitor Tracking", 
        "Education Policy", "Local Language", "Travel Logistics", "Cold Outreach", "Workshop Management"
    ],
    "Inside Sales Outreach Intern ( online )": [
        "Inbound Lead Mgmt", "Email Marketing", "LinkedIn Outreach", "Zoom Pitching", "CRM Hygiene", 
        "Digital Communication", "Social Selling", "Webinar Coordination", "Sales Copywriting", "Sequence Design", 
        "Customer Profiling", "Overcoming Objections", "Online Demos", "Lead Scoring", "Outreach Tools", 
        "Time Zone Management", "Active Listening", "Value Propositions", "Sales Funnels", "Digital Documentation", 
        "Persuasive Writing", "Slack/Discord", "Data Mining", "Conversion Optimization", "Virtual Networking"
    ],
    "Inside Sales Outreach Intern ( offline )": [
        "Cold Calling", "Lead Generation", "Telemarketing", "Persuasive Communication", "Sales Scripts", 
        "Database Management", "Product Knowledge", "Appointment Scheduling", "Phone Etiquette", "Resilience", 
        "Quota Management", "Pain Point ID", "Cross-selling", "Up-selling", "Call Analytics", "Market Research", 
        "Consultative Selling", "Voice Modulation", "Referral Generation", "Benchmarking", "Target Audience", 
        "Pipeline Management", "Record Keeping", "Sales Motivation", "Fast-paced Work"
    ],
    "Mental Health Counselling Intern": [
        "Active Listening", "Empathy", "Psychological First Aid", "Crisis Intervention", "Counseling Skills", 
        "CBT Basics", "Client Assessment", "Confidentiality", "Case Documentation", "Mental Health Screening", 
        "Group Facilitation", "Resource Referral", "Emotional Regulation", "Boundaries", "Patient Advocacy", 
        "Awareness Content", "Developmental Psychology", "Trauma-Informed Care", "Stress Management", "Conflict Mediation", 
        "Motivational Interviewing", "Cultural Sensitivity", "Suicide Prevention", "Rapport Building", "Self-Care"
    ],
    "Newsletter Writing Intern": [
        "Email Marketing", "Copywriting", "Audience Segmentation", "Subject Line Optimization", "CTR Analysis", 
        "Editorial Calendar", "Visual Hierarchy", "A/B Testing", "Brand Voice", "Storytelling", "Hyperlink Strategy", 
        "CTA Design", "Spam Filters", "Curated Content", "Newsletter Analytics", "HTML Email", "Compliance", 
        "Subscriber Growth", "Proofreading", "Interviewer Skills", "Survey Integration", "Community Building", 
        "Micro-copy", "Data Visualization", "Platform Migration"
    ],
    "Regional Sales Support Intern": [
        "Regional Research", "Local Language", "Territory Mapping", "Sales Reporting", "Distributor Coordination", 
        "Lead Qualification", "Logistics", "Field Support", "CRM", "Competition Analysis", "Inventory Tracking", 
        "Localization", "Documentation", "Stakeholder Comm", "Payment Follow-ups", "Marketing Support", 
        "Pain Point Analysis", "Travel Planning", "Data Management", "Promotional Events", "Product Training", 
        "Client Onboarding", "Conflict Resolution", "Route Optimization", "Market Trends"
    ],
    "SEO Content Writing Intern": [
        "Keyword Research", "On-Page SEO", "Search Intent", "Meta Tags", "Content Strategy", "Google Analytics", 
        "Search Console", "Internal Linking", "Backlink Outreach", "Gap Analysis", "Readability", "Heading Hierarchy", 
        "LSI Keywords", "Featured Snippets", "Content Refreshing", "Plagiarism Checking", "WordPress", "Technical SEO", 
        "E-E-A-T", "Anchor Text", "Copywriting", "Topic Clustering", "Alt-text", "Performance Tracking", "AI Refinement"
    ],
    "Video Editing Intern": [
        "Adobe Premiere Pro", "After Effects", "Motion Graphics", "Color Grading", "Audio Syncing", 
        "Video Compression", "Storyboarding", "VFX", "Subtitling", "Social Media Formats", "Keyframing", 
        "Transition Design", "B-roll", "Sound Design", "Thumbnail Design", "Rough Cut", "Multi-camera", 
        "Green Screen", "Video Archiving", "Narrative Pacing", "YouTube SEO", "Motion Typography", 
        "Export Settings", "Feedback Implementation", "DaVinci Resolve"
    ],
    "Photography Intern": [
        "Camera Operation", "Studio Lighting", "Adobe Lightroom", "Adobe Photoshop", "Portrait Photography", 
        "Product Photography", "Composition Rules", "Retouching", "Event Photography", "Light Manipulation", 
        "ISO Mastery", "Color Correction", "Metadata Mgmt", "Creative Direction", "File Formats", 
        "Backdrop Arrangement", "Action Shots", "Visual Storytelling", "Photo Culling", "Equipment Maintenance", 
        "Digital Asset Mgmt", "Moodboarding", "Trend Research", "Conceptual Photography", "Mobile Photography"
    ],
    "Locally sales Intern (Offline )": [
        "Door-to-Door", "Face-to-Face Pitching", "Cold Canvassing", "Local Networking", "Demonstration Skills", 
        "Territory Management", "Negotiation", "Objection Handling", "Customer Psychology", "Lead Collection", 
        "Market Intelligence", "Relationship Building", "Brand Representation", "Target Management", "Reporting", 
        "Competitor Tracking", "Public Speaking", "Closing Techniques", "Referral Marketing", "Feedback Gathering", 
        "Time Management", "Interpersonal Skills", "Payment Collection", "Follow-up", "Local Language"
    ],
    "YouTube Optimization Intern": [
        "YouTube Studio", "Title Optimization", "Description Writing", "Tag Strategy", "Thumbnail Strategy", 
        "End Screens", "YouTube SEO", "Playlist Curation", "Community Tab", "Comment Moderation", 
        "Channel Auditing", "Trends Research", "A/B Testing", "Algorithm Awareness", "Retention Analysis", 
        "CTR Optimization", "Video Chaptering", "Monetization", "Influencer Outreach", "Copyright Mgmt", 
        "Promotion", "Livestream Setup", "Growth Hacks", "Transcription", "Viral Analysis"
    ],
    "Operations Intern": [
        "Process Mapping", "SOPs", "Workflow Automation", "Project Tools", "Inventory Mgmt", "Data Entry", 
        "Vendor Mgmt", "Quality Assurance", "Logistics Planning", "Supply Chain", "Resource Allocation", 
        "Crisis Mgmt", "Coordination", "Operational Efficiency", "Documentation", "Time Tracking", 
        "Admin Support", "Problem Solving", "Google Workspace", "Dashboard Mgmt", "Minutes of Meeting", 
        "Scheduling", "Budget Tracking", "Policy Compliance", "System Auditing"
    ]
   
}

# ==========================================
# 2. ENVIRONMENT
# ==========================================

current_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()
env_path = current_dir / ".env"
load_dotenv(dotenv_path=env_path)

api_key = os.getenv("GEMINI_API_KEY")

st.set_page_config(page_title="Conversely AI | Assignment Architect", layout="wide")
st.title("🏗️ Conversely AI: Assignment Architect (PDF Edition)")

if not api_key:
    st.error("🚨 API Key not found!")
    st.stop()

client = genai.Client(api_key=api_key)

# ==========================================
# 3. SIDEBAR - FILE + LIBRARY VIEW
# ==========================================

with st.sidebar:
    st.header("📂 Integrations")

    uploaded_file = st.file_uploader("Upload Job Role Directory", type=['xlsx', 'csv'])

    if uploaded_file:
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)

            st.success("Dataset Loaded!")
            selected_job = st.selectbox("Select Role from File", df.iloc[:, 0].tolist())

        except Exception as e:
            st.error(f"Error loading file: {e}")

    st.markdown("---")
    st.subheader("📚 Skills Library Preview")
    for role_name in SKILLS_LIBRARY:
        st.write(f"**{role_name}**")
        st.caption(", ".join(SKILLS_LIBRARY[role_name]))

# ==========================================
# 4. MAIN INPUT SECTION
# ==========================================

default_role = selected_job if 'selected_job' in locals() else "AI Engineer Intern"
role = st.text_input("🎯 Job Role", value=default_role)

# Auto-suggest skills
suggested_skills = SKILLS_LIBRARY.get(role, [])
selected_skills = st.multiselect(
    "🛠️ Core Skills",
    options=suggested_skills,
    default=suggested_skills[:2] if suggested_skills else []
)

extra_skills = st.text_area(
    "➕ Extra Preferences",
    placeholder="Fintech exposure, presentation skills, startup mindset..."
)

col1, col2 = st.columns(2)

with col1:
    num_assignments = st.number_input("📚 Number of Assignments", 1, 6, 4)

with col2:
    difficulty_level = st.select_slider(
        "🔥 Difficulty",
        options=["Standard", "Challenging", "Elite", "Hardcore"],
        value="Elite"
    )

# ==========================================
# 5. ASSIGNMENT GENERATOR
# ==========================================

def generate_elite_assignments(job_role, skills, extra, count, difficulty):

    skills_text = ", ".join(skills)

    prompt = f"""
    Act as a Lead Hiring Architect.

    Create a {count}-level assignment suite for '{job_role}'.

    Core Skills: {skills_text}
    Extra Preferences: {extra}
    Baseline Difficulty: {difficulty}

    Make assignments AI-resistant.

    For EACH assignment include:

    # Assignment [Number]: [Title]

    - Objective
    - Task
    - Tools/Stack
    - Deliverables
    - Elite Evaluation Criteria
    - Deadline
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(temperature=0.7)
    )

    return response.text


# ==========================================
# 6. PDF GENERATOR
# ==========================================

def generate_pdf(title, content):

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=10)
    pdf.add_page()

    pdf.set_font("Arial", "B", 18)
    pdf.cell(0, 10, title, ln=True)

    pdf.ln(5)
    pdf.set_font("Arial", size=11)

    lines = content.split("\n")

    for line in lines:
        pdf.multi_cell(0, 6, line)

    return pdf.output(dest="S").encode("latin-1")


# ==========================================
# 7. EXECUTION
# ==========================================

if st.button("🚀 Generate Assignment Suite (PDF Ready)"):
    if not selected_skills:
        st.warning("Please select at least one skill.")
    else:
        with st.spinner("Architecting elite assignments..."):
            try:
                result = generate_elite_assignments(
                    role,
                    selected_skills,
                    extra_skills,
                    num_assignments,
                    difficulty_level
                )

                st.markdown("---")
                st.markdown(result)

                pdf_bytes = generate_pdf(
                    f"{role} - Assignment Suite",
                    result
                )

                st.download_button(
                    label="📥 Download as PDF",
                    data=pdf_bytes,
                    file_name=f"{role.replace(' ', '_')}_Assignments.pdf",
                    mime="application/pdf"
                )

            except Exception as e:
                st.error(f"Generation failed: {e}")

st.markdown("---")
st.caption("Conversely AI Engineering Internal Tool | PDF Version")