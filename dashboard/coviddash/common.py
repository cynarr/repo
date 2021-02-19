from datetime import date
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from . import database_conn as db_conn


# Load configs for filters
config_available_languages = [{'label': 'All', 'value': ''}] 
config_available_languages += [{'label': pl, 'value': l} for pl, l in db_conn.get_available_languages()]

config_min_date, config_max_date = db_conn.get_min_and_max_dates()

config_available_sentiments = [{'label': 'All', 'value': ''}]
config_available_sentiments += [{'label': s.title(), 'value': s} for s in db_conn.get_available_sentiments()]

config_available_producing_countries = [{'label': 'All', 'value': ''}]
config_available_producing_countries += [{'label': n, 'value': s} for n, s in db_conn.get_available_producing_countries()]

config_available_mentioned_countries = [{'label': 'All', 'value': ''}]
config_available_mentioned_countries += [{'label': n, 'value': s} for n, s in db_conn.get_available_mentioned_countries()]


def load_wrap(children):
    return dcc.Loading(
        type="default",
        fullscreen=True,
        style={'backgroundColor': 'rgba(0,0,0,0.5)'},
        children=children
    )


date_range_col = dbc.Col(
    dbc.FormGroup(
        [
            dbc.Label("Date range", html_for="date-range-filter"),
            html.Br(),
            dcc.DatePickerRange(
                id='date-range-filter',
                display_format='YYYY-MM-DD',
                min_date_allowed=config_min_date,
                max_date_allowed=config_max_date,
                start_date=config_min_date,
                end_date=config_max_date
            ),
        ]
    ),
    width=3,
)


mode_col = dbc.Col(
    dbc.FormGroup(
        [
            dbc.Label("Countries are", html_for="polarity-selector"),
            dbc.Select(
                id='mode-selector',
                options=[
                    {'label': 'Producing news', 'value': 'produce'},
                    {'label': 'Mentioned in news', 'value': 'mention'},
                ],
                value='mentions'
            ),
        ]
    ),
    width=2,
)


polarity_col = dbc.Col(
    dbc.FormGroup(
        [
            dbc.Label("Sentiment polarity", html_for="polarity-selector"),
            dbc.Select(
                id='polarity-selector',
                options=[
                    {'label': 'Summary', 'value': 'summary'},
                    {'label': 'Positive', 'value': 'positive'},
                    {'label': 'Neutral', 'value': 'neutral'},
                    {'label': 'Negative', 'value': 'negative'}
                ],
                value='summary'
            ),
        ]
    ),
    width=2,
)


language_col = dbc.Col(
    dbc.FormGroup(
        [
            dbc.Label("Language", html_for="language-dropdown"),
            dbc.Select(
                id='language-dropdown',
                options=config_available_languages,
                value=''
            )
        ]
    ),
    width=2,
)

media_country_col = dbc.Col(
    dbc.FormGroup(
        [
            dbc.Label("Producing country", html_for="media-country"),
            dbc.Select(
                id='media-country',
                options=config_available_producing_countries,
                value=''
            )
        ]
    ),
    id="media-country-col",
    width=2,
)

mention_country_col = dbc.Col(
    dbc.FormGroup(
        [
            dbc.Label("Mentioned country", html_for="mention-country"),
            dbc.Select(
                id='mention-country',
                options=config_available_mentioned_countries,
                value=''
            )
        ]
    ),
    id="mention-country-col",
    width=2,
)

map_sentiments_right_cols = [
    mode_col,
    polarity_col,
    language_col,
    media_country_col,
    mention_country_col,
]

from io import StringIO

state_url_csv = StringIO("""domain,cc2
100komma7.lu,LU
1tv.am,AM
1tv.com.ua,UA
andorradifusio.ad,AD
ard.de,DE
armradio.am,AM
avro.nl,NL
bbc.co.uk,GB
bbc.com,GB
bbcfrance.fr,GB
bbcstudioworks.com,GB
bbcworldwide.com,GB
bhrt.ba,BA
bnn.nl,NL
bnnvara.nl,NL
bnr.bg,BG
bnt.bg,BG
boeddhistischeomroep.nl,NL
brf.be,BE
cadenaser.com,ES
ceskatelevize.cz,CZ
cfi.fr,FR
cope.es,ES
ctk.cz,CZ
cybc.com.cy,CY
dr.dk,DK
dw.com,DE
dwnewsvdyyiamwnp.onion,DE
eitb.eus,ES
eo.nl,NL
err.ee,EE
ert.gr,GR
europe1.fr,FR
fipradio.fr,FR
fondationfrancetelevisions.fr,FR
france.tv,FR
francebleu.fr,FR
franceculture.fr,FR
franceinter.fr,FR
francemusique.fr,FR
francetvinfo.fr,FR
gpb.ge,GE
hr.de,DE
hrt.hr,HR
humanistischeomroep.nl,NL
ikonrtv.nl,NL
itv.az,AZ
joodseomroep.nl,NL
katholieknederland.nl,NL
kaztrk.kz,KZ
kro.nl,NL
kunskapskanalen.se,SE
kvf.fo,FO
lemouv.fr,FR
lrt.lt,LT
lsm.lv,LV
ltv.lt,LV
maisondelaradio.fr,FR
mc-doualiya.com,FR
mdr.de,DE
mediaklikk.hu,HU
mfptv.fr,FR
mouv.fr,FR
mrt.com.mk,MK
mtv.hu,HU
mtv3.fi,FI
ncrv.nl,NL
ndr.de,DE
npo.nl,NL
nrcu.gov.ua,UA
nrk.no,NO
ohmnet.nl,NL
oireachtas.ie,IE
orf.at,AT
polskieradio.pl,PL
radio.li,LI
radiobarcelona.cat,ES
radiobremen.de,DE
radiofrance.fr,FR
rai.it,IT
raiplay.it,IT
raipubblicita.it,IT
rbb-online.de,DE
redbeemedia.com,GB
rfi.fr,FR
rmb.be,BE
rozhlas.cz,CZ
rozhlas.sk,SK
rsi.ch,CH
rtbf.be,BE
rtcg.me,ME
rte.ie,IE
rtp.pt,PT
rts.rs,RS
rtsh.al,AL
rtvc.es,ES
rtve.es,ES
rtvs.sk,SK
rtvslo.si,SI
ruv.is,IS
sanmarinortv.sm,SM
sr.de,DE
srgssr.ch,CH
srr.ro,RO
stv.sk,SK
sverigesradio.se,SE
svt.se,SE
swr.de,DE
tf1.fr,FR
tg4.ie,IE
trm.md,MD
trt.net.tr,TR
trt1.com.tr,TR
tv4.se,SE
tveinternacional.es,ES
tvm.com.mt,MT
tvp.pl,PL
tvr.by,BY
tvr.ro,RO
uktv.co.uk,GB
ur.se,SE
vara.nl,NL
vaticannews.va,VA
vgtrk.com,RU
vpro.nl,NL
vrt.be,BE
wdr.de,DE
yle.fi,FI
zdf.de,DE
zvk.nl,NL
""")

import pycountry
import pandas as pd
def remove_note(s):
    return s.rsplit(" (", 1)[0]

def country_name(cc2):
    return remove_note(pycountry.countries.get(alpha_2=cc2).name)


state_data_df = pd.read_csv(state_url_csv, sep=",")

state_data_df["country"] = state_data_df["cc2"].map(country_name)
state_data_df = state_data_df[["country", "domain"]]