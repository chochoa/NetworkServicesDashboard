import os
# EMEAR
countryList = ['af', 'al', 'dz', 'ad', 'ao', 'am', 'at', 'az', 'bh', 'by', 'be', 'bj', 'ba', 'bw', 'bv', 'io', 'bg', 'bf', 'bi', 'cm', 'cv', 'cf', 'td', 'km', 'cg', 'cd', 'ci', 'hr', 'cy', 'cz', 'dk', 'dj', 'eg', 'gq', 'ee', 'et', 'fo', 'fi', 'fr', 'ga', 'gm', 'ge', 'de', 'gh', 'gi', 'gr', 'gl', 'gn', 'gw', 'hu', 'is', 'iq', 'ie', 'il', 'it', 'jo', 'kz', 'ke', 'kw', 'kg', 'lv', 'lb', 'ls', 'lr', 'ly', 'li', 'lt', 'lu', 'mk', 'mg', 'mw', 'ml', 'mt', 'mr', 'mu', 'yt', 'md', 'mc', 'me', 'ma', 'mz', 'na', 'nl', 'ne', 'ng', 'no', 'om', 'pk', 'ps', 'pl', 'pt', 'qa', 're', 'ro', 'ru', 'rw', 'sh', 'sm', 'st', 'sa', 'sn', 'si', 'rs', 'sc', 'sl', 'sk', 'so', 'za', 'es', 'sz', 'se', 'ch', 'tj', 'tz', 'tg', 'tn','tr', 'tm', 'ug', 'ua', 'ae', 'gb', 'uz', 'va', 'ye', 'zm', 'zw']
for item in countryList:
	os.system("nugsl-worldmap -c " + item + " -o emear/" + item + ".svg")

# AJPC
countryList = ['as', 'aq', 'au', 'bd', 'bt', 'bn', 'kh', 'cn', 'cx', 'cc', 'ck', 'tl', 'fj', 'pf', 'hm', 'hk', 'in', 'id', 'jp', 'ki', 'la', 'mo', 'my', 'mv', 'mh', 'fm', 'mn', 'mm', 'nr', 'np', 'nc', 'nz', 'nu', 'nf', 'pw', 'pg', 'ph', 'pn', 'kr', 'ws', 'sg', 'sb', 'lk', 'sj', 'tw', 'th', 'tk', 'to', 'tv', 'vu', 'vn', 'wf']
for item in countryList:
	os.system("nugsl-worldmap -c " + item + " -o ajpc/" + item + ".svg")

# AMER
countryList = ['ai', 'ag', 'ar', 'aw', 'bs', 'bb', 'bz', 'bm', 'bo', 'br', 'vg', 'ca', 'ky', 'cl', 'co', 'cr', 'dm', 'do', 'ec', 'sv', 'fk', 'gf', 'gd', 'gp', 'gu', 'gt', 'gy', 'ht', 'hn', 'jm', 'mq', 'mx', 'ms', 'an', 'ni', 'mp', 'pa', 'py', 'pe', 'pr', 'kn', 'lc', 'vc', 'sr', 'tt', 'tc', 'um', 'uy', 'vi', 'us', 've']
for item in countryList:
	os.system("nugsl-worldmap -c " + item + " -o amer/" + item + ".svg")