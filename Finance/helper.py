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

def render(  dict, template, template_file = None, ):
    if (template):
        return chevron.render(template, dict)
    with open(template_file, 'r') as f:
        result = chevron.render(f, dict)
    return result

def render_sections(template_file, output_file):
    with open(template_file, 'r') as f:
        template = f.read()


    str_all = ""
    str_seg = str_pre
    count = 0
    for k, v in dict_industry.items():
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

def test_renders():
    with open('single_item.templt', 'r') as f:
        result = f.read()
    print(result)


def test_render():
    templt = 'single_item.templt'
    file_res = 'generated.html'
    render_sections(templt,file_res)

def main():
    test_render()

if __name__ == "__main__":
    main()