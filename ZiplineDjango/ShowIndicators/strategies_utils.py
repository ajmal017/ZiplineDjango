from ShowIndicators.indicators import EMAdecision, SARdecision, KAMAdecision, SMAdecision, TEMAdecision, TRIMAdecision, WMAdecision # pylint: disable=E0401
from ShowIndicators.simulator import Simulator
import pandas as pd
import numpy as np
import datetime as dt
import json
from ShowIndicators.models import Strategies


def testStrategy(data, security, tries = 100):
    result = []

    for i in range(tries): # pylint: disable=W0612
        strategy = {}
        sim = Simulator(data, std_purchase= 10)

        if np.random.randint(0,2)==1:
            days = np.random.randint(20,100)
            sim.add_indicator('EMA-{}'.format(days),EMAdecision(data,days))
            strategy.update({'EMA':{'parameters':{'days':days}}})
            #TODO crear funcion para agregar parametros automatico
        if np.random.randint(0,2)==1:
            days = np.random.randint(20,100)
            sim.add_indicator('KAMA-{}'.format(days),KAMAdecision(data,days))
            strategy.update({'KAMA':{'parameters':{'days':days}}})
        if np.random.randint(0,2)==1:
            days = np.random.randint(20,100)
            sim.add_indicator('SMA-{}'.format(days),SMAdecision(data,days))
            strategy.update({'SMA':{'parameters':{'days':days}}})
        if np.random.randint(0,2)==1:
            days = np.random.randint(20,100)
            sim.add_indicator('TEMA-{}'.format(days),TEMAdecision(data,days))
            strategy.update({'TEMA':{'parameters':{'days':days}}})
        if np.random.randint(0,2)==1:
            days = np.random.randint(20,100)
            sim.add_indicator('TRIMA-{}'.format(days),TRIMAdecision(data,days))
            strategy.update({'TRIMA':{'parameters':{'days':days}}})
        if np.random.randint(0,2)==1:
            days = np.random.randint(20,100)
            sim.add_indicator('WMA-{}'.format(days),WMAdecision(data,days))
            strategy.update({'WMA':{'parameters':{'days':days}}})
        if np.random.randint(0,2)==1:
            acel = np.random.randint(20,100)/1000
            maxacel = np.random.randint(20,100)/100
            sim.add_indicator('SAR-{}-{}'.format(acel, maxacel), SARdecision(data,aceleration = acel, max = maxacel))
            strategy.update({'SAR':{'parameters':{'aceleration':acel, 'max_aceleration':maxacel}}})
        sim.calc_earning()
        strategy = json.dumps(strategy)
        iteration_result =[security,strategy, sim.real_final_capital, sim.diference_percentage]
        print(iteration_result)
        result.append(iteration_result)
        sqlappend = Strategies(security = security, strategy = strategy, percentage_up= sim.diference_percentage, trades = sim.operations_made, max_point = sim.highest_point, min_point = sim.lowest_point )
        print(sqlappend)
        sqlappend.save()
        sim.cleanSimulator()

    cols = ['Security','Strategy','Final_Capital','%Up']
    result = pd.DataFrame(result, columns=cols)
    

def findBestStrategy(security):
    all_strategies = []
    for i in list(Strategies.objects.all().values()): #pylint: disable = E1101
        query = []
        for y in i:
            query.append(i[y])
        all_strategies.append(query)
    print(all_strategies[0])
    all_strategies = pd.DataFrame(all_strategies, columns = ['id','Security','Strategy','%Up','LastModified','MaxPoint', 'MinPoint', 'Trades'])
    security_strategies = all_strategies[all_strategies['Security']==security]
    best_strategy = security_strategies[ security_strategies['%Up'] == security_strategies['%Up'].max()]
    return best_strategy


def jsonToStrategy(strategy, data):
    sim = Simulator(data, std_purchase = 10)
    for name, indicator in strategy:
        indicator_name = '{name}_'
        sim.add_indicator('{name}_',)

    return