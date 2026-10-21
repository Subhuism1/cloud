import json, os
info=json.load(open('tinfo.json'))
W={299:'two ninety-nine',399:'three ninety-nine',499:'four ninety-nine',799:'seven ninety-nine',999:'nine ninety-nine',1499:'fourteen ninety-nine'}
U={299:(4,'four'),399:(5,'five'),499:(6,'six'),799:(9,'nine'),999:(12,'twelve'),1499:(18,'eighteen')}
FEAT=["Every ceremony, the dress code, the venue map, and a live countdown, all in one link.",
 "Every event, the blessings, the hosts, the venue map, and a live countdown, all in one link.",
 "Your story, your events, a gallery, the venue map, and a live countdown, all in one link.",
 "Every detail, from ceremonies and dress code to directions and a countdown, all in one link."]
# slug: (hook_voice, h1, h2, sub, c1a, c1b, tint, endbg, gold, feat_idx)
T={
'zaytoon':("What if your Nikah invitation glowed in cream, gold and olive?","Your Nikah invitation,","in cream, gold and olive","Radiant Nikah · Cream, gold & olive",(30,34,16),(44,50,24),(236,214,150),1),
'zafraan':("What if your Nikah invitation felt like a warm terracotta sunset?","Your Nikah invitation,","in terracotta and saffron","Warm terracotta · Saffron Nikah",(52,22,12),(86,38,20),(255,196,120),1),
'khatim':("What if your Nikah invitation looked like an engraved emerald seal?","Engraved in emerald","and antique gold","Engraved Nikah · Emerald & antique gold",(6,34,28),(8,48,40),(222,196,120),1),
'reshm-e-noor':("What if your Nikah invitation felt soft, modern and effortlessly warm?","Soft, modern, warm","cream · terracotta · sage","Warm modern Nikah · Terracotta rose & sage",(60,34,28),(110,64,52),(255,224,190),2),
'noor-e-nikah':("What if your Nikah and Walima shared one beautiful link?","Nikah and Walima,","one beautiful link","Nikah & Walima · Emerald-and-gold motifs",(6,34,30),(10,52,44),(240,214,140),1),
'sukoon':("What if your Nikah invitation felt like a serene dusk?","A serene Nikah","invitation at dusk","Serene dusk · Blush, aubergine & rose copper",(40,18,44),(60,24,66),(240,190,170),0),
'zumurrud':("What if your Nikah invitation shone in deep emerald and gold?","Deep emerald,","pure gold","Deep emerald · Gold Nikah",(4,40,30),(6,60,44),(244,214,120),3),
'gulnaar':("What if your Baat Pakki invitation bloomed in soft rose?","Your Baat Pakki,","in soft blush-rose","Soft blush-rose · Baat Pakki",(70,28,40),(118,52,70),(255,214,214),2),
'mukhmal':("What if your wedding invitation opened like velvet drapes by candlelight?","Velvet drapes,","candlelight and gold","Burgundy velvet · Candlelit chandeliers",(46,8,14),(74,12,20),(240,200,130),0),
'rang-mahal':("What if your wedding invitation opened like a palace gate in ruby and marigold?","A palace gate in","ruby and marigold","Palace gate · Ruby, marigold & gold",(60,10,18),(100,16,30),(255,200,90),3),
'chameli':("What if your wedding invitation opened like carved teak doors onto a jasmine courtyard?","Teak doors open on","a jasmine courtyard","Carved teak doors · Jasmine garlands",(46,28,14),(74,46,22),(255,232,170),2),
'anand-karaj':("What if your Anand Karaj invitation had everything in one link?","Your Anand Karaj,","everything in one link","Anand Karaj · Blessings, hosts & RSVP",(46,20,12),(80,34,18),(255,208,130),1),
'anand-noor':("What if your Anand Karaj invitation glowed in royal indigo and gold?","Royal indigo","and golden light","Royal indigo & gold · Anand Karaj",(16,18,52),(22,26,84),(250,214,130),0),
'amrit-vela':("What if your Anand Karaj invitation opened like the first light of dawn?","The first light","of your dawn","Dawn-lit Anand Karaj · Blush, lilac & aqua",(36,22,60),(52,34,92),(255,214,170),2),
'sehaj':("What if your Anand Karaj invitation felt calm, editorial and timeless?","Calm, editorial,","ink black and gold","Handmade paper · Ink black & gold",(18,18,18),(14,14,14),(236,208,140),3),
'kesri':("What if your Anand Karaj invitation carried the saffron of the Nishan Sahib?","Nishan Sahib saffron","on a midnight blue","Gurdwara-ready · Saffron & Nihang blue",(12,16,44),(14,22,70),(255,170,60),0),
'phulkari':("What if your Anand Karaj invitation was stitched in golden phulkari?","Stitched in golden","phulkari on bridal red","Ivory khaddar · Golden phulkari",(70,12,18),(112,18,28),(255,208,120),2),
'sunehri-darbar':("What if your Anand Karaj invitation shone like the Darbar Sahib at night?","Golden as the Darbar","Sahib at night","Midnight blue · Temple gold",(10,18,48),(12,26,76),(255,214,120),1),
'papercut-lotus':("What if your wedding invitation bloomed like a paper-cut lotus pond?","A paper-cut","lotus pond","Layered lotus pond · Carved arch",(70,16,40),(112,24,62),(255,214,170),2),
'royale':("What if your wedding invitation opened like a palace gate with painted elephants?","Painted elephants,","a mandap at dusk","Maroon palace gate · Garden mandap",(56,10,26),(90,16,40),(255,204,130),0),
'pink-blossom':("What if your wedding invitation arrived in a blush-pink envelope of petals?","A blush envelope,","a shower of petals","Blush-pink envelope · Petal shower",(86,36,52),(132,58,82),(255,230,230),3),
'royal-heritage':("What if your wedding invitation opened like a maroon and gold royal cover?","Maroon and gold,","royal heritage","Maroon & gold · Floral border",(64,12,20),(100,18,30),(255,208,130),1),
'south-mandapam':("What if your wedding invitation spoke in five South Indian languages?","Five languages,","one South Indian invitation","South Indian · Five languages",(46,28,6),(74,46,10),(255,214,110),1),
'meenakshi-mandir':("What if your wedding invitation rose like a painted gopuram against the sky?","A painted gopuram","against a bright sky","Painted gopuram · South Indian",(14,30,60),(20,46,92),(255,214,120),0),
'sangam':("What if your wedding invitation honoured every faith in one link?","One invitation,","every faith","Hindu · Christian · Muslim · One link",(30,30,34),(40,40,48),(240,220,170),2),
'garden-vows':("What if your save the date felt like a soft garden in ivory and sage?","A soft garden","save the date","Ivory & sage · Garden save the date",(34,42,30),(56,70,48),(244,238,214),None),
'olive-wine':("What if your save the date carried the air of a French countryside?","A French-countryside","save the date","Olive & wine · Countryside",(44,40,18),(80,30,44),(236,214,160),None),
'silver-locket':("What if your save the date looked like a black and white editorial?","A black and white","editorial save the date","Lilies & silver · Editorial",(20,20,22),(14,14,16),(222,224,230),None),
'royal-lotus':("What if your wedding invitation opened with a rope pull at a Rajasthani palace gate?","A Rajasthani palace","gate opens for you","Gold & maroon · Lotus-tap gate",(60,14,20),(96,22,32),(255,214,140),3),
'royal-blush':("What if your wedding invitation came in wine and gold?","Wine and gold,","fully loaded","Wine & gold · Gift registry, hosts & RSVP",(66,14,30),(104,22,50),(255,208,170),1),
'midnight-luxe':("What if your wedding invitation felt like midnight black and gold?","Midnight black","and gold","Black & gold · Modern sophistication",(14,14,14),(10,10,10),(240,206,120),0),
'golden-noir':("What if your wedding invitation was black with champagne gold?","Black hues,","champagne gold","Noir & champagne gold · Luxurious",(16,14,12),(12,10,8),(236,214,160),2),
'gilded-veil':("What if your guests had to scratch to reveal your wedding date?","Scratch to reveal,","glass and gold","Glass & gold · Scratch-to-reveal date",(40,34,22),(70,56,30),(250,226,160),3),
'azure-royale':("What if your wedding invitation came in navy and gold?","Navy and gold,","fully loaded","Navy & gold · Gift registry, hosts & RSVP",(10,20,52),(14,30,86),(248,214,130),1),
'azure-dreams':("What if your wedding invitation glowed in luminous blue glass?","Luminous blue,","glass-inspired","Luminous blue · Glass details",(10,32,64),(16,52,104),(220,236,255),2),
'crimson-royale':("What if your wedding invitation opened like royal theatre curtains?","Royal theatre","curtains, crimson","Crimson curtains · Golden accents",(66,8,16),(110,12,26),(255,208,130),0),
'emerald-royale':("What if your wedding invitation came in rich emerald and gold?","Rich emerald","and golden elegance","Rich emerald · Golden elegance",(6,38,28),(8,58,42),(244,214,120),3),
'scarlet-stamp':("What if your wedding invitation was bold, loud and unforgettable?","Bold, thick borders,","a scarlet stamp","Neo-brutalist · Thick borders",(70,12,12),(160,20,20),(255,240,200),2),
'grand-celebration':("What if your wedding invitation had a section for everything?","One grand invitation,","every section","Multi-section · Registry, hosts & RSVP",(34,24,12),(60,42,18),(255,214,140),1),
'whispering-leaves':("What if your wedding invitation whispered in leafy green and gold?","Gentle green,","luxurious gold","Gentle green · Golden accents",(14,40,24),(20,62,36),(238,222,150),0),
'celestial-clouds':("What if your wedding invitation floated on cloud-white and sky blue?","Weightless,","cloud-white and sky blue","Cloud-white · Sky blue",(30,60,100),(46,90,150),(255,255,255),2),
'azure-maison':("What if your wedding invitation opened like blue and white porcelain?","Blue orchids on","porcelain white","Blue-and-white porcelain · Script names",(14,34,70),(20,52,106),(236,244,255),3),
'burgundy-maison':("What if your wedding invitation came sealed in a garnet envelope?","A garnet envelope,","a wax seal","Garnet envelope · Wax seal · Botanical relief",(56,10,22),(92,16,36),(255,226,200),0),
'ivory-palace':("What if your wedding invitation opened through carved ivory doors?","Carved ivory doors","open on your names","Carved ivory doors · Palace",(48,42,30),(86,76,54),(255,244,214),1),
'garden-of-dreams':("What if your guests walked down a flowering aisle to your names?","A flowering aisle,","arches, vines, orchids","Flowering aisle · Orchids",(30,40,28),(48,66,44),(255,236,236),2),
'golden-key':("What if your wedding invitation unlocked a rose-gold gate in a pastel sky?","A rose-gold gate","in a pastel sky","Pastel-sky fantasy · Rose-gold gate",(70,40,60),(120,76,104),(255,226,214),0),
}
CHORDS=[[[48,55,59,64],[45,52,55,60],[41,48,52,57],[43,50,55,59]],
        [[50,57,62,64],[47,54,59,62],[43,50,55,59],[45,52,57,61]],
        [[45,52,57,60],[41,48,53,57],[43,50,55,58],[40,47,52,56]],
        [[52,59,64,67],[48,55,60,64],[45,52,57,60],[47,54,59,62]],
        [[46,53,58,62],[43,50,55,58],[39,46,51,55],[41,48,53,57]],
        [[53,60,65,69],[50,57,62,65],[46,53,58,62],[48,55,60,64]]]
