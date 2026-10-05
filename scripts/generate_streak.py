#!/usr/bin/env python3
import urllib.request
import re
from datetime import datetime, timedelta
import os

def generate_svg():
    username = 'johankvn22'
    all_days = {}
    current_year = datetime.now().year
    
    for year in range(2022, current_year + 1):
        url = f'https://github.com/users/{username}/contributions?from={year}-01-01&to={year}-12-31'
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
        try:
            html = urllib.request.urlopen(req, timeout=20).read().decode('utf-8')
            tooltips = dict(re.findall(r'for=\"([^\"]+)\"[^>]*>([0-9,]+|No)\s+contribution', html))
            days = re.findall(r'data-date=\"([0-9]{4}-[0-9]{2}-[0-9]{2})\" id=\"([^\"]+)\"', html)
            for d_str, comp_id in days:
                cnt_str = tooltips.get(comp_id, '0')
                cnt = 0 if cnt_str == 'No' else int(cnt_str.replace(',', ''))
                all_days[d_str] = cnt
        except Exception as e:
            print(f'Error fetching {year}: {e}')

    total_contribs = sum(all_days.values())
    active_days = sorted([datetime.strptime(d, '%Y-%m-%d').date() for d, c in all_days.items() if c > 0])
    
    first_date_str = active_days[0].strftime('%b %-d, %Y') if active_days else 'Jun 3, 2022'
    date_range_str = f'{first_date_str} - Present'
    
    # Streaks calculation
    max_streak = 0
    max_streak_range = (None, None)
    cur_run = 0
    run_start = None
    prev = None
    
    for d in active_days:
        if prev is None or d == prev + timedelta(days=1):
            if cur_run == 0:
                run_start = d
            cur_run += 1
        else:
            if cur_run > max_streak:
                max_streak = cur_run
                max_streak_range = (run_start, prev)
            cur_run = 1
            run_start = d
        prev = d
        
    if cur_run > max_streak:
        max_streak = cur_run
        max_streak_range = (run_start, prev)
        
    longest_streak_range_str = f'{max_streak_range[0].strftime("%b %-d, %Y")} - {max_streak_range[1].strftime("%b %-d, %Y")}' if max_streak_range[0] else ''
    
    # Current streak
    today = datetime.now().date()
    check_d = today
    if all_days.get(check_d.strftime('%Y-%m-%d'), 0) == 0:
        check_d = today - timedelta(days=1)
        
    curr_streak = 0
    curr_start = check_d
    while all_days.get(check_d.strftime('%Y-%m-%d'), 0) > 0:
        curr_streak += 1
        curr_start = check_d
        check_d -= timedelta(days=1)
        
    if curr_streak == 0:
        curr_streak_range_str = today.strftime('%b %-d')
    elif curr_start == today:
        curr_streak_range_str = today.strftime('%b %-d')
    else:
        curr_streak_range_str = f'{curr_start.strftime("%b %-d")} - {today.strftime("%b %-d")}'
        
    total_str = f'{total_contribs:,}'
    
    svg_content = f'''<svg xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'
            style='isolation: isolate' viewBox='0 0 495 195' width='495px' height='195px' direction='ltr'>
    <style>
        @keyframes currstreak {{
            0% {{ font-size: 3px; opacity: 0.2; }}
            80% {{ font-size: 34px; opacity: 1; }}
            100% {{ font-size: 28px; opacity: 1; }}
        }}
        @keyframes fadein {{
            0% {{ opacity: 0; }}
            100% {{ opacity: 1; }}
        }}
    </style>
    <defs>
        <clipPath id='outer_rectangle'>
            <rect width='495' height='195' rx='4.5'/>
        </clipPath>
        <mask id='mask_out_ring_behind_fire'>
            <rect width='495' height='195' fill='white'/>
            <ellipse id='mask-ellipse' cx='247.5' cy='32' rx='13' ry='18' fill='black'/>
        </mask>
    </defs>
    <g clip-path='url(#outer_rectangle)'>
        <g style='isolation: isolate'>
            <rect stroke='#000000' stroke-opacity='0' fill='#FFFEFE' rx='4.5' x='0.5' y='0.5' width='494' height='194'/>
        </g>
        <g style='isolation: isolate'>
            <line x1='165' y1='28' x2='165' y2='170' vector-effect='non-scaling-stroke' stroke-width='1' stroke='#E4E2E2' stroke-linejoin='miter' stroke-linecap='square' stroke-miterlimit='3'/>
            <line x1='330' y1='28' x2='330' y2='170' vector-effect='non-scaling-stroke' stroke-width='1' stroke='#E4E2E2' stroke-linejoin='miter' stroke-linecap='square' stroke-miterlimit='3'/>
        </g>
        <g style='isolation: isolate'>
            <!-- Total Contributions big number -->
            <g transform='translate(82.5, 48)'>
                <text x='0' y='32' stroke-width='0' text-anchor='middle' fill='#151515' stroke='none' font-family='"Segoe UI", Ubuntu, sans-serif' font-weight='700' font-size='28px' font-style='normal' style='opacity: 0; animation: fadein 0.5s linear forwards 0.6s'>
                    {total_str}
                </text>
            </g>

            <!-- Total Contributions label -->
            <g transform='translate(82.5, 84)'>
                <text x='0' y='32' stroke-width='0' text-anchor='middle' fill='#151515' stroke='none' font-family='"Segoe UI", Ubuntu, sans-serif' font-weight='400' font-size='14px' font-style='normal' style='opacity: 0; animation: fadein 0.5s linear forwards 0.7s'>
                    Total Contributions
                </text>
            </g>

            <!-- Total Contributions range -->
            <g transform='translate(82.5, 114)'>
                <text x='0' y='32' stroke-width='0' text-anchor='middle' fill='#464646' stroke='none' font-family='"Segoe UI", Ubuntu, sans-serif' font-weight='400' font-size='12px' font-style='normal' style='opacity: 0; animation: fadein 0.5s linear forwards 0.8s'>
                    {date_range_str}
                </text>
            </g>
        </g>
        <g style='isolation: isolate'>
            <!-- Current Streak label -->
            <g transform='translate(247.5, 108)'>
                <text x='0' y='32' stroke-width='0' text-anchor='middle' fill='#FB8C00' stroke='none' font-family='"Segoe UI", Ubuntu, sans-serif' font-weight='700' font-size='14px' font-style='normal' style='opacity: 0; animation: fadein 0.5s linear forwards 0.9s'>
                    Current Streak
                </text>
            </g>

            <!-- Current Streak range -->
            <g transform='translate(247.5, 145)'>
                <text x='0' y='21' stroke-width='0' text-anchor='middle' fill='#464646' stroke='none' font-family='"Segoe UI", Ubuntu, sans-serif' font-weight='400' font-size='12px' font-style='normal' style='opacity: 0; animation: fadein 0.5s linear forwards 0.9s'>
                    {curr_streak_range_str}
                </text>
            </g>

            <!-- Ring around number -->
            <g mask='url(#mask_out_ring_behind_fire)'>
                <circle cx='247.5' cy='71' r='40' fill='none' stroke='#FB8C00' stroke-width='5' style='opacity: 0; animation: fadein 0.5s linear forwards 0.4s'></circle>
            </g>
            <!-- Fire icon -->
            <g transform='translate(247.5, 19.5)' stroke-opacity='0' style='opacity: 0; animation: fadein 0.5s linear forwards 0.6s'>
                <path d='M -12 -0.5 L 15 -0.5 L 15 23.5 L -12 23.5 L -12 -0.5 Z' fill='none'/>
                <path d='M 1.5 0.67 C 1.5 0.67 2.24 3.32 2.24 5.47 C 2.24 7.53 0.89 9.2 -1.17 9.2 C -3.23 9.2 -4.79 7.53 -4.79 5.47 L -4.76 5.11 C -6.78 7.51 -8 10.62 -8 13.99 C -8 18.41 -4.42 22 0 22 C 4.42 22 8 18.41 8 13.99 C 8 8.6 5.41 3.79 1.5 0.67 Z M -0.29 19 C -2.07 19 -3.51 17.6 -3.51 15.86 C -3.51 14.24 -2.46 13.1 -0.7 12.74 C 1.07 12.38 2.9 11.53 3.92 10.16 C 4.31 11.45 4.51 12.81 4.51 14.2 C 4.51 16.85 2.36 19 -0.29 19 Z' fill='#FB8C00' stroke-opacity='0'/>
            </g>

            <!-- Current Streak big number -->
            <g transform='translate(247.5, 48)'>
                <text x='0' y='32' stroke-width='0' text-anchor='middle' fill='#151515' stroke='none' font-family='"Segoe UI", Ubuntu, sans-serif' font-weight='700' font-size='28px' font-style='normal' style='animation: currstreak 0.6s linear forwards'>
                    {curr_streak}
                </text>
            </g>

        </g>
        <g style='isolation: isolate'>
            <!-- Longest Streak big number -->
            <g transform='translate(412.5, 48)'>
                <text x='0' y='32' stroke-width='0' text-anchor='middle' fill='#151515' stroke='none' font-family='"Segoe UI", Ubuntu, sans-serif' font-weight='700' font-size='28px' font-style='normal' style='opacity: 0; animation: fadein 0.5s linear forwards 1.2s'>
                    {max_streak}
                </text>
            </g>

            <!-- Longest Streak label -->
            <g transform='translate(412.5, 84)'>
                <text x='0' y='32' stroke-width='0' text-anchor='middle' fill='#151515' stroke='none' font-family='"Segoe UI", Ubuntu, sans-serif' font-weight='400' font-size='14px' font-style='normal' style='opacity: 0; animation: fadein 0.5s linear forwards 1.3s'>
                    Longest Streak
                </text>
            </g>

            <!-- Longest Streak range -->
            <g transform='translate(412.5, 114)'>
                <text x='0' y='32' stroke-width='0' text-anchor='middle' fill='#464646' stroke='none' font-family='"Segoe UI", Ubuntu, sans-serif' font-weight='400' font-size='12px' font-style='normal' style='opacity: 0; animation: fadein 0.5s linear forwards 1.4s'>
                    {longest_streak_range_str}
                </text>
            </g>
        </g>
    </g>
</svg>'''

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_path = os.path.join(base_dir, 'streak.svg')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(svg_content.strip() + '\n')
    print(f'Successfully updated {output_path} with Total: {total_str}, Streak: {curr_streak}, Longest: {max_streak}')

if __name__ == '__main__':
    generate_svg()
