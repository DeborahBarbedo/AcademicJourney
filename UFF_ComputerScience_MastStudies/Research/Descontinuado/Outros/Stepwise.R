### Modelagem
setwd("~/PDPA")
dados = read.csv("dados_stepwise.csv", sep=",", dec=".")



summary(dados)


#Saving output
sink(file = "Stepwise Regression.txt", append = T, type = c("output", "message"),
     split = T)

#
# # --- Stepwise Regression --- #
#
modelo_basico = glm(  ocorrencia ~ 1
                      , family = binomial(link = "logit")
                      , data = dados)

modelo_total <-glm(  ocorrencia ~ .
                     , family = binomial(link = "logit")
                     , data = dados)

summary(modelo_total)


library(MASS)
#
step_mod = stepAIC(modelo_basico
                   , list(lower = formula(modelo_basico)
                          , upper = formula(modelo_total))
                   , direction="both"
                   , trace = T)
summary(step_mod)