PAT=[[0,1,2,3,2,1],[0,2,1,3,2,1],[0,1,2,1,3,2],[3,2,1,0,1,2]]
FONTS=['Bitstream Charter:bold','DejaVu Serif:bold','Liberation Serif:bold','Caladea:bold']
PY=[1290,1210,1340]
os.makedirs('cfgs',exist_ok=True)
order=[l.split('|')[0] for l in open('tlist.txt')]
for idx,slug in enumerate(order):
    d=info[slug]; hv,h1,h2,sub,tint,endbg,gold,fi=T[slug]; inr=int(d['price']); usd,usdw=U[inr]
    name=d['name']; kw=d['kw']
    std=(fi is None)
    feat = "Your date, a countdown, and everything your guests need, all in one link." if std else FEAT[fi]
    c1={0:("Ceremonies · Dress code","Venue map · Live countdown"),1:("Events · Blessings · Hosts","Venue map · Live countdown"),2:("Your story · Gallery","Venue map · Live countdown"),3:("Every detail, one link","Directions · Live countdown")}.get(fi,("Your date · Countdown","Everything guests need"))
    rsvpline = "Guests R S V P in one tap." if not std else "Guests can reply in one tap."
    cfg=dict(slug=slug,title=name,kw=kw,inr=str(inr),usd=str(usd),
      hook=[h1,h2],name_sub=sub,c1=list(c1),
      segs=[[hv,0.25],[f"Meet {name}.",0.15],[feat,0.25],[rsvpline,0.25],
            [f"Just {W[inr]} rupees, or {usdw} dollars outside India. Available worldwide.",0.2],
            [f"Templates start at just two ninety-nine rupees. Comment {kw.upper()}, and I'll send you the link.",0.35],
            ["Find us at save our date, dot, in.",0.3]],
      gold=list(gold),tint=list(tint),endbg=list(endbg),
      serif=FONTS[(idx+hash(slug)%3)%4], panel_y=PY[idx%3], zoom=[0.05,0.07,0.09,0.06][idx%4], zdir=('in' if idx%2==0 else 'out'),
      drift=[0,16,28,10][idx%4], plateau=[0.22,0.3,0.4][idx%3], openAt=1.8,
      music=dict(chords=CHORDS[idx%6],bpm=[58,62,66,70,60,64][(idx*5)%6],seed=idx+11,pattern=PAT[idx%4],decay=[2.6,3.2,3.8][idx%3],sub=[2,2,1][idx%3]))
    json.dump(cfg,open(f'cfgs/{slug}.json','w'),ensure_ascii=False,indent=1)
print(len(order),'configs')
