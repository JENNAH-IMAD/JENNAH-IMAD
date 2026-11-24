"""Generate portfolio section GIFs, keeping every project link in the README."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
ROOT=Path(__file__).resolve().parents[1]
FONT='/usr/share/fonts/truetype/dejavu/'
def font(size,bold=False): return ImageFont.truetype(FONT+('DejaVuSansMono-Bold.ttf' if bold else 'DejaVuSansMono.ttf'),size)
CARDS=[
('profile-intro','01 / PROFILE','Software engineer. Builder.',['Full-stack development / AI / Software delivery','Casablanca, Morocco · Open to new opportunities','','I turn ideas into useful applications: business tools,','booking systems and communication platforms.','From understanding the need to building and deploying.']),
('profile-stack','02 / TOOLKIT','Tools I build with',['FRONTEND   React · Angular · Next.js · TypeScript','           Tailwind CSS · Ant Design','','BACKEND    Spring Boot · ASP.NET Core · Node.js · Django','DATA       PostgreSQL · MySQL · SQL Server · MongoDB','DELIVERY   Docker · GitHub Actions · Linux · Nginx','           Terraform · Google Cloud']),
('profile-projects','03 / SELECTED WORK','Built to solve real problems',['Explore the projects below / source code on GitHub']),
('profile-about','04 / BACKGROUND','Engineering meets curiosity.',['Computer Science & Networks / MIAGE','EMSI Casablanca','','Full-stack internships at Eurafric Information and Munisys.','Freelance application development.','AI-assisted exploration, with careful review of the results.']),
('profile-contact','05 / CONNECT','Let’s build something useful.',['Available for opportunities and meaningful collaborations.'])]
PROJECTS=[('meeting-planner','Meeting Planner','Meeting-room booking / availability'),('team-talk','TeamTalk','Full-stack team communication'),('equipment-manager','IT Equipment Request Manager','Requests / approval workflows'),('insect-detector','Insect Detector','Machine learning / insect classification'),('portfolio','ImFix Portfolio','The visual identity behind this profile')]
for slug,title,desc in PROJECTS: CARDS.append(('profile-project-'+slug,'PROJECT / SOURCE CODE',title,[desc,'View repository  →']))
def render(name,label,title,lines):
 h=146+len(lines)*27
 frames=[]
 for i in range(12):
  im=Image.new('RGB',(1000,h),'#171a1b'); d=ImageDraw.Draw(im)
  d.rounded_rectangle((1,1,998,h-2),radius=5,outline='#373c3e')
  d.text((32,25),label,font=font(12),fill='#9aa2a1')
  d.text((32,56),title,font=font(29,True),fill='#e6e8e7')
  d.line((32,105,968,105),fill='#303638')
  for j,line in enumerate(lines):d.text((32,125+j*27),line,font=font(15),fill='#b9c0bf')
  # A restrained moving status marker provides continuous visible motion.
  x=32+round(i/11*904)
  d.rectangle((x,h-13,x+30,h-11),fill='#c6cecd')
  frames.append(im)
 palette=frames[0].quantize(colors=64)
 frames=[im.quantize(palette=palette,dither=Image.Dither.NONE) for im in frames]
 frames[0].save(ROOT/'cards'/f'{name}.gif',save_all=True,append_images=frames[1:]+frames[-2:0:-1],duration=130,loop=0,optimize=True,disposal=1)
for card in CARDS:render(*card)
print('Generated',len(CARDS),'animated section cards')
