"""Portfolio detail cards. Repository evidence is recorded in data/profile-projects.json."""
import json
from pathlib import Path
from html import escape
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'cards'
FONT='ui-monospace,SFMono-Regular,Menlo,monospace'
CSS='@keyframes rise{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}.enter{animation:rise .8s ease both}@media(prefers-reduced-motion:reduce){.enter{animation:none}}'
def card(name,kicker,title,lines):
 h=145+len(lines)*28
 body=f'<rect x="1" y="1" width="878" height="{h-2}" rx="14" fill="#171a1b" stroke="#373c3e"/><text x="32" y="35" fill="#aab5c2" font-size="11" letter-spacing="1.5">{escape(kicker)}</text><text x="32" y="79" fill="#e6e8e7" font-size="27" font-weight="600">{escape(title)}</text><path d="M32 103H848" stroke="#373c3e"/>'
 for i,line in enumerate(lines):body+=f'<text class="enter" style="animation-delay:{i*.08}s" x="32" y="{137+i*28}" fill="#c0c7ce" font-size="15">{escape(line)}</text>'
 (OUT/(name+'.svg')).write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="880" height="{h}" viewBox="0 0 880 {h}" role="img" aria-label="{escape(title)}"><title>{escape(title)}</title><style>{CSS}</style><g font-family="{FONT}">{body}</g></svg>')
def main():
 OUT.mkdir(exist_ok=True)
 card('profile-intro','01 / WHOAMI','Software engineer / Full-stack developer',[
 'Casablanca, Morocco · Open to new opportunities','I turn ideas into useful applications, from need to deployment.',
 'Business tools, booking systems and communication platforms.',
 'React, Angular, Spring Boot and ASP.NET Core.',
 'AI-assisted exploration, with careful review of the results.'])
 card('profile-toolkit','02 / TOOLKIT','Interfaces. APIs. Delivery.',[
 'FRONTEND    React · Angular · Next.js · TypeScript',
 '            Tailwind CSS · Ant Design · Bootstrap',
 'BACKEND     Spring Boot · ASP.NET Core · Node.js',
 '            REST APIs · JWT · SignalR',
 'DATA        PostgreSQL · MySQL · SQL Server',
 'DELIVERY    Docker · GitHub Actions · Linux'])
 card('profile-work','03 / SELECTED WORK','Applications with a purpose',[
 'Explore selected repositories below. Each project card is clickable.'])
 projects=[('equipment','IT Equipment Request Manager','Internal equipment requests and approval workflows.'),('team','TeamTalk','Full-stack team communication platform.'),('insect','Insect Detector','Computer vision / insect classification.'),('meeting','Meeting Planner','Meeting-room booking and availability.'),('alias','Alias Convert PDF','Bank statement conversion / PaddleOCR / Sage exports.')]
 for slug,title,desc in projects:card('featured-'+slug,'PROJECT / VIEW SOURCE',title,[desc,'Open repository →'])
 card('profile-now','04 / NOW','Building, learning, moving forward.',[
 'Full-stack applications, software delivery and applied AI.',
 'Engineering degree in Computer Science & Networks / MIAGE.',
 'EMSI Casablanca · Looking for a team to contribute and grow.'])
 card('profile-connect','05 / CONNECT','Let’s build something useful.',[
 'Available for opportunities and thoughtful collaborations.'])
if __name__=='__main__':main()
