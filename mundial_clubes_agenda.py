import datetime

def generate_ics_content(matches):
    ics_header = """BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Google Inc//Google Calendar 1.0//EN
X-WR-CALNAME:Mundial de Clubes 2025
X-WR-TIMEZONE:America/Sao_Paulo
BEGIN:VTIMEZONE
TZID:America/Sao_Paulo
X-LIC-LOCATION:America/Sao_Paulo
BEGIN:STANDARD
TZOFFSETFROM:-0200
TZOFFSETTO:-0300
TZNAME:BRT
DTSTART:19700101T000000
END:STANDARD
END:VTIMEZONE
"""
    ics_footer = "END:VCALENDAR"
    events = []

    for match in matches:
        # Assuming match['date'] is in 'DD de Mês' format and match['time_brasilia'] can be 'HHh' or 'HH:MM'
        # Convert month names
        month_map = {
            'junho': 6, 'julho': 7
        }

        day = int(match['date'].split(' de ')[0])
        month_name = match['date'].split(' de ')[1]
        month = month_map[month_name]
        year = 2025 # All matches are in 2025

        # --- CORREÇÃO AQUI ---
        # Handle both 'HHh' and 'HH:MM' formats for time
        time_str = match['time_brasilia']
        if 'h' in time_str:
            hour = int(time_str.split('h')[0])
            minute = 0
        elif ':' in time_str:
            hour = int(time_str.split(':')[0])
            minute = int(time_str.split(':')[1])
        else:
            # Fallback or error if format is unexpected
            print(f"Aviso: Formato de hora inesperado para {time_str}. Pulando este evento.")
            continue
        # --- FIM DA CORREÇÃO ---
        
        # Create datetime objects for start and end (assuming 2-hour match duration)
        # Using pytz to correctly handle timezone awareness for Google Calendar
        # Note: Google Calendar handles TZID well, but direct datetime objects benefit from awareness.
        # For this script, the string formatting with TZID is key for the ICS file.
        
        # The timezone offset for Brasília is -03:00 (BRT)
        start_dt = datetime.datetime(year, month, day, hour, minute, 0)
        
        # Manually create a timezone for -03:00 (BRT) if not using a library like pytz
        # Using a fixed offset for simplicity as TZID is handled in ICS header
        # However, for correct local calculations within Python, timezone objects are better.
        # For the purpose of generating the string, the datetime object works.
        
        # It's important that DTSTART/DTEND in ICS specify TZID, which is already present.
        # The actual datetime object in Python can be naive, as the TZID handles the interpretation.
        
        end_dt = start_dt + datetime.timedelta(hours=2) # Assuming 2-hour duration

        # Format for .ics
        dtstart = start_dt.strftime("%Y%m%dT%H%M%S")
        dtend = end_dt.strftime("%Y%m%dT%H%M%S")

        summary = f"{match['team1']} x {match['team2']}"
        location = match['venue']
        description = f"Mundial de Clubes FIFA 2025 - {match['stage']}"

        event = f"""BEGIN:VEVENT
UID:{start_dt.strftime("%Y%m%d%H%M%S")}-{match['team1'].replace(' ', '')}-{match['team2'].replace(' ', '')}@google.com
DTSTART;TZID=America/Sao_Paulo:{dtstart}
DTEND;TZID=America/Sao_Paulo:{dtend}
SUMMARY:{summary}
LOCATION:{location}
DESCRIPTION:{description}
END:VEVENT"""
        events.append(event)

    return ics_header + "\n".join(events) + "\n" + ics_footer

