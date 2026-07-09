from template_matcher_napa import extract_napa_feilds
from template_matcher_autozone import extract_autozone_feilds
from template_matcher_oreilly import extract_oreilly_feilds
from template_matcher_car_quest import extract_car_quest_feilds
from template_matcher_worldpac import extract_worldpac_feilds
#from template_matcher_advanceautoparts import extract_advanceautoparts_feilds
from template_matcher_autoparts_warehouse import extract_autoparts_warehouse_feilds
EXTRACTORS = {
    "NAPA": extract_napa_feilds,
    "AUTOZONE": extract_autozone_feilds,
    "OREILLY": extract_oreilly_feilds,
    "CARQUEST": extract_car_quest_feilds,
    "WORLDPAC": extract_worldpac_feilds,
    #"ADVANCE AUTO PARTS": extract_advanceautoparts_feilds,
    "AUTOPARTS WAREHOUSE": extract_autoparts_warehouse_feilds
}
