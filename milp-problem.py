#region Imports
import sys
import gurobipy as gp
#endregion

#region Problem values (Valus of Instance 1)
NUM_VAGOES = 0
NUM_TRECHOS = 0
NUM_ATIVIDADES = 0
NUM_TRENS = 0
VAGOES_TREM_SAIDA = []
VAGOES_TREM_CHEGADA = []
P = 5
M = sys.maxint
PSA = []
PCH = []
AMV = []
RELEASE = []
#endregion

#region Auxiliar constants
FIRST_OP = 0
LAST_OP = NUM_ATIVIDADES - 1
#endregion

#region Simplify instances informed values
n = NUM_VAGOES
m = NUM_TRECHOS
o = NUM_ATIVIDADES
v = NUM_TRENS
ns = VAGOES_TREM_SAIDA
nc = VAGOES_TREM_CHEGADA
#endregion

#region Initialize model
model = gp.Model("milp")
#endregion

#region Declare decision variables
var_y = model.addVar(vtype=gp.GRB.CONTINUOS, name="y")          ## y[i,j]
var_z = model.addVar(vtype=gp.GRB.BINARY, name="z")             ## z[i,q,j]
var_x = model.addVar(vtype=gp.GRB.BINARY, name="x")             ## x[q,i,j,k,l]
var_f = model.addVar(vtype=gp.GRB.BINARY, name="f")             ## f[i,j]
var_c = model.addVar(vtype=gp.GRB.CONTINUOS, name="c")          ## C[j]
var_c_max = model.addVar(vtype=gp.GRB.CONTINUOS, name="c_max")  ## Cmax
#endregion

#region Define objective function
model.setObjective(var_c_max, gp.GRB.MINIMIZE)
#endregion

#region Notes
## Observações
# O[i,j] = i-ésima circulação do vagão j
# H = tempo de horizonte definido pelo analista

## Parâmetros
# P = tempo de circulação (i) de um vagão j em um trecho q
# r[j] = instante de chegada do vagão j, ou seja, horário de chegada do trem t (em que j pertence à t)
# AMV[q,s] = será igual a 1 se q estiver ligado em s; 0 caso contrário
# PCH[j] = trecho do pátio em que o vagão j está posicionado ao receber o trem de chegada t
# PSA[j] = trecho do pátio em que o vagão j deverá estar posicionado para que o trem de saída t possa sair

## Variáveis
# y[i,j] = instante de início da i-ésima operação do vagão j. (real)
# z[i,q,j] = será 1 se a i-ésima operação do vagão j acontecer no trecho q; 0 caso contrário. (binário)
# x[q,i,j,k,l] = será 1 se a i-ésima operação do vagão j precede a k-ésima operação do vagão l no trecho q; 0 caso contrário. (binário)
# f[i,j] = será 1 se a i-ésima operação do vagão j é a última, antes da partida do seu trem t; 0 caso contrário. (binário)
# C[j] = instante de conclusão do vagão j / horário de partida do trem t. (real)
# C[max] = horário da partida do último vagão j do trem t [makespan]. (real)
#endregion

#region Define constraint
#region C1
c1 = model.addConstr
(
  (var_y[i+1,j] >= var_y[i,j] 
  + (P * gp.quicksum(var_x[q, i, j] for q in range(m))))
  for j in range(n) 
  for i in range(o)
  if i < o
)
#endregion

#region C2
c2 = model.addConstr
(
  (
    var_y[i+1,j] 
    >= var_y[k,l]
    - (M * var_x[q,i,j,k,l])
    - (M * (1 - var_z[i,q,j]))
    - (M * (1 - var_z[k,q,l]))
  )
  for j,l in range(n) 
  for k,i in range(o)
  for q in range(m)
  if i < o
)
#endregion

#region C3
c3 = model.addConstr
(
  (
    var_y[k,l] 
    >= var_y[i+1,j]
    - (M * (1 - var_x[q,i,j,k,l]))
    - (M * (1 - var_z[i,q,j]))
    - (M * (1 - var_z[k,q,l]))
  )
  for j,l in range(n) 
  for k,i in range(o)
  for q in range(m)
  if i < o
)
#endregion

