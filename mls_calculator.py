import json
import requests
class mls_calcuator(object):
    def __init__(self,rate,coal_price,freight,sendcount,recivecount,waybillNumber):
          self.rate = rate
          self.coal_price = coal_price
          self.freight = freight
          self.sendcount= sendcount
          self.recivecount = recivecount
          self.waybillNumber = waybillNumber


    # 基本参数
    def parameter_input(self):
        rate  = int(input('税率'))/100
        #print(rate)
        coal_price = int(input('坑口含税价'))
        freight = int(input('运费（不含税）'))
        sendcount= int(input('实发吨位'))
        recivecount= int(input('实收吨位'))
        mls_calcuator.calcuate_formula1(coal_price,sendcount,recivecount,freight,rate)

    # 调物流查询接口
    def parameter_transport(self):
        waybillNumber = input('运单号')
        url = 'http://web.sijibao.co/WEBproject/Companyservice/Order/queryOrderDetail'
        paramas1 = {'ordernumber':waybillNumber}
        headers = {'certification':'1d6a93608b254ce0abb202e272f77dc1'}
        res = requests.get(url, headers=headers, params=paramas1)
        #print(res.status_code,res.json())
        response = res.json()
        driverFee = float(response.get('data').get('driverIncome').get('acturalFee').get('acturalTransFee'))       # 实付司机运费
        scheduleFee = float(response.get('data').get('driverIncome').get('acturalFee').get('acturalScheduleFee'))  # 调度费
        loseFee = float(response.get('data').get('driverIncome').get('deductionFee').get('loseFee'))               # 亏吨扣款
        print(driverFee, scheduleFee, loseFee)
        transportFee= driverFee + scheduleFee            # 实付物流
        print(transportFee)
        trans_paramas = [loseFee,transportFee]
        return trans_paramas

    '''
    # 计算公式1
    def formula(self):
        self.formula1 = '公式一'
        self.formula1 = '公式二'                                           
    '''

    def calcuate_formula1(coal_price,sendcount,recivecount,freight,rate):

        # 三种情况下，调用此函数（实收吨数<货源吨数&&实收吨数<实发吨数）
        total_coalPrice= coal_price * sendcount                                                 # 采购商实付煤款
        print(total_coalPrice)
        trans_paramas = mls_calcuator.parameter_transport(object)
        loseFee = trans_paramas[0]
        buyer_pay =   recivecount * freight*(1 + rate) - loseFee                                # 采购商实付运费
        print(buyer_pay)
        transportFee = trans_paramas[1]
        income = buyer_pay - transportFee                                                      # 平台收益
        print(income)


    '''  
    def calcuate_formula2(self):
        self.total_coalPrice= self.coal_price * self.sendcount                                  # 煤款
        self.buyer_pay =   ''                                                                   # 采购商实付
        self.income = self.buyer_pay - self.transportFee                                        # 平台收益
    '''

#mls_calcuator.parameter_input(object)
mls_calcuator.parameter_transport(object)