from math import exp



def sigmoid(x):
    return 1/(1 + exp(-x))



def proba_juste(beta, theta, d, q):
    """Donne en fonction des paramètres la probabilité que la réponse soit juste"""
    K = len(theta)
    s = beta
    for k in range(K):
        s += q[k]*theta[k]*d
    return sigmoid(s)


def proba_reponse(beta, theta, d, q, reponse):
    """Donne en fonction des paramètres la probabilité que la réponse corresponde à reponse (=0 ou 1)"""
    p = proba_juste(beta, theta, d, q)
    if reponse==1:
        return p
    else:
        return 1-p



def vraisemblance(questions, beta, theta, diff, matQ, reponses):
    L = 1
    # questions contient la liste des questions répondues
    for i in range(len(questions)):
        L = L*proba_reponse(beta, theta, diff[i], matQ[i], reponses[i])
    return L