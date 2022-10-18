
import jqdatasdk as jq

jq.auth('13764432461', 'Swisschina6')

jq_all_stocks_brief = jq.get_all_securities(types=['stock'], date=None)