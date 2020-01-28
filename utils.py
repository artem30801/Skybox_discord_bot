'''File with different functions for bot, that somewhy not in the main body'''

from datetime import datetime, timezone, timedelta
from collections import namedtuple

# using pytz requires additional work, it's easier to handle it manually
# https://en.wikipedia.org/wiki/List_of_time_zone_abbreviations
# pylint: disable=line-too-long
TIMEZONES = {
    "ACDT" : timezone(timedelta(hours=10, minutes=30)), # Australian Central Daylight Savings Time
    "ACST" : timezone(timedelta(hours=9, minutes=30)), # Australian Central Standard Time
    "ACT" : timezone(-timedelta(hours=5, minutes=0)), # Acre Time
    "ACWST" : timezone(timedelta(hours=8, minutes=45)), # Australian Central Western Standard Time (unofficial)
    "ADT" : timezone(-timedelta(hours=3, minutes=0)), # Atlantic Daylight Time
    "AEDT" : timezone(timedelta(hours=11, minutes=0)), # Australian Eastern Daylight Savings Time
    "AEST" : timezone(timedelta(hours=10, minutes=0)), # Australian Eastern Standard Time
    "AFT" : timezone(timedelta(hours=4, minutes=30)), # Afghanistan Time
    "AKDT" : timezone(-timedelta(hours=8, minutes=0)), # Alaska Daylight Time
    "AKST" : timezone(-timedelta(hours=9, minutes=0)), # Alaska Standard Time
    "ALMT" : timezone(timedelta(hours=6, minutes=0)), # Alma-Ata Time[1]
    "AMST" : timezone(-timedelta(hours=3, minutes=0)), # Amazon Summer Time (Brazil)[2]
    "AMT" : timezone(-timedelta(hours=4, minutes=0)), # Amazon Time (Brazil)[3]
    "ANAT" : timezone(timedelta(hours=12, minutes=0)), # Anadyr Time[4]
    "AQTT" : timezone(timedelta(hours=5, minutes=0)), # Aqtobe Time[5]
    "ART" : timezone(-timedelta(hours=3, minutes=0)), # Argentina Time
    "AST" : timezone(timedelta(hours=3, minutes=0)), # Arabia Standard Time
    "AWST" : timezone(timedelta(hours=8, minutes=0)), # Australian Western Standard Time
    "AZOST" : timezone(timedelta(hours=0, minutes=0)), # Azores Summer Time
    "AZOT" : timezone(-timedelta(hours=1, minutes=0)), # Azores Standard Time
    "AZT" : timezone(timedelta(hours=4, minutes=0)), # Azerbaijan Time
    "BDT" : timezone(timedelta(hours=8, minutes=0)), # Brunei Time
    "BIOT" : timezone(timedelta(hours=6, minutes=0)), # British Indian Ocean Time
    "BIT" : timezone(-timedelta(hours=12, minutes=0)), # Baker Island Time
    "BOT" : timezone(-timedelta(hours=4, minutes=0)), # Bolivia Time
    "BRST" : timezone(-timedelta(hours=2, minutes=0)), # Brasília Summer Time
    "BRT" : timezone(-timedelta(hours=3, minutes=0)), # Brasília Time
    "BST" : timezone(timedelta(hours=6, minutes=0)), # Bangladesh Standard Time
    "BTT" : timezone(timedelta(hours=6, minutes=0)), # Bhutan Time
    "CAT" : timezone(timedelta(hours=2, minutes=0)), # Central Africa Time
    "CCT" : timezone(timedelta(hours=6, minutes=30)), # Cocos Islands Time
    "CDT" : timezone(-timedelta(hours=5, minutes=0)), # Central Daylight Time (North America)
    "CEST" : timezone(timedelta(hours=2, minutes=0)), # Central European Summer Time (Cf. HAEC)
    "CET" : timezone(timedelta(hours=1, minutes=0)), # Central European Time
    "CHADT" : timezone(timedelta(hours=13, minutes=45)), # Chatham Daylight Time
    "CHAST" : timezone(timedelta(hours=12, minutes=45)), # Chatham Standard Time
    "CHOT" : timezone(timedelta(hours=8, minutes=0)), # Choibalsan Standard Time
    "CHOST" : timezone(timedelta(hours=9, minutes=0)), # Choibalsan Summer Time
    "CHST" : timezone(timedelta(hours=10, minutes=0)), # Chamorro Standard Time
    "CHUT" : timezone(timedelta(hours=10, minutes=0)), # Chuuk Time
    "CIST" : timezone(-timedelta(hours=8, minutes=0)), # Clipperton Island Standard Time
    "CIT" : timezone(timedelta(hours=8, minutes=0)), # Central Indonesia Time
    "CKT" : timezone(-timedelta(hours=10, minutes=0)), # Cook Island Time
    "CLST" : timezone(-timedelta(hours=3, minutes=0)), # Chile Summer Time
    "CLT" : timezone(-timedelta(hours=4, minutes=0)), # Chile Standard Time
    "COST" : timezone(-timedelta(hours=4, minutes=0)), # Colombia Summer Time
    "COT" : timezone(-timedelta(hours=5, minutes=0)), # Colombia Time
    "CST" : timezone(-timedelta(hours=6, minutes=0)), # Central Standard Time (North America)
    "CT" : timezone(timedelta(hours=8, minutes=0)), # China Time
    "CVT" : timezone(-timedelta(hours=1, minutes=0)), # Cape Verde Time
    "CWST" : timezone(timedelta(hours=8, minutes=45)), # Central Western Standard Time (Australia) unofficial
    "CXT" : timezone(timedelta(hours=7, minutes=0)), # Christmas Island Time
    "DAVT" : timezone(timedelta(hours=7, minutes=0)), # Davis Time
    "DDUT" : timezone(timedelta(hours=10, minutes=0)), # Dumont d'Urville Time
    "DFT" : timezone(timedelta(hours=1, minutes=0)), # AIX-specific equivalent of Central European Time[NB 1]
    "EASST" : timezone(-timedelta(hours=5, minutes=0)), # Easter Island Summer Time
    "EAST" : timezone(-timedelta(hours=6, minutes=0)), # Easter Island Standard Time
    "EAT" : timezone(timedelta(hours=3, minutes=0)), # East Africa Time
    "ECT" : timezone(-timedelta(hours=4, minutes=0)), # Eastern Caribbean Time (does not recognise DST)
    "EDT" : timezone(-timedelta(hours=4, minutes=0)), # Eastern Daylight Time (North America)
    "EEST" : timezone(timedelta(hours=3, minutes=0)), # Eastern European Summer Time
    "EET" : timezone(timedelta(hours=2, minutes=0)), # Eastern European Time
    "EGST" : timezone(timedelta(hours=0, minutes=0)), # Eastern Greenland Summer Time
    "EGT" : timezone(-timedelta(hours=1, minutes=0)), # Eastern Greenland Time
    "EIT" : timezone(timedelta(hours=9, minutes=0)), # Eastern Indonesian Time
    "EST" : timezone(-timedelta(hours=5, minutes=0)), # Eastern Standard Time (North America)
    "FET" : timezone(timedelta(hours=3, minutes=0)), # Further-eastern European Time
    "FJT" : timezone(timedelta(hours=12, minutes=0)), # Fiji Time
    "FKST" : timezone(-timedelta(hours=3, minutes=0)), # Falkland Islands Summer Time
    "FKT" : timezone(-timedelta(hours=4, minutes=0)), # Falkland Islands Time
    "FNT" : timezone(-timedelta(hours=2, minutes=0)), # Fernando de Noronha Time
    "GALT" : timezone(-timedelta(hours=6, minutes=0)), # Galápagos Time
    "GAMT" : timezone(-timedelta(hours=9, minutes=0)), # Gambier Islands Time
    "GET" : timezone(timedelta(hours=4, minutes=0)), # Georgia Standard Time
    "GFT" : timezone(-timedelta(hours=3, minutes=0)), # French Guiana Time
    "GILT" : timezone(timedelta(hours=12, minutes=0)), # Gilbert Island Time
    "GIT" : timezone(-timedelta(hours=9, minutes=0)), # Gambier Island Time
    "GMT" : timezone(timedelta(hours=0, minutes=0)), # Greenwich Mean Time
    "GST" : timezone(-timedelta(hours=2, minutes=0)), # South Georgia and the South Sandwich Islands Time
    "GYT" : timezone(-timedelta(hours=4, minutes=0)), # Guyana Time
    "HDT" : timezone(-timedelta(hours=9, minutes=0)), # Hawaii–Aleutian Daylight Time
    "HAEC" : timezone(timedelta(hours=2, minutes=0)), # Heure Avancée d'Europe Centrale French-language name for CEST
    "HST" : timezone(-timedelta(hours=10, minutes=0)), # Hawaii–Aleutian Standard Time
    "HKT" : timezone(timedelta(hours=8, minutes=0)), # Hong Kong Time
    "HMT" : timezone(timedelta(hours=5, minutes=0)), # Heard and McDonald Islands Time
    "HOVST" : timezone(timedelta(hours=8, minutes=0)), # Hovd Summer Time (not used from 2017-present)
    "HOVT" : timezone(timedelta(hours=7, minutes=0)), # Hovd Time
    "ICT" : timezone(timedelta(hours=7, minutes=0)), # Indochina Time
    "IDLW" : timezone(-timedelta(hours=12, minutes=0)), # International Day Line West time zone
    "IDT" : timezone(timedelta(hours=3, minutes=0)), # Israel Daylight Time
    "IOT" : timezone(timedelta(hours=3, minutes=0)), # Indian Ocean Time
    "IRDT" : timezone(timedelta(hours=4, minutes=30)), # Iran Daylight Time
    "IRKT" : timezone(timedelta(hours=8, minutes=0)), # Irkutsk Time
    "IRST" : timezone(timedelta(hours=3, minutes=30)), # Iran Standard Time
    "IST" : timezone(timedelta(hours=5, minutes=30)), # Indian Standard Time
    "JST" : timezone(timedelta(hours=9, minutes=0)), # Japan Standard Time
    "KALT" : timezone(timedelta(hours=2, minutes=0)), # Kaliningrad Time
    "KGT" : timezone(timedelta(hours=6, minutes=0)), # Kyrgyzstan Time
    "KOST" : timezone(timedelta(hours=11, minutes=0)), # Kosrae Time
    "KRAT" : timezone(timedelta(hours=7, minutes=0)), # Krasnoyarsk Time
    "KST" : timezone(timedelta(hours=9, minutes=0)), # Korea Standard Time
    "LHST" : timezone(timedelta(hours=10, minutes=30)), # Lord Howe Standard Time
    "LINT" : timezone(timedelta(hours=14, minutes=0)), # Line Islands Time
    "MAGT" : timezone(timedelta(hours=12, minutes=0)), # Magadan Time
    "MART" : timezone(-timedelta(hours=9, minutes=30)), # Marquesas Islands Time
    "MAWT" : timezone(timedelta(hours=5, minutes=0)), # Mawson Station Time
    "MDT" : timezone(-timedelta(hours=6, minutes=0)), # Mountain Daylight Time (North America)
    "MET" : timezone(timedelta(hours=1, minutes=0)), # Middle European Time Same zone as CET
    "MEST" : timezone(timedelta(hours=2, minutes=0)), # Middle European Summer Time Same zone as CEST
    "MHT" : timezone(timedelta(hours=12, minutes=0)), # Marshall Islands Time
    "MIST" : timezone(timedelta(hours=11, minutes=0)), # Macquarie Island Station Time
    "MIT" : timezone(-timedelta(hours=9, minutes=30)), # Marquesas Islands Time
    "MMT" : timezone(timedelta(hours=6, minutes=30)), # Myanmar Standard Time
    "MSK" : timezone(timedelta(hours=3, minutes=0)), # Moscow Time
    "MST" : timezone(timedelta(hours=8, minutes=0)), # Malaysia Standard Time
    "MUT" : timezone(timedelta(hours=4, minutes=0)), # Mauritius Time
    "MVT" : timezone(timedelta(hours=5, minutes=0)), # Maldives Time
    "MYT" : timezone(timedelta(hours=8, minutes=0)), # Malaysia Time
    "NCT" : timezone(timedelta(hours=11, minutes=0)), # New Caledonia Time
    "NDT" : timezone(-timedelta(hours=2, minutes=30)), # Newfoundland Daylight Time
    "NFT" : timezone(timedelta(hours=11, minutes=0)), # Norfolk Island Time
    "NOVT" : timezone(timedelta(hours=7, minutes=0)), # Novosibirsk Time [9]
    "NPT" : timezone(timedelta(hours=5, minutes=45)), # Nepal Time
    "NST" : timezone(-timedelta(hours=3, minutes=30)), # Newfoundland Standard Time
    "NT" : timezone(-timedelta(hours=3, minutes=30)), # Newfoundland Time
    "NUT" : timezone(-timedelta(hours=11, minutes=0)), # Niue Time
    "NZDT" : timezone(timedelta(hours=13, minutes=0)), # New Zealand Daylight Time
    "NZST" : timezone(timedelta(hours=12, minutes=0)), # New Zealand Standard Time
    "OMST" : timezone(timedelta(hours=6, minutes=0)), # Omsk Time
    "ORAT" : timezone(timedelta(hours=5, minutes=0)), # Oral Time
    "PDT" : timezone(-timedelta(hours=7, minutes=0)), # Pacific Daylight Time (North America)
    "PET" : timezone(-timedelta(hours=5, minutes=0)), # Peru Time
    "PETT" : timezone(timedelta(hours=12, minutes=0)), # Kamchatka Time
    "PGT" : timezone(timedelta(hours=10, minutes=0)), # Papua New Guinea Time
    "PHOT" : timezone(timedelta(hours=13, minutes=0)), # Phoenix Island Time
    "PHT" : timezone(timedelta(hours=8, minutes=0)), # Philippine Time
    "PKT" : timezone(timedelta(hours=5, minutes=0)), # Pakistan Standard Time
    "PMDT" : timezone(-timedelta(hours=2, minutes=0)), # Saint Pierre and Miquelon Daylight Time
    "PMST" : timezone(-timedelta(hours=3, minutes=0)), # Saint Pierre and Miquelon Standard Time
    "PONT" : timezone(timedelta(hours=11, minutes=0)), # Pohnpei Standard Time
    "PST" : timezone(-timedelta(hours=8, minutes=0)), # Pacific Standard Time (North America)
    "PYST" : timezone(-timedelta(hours=3, minutes=0)), # Paraguay Summer Time[10]
    "PYT" : timezone(-timedelta(hours=4, minutes=0)), # Paraguay Time[11]
    "RET" : timezone(timedelta(hours=4, minutes=0)), # Réunion Time
    "ROTT" : timezone(-timedelta(hours=3, minutes=0)), # Rothera Research Station Time
    "SAKT" : timezone(timedelta(hours=11, minutes=0)), # Sakhalin Island Time
    "SAMT" : timezone(timedelta(hours=4, minutes=0)), # Samara Time
    "SAST" : timezone(timedelta(hours=2, minutes=0)), # South African Standard Time
    "SBT" : timezone(timedelta(hours=11, minutes=0)), # Solomon Islands Time
    "SCT" : timezone(timedelta(hours=4, minutes=0)), # Seychelles Time
    "SDT" : timezone(-timedelta(hours=10, minutes=0)), # Samoa Daylight Time
    "SGT" : timezone(timedelta(hours=8, minutes=0)), # Singapore Time
    "SLST" : timezone(timedelta(hours=5, minutes=30)), # Sri Lanka Standard Time
    "SRET" : timezone(timedelta(hours=11, minutes=0)), # Srednekolymsk Time
    "SRT" : timezone(-timedelta(hours=3, minutes=0)), # Suriname Time
    "SST" : timezone(-timedelta(hours=11, minutes=0)), # Samoa Standard Time
    "SYOT" : timezone(timedelta(hours=3, minutes=0)), # Showa Station Time
    "TAHT" : timezone(-timedelta(hours=10, minutes=0)), # Tahiti Time
    "THA" : timezone(timedelta(hours=7, minutes=0)), # Thailand Standard Time
    "TFT" : timezone(timedelta(hours=5, minutes=0)), # French Southern and Antarctic Time[12]
    "TJT" : timezone(timedelta(hours=5, minutes=0)), # Tajikistan Time
    "TKT" : timezone(timedelta(hours=13, minutes=0)), # Tokelau Time
    "TLT" : timezone(timedelta(hours=9, minutes=0)), # Timor Leste Time
    "TMT" : timezone(timedelta(hours=5, minutes=0)), # Turkmenistan Time
    "TRT" : timezone(timedelta(hours=3, minutes=0)), # Turkey Time
    "TOT" : timezone(timedelta(hours=13, minutes=0)), # Tonga Time
    "TVT" : timezone(timedelta(hours=12, minutes=0)), # Tuvalu Time
    "ULAST" : timezone(timedelta(hours=9, minutes=0)), # Ulaanbaatar Summer Time
    "ULAT" : timezone(timedelta(hours=8, minutes=0)), # Ulaanbaatar Standard Time
    "UTC" : timezone(timedelta(hours=0, minutes=0)), # Coordinated Universal Time
    "UYST" : timezone(-timedelta(hours=2, minutes=0)), # Uruguay Summer Time
    "UYT" : timezone(-timedelta(hours=3, minutes=0)), # Uruguay Standard Time
    "UZT" : timezone(timedelta(hours=5, minutes=0)), # Uzbekistan Time
    "VET" : timezone(-timedelta(hours=4, minutes=0)), # Venezuelan Standard Time
    "VLAT" : timezone(timedelta(hours=10, minutes=0)), # Vladivostok Time
    "VOLT" : timezone(timedelta(hours=4, minutes=0)), # Volgograd Time
    "VOST" : timezone(timedelta(hours=6, minutes=0)), # Vostok Station Time
    "VUT" : timezone(timedelta(hours=11, minutes=0)), # Vanuatu Time
    "WAKT" : timezone(timedelta(hours=12, minutes=0)), # Wake Island Time
    "WAST" : timezone(timedelta(hours=2, minutes=0)), # West Africa Summer Time
    "WAT" : timezone(timedelta(hours=1, minutes=0)), # West Africa Time
    "WEST" : timezone(timedelta(hours=1, minutes=0)), # Western European Summer Time
    "WET" : timezone(timedelta(hours=0, minutes=0)), # Western European Time
    "WIT" : timezone(timedelta(hours=7, minutes=0)), # Western Indonesian Time
    "WST" : timezone(timedelta(hours=8, minutes=0)), # Western Standard Time
    "YAKT" : timezone(timedelta(hours=9, minutes=0)), # Yakutsk Time
    "YEKT" : timezone(timedelta(hours=5, minutes=0)), # Yekaterinburg Time
}
# pylint: enable=line-too-long

