import requests
from bs4 import BeautifulSoup
import csv

# Name transform map, to keep consistent names with the provided training data
name_map = {
    'Manchester City': 'Man City',
    'Arsenal': 'Arsenal',
    'Liverpool': 'Liverpool',
    'Manchester United': 'Man United',
    'Tottenham Hotspur': 'Tottenham',
    'Aston Villa': 'Aston Villa',
    'Chelsea': 'Chelsea',
    'Newcastle United': 'Newcastle',
    'West Ham United': 'West Ham',
    'Everton': 'Everton',
    'Nottingham Forest': "Nott'm Forest",
    'Brighton & Hove Albion': 'Brighton',
    'Wolverhampton Wanderers': 'Wolves',
    'Fulham': 'Fulham',
    'Crystal Palace': 'Crystal Palace',
    'Brentford': 'Brentford',
    'AFC Bournemouth': 'Bournemouth',
    'Burnley': 'Burnley',
    'Cardiff City': 'Cardiff',
    'Huddersfield Town': 'Huddersfield',
    'Hull City': 'Hull',
    'Leeds United': 'Leeds',
    'Leicester City': 'Leicester',
    'Luton Town': 'Luton',
    'Middlesbrough': 'Middlesbrough',
    'Norwich City': 'Norwich',
    'Queens Park Rangers': 'QPR',
    'Reading': 'Reading',
    'Sheffield United': 'Sheffield United',
    'Southampton': 'Southampton',
    'Stoke City': 'Stoke',
    'Sunderland': 'Sunderland',
    'Swansea City': 'Swansea',
    'Watford': 'Watford',
    'West Bromwich Albion': 'West Brom',
    'Wigan Athletic': 'Wigan'
}
    
# Function to scrape team data for English Premier League
def scrape_premier_league_teams(years):
    with open('epl-teams.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Team', 'Year', 'OA', 'AT', 'MD', 'DF', 'CW']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for r, year in years:
            url = f"https://sofifa.com/teams?type=all&lg%5B0%5D=13&r={r}&set=true"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
            }
        
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                team_table = soup.find('table').find('tbody')
        
                if team_table:
        
                        rows = team_table.find_all('tr')
                        for row in rows:
                            team_info = row.find_all('td')
                            
                            team_name = team_info[1].find('a').text.strip()
                            oa = team_info[3].text.strip() # overall score
                            at = team_info[4].text.strip() # attack
                            md = team_info[5].text.strip() # midfield
                            df = team_info[6].text.strip() # defence
                            cw = team_info[7].text.strip() # club worth
        
                            writer.writerow({'Team': name_map[team_name], 'Year': year, 'OA': oa, 'AT': at, 'MD': md, 'DF': df, 'CW': cw})
                else:
                    print("Team table not found on the page.")
            else:
                print("Failed to retrieve the page.")


if __name__=='__main__':
    # Call the function to start scraping team data
    years = [('240016', 2024), ('230054', 2023), ('220069', 2022), ('210064', 2021), ('200061', 2020), ('190075', 2019), ('180084', 2018), ('170099', 2017), ('160058', 2016), ('150059', 2015), ('140052', 2014), ('130034', 2013)]
    scrape_premier_league_teams(years)