#region C4
c4 = model.addConstr
(
  (
    gp.quicksum(var_z[FIRST_OP,q,j] for q in range(m))
    <= 1
  )
  for j in range(n) 
  # for i in range(o)
  # if i == 1
)
#endregion

#region C5
c5 = model.addConstr
(
  (
    var_x[q,i,j,k,l] 
    + gp.quicksum(var_x[s,k-1,l,i+1,j] for s in range(m))
    <= 1
  )
  for j,l in range(n) 
  for k,i in range(o)
  for q in range(m)
  if i < o and k > FIRST_OP and j != l
)
#endregion

#region C6
c6 = model.addConstr
(
  (
    var_x[q,i,j,k,l] 
    + var_x[q,k,l,i,j] 
    >= 1
    - (M * (1 - var_z[i,q,j]))
    - (M * (1 - var_z[k,q,l]))
  )
  for j,l in range(n) 
  for k,i in range(o)
  for q in range(m)
  if j != l
)
#endregion

#region C7
c7 = model.addConstr
(
  (
    gp.quicksum(var_z[i,q,j] for q in range(m))
    == 1
    - gp.quicksum(var_f[k,j] for k in range(i-1))
  )
  for j in range(n) 
  for i in range(o)
  if i > FIRST_OP
)
#endregion

#region C8
c8 = model.addConstr
(
  (
   var_f[i,j]
   <= var_z[i,PSA[j],j]
  )
  for j in range(ns) 
  for i in range(o)
  # for q in range(m)
  # if q == PSA[j]
)
#endregion

#region C9
c9 = model.addConstr
(
  (
   gp.quicksum(var_f[i,j] for i in range(o))
   == 1
  )
  for j in range(ns) 
)
#endregion

#region C10
c10 = model.addConstr
(
  (
   gp.quicksum(var_f[i,j] for i in range(o))
   == 0
  )
  for j in range(nc) 
)
#endregion

#region C11
c11 = model.addConstr
(
  (
   var_z[FIRST_OP,PCH[j],j]
   == 1
  )
  for j in range(n) 
  # for i in range(o) 
  # for q in range(m) 
  # if q == PCH[j] and i == 1
)
#endregion

#region C12
c12 = model.addConstr
(
  (
   var_y[FIRST_OP,j]
   == RELEASE[j]
  )
  for j in range(ns) 
  # for i in range(o) 
  # if i == 1
)
#endregion

#region C13
c13 = model.addConstr
(
  (
   var_y[FIRST_OP,j]
   >= RELEASE[j]
  )
  for j in range(ns) 
  # for i in range(o) 
  # if i == 1
)
#endregion

#region C14
c14 = model.addConstr
(
  (
   var_y[FIRST_OP,j]
   == var_y[FIRST_OP,l]
  )
  for j,l in range(nc) 
  # for i in range(o)
  # if i == 1
)
#endregion

#region C15
c15 = model.addConstr
(
  (
   var_z[i+1,q,j]
   <= gp.quicksum(AMV[s,q] * var_z[i,s,j] for s in range(m))
  )
  for j in range(n) 
  for i in range(o)
  for q in range(m)
  # if i < o
)
#endregion

#region C16
c16 = model.addConstr
(
  (
   var_c[j]
   >= var_y[i,l]
  )
  for j,l in range(ns) 
  for i in range(o)
  # if i < o
)
#endregion

#region C17
c17 = model.addConstr
(
  (
   var_c[j]
   >= var_y[LAST_OP,j]
  )
  for j in range(nc) 
  # for i in range(o)
  # if i == o
)
#endregion

#region C18
c18 = model.addConstr
(
  (
   var_y[i+1,j]
   >= var_c[j] 
   - M 
   * (1 - gp.quicksum(var_f[k,j] for k in range(i)))
  )
  for j in range(n) 
  for i in range(o)
  # if i < o
)
#endregion

#region C19
c19 = model.addConstr
(
  (
   var_c_max >= var_c[j]
  )
  for j in range(ns) 
)
#endregion

#endregion

#region Execute model
model.optimize()
#endregion