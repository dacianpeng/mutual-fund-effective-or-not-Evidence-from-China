import re

def format_code(code = '601006sh', target_pattern = '601006.XSHG'):

    code = re.findall('\d+', code)[0]

    dotted = '.' in target_pattern
    code_first = target_pattern[0].isdigit()
    upper = target_pattern.isupper()
    ISO10383 = re.search('XSHE|XSHG', target_pattern.upper())

    sh_market = '6\d{5}|9\d{5}'
    sz_market = '0\d{5}|2\d{5}|3\d{5}'
    bj_market = '8\d{5}|4\d{5}'

    if re.match(sh_market, code):
        if ISO10383 and upper:
            market = 'XSHG'
        elif not ISO10383 and upper:
            market = 'SH'
        elif not ISO10383 and not upper:
            market = 'sh'
    elif re.match(sz_market, code):
        if ISO10383 and upper:
            market = 'XSHE'
        elif not ISO10383 and upper:
            market = 'SZ'
        elif not ISO10383 and not upper:
            market = 'sz'
    elif re.match(bj_market, code):
        if ISO10383 and upper:
            if int(code[0]) == 4:
                market = 'XSHE'
            elif int(code[0]) == 8:
                market = 'XSHG'
        elif not ISO10383 and upper:
            market = 'BJ'
        elif not ISO10383 and not upper:
            market = 'bj'

    target_pattern = [market, '.', code]

    if not dotted:
        target_pattern.remove('.')
    if code_first:
        target_pattern.reverse()

    return ''.join(target_pattern)