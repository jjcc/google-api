import chevron




str_pre = '''    <div class="row text-center text-lg-left">
'''
str_post = '''    </div>

'''


import chevron


dict_industry = { "KBE":"Bank","KRE":"Regional Banking","KCE":"Capital Markets","KIE":"Insurance",
                  "XAR":"Aerospace & Defense","XTN":"Transportation","XBI":"Biotech","XPH":"Pharmaceuticals",
                  "XHE":"Health Care Equipment","XHS":"Health Care Services","XOP":"Oil & Gas Exploration & Production",
                  "XES":"Gas Equipment & Services","XME":"Metals & Mining","XRT":"Retail","XHB":"Homebuilders",
                  "XSD":"Semiconductor","XSW":"Software & Services","XNTK":"NYSE Technology",
                  "XITK":"FactSet Innovative Technology","XTL":"Telecom","XWEB":"Internet"
                }

dict_smartbeta = {"SPYD":"SPDR Portfolio S&P 500 High Dividend","SDY":"SPDR S&P Dividend","WDIV":"SPDR S&P Global Dividend",
                "DWX":"SPDR S&P International Dividend","EDIV":"SPDR S&P Emerging Markets Dividend",
                "QUS":"SPDR MSCI USA StrategicFactors","QWLD":"SPDR MSCI World StrategicFactors",
                "QEFA":"SPDR MSCI EAFE StrategicFactors","QEMM":"SPDR MSCI Emerging Markets StrategicFactors",
                "ONEY":"SPDR Russell 1000 Yield Focus","ONEV":"SPDR Russell 1000 Low Volatility Focus",
                "ONEO":"SPDR Russell 1000 Momentum Focus","LGLV":"SPDR SSGA US Large Cap Low Volatility Index",
                "SMLV":"SPDR SSGA US Small Cap Low Volatility Index","MMTM":"SPDR S&P 1500 Momentum Tilt",
                "VLU":"SPDR S&P 1500 Value Tilt","DWFI":"SPDR Dorsey Wright® Fixed Income Allocation"
                  }


def render(  dict, template, template_file = None, ):
    if (template):
        return chevron.render(template, dict)
    with open(template_file, 'r') as f:
        result = chevron.render(f, dict)
    return result

def render_sections(template_file, output_file,dict_input=dict_industry):
    with open(template_file, 'r') as f:
        template = f.read()


    str_all = ""
    str_seg = str_pre
    count = 0
    for k, v in dict_input.items():
        name_desc = k +":"+ v
        name_lower = k.lower()

        dict = { 'name':k, 'name_desc':name_desc,'name_lower':name_lower}
        sec_item = render(dict, template )
        str_seg += sec_item


        count += 1
        if count%3 == 0:
            str_seg += str_post
            str_all += str_seg
            str_seg = str_pre

    if( count%3 != 0):
        str_seg += str_post
        str_all += str_seg

    with open(output_file, 'w') as fout:
        fout.write(str_all)


def test_render():
    templt = 'single_item.templt'
    file_res = 'generated.html'
    render_sections(templt,file_res)

def main():
    test_render()

if __name__ == "__main__":
    main()