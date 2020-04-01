#!/usr/bin/env python
# coding: utf-8

from __future__ import division
from pyomo.environ import *


base_price=[10,10,10]
target_trade_spend = 10515.58
intercept = 15
coef_1 =-3
coef_2 =0.004
target_edlp_spend = 1906.41
target_tpr_spend = 8609.172

model = ConcreteModel(name='Spend_Optim')
idx = range(3)
model.idx = idx
model.edlp = Var(idx, initialize=10, bounds=(9.5, 10))
model.tpr = Var(idx, initialize=10, bounds=(5, 50))

# model.S = Set(initialize={1,2,3})
# model.x = Var(model.S)
model.flag = Var(idx,initialize=0,domain=Binary)



unit_sales = list(exp((log(model.edlp[i])*coef_1)*model.flag[i]
                 +(log(base_price[i])*coef_1+model.tpr[i]*coef_2)*(1-model.flag[i])
                 +intercept) for i in model.idx)

price = list((base_price[i]*(1-model.tpr[i]/100)*(1-model.flag[i])) 
        +(model.edlp[i]*model.flag[i]) for i in model.idx)

dollar_sales = [a*b for a,b in zip(unit_sales,price)]

trade_spent = [a-b for a,b in zip(base_price, price)]

total_trade_spent = [a*b for a,b in zip(trade_spent, unit_sales)]

edlp_trade_spent = [a*b for a,b in zip(total_trade_spent, model.flag)]

tpr_trade_spent = [a*(1-b) for a,b in zip(total_trade_spent, model.flag)]

flag_util = [a*(1-b) for a,b in zip(model.flag, model.flag)]

model.obj = Objective(expr=sum(dollar_sales) ,sense= maximize)


model.c1 = Constraint(expr = sum(total_trade_spent) == target_trade_spend )
model.c2 = Constraint(expr = sum(edlp_trade_spent) == target_edlp_spend )
model.c3 = Constraint(expr = sum(tpr_trade_spent) == target_tpr_spend )
# model.c4 = Constraint(expr = (model.flag[0]*(1-model.flag[0]) ==0) )
# model.c5 = Constraint(expr = (model.flag[1]*(1-model.flag[1]) ==0) )
# model.c6 = Constraint(expr = (model.flag[2]*(1-model.flag[2]) ==0) )


# edlp = [10,10,10]
# flag = [0,0,1]
# tpr = [10,10,10]
# unit_sales = list(exp((log(edlp[i])*coef_1)*flag[i]
#                  +(log(base_price[i])*coef_1+tpr[i]*coef_2)*(1-flag[i])
#                  +intercept) for i in idx)
# unit_sales
# price = list((base_price[i]*(1-tpr[i]/100)*(1-flag[i])) 
#         +(edlp[i]*flag[i]) for i in idx)
# price

# for i in idx:
#     model.flag[i].domain = Integers
# exp1 = sum(model.edlp[i]*(1-model.tpr[i]/100)*exp((intercept+log(model.edlp[i])*coef_1+model.tpr[i]*coef_2)) for i in model.idx)
# exp1 = sum((exp((log(model.edlp[i])*coef_1)*model.flag[i]
#            +(log(base_price[i])*coef_1+model.tpr[i]*coef_2)*(1-model.flag[i]) + intercept)) * 
#             ((base_price[i]*(1-model.tpr[i]/100)*(1-model.flag[i])) + (model.edlp[i]*model.flag[i])) for i in model.idx)

# exp2 = base_price[i] - ((base_price[i]*(1-model.tpr[i]/100)*(1-model.flag[i])) + (model.edlp[i]*model.flag[i]))


opt = SolverFactory('bonmin')
opt.solve(model)
model.display()