# Data extracted from the FIFA website, focusing on Brasília times
# Note: LAFC/Club América is represented as 'LAFC/América' for simplicity in teams
matches_data = [
    {'date': '14 de junho', 'time_brasilia': '21h', 'team1': 'Al Ahly FC', 'team2': 'Inter Miami CF', 'venue': 'Estádio Hard Rock, Miami', 'stage': 'Fase de Grupos'},
    {'date': '15 de junho', 'time_brasilia': '13h', 'team1': 'FC Bayern München', 'team2': 'Auckland City FC', 'venue': 'Estádio TQL, Cincinnati', 'stage': 'Fase de Grupos'},
    {'date': '15 de junho', 'time_brasilia': '16h', 'team1': 'Paris Saint-Germain', 'team2': 'Atlético de Madrid', 'venue': 'Estádio Rose Bowl, Los Angeles', 'stage': 'Fase de Grupos'},
    {'date': '15 de junho', 'time_brasilia': '19h', 'team1': 'SE Palmeiras', 'team2': 'FC Porto', 'venue': 'Estádio MetLife, Nova York-Nova Jersey', 'stage': 'Fase de Grupos'},
    {'date': '15 de junho', 'time_brasilia': '23h', 'team1': 'Botafogo', 'team2': 'Seattle Sounders FC', 'venue': 'Lumen Field, Seattle', 'stage': 'Fase de Grupos'},
    {'date': '16 de junho', 'time_brasilia': '16h', 'team1': 'Chelsea FC', 'team2': 'Los Angeles FC/Club América', 'venue': 'Estádio Mercedes-Benz, Atlanta', 'stage': 'Fase de Grupos'},
    {'date': '16 de junho', 'time_brasilia': '19h', 'team1': 'CA Boca Juniors', 'team2': 'SL Benfica', 'venue': 'Estádio Hard Rock, Miami', 'stage': 'Fase de Grupos'},
    {'date': '16 de junho', 'time_brasilia': '22h', 'team1': 'CR Flamengo', 'team2': 'Espérance Sportive de Tunis', 'venue': 'Lincoln Financial Field, Filadélfia', 'stage': 'Fase de Grupos'},
    {'date': '17 de junho', 'time_brasilia': '13h', 'team1': 'Fluminense FC', 'team2': 'Borussia Dortmund', 'venue': 'Estádio MetLife, Nova York-Nova Jersey', 'stage': 'Fase de Grupos'},
    {'date': '17 de junho', 'time_brasilia': '16h', 'team1': 'CA River Plate', 'team2': 'Urawa Red Diamonds', 'venue': 'Lumen Field, Seattle', 'stage': 'Fase de Grupos'},
    {'date': '17 de junho', 'time_brasilia': '19h', 'team1': 'Ulsan HD', 'team2': 'Mamelodi Sundowns FC', 'venue': 'Estádio Inter&Co, Orlando', 'stage': 'Fase de Grupos'},
    {'date': '17 de junho', 'time_brasilia': '22h', 'team1': 'CF Monterrey', 'team2': 'FC Internazionale Milano', 'venue': 'Estádio Rose Bowl, Los Angeles', 'stage': 'Fase de Grupos'},
    {'date': '18 de junho', 'time_brasilia': '13h', 'team1': 'Manchester City', 'team2': 'Wydad AC', 'venue': 'Lincoln Financial Field, Filadélfia', 'stage': 'Fase de Grupos'},
    {'date': '18 de junho', 'time_brasilia': '16h', 'team1': 'Real Madrid C. F.', 'team2': 'Al Hilal', 'venue': 'Estádio Hard Rock, Miami', 'stage': 'Fase de Grupos'},
    {'date': '18 de junho', 'time_brasilia': '19h', 'team1': 'CF Pachuca', 'team2': 'FC Salzburg', 'venue': 'Estádio TQL, Cincinnati', 'stage': 'Fase de Grupos'},
    {'date': '18 de junho', 'time_brasilia': '22h', 'team1': 'Al Ain FC', 'team2': 'Juventus FC', 'venue': 'Audi Field, Washington, D.C.', 'stage': 'Fase de Grupos'},
    {'date': '19 de junho', 'time_brasilia': '13h', 'team1': 'SE Palmeiras', 'team2': 'Al Ahly FC', 'venue': 'Estádio MetLife, Nova York-Nova Jersey', 'stage': 'Fase de Grupos'},
    {'date': '19 de junho', 'time_brasilia': '16h', 'team1': 'Inter Miami CF', 'team2': 'FC Porto', 'venue': 'Estádio Mercedes-Benz, Atlanta', 'stage': 'Fase de Grupos'},
    {'date': '19 de junho', 'time_brasilia': '19h', 'team1': 'Seattle Sounders FC', 'team2': 'Atlético de Madrid', 'venue': 'Lumen Field, Seattle', 'stage': 'Fase de Grupos'},
    {'date': '19 de junho', 'time_brasilia': '22h', 'team1': 'Paris Saint-Germain', 'team2': 'Botafogo', 'venue': 'Estádio Rose Bowl, Los Angeles', 'stage': 'Fase de Grupos'},
    {'date': '20 de junho', 'time_brasilia': '13h', 'team1': 'SL Benfica', 'team2': 'Auckland City FC', 'venue': 'Estádio Inter&Co, Orlando', 'stage': 'Fase de Grupos'},
    {'date': '20 de junho', 'time_brasilia': '15h', 'team1': 'CR Flamengo', 'team2': 'Chelsea FC', 'venue': 'Lincoln Financial Field, Filadélfia', 'stage': 'Fase de Grupos'},
    {'date': '20 de junho', 'time_brasilia': '19h', 'team1': 'Los Angeles FC/Club América', 'team2': 'Espérance Sportive de Tunis', 'venue': 'GEODIS Park, Nashville', 'stage': 'Fase de Grupos'},
    {'date': '20 de junho', 'time_brasilia': '22h', 'team1': 'FC Bayern München', 'team2': 'CA Boca Juniors', 'venue': 'Estádio Hard Rock, Miami', 'stage': 'Fase de Grupos'},
    {'date': '21 de junho', 'time_brasilia': '13h', 'team1': 'Mamelodi Sundowns FC', 'team2': 'Borussia Dortmund', 'venue': 'Estádio TQL, Cincinnati', 'stage': 'Fase de Grupos'},
    {'date': '21 de junho', 'time_brasilia': '16h', 'team1': 'FC Internazionale Milano', 'team2': 'Urawa Red Diamonds', 'venue': 'Lumen Field, Seattle', 'stage': 'Fase de Grupos'},
    {'date': '21 de junho', 'time_brasilia': '19h', 'team1': 'Fluminense FC', 'team2': 'Ulsan HD', 'venue': 'Estádio MetLife, Nova York-Nova Jersey', 'stage': 'Fase de Grupos'},
    {'date': '21 de junho', 'time_brasilia': '22h', 'team1': 'CA River Plate', 'team2': 'CF Monterrey', 'venue': 'Estádio Rose Bowl, Los Angeles', 'stage': 'Fase de Grupos'},
    {'date': '22 de junho', 'time_brasilia': '13h', 'team1': 'Juventus FC', 'team2': 'Wydad AC', 'venue': 'Lincoln Financial Field, Filadélfia', 'stage': 'Fase de Grupos'},
    {'date': '22 de junho', 'time_brasilia': '16h', 'team1': 'Real Madrid C. F.', 'team2': 'CF Pachuca', 'venue': 'Estádio Bank of America, Charlotte', 'stage': 'Fase de Grupos'},
    {'date': '22 de junho', 'time_brasilia': '19h', 'team1': 'FC Salzburg', 'team2': 'Al Hilal', 'venue': 'Audi Field, Washington, D.C.', 'stage': 'Fase de Grupos'},
    {'date': '22 de junho', 'time_brasilia': '22h', 'team1': 'Manchester City', 'team2': 'Al Ain FC', 'venue': 'Estádio Mercedes-Benz, Atlanta', 'stage': 'Fase de Grupos'},
    {'date': '23 de junho', 'time_brasilia': '16h', 'team1': 'Seattle Sounders FC', 'team2': 'Paris Saint-Germain', 'venue': 'Lumen Field, Seattle', 'stage': 'Fase de Grupos'},
    {'date': '23 de junho', 'time_brasilia': '16h', 'team1': 'Atlético de Madrid', 'team2': 'Botafogo', 'venue': 'Estádio Rose Bowl, Los Angeles', 'stage': 'Fase de Grupos'},
    {'date': '23 de junho', 'time_brasilia': '22h', 'team1': 'Inter Miami CF', 'team2': 'SE Palmeiras', 'venue': 'Estádio Hard Rock, Miami', 'stage': 'Fase de Grupos'},
    {'date': '23 de junho', 'time_brasilia': '22h', 'team1': 'FC Porto', 'team2': 'Al Ahly FC', 'venue': 'Estádio MetLife, Nova York-Nova Jersey', 'stage': 'Fase de Grupos'},
    {'date': '24 de junho', 'time_brasilia': '16h', 'team1': 'Auckland City FC', 'team2': 'CA Boca Juniors', 'venue': 'GEODIS Park, Nashville', 'stage': 'Fase de Grupos'},
    {'date': '24 de junho', 'time_brasilia': '16h', 'team1': 'SL Benfica', 'team2': 'FC Bayern München', 'venue': 'Estádio Bank of America, Charlotte', 'stage': 'Fase de Grupos'},
    {'date': '24 de junho', 'time_brasilia': '22h', 'team1': 'Los Angeles FC/Club América', 'team2': 'CR Flamengo', 'venue': 'Camping World Stadium, Orlando', 'stage': 'Fase de Grupos'},
    {'date': '24 de junho', 'time_brasilia': '22h', 'team1': 'Espérance Sportive de Tunis', 'team2': 'Chelsea FC', 'venue': 'Lincoln Financial Field, Filadélfia', 'stage': 'Fase de Grupos'},
    {'date': '25 de junho', 'time_brasilia': '16h', 'team1': 'Borussia Dortmund', 'team2': 'Ulsan HD', 'venue': 'Estádio TQL, Cincinnati', 'stage': 'Fase de Grupos'},
    {'date': '25 de junho', 'time_brasilia': '16h', 'team1': 'Mamelodi Sundowns FC', 'team2': 'Fluminense FC', 'venue': 'Estádio Hard Rock, Miami', 'stage': 'Fase de Grupos'},
    {'date': '25 de junho', 'time_brasilia': '22h', 'team1': 'FC Internazionale Milano', 'team2': 'CA River Plate', 'venue': 'Lumen Field, Seattle', 'stage': 'Fase de Grupos'},
    {'date': '25 de junho', 'time_brasilia': '22h', 'team1': 'Urawa Red Diamonds', 'team2': 'CF Monterrey', 'venue': 'Estádio Rose Bowl, Los Angeles', 'stage': 'Fase de Grupos'},
    {'date': '26 de junho', 'time_brasilia': '16h', 'team1': 'Juventus FC', 'team2': 'Manchester City', 'venue': 'Camping World Stadium, Orlando', 'stage': 'Fase de Grupos'},
    {'date': '26 de junho', 'time_brasilia': '16h', 'team1': 'Wydad AC', 'team2': 'Al Ain FC', 'venue': 'Audi Field, Washington, D.C.', 'stage': 'Fase de Grupos'},
    {'date': '26 de junho', 'time_brasilia': '22h', 'team1': 'Al Hilal', 'team2': 'CF Pachuca', 'venue': 'GEODIS Park, Nashville', 'stage': 'Fase de Grupos'},
    {'date': '26 de junho', 'time_brasilia': '22h', 'team1': 'FC Salzburg', 'team2': 'Real Madrid C. F.', 'venue': 'Lincoln Financial Field, Filadélfia', 'stage': 'Fase de Grupos'},
    # Oitavas de final (com placeholders para equipes ainda não definidas)
    {'date': '28 de junho', 'time_brasilia': '12:00', 'team1': 'Vencedor Grupo A', 'team2': 'Segundo Grupo B', 'venue': 'Lincoln Financial Field, Filadélfia', 'stage': 'Oitavas de Final'},
    {'date': '28 de junho', 'time_brasilia': '16:00', 'team1': 'Vencedor Grupo C', 'team2': 'Segundo Grupo D', 'venue': 'Estádio Bank of America, Charlotte', 'stage': 'Oitavas de Final'},
    {'date': '29 de junho', 'time_brasilia': '12:00', 'team1': 'Vencedor Grupo B', 'team2': 'Segundo Grupo A', 'venue': 'Estádio Mercedes-Benz, Atlanta', 'stage': 'Oitavas de Final'},
    {'date': '29 de junho', 'time_brasilia': '16:00', 'team1': 'Vencedor Grupo D', 'team2': 'Segundo Grupo C', 'venue': 'Estádio Hard Rock, Miami', 'stage': 'Oitavas de Final'},
    {'date': '30 de junho', 'time_brasilia': '15:00', 'team1': 'Vencedor Grupo E', 'team2': 'Segundo Grupo F', 'venue': 'Estádio Bank of America, Charlotte', 'stage': 'Oitavas de Final'},
    {'date': '30 de junho', 'time_brasilia': '21:00', 'team1': 'Vencedor Grupo G', 'team2': 'Segundo Grupo H', 'venue': 'Camping World Stadium, Orlando', 'stage': 'Oitavas de Final'},
    {'date': '1 de julho', 'time_brasilia': '15:00', 'team1': 'Vencedor Grupo H', 'team2': 'Segundo Grupo G', 'venue': 'Estádio Hard Rock, Miami', 'stage': 'Oitavas de Final'},
    {'date': '1 de julho', 'time_brasilia': '21:00', 'team1': 'Vencedor Grupo F', 'team2': 'Segundo Grupo E', 'venue': 'Estádio Mercedes-Benz, Atlanta', 'stage': 'Oitavas de Final'},
    # Quartas de final
    {'date': '4 de julho', 'time_brasilia': '15:00', 'team1': 'Vencedor Jogo 53', 'team2': 'Vencedor Jogo 54', 'venue': 'Camping World Stadium, Orlando', 'stage': 'Quartas de Final'},
    {'date': '4 de julho', 'time_brasilia': '21:00', 'team1': 'Vencedor do jogo', 'team2': 'Vencedor do jogo 50', 'venue': 'Lincoln Financial Field, Filadélfia', 'stage': 'Quartas de Final'}, # 'Vencedor do jogo' precisa de ajuste se for um placeholder genérico
    {'date': '5 de julho', 'time_brasilia': '12:00', 'team1': 'Vencedor Jogo 51', 'team2': 'Vencedor Jogo 52', 'venue': 'Estádio Mercedes-Benz, Atlanta', 'stage': 'Quartas de Final'},
    {'date': '5 de julho', 'time_brasilia': '16:00', 'team1': 'Vencedor Jogo 55', 'team2': 'Vencedor Jogo 56', 'venue': 'Estádio MetLife, Nova York-Nova Jersey', 'stage': 'Quartas de Final'},
    # Semifinais
    {'date': '8 de julho', 'time_brasilia': '15:00', 'team1': 'Vencedor Jogo 57', 'team2': 'Vencedor Jogo 58', 'venue': 'Estádio MetLife, Nova York-Nova Jersey', 'stage': 'Semifinal'},
    {'date': '9 de julho', 'time_brasilia': '15:00', 'team1': 'Vencedor Jogo 59', 'team2': 'Vencedor Jogo 60', 'venue': 'Estádio MetLife, Nova York-Nova Jersey', 'stage': 'Semifinal'},
    # Final
    {'date': '13 de julho', 'time_brasilia': '15:00', 'team1': 'Vencedor Jogo 61', 'team2': 'Vencedor Jogo 62', 'venue': 'Estádio MetLife, Nova York-Nova Jersey', 'stage': 'Final'}
]

ics_output = generate_ics_content(matches_data)
print(ics_output)