def get_timezone_from_abbr(timezone_abbreviation: str) -> timezone:
    '''parse input string (format is TIMEZONE+/-HOURS[:MINUTES]) and returns according timezone'''
    if '+' in timezone_abbreviation:
        [zone, offset] = timezone_abbreviation.split('+')
        zone = TIMEZONES[zone]
        offset = get_datetime_from_strtime(offset)
        zone = timezone(zone.utcoffset(None) + timedelta(hours=offset.hour, minutes=offset.minute))
        return zone

    if '-' in timezone_abbreviation:
        [zone, offset] = timezone_abbreviation.split('-')
        zone = TIMEZONES[zone]
        offset = get_datetime_from_strtime(offset)
        zone = timezone(zone.utcoffset(None) - timedelta(hours=offset.hour, minutes=offset.minute))
        return zone

    if '−' in timezone_abbreviation:
        [zone, offset] = timezone_abbreviation.split('−')
        zone = TIMEZONES[zone]
        offset = get_datetime_from_strtime(offset)
        zone = timezone(zone.utcoffset(None) - timedelta(hours=offset.hour, minutes=offset.minute))
        return zone
    return TIMEZONES[timezone_abbreviation]

TimezoneSetup = namedtuple('TimezoneSetup', ['Abbreviation', 'Offset', 'Name'])

def get_datetime_from_strtime(time: str) -> datetime:
    '''parse input string and returns datetime with hours and minutes from string'''
    time_format = '%H'
    if ':' in time:
        time_format = '%H:%M'
    return datetime.strptime(time, time_format)


def read_timezones_file(file_name, file_encoding='utf-8') -> [TimezoneSetup]:
    '''reads file with list of timezones and converts to the array for TIMEZONES dict'''
    existing_zones = set()
    result = []
    with open(file_name, encoding=file_encoding) as tz_file:
        data = tz_file.read()
        data = data.splitlines()
        for line in data:
            line = line.split('\t')
            abbr = line[0]
            name = line[1]
            offset = line[2]

            if "UTC" not in offset:
                raise Exception("No UTC")
            if offset.count('UTC') > 1:
                print(f'Skipping {name}')
                continue

            if '+' in offset:
                offset = offset.split('+')[1]
                time = get_datetime_from_strtime(offset)
                offset = f'timezone(timedelta(hours={time.hour}, minutes={time.minute}))'
            elif '−' in offset:
                offset = offset.split('−')[1]
                time = get_datetime_from_strtime(offset)
                offset = f'timezone(-timedelta(hours={time.hour}, minutes={time.minute}))'
            elif '±' in offset:
                offset = 'timezone(timedelta(hours=0, minutes=0))'

            if abbr in existing_zones:
                print(f'{abbr} already exists!')
                continue

            existing_zones.add(abbr)
            result.append(TimezoneSetup(abbr, offset, name))
    return result

if __name__ == "__main__":
    RESULT = read_timezones_file('timezones.temp')
    with open('setup.temp', "w", encoding='utf-8') as setup_file:
        print('Start writing to timezones file')
        for timezone in RESULT:
            setup_file.write(f'"{timezone.Abbreviation}" : {timezone.Offset}, # {timezone.Name}\n')
        print('Finished')
