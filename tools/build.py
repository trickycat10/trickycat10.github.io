"""Generate the portfolio pages from shared layout and career content."""
from pathlib import Path
from math import sin, cos, pi
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from xml.sax.saxutils import escape

out = Path(__file__).resolve().parent.parent
out.mkdir(exist_ok=True)
roles = [
    ('May 2026 – present','ASP.NET Developer','I build C# APIs that connect electronic health record systems.','I optimized SQL Server queries and implemented role-based access controls. Average API response time fell by 30%.'),
    ('Mar – Apr 2026','EUS Retail Engineer','I supported retail operations and coordinated incident response.','I managed more than 50 ServiceNow tickets per week, maintained 98% SLA compliance, and worked with field engineers to improve triage.'),
    ('Sep 2024 – Feb 2026','Cloud Infrastructure Services Associate','I managed access and provisioning across cloud and workplace tools.','My work covered IAM, Azure and Office 365 for more than 2,000 users, alongside device policies and change management.')
]
projects = [
    ('healthaxis','HealthAxis','Clinic management platform','C# · ASP.NET Core · Angular','I built a clinic platform with an Angular portal, a Blazor administration console and an ASP.NET Core API backed by SQL Server.',
    [('Application architecture','The Angular portal and Blazor admin console use an API that accesses SQL Server through Entity Framework Core. JWT authentication protects access.'),('Background work','I used RabbitMQ and MassTransit for event-driven workflows, keeping message handling separate from request handling.'),('Testing and operations','I covered services with xUnit tests and added centralized logging with Elasticsearch and Kibana. The AWS deployment design uses Elastic Beanstalk, RDS and S3.')]),
    ('f1-podium-predictor','F1 Podium Predictor','Race prediction and ranking','Python · LightGBM · Streamlit','I built a model that ranks drivers by their chances of finishing on the podium, using historical race data from FastF1 and Jolpica.',
    [('Working with race history','I used rolling features based on earlier races so later results could not leak into predictions.'),('From rankings to probabilities','LightGBM LambdaRank produces driver rankings. I used 10,000-run Plackett–Luce simulations to turn those rankings into podium odds for a Streamlit dashboard.'),('Evaluation','Across 951 driver entries from 2024–2025, the evaluation produced an NDCG@3 ranking score of 0.887 and a reported podium hit rate of 82.5%.')])
]
github='https://github.com/trickycat10'
linkedin='https://www.linkedin.com/in/abhishek-upadhyay-87bbb3228/'
email='abhishek.all.2001@gmail.com'
resume='/abhishek-upadhyay-resume.pdf'
def page(path,title,body,section,description):
    nav=''.join(f'<a href="{url}"'+(' aria-current="page"' if label==section else '')+f'>{label}</a>' for url,label in [('/','Home'),('/projects/','Projects')])
    dest=out/path/'index.html'
    dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_text(f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{title} | Abhishek Upadhyay</title><meta name="description" content="{description}"><meta name="theme-color" content="#101925"><link rel="stylesheet" href="/style.css"></head><body><a class="skip" href="#main">Skip to content</a><header><div class="wrap bar"><a class="brand" href="/">Abhishek Upadhyay<span>.</span></a><nav aria-label="Main navigation">{nav}<a class="resume" href="{resume}">Résumé</a></nav></div></header><main id="main" class="wrap">{body}</main><footer><div class="wrap foot"><div><h2>Get in touch</h2><a href="mailto:{email}">{email}</a></div><div class="social"><a href="{github}">GitHub</a><a href="{linkedin}">LinkedIn</a><a href="{resume}" download>Download résumé</a></div></div></footer></body></html>''')
timeline=''.join(f'<details><summary><span class="date">{date}</span><strong>{role}</strong></summary><p>{intro} {work}</p></details>' for date,role,intro,work in roles)
page('','Software developer in Noida',f'''<section class="hero"><div class="contour" aria-hidden="true"></div><div class="hero-copy"><p class="eyebrow">Software developer <i></i> Noida, India</p><h1>From infrastructure<br>to <em>software development.</em></h1><p class="intro">I’m Abhishek, a .NET developer at UST. I started in cloud infrastructure, moved into technical support, and now build APIs in C#.</p><div class="actions"><a class="button" href="{resume}">View résumé</a><a class="quiet" href="/projects/">Browse projects</a></div></div></section><section class="split"><div><p class="eyebrow">Experience at UST</p><h2>My journey</h2></div><div class="timeline">{timeline}</div></section><section class="split"><h2>Education</h2><div><h3>B.Tech in Information Technology</h3><p>Madan Mohan Malaviya University of Technology, Gorakhpur<br>2020–2024 · CGPA 8.04/10</p></div></section>''','Home','Abhishek Upadhyay’s career in software development, technical support and cloud infrastructure.')
rows=''
for slug,name,short,stack,intro,sections in projects:
    art='clinic' if slug=='healthaxis' else 'race'
    rows+=f'<a class="project" href="/projects/{slug}/"><span class="thumb {art}" aria-hidden="true"></span><div><h2>{name}</h2><p>{short}</p><small>{stack}</small></div><span class="read">Read case study</span></a>'
    content=''.join(f'<section class="split"><h2>{head}</h2><p>{para}</p></section>' for head,para in sections)
    page('projects/'+slug,name,f'<section class="lead"><a class="quiet" href="/projects/">All projects</a><h1>{name}</h1><p class="intro">{intro}</p><small>{stack}</small></section>{content}','Projects',short+' by Abhishek Upadhyay.')
page('projects','Projects',f'<section class="lead"><h1>Projects</h1><p class="intro">A closer look at the systems I’ve built and the engineering decisions behind them.</p></section><div class="projects">{rows}</div>','Projects','Selected engineering projects and technical case studies by Abhishek Upadhyay.')
# Draw abstract contours locally so the site needs no external art or fonts.
paths=[]
for i in range(30):
    pts=[]
    for j in range(241):
        a=j*pi/120
        r=(35+i*6)*(1+.14*sin(3*a+.3)+.08*cos(5*a))
        pts.append(f'{235+r*cos(a):.1f},{180+.76*r*sin(a):.1f}')
    paths.append('<path d="M'+' L'.join(pts)+' Z"/>')
(out/'contours.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 480 360"><g fill="none" stroke="#63d7c5" stroke-width=".8">'+''.join(paths)+'</g></svg>')
styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='ResumeHead',fontSize=13,leading=17,textColor=HexColor('#135d58'),spaceBefore=9,spaceAfter=4))
styles.add(ParagraphStyle(name='ResumeBody',fontSize=9.5,leading=13,spaceAfter=4))
story=[]
def para(t,style='ResumeBody'):
    story.append(Paragraph(escape(t),styles[style]))
para('Abhishek Upadhyay','Title')
para('Software Developer (.NET) · Noida, India')
para(email+'  |  github.com/trickycat10')
para('Experience at UST','ResumeHead')
for date,role,intro,work in roles:
    para(role+'  |  '+date,'Heading4')
    para(intro+' '+work)
para('Selected projects','ResumeHead')
for slug,name,short,stack,intro,sections in projects:
    para(name+'  |  '+stack,'Heading4')
    para(intro+' '+sections[-1][1])
para('Education','ResumeHead')
para('B.Tech in Information Technology · Madan Mohan Malaviya University of Technology, Gorakhpur · 2020–2024 · CGPA 8.04/10')
para('Technical skills','ResumeHead')
para('C#, SQL, JavaScript, Python, ASP.NET Core, Entity Framework Core, Angular, Blazor, SQL Server, Redis, RabbitMQ, Azure, AWS, Git and Linux.')
SimpleDocTemplate(str(out/resume.lstrip('/')),pagesize=A4,title='Abhishek Upadhyay | Résumé',leftMargin=41,rightMargin=41,topMargin=36,bottomMargin=36).build(story)
