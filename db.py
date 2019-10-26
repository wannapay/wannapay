##    This program is free software: you can redistribute it and/or modify
##    it under the terms of the GNU General Public License as published by
##    the Free Software Foundation, either version 3 of the License, or
##    (at your option) any later version.
##
##    This program is distributed in the hope that it will be useful,
##    but WITHOUT ANY WARRANTY; without even the implied warranty of
##    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##    GNU General Public License for more details.
##
##    You should have received a copy of the GNU General Public License
##    along with this program.  If not, see <https://www.gnu.org/licenses/>.

import json
import os.path


if __name__ == '__main__':

    param = {'t mouse':1/4, 't key':1/10, 'wait factor':1, 't confirm min':4, 'pixel per sec':500000,
             'text region':(-550, 0, 370, 24)}

    img = {
        'but_pay':{'name':'but_pay_over.png', 'confidence':0.9, 'grayscale':False, 'src':'but_pay_over.gif'},
        '0_pps':{'name':'logo.png', 'confidence':0.8, 'grayscale':True, 'src':'logo.gif'},
        '1_payBill_a':{'name':'but_payBill_over.png', 'confidence':0.9, 'grayscale':False, 'src':'but_payBill_over.gif'},
        '1_payBill_b':{'name':'but_payBill.png', 'confidence':0.9, 'grayscale':False, 'src':'but_payBill.gif'},
        '2_proceed':{'name':'but_proceed.png', 'confidence':0.95, 'grayscale':False, 'src':'but_proceed.gif', 'crop':(5, 0, 75, 26)},
        '3_cancel':{'name':'but_cancel.png', 'confidence':0.95, 'grayscale':False, 'src':'but_cancel.gif', 'crop':(5, 0, 51, 26)},
        '3_pay':{'name':'but_pay2.png', 'confidence':0.95, 'grayscale':False, 'src':'but_pay2.gif', 'crop':(5, 0, 51, 26)},
        '4_tick':{'name':'tick.png', 'confidence':0.8, 'grayscale':True, 'src':'tick.jpg'},
    }

    payBill = {'imgs':(img['1_payBill_a'], img['1_payBill_b']), 'offset':{'x':0,'y':0}, 't_wait':1}
    text = {'imgs':({'name':'t.png', 'confidence':0.95, 'grayscale':True},), 'offset':{'x':-param['text region'][2]/2,'y':0}}
    water = {'imgs':(img['0_pps'],), 't_wait':1}
    ird = {'imgs': (img['0_pps'],), 't_wait':1}
    rates_n_rent = {'imgs':(img['0_pps'],), 't_wait':1}
    amount = {'imgs':(img['2_proceed'],), 'offset':{'x':52,'y':-190}, 'amount_keys':True}
    amount_tax = {'imgs':(img['2_proceed'],), 'offset':{'x':52,'y':-190}, 'amount_keys':True}
    proceed = {'imgs':(img['2_proceed'],), 'offset':{'x':0,'y':0}, 't_wait':1}
    tax_type = {'imgs':(img['2_proceed'],), 'offset':{'x':35,'y':-220}, 'keys':'1',}
    tax_radio_1 = {'imgs':(img['2_proceed'],), 'offset':{'x':-92,'y':-180},}
    tax_radio_2  = {'imgs':(img['2_proceed'],), 'offset':{'x':8,'y':-180},}
    pay = {'imgs':(img['3_pay'],), 'offset':{'x':0,'y':0}, 't_wait':1}
    cancel = {'imgs':(img['3_cancel'],), 'offset':{'x':0,'y':0}, 't_wait':1}
    result_demo = {'imgs':(img['3_cancel'],), 'offset':{'x':0,'y':0}}
    result_real = {'imgs':(img['4_tick'],), 'offset':{'x':0,'y':0}}

    pps = {
        'demo':{ 'wsd':(payBill, text, water, amount, proceed, cancel, result_demo,),
                    'tax1':(payBill, text, ird, amount_tax, tax_type, tax_radio_1, proceed, cancel, result_demo,),
                    'tax2':(payBill, text, ird, amount_tax, tax_type, tax_radio_2, proceed, cancel, result_demo,),
                    'grr':(payBill, text, rates_n_rent, amount, proceed, cancel, result_demo,)},

        'real':{ 'wsd':(payBill, text, water, amount, proceed, pay, result_real,),
                    'tax1':(payBill, text, ird, amount_tax, tax_type, tax_radio_1, proceed, pay, result_real,),
                    'tax2':(payBill, text, ird, amount_tax, tax_type, tax_radio_2, proceed, pay, result_real,),
                    'grr':(payBill, text, rates_n_rent, amount, proceed, pay, result_real,) }
        }

    with open('pps.json', 'w') as f:
        json.dump(pps, f, indent=4)
        print('updated:', 'pps.json')
    with open('img.json', 'w') as f:
        json.dump(img, f, indent=4)
        print('updated:', 'img.json')
    with open('param.json', 'w') as f:
        json.dump(param, f, indent=4)
        print('updated:', 'param.json')
else:
    if os.path.isfile('pps.json'):
        with open('pps.json', 'r') as f:
            pps = json.load(f)
    if os.path.isfile('img.json'):
        with open('img.json', 'r') as f:
            img = json.load(f)
    if os.path.isfile('param.json'):
        with open('param.json', 'r') as f:
            param = json.load(f)
