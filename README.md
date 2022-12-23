## Conjuntos
- vagões/jobs = j (J)
- trechos/máquinas = q (Q)
- operacoes = i (I)
- trens = t (T)
- linhas = g (G)

## Observações
- 't' é um subconjunto de 'j'
- T pode ser subdividido em:
    - Trem de chegada T[a]
    - Trem de saída T[b]
- O[i,j] = i-ésima circulação do vagão j
- H = tempo de horizonte definido pelo analista

## Parâmetros
- P = tempo de circulação (i) de um vagão j em um trecho q
- r[j] = instante de chegada do vagão j, ou seja, horário de chegada do trem t (em que j pertence à t)
- AMV[q,s] = será igual a 1 se q estiver ligado em s; 0 caso contrário
- PCH[j] = trecho do pátio em que o vagão j está posicionado ao receber o trem de chegada t
- PSA[j] = trecho do pátio em que o vagão j deverá estar posicionado para que o trem de saída t possa sair

## Variáveis
- y[i,j] = instante de início da i-ésima operação do vagão j. (real)
- z[i,q,j] = será 1 se a i-ésima operação do vagão j acontecer no trecho q; 0 caso contrário. (binário)
- x[q,i,j,k,l] = será 1 se a i-ésima operação do vagão j precede a k-ésima operação do vagão l no trecho q; 0 caso contrário. (binário)
- f[i,j] = será se a i-ésima operação do vagão j é a última, antes da partida do seu trem t; 0 caso contrário. (binário)
- C[j] = instante de conclusão do vagão j / horário de partida do trem t. (real)
- C[max] = horário da partida do último vagão j do trem t [makespan]. (real